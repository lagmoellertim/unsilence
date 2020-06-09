from unsilence import Unsilence

u = Unsilence("[input_file]")

u.detect_silence()

estimated_time = u.estimate_time(audible_speed=5, silent_speed=2)  # Estimate time savings
print(estimated_time)

u.render_media("[output_file]")  # No options specified
u.render_media("[output_file]", audible_speed=2, silent_speed=8)  # Speed options
u.render_media("[output_file]", audible_volume=2, silent_volume=0)  # Volume options
u.render_media("[output_file]", audio_only=True)  # Audio only specified
