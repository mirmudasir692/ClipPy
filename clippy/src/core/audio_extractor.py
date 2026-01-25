import ffmpeg
from pathlib import Path

from ..utils.validation import validate_video_file, validate_ffmpeg
from ..cli.interface import validate_and_get_output_path


def extract_audio(video_path, output_path, audio_format='mp3', start=None, end=None):
    try:
        audio_codec = 'mp3' if audio_format.lower() == 'mp3' else 'pcm_s16le'

        # Build input arguments for slicing
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