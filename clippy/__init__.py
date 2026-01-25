"""Main package file for ClipPy."""

from .src.core.audio_extractor import get_audio_from_video, extract_audio, get_default_output_path
from .src.core.video_tools import merge_videos, composite_image_over_video
from .src.utils.validation import validate_video_file, validate_ffmpeg

__version__ = "1.0.0"
__author__ = "ClipPy Team"
__all__ = [
    "get_audio_from_video", 
    "extract_audio", 
    "get_default_output_path",
    "validate_video_file",
    "validate_ffmpeg",
    "merge_videos",
    "composite_image_over_video"
]
