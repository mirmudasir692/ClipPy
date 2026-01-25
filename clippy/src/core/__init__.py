"""Core module for ClipPy package."""
from .audio_extractor import get_audio_from_video, extract_audio, get_default_output_path
from .video_tools import merge_videos, composite_image_over_video

__all__ = ["get_audio_from_video", "extract_audio", "get_default_output_path", "merge_videos", "composite_image_over_video"]
