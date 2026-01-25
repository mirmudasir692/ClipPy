import os
import subprocess
from pathlib import Path


def validate_video_file(video_path):
    video_path = Path(video_path)
    
    if not video_path.exists():
        print(f"Error: Video file '{video_path}' does not exist.")
        return False

    if not video_path.is_file():
        print(f"Error: '{video_path}' is not a file.")
        return False

    supported_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp', '.f4v'}
    file_extension = video_path.suffix.lower()

    if file_extension not in supported_extensions:
        print(f"Warning: File extension '{file_extension}' might not be supported.")
        print(f"Supported extensions: {', '.join(supported_extensions)}")
        return False

    return True


def validate_ffmpeg():
    try:
        result = subprocess.run(['ffmpeg', '-version'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True)
        return result.returncode == 0
    except FileNotFoundError:
        print("Error: ffmpeg is not installed or not found in system PATH.")
        print("Please install ffmpeg before running this script.")
        return False
    except Exception as e:
        print(f"Error checking ffmpeg: {e}")
        return False
