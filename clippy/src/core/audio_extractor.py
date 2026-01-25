import ffmpeg
from pathlib import Path

from ..utils.validation import validate_video_file, validate_ffmpeg
from ..cli.interface import validate_and_get_output_path


def extract_audio(video_path, output_path, audio_format='mp3'):
    try:
        audio_codec = 'mp3' if audio_format.lower() == 'mp3' else 'pcm_s16le'

        stream = ffmpeg.input(str(video_path))
        stream = ffmpeg.output(stream, str(output_path), acodec=audio_codec, loglevel='quiet')

        ffmpeg.run(stream, overwrite_output=True, quiet=True)

        print(f"Successfully extracted audio to: {output_path}")
        return True

    except ImportError:
        print("Error: ffmpeg-python is not installed.")
        print("Install it using: pip install ffmpeg-python")
        return False
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during audio extraction: {e}")
        return False


def get_default_output_path(video_path, audio_format='mp3'):
    video_path = Path(video_path)
    output_filename = video_path.stem + '.' + audio_format
    return video_path.parent / output_filename


def get_audio_from_video(video_path, output_path=None, audio_format='mp3'):
    """
    Library function to extract audio from video.
    
    Args:
        video_path (str): Path to the input video file
        output_path (str, optional): Path for the output audio file
        audio_format (str): Audio format ('mp3' or 'wav')
        
    Returns:
        bool: True if extraction was successful, False otherwise
    """
    if not validate_video_file(video_path):
        return False
    
    if not validate_ffmpeg():
        return False
    
    output_path = validate_and_get_output_path(video_path, output_path, audio_format)
    
    return extract_audio(video_path, str(output_path), audio_format)
