"""Core module for ClipPy package."""
from .audio_extractor import get_audio_from_video, extract_audio, get_default_output_path
from .video_tools import merge_videos, composite_image_over_video, convert_video_resolutions, get_video_thumbnail, crop_video
from ..setup.setup import setup

__all__ = ["get_audio_from_video", "extract_audio", "get_default_output_path", "merge_videos", "composite_image_over_video", "setup", "convert_video_resolutions", "get_video_thumbnail", "crop_video"]
