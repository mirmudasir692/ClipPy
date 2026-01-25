from clippy import get_audio_from_video, merge_videos, composite_image_over_video

composite_image_over_video(
    video_path="vid.mp4",
    image_path="logo.png",
    start=20,
    opacity=0.3,
    position="center"
)
