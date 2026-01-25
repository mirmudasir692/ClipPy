import argparse
import sys
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="ClipPy - Extract audio from video files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python %(prog)s -i video.mp4                    # Extract to video.mp3
  python %(prog)s -i video.mp4 -o audio.wav      # Extract to audio.wav
  python %(prog)s -i video.mkv -f mp3            # Extract to video.mp3
        """
    )

    parser.add_argument('-i', '--input', required=True, help='Input video file path')
    parser.add_argument('-o', '--output', help='Output audio file path (optional)')
    parser.add_argument('-f', '--format', choices=['mp3', 'wav'], default='mp3',
                       help='Output audio format (default: mp3)')

    return parser.parse_args()


def show_usage_instructions():
    print("ClipPy - Audio Extraction Tool")
    print("==============================")
    print("This script extracts audio from video files using ClipPy.")
    print()
    print("Usage: python main.py -i <input_video> [-o <output_audio>] [-f <format>]")
    print()
    print("Options:")
    print("  -i, --input   Input video file path (required)")
    print("  -o, --output  Output audio file path (optional)")
    print("  -f, --format  Output format: mp3 or wav (default: mp3)")
    print()
    print("Example: python main.py -i video.mp4 -o audio.mp3")


def install_dependencies():
    print()
    print("To install required dependencies, run:")
    print("pip install ffmpeg-python")


def validate_and_get_output_path(input_path, output_path=None, audio_format='mp3'):
    if output_path:
        output_path = Path(output_path)
    else:
        input_path = Path(input_path)
        output_filename = input_path.stem + '.' + audio_format
        output_path = input_path.parent / output_filename

    output_dir = output_path.parent
    if not output_dir.exists():
        print(f"Error: Output directory does not exist: {output_dir}")
        sys.exit(1)

    return output_path
