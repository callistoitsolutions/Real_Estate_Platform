import os
import subprocess
import imageio_ffmpeg
from django.conf import settings

def generate_property_slideshow(image_paths, output_relative_path):
    output_full_path = os.path.join(settings.MEDIA_ROOT, output_relative_path)
    os.makedirs(os.path.dirname(output_full_path), exist_ok=True)

    print("=" * 60)
    print("🎬 GENERATING ROCK-SOLID PROFESSIONAL PROPERTY VIDEO")

    valid_images = [p for p in image_paths if os.path.exists(p)]
    if not valid_images:
        print("❌ ERROR: No valid images found on disk.")
        return None

    slide_duration = 3.5
    fade_duration = 0.8
    fps = 30
    total_frames = int(slide_duration * fps)
    num_images = len(valid_images)

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    input_args = []
    filter_complex = []

    for i, img_path in enumerate(valid_images):
        clean_path = img_path.replace('\\', '/')
        
        # FIX 1: Read as a single static image (Remove -loop 1 and -t)
        # This prevents loading huge 5160x3440 frames repeatedly into memory.
        input_args.extend(["-i", clean_path])

        filter_complex.append(
            f"[{i}:v]split=2[bg_src{i}][fg_src{i}];"
            
            # FIX 2: Process the blur and fit on a SINGLE frame, ensuring it is 1280x720
            f"[bg_src{i}]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,boxblur=20:10[bg_blur{i}];"
            f"[fg_src{i}]scale=1280:720:force_original_aspect_ratio=decrease[fg_fit{i}];"
            f"[bg_blur{i}][fg_fit{i}]overlay=(W-w)/2:(H-h)/2[base_frame{i}];"
            
            # FIX 3: Loop the pre-rendered 1280x720 frame into a video stream.
            # loop={total_frames-1} guarantees it outputs exactly `total_frames` lengths.
            f"[base_frame{i}]loop=loop={total_frames - 1}:size=1:start=0,setpts=N/({fps}*TB)[stream{i}];"
            
            # Finally, apply the zoom effect safely to the 1280x720 stream
            f"[stream{i}]fps={fps},"
            f"scale='w=2*trunc(1280*(1+0.08*n/{total_frames})/2):h=2*trunc(720*(1+0.08*n/{total_frames})/2):eval=frame',"
            f"crop=1280:720:(iw-1280)/2:(ih-720)/2,"
            f"setsar=1,format=yuv420p[v{i}];"
        )

    if num_images == 1:
        filter_complex.append("[v0]copy[outv]")
    else:
        prev_stream = "[v0]"
        offset = slide_duration - fade_duration
        for i in range(1, num_images):
            next_stream = f"[v{i}]"
            out_stream = f"[x{i}]" if i < num_images - 1 else "[outv]"
            filter_complex.append(
                f"{prev_stream}{next_stream}xfade=transition=fade:duration={fade_duration}:offset={offset:.2f}{out_stream};"
            )
            prev_stream = out_stream
            offset += (slide_duration - fade_duration)

    cmd = [
        ffmpeg_exe, "-y",
        *input_args,
        "-filter_complex", "".join(filter_complex),
        "-map", "[outv]",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", # Optimizes MP4 for web playback
        output_full_path
    ]

    print("🚀 Executing FFmpeg command...")
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("✅ SUCCESS: Smooth Professional Video rendered!")
        return output_relative_path
    except subprocess.CalledProcessError as e:
        print("❌ FFmpeg ERROR details:")
        print(e.stderr)
        return None