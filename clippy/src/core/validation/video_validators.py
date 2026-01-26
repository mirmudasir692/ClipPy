import subprocess
import os
import json

def validate_video(video_path: str = ""):
    """
    Validates a video file for corruption and malicious structure.
    
    Args:
        video_path (str): Path to the video file.
        
    Returns:
        tuple: (bool, str) -> (is_valid, reason)
    """
    
    if video_path == "":
        raise ValueError("video_path must be provided")

    if not os.path.exists(video_path):
        return False, "File does not exist."

    if os.path.getsize(video_path) == 0:
        return False, "File is empty (corrupt)."
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-show_streams',
        '-select_streams', 'v', 
        '-of', 'json',
        video_path
    ]

    try:
        result = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            error_msg = result.stderr.strip()
            if not error_msg:
                error_msg = "Unknown parsing error."
            return False, f"File is corrupted or invalid format: {error_msg}"
        try:
            data = json.loads(result.stdout)
            streams = data.get('streams', [])
            
            if not streams:
                return False, "Malicious/Invalid: No video stream found. File might be renamed or mislabeled."
            
            video_stream = streams[0]
            codec_name = video_stream.get('codec_name', '')
            width = video_stream.get('width', 0)
            
            if not codec_name:
                return False, "Invalid video stream detected."
                
            if width == 0:
                return False, "Corrupted video metadata (invalid resolution)."

        except json.JSONDecodeError:
            return False, "Malicious/Corrupt: File structure is unreadable."
        if result.stderr and "Invalid data" in result.stderr:
             return False, f"Warning: File contains corrupted segments. {result.stderr[:100]}"

        return True, "Video file is valid."

    except subprocess.TimeoutExpired:
        return False, "Validation timed out. File might be malformed or infinite."
    except Exception as e:
        return False, f"An unexpected error occurred: {str(e)}"