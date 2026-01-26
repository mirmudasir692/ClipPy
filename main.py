from clippy.src.core.validation import validate_video

is_valid, reason = validate_video("Audio1.mp3")
print("reason : ", reason)
if is_valid:
    print("Good to go")
else:
    print(f"Error: {reason}")