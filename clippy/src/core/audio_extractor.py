import ffmpeg
from pathlib import Path
import tempfile
import os
from typing import Optional


from ..utils.validation import validate_video_file, validate_ffmpeg
from ..cli.interface import validate_and_get_output_path


def extract_audio(video_path, output_path, audio_format='mp3', start=None, end=None):
    try:
        audio_codec = 'mp3' if audio_format.lower() == 'mp3' else 'pcm_s16le'

        input_kwargs = {}
        if start is not None:
            input_kwargs['ss'] = start
        if end is not None:
            input_kwargs['to'] = end

        stream = ffmpeg.input(str(video_path), **input_kwargs)
        stream = ffmpeg.output(stream, str(output_path), acodec=audio_codec, loglevel='quiet')

        ffmpeg.run(stream, overwrite_output=True, quiet=True)

        return True

    except ImportError:
        return False
    except ffmpeg.Error as e:
        return False
    except Exception as e:
        return False

def get_default_output_path(video_path, audio_format='mp3'):
    video_path = Path(video_path)
    output_filename = video_path.stem + '.' + audio_format
    return video_path.parent / output_filename


def get_audio_from_video(video_path, output_path=None, audio_format='mp3', start=None, end=None):
    """
    Library function to extract audio from video.
    
    Args:
        video_path (str): Path to the input video file
        output_path (str, optional): Path for the output audio file
        audio_format (str): Audio format ('mp3' or 'wav')
        start (float/str, optional): Start time of the slice (e.g., 10.5 or "00:00:10")
        end (float/str, optional): End time of the slice (e.g., 15.0 or "00:00:15")
        
    Returns:
        bool: True if extraction was successful, False otherwise
    """
    if not validate_video_file(video_path):
        return False
    
    if not validate_ffmpeg():
        return False
    
    output_path = validate_and_get_output_path(video_path, output_path, audio_format)
    
    return extract_audio(video_path, str(output_path), audio_format, start, end)

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