import ffmpeg
import tempfile
import os
from typing import Optional, Any
from pathlib import Path
import subprocess

def get_available_video_encoder():
    """
    Returns the best available H.264 encoder on the system.
    Priority:
    1. libx264 (best quality)
    2. libopenh264 (widely available)
    3. h264_vaapi (hardware)
    """
    try:
        result = subprocess.run(
            ["ffmpeg", "-encoders"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        encoders = result.stdout

        if "libx264" in encoders:
            return "libx264"
        if "libopenh264" in encoders:
            return "libopenh264"
        if "h264_vaapi" in encoders:
            return "h264_vaapi"

    except Exception:
        pass

    return None


def merge_videos(video1_path: Optional[str] = None, video2_path: Optional[str] = None, output_path: Optional[str] = None) -> bool:
    """
    Merge two video files using FFmpeg via stream copy (fast method).
    """
    list_file_path = None
    
    try:
        if video1_path is None or video2_path is None or output_path is None:
            raise ValueError("All paths must be provided")

        v1 = Path(video1_path)
        v2 = Path(video2_path)
        out = Path(output_path)

        if not v1.exists():
            raise FileNotFoundError(f"Video 1 not found: {v1}")
        if not v2.exists():
            raise FileNotFoundError(f"Video 2 not found: {v2}")

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(f"file '{v1.resolve()}'\n")
            f.write(f"file '{v2.resolve()}'\n")
            list_file_path = f.name

        (
            ffmpeg
            .input(list_file_path, format='concat', safe=0)
            .output(str(out), c='copy')
            .overwrite_output()
            .run(quiet=True, capture_stdout=True, capture_stderr=True)
        )

        return True

    except ffmpeg.Error as e:
        stderr = e.stderr.decode('utf8') if e.stderr else 'Unknown error'
        return False
    except Exception as e:
        return False
    finally:
        if list_file_path and os.path.exists(list_file_path):
            os.remove(list_file_path)

def convert_video_resolutions(input_file, resolutions, output_dir="output"):
    if not os.path.exists(input_file):
        return

    os.makedirs(output_dir, exist_ok=True)

    encoder = get_available_video_encoder()
    if not encoder:
        return


    filename = os.path.splitext(os.path.basename(input_file))[0]
    extension = ".mp4"

    bitrate_map = {
        "240": "400k",
        "360": "600k",
        "480": "1000k",
        "720": "2500k",
        "1080": "5000k",
        "1440": "10000k",
        "2160": "20000k"
    }


    for r in resolutions:
        res_str = str(r).replace("p", "")
        bitrate = bitrate_map.get(res_str, "1500k")
        output_path = os.path.join(output_dir, f"{filename}_{res_str}p{extension}")

        command = [
            "ffmpeg",
            "-i", input_file,
            "-vf", f"scale=-2:{res_str}",
            "-c:v", encoder,
            "-b:v", bitrate,
            "-c:a", "aac",
            "-b:a", "128k",
            "-y",
            output_path
        ]

        if encoder == "libx264":
            command.insert(command.index("-b:v"), "-preset")
            command.insert(command.index("-b:v") + 1, "medium")

        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        except subprocess.CalledProcessError as e:
            pass


def composite_image_over_video(
    video_path: str,
    image_path: str,
    start: float | None = None,
    end: float | None = None,
    opacity: float = 1.0,         
    vcodec: str = "libopenh264", 
    use_gpu: bool = False,       
    position: str = "top-left"  
) -> bool:
    """
    High-performance image overlay (max-speed version)

    Features:
    ✔ Configurable overlay position
    ✔ Audio preserved (copy)
    ✔ Minimal CPU usage
    ✔ Optional GPU encoding
    """

    try:
        if not video_path or not image_path:
            raise ValueError("video_path and image_path must be provided")

        input_path = Path(video_path)
        output_path = input_path.with_name(f"{input_path.stem}_overlay.mp4")

        video = ffmpeg.input(video_path)
        image = ffmpeg.input(image_path, loop=1)

        if opacity < 1.0:
            image = image.filter("format", "rgba").filter("colorchannelmixer", aa=opacity)

        enable_expr = None
        s = 0 if start is None else start
        if start is not None or end is not None:
            enable_expr = f"between(t,{s},{end})" if end is not None else f"gte(t,{s})"

        pos_map = {
            "top-left":    ("0", "0"),
            "top-right":   ("main_w-overlay_w", "0"),
            "bottom-left": ("0", "main_h-overlay_h"),
            "bottom-right":("main_w-overlay_w", "main_h-overlay_h"),
            "center":      ("(main_w-overlay_w)/2", "(main_h-overlay_h)/2")
        }
        x_expr, y_expr = pos_map.get(position, ("0", "0"))

        overlay_args: dict[str, Any] = {
            "x": x_expr,
            "y": y_expr,
            "enable": enable_expr,
            "eof_action": "repeat",
            "shortest": 1,
        }

        video_out = ffmpeg.overlay(
            video.video,
            image,
            **{k: v for k, v in overlay_args.items() if v is not None}
        )

        # Encoder settings
        output_args: dict[str, Any] = {
            "pix_fmt": "yuv420p",
            "c:a": "copy", 
        }

        if use_gpu:
            output_args["c:v"] = "h264_vaapi" 
        else:
            output_args["c:v"] = vcodec
            if vcodec == "libopenh264":
                pass
            elif vcodec == "mpeg4":
                output_args["qscale:v"] = "5"

        (
            ffmpeg
            .output(
                video_out,
                video.audio, 
                output_path.as_posix(),
                **output_args
            )
            .overwrite_output()
            .run()
        )

        return True

    except ffmpeg.Error as e:
        return False
    except Exception as e:
        return False