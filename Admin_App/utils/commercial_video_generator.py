import os
import subprocess
import traceback
import imageio_ffmpeg
from django.conf import settings

def generate_commercial_property_slideshow(
    image_paths,
    output_relative_path,
    seconds_per_image=2.5,
    fade_duration=0.6,
    max_images=10,       # CHANGED: 8 -> 10, slightly more images since we have more time budget now
    timeout_seconds=25   # CHANGED: 15 -> 25, gives blur+motion enough room to finish safely
):
    """
    Generates a 720p HD MP4 walkthrough video slideshow from property image paths.
    Applies blurred-background padding and a dynamic cinematic Ken Burns zoom + pan animation.

    image_paths: list of absolute file paths to image files
    output_relative_path: relative path under MEDIA_ROOT (e.g., 'commercial_rent/videos/auto_12.mp4')
    seconds_per_image: duration of each image slide in seconds
    fade_duration: duration of crossfade transition between slides
    max_images: max number of images used in the slideshow (keeps encode time bounded)
    timeout_seconds: kill ffmpeg if it runs longer than this (safety net)
    Returns relative path string on success, or None on failure.
    """
    if not image_paths or len(image_paths) < 3:
        return None

    valid_images = [p for p in image_paths if os.path.exists(p)]
    if len(valid_images) < 3:
        return None

    if len(valid_images) > max_images:
        valid_images = valid_images[:max_images]

    fps = 24  # CHANGED: restored to 24 for smoother cinematic motion
    total_frames = int(seconds_per_image * fps)
    num_images = len(valid_images)

    # CHANGED: zoom range restored closer to original cinematic feel
    zoom_step = 0.08 / total_frames

    try:
        output_abs_path = os.path.join(settings.MEDIA_ROOT, output_relative_path)
        os.makedirs(os.path.dirname(output_abs_path), exist_ok=True)

        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        input_args = []
        filter_complex = []

        # 1. Build Inputs & Visual FX (Blurred BG + Cinematic Zoom + Pan)
        for i, img_path in enumerate(valid_images):
            clean_path = img_path.replace('\\', '/')
            input_args.extend(["-loop", "1", "-t", str(seconds_per_image), "-i", clean_path])

            # CHANGED: boxblur restored (4:1 — a middle ground: still visibly blurred/cinematic,
            # but cheaper than the original 6:2 so it doesn't fully undo our speed gains)
            filter_complex.append(
                f"[{i}:v]split=2[bg{i}][fg{i}];"
                f"[bg{i}]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,boxblur=4:1[bg_blur{i}];"
                f"[fg{i}]scale=1280:720:force_original_aspect_ratio=decrease[fg_fit{i}];"
                f"[bg_blur{i}][fg_fit{i}]overlay=(W-w)/2:(H-h)/2,format=yuv420p[base{i}];"
                f"[base{i}]fps={fps},"
                f"zoompan=z='min(zoom+{zoom_step:.6f},1.08)':d=1:s=1280x720:fps={fps},"
                f"setsar=1,format=yuv420p[v{i}];"
            )

        # 2. Build Smooth Crossfade Transitions
        prev_stream = "[v0]"
        offset = seconds_per_image - fade_duration
        for i in range(1, num_images):
            next_stream = f"[v{i}]"
            out_stream = f"[x{i}]" if i < num_images - 1 else "[outv]"
            filter_complex.append(
                f"{prev_stream}{next_stream}xfade=transition=fade:duration={fade_duration}:offset={offset:.2f}{out_stream};"
            )
            prev_stream = out_stream
            offset += (seconds_per_image - fade_duration)

        # 3. Assemble Complete FFmpeg Command
        cmd = [
            ffmpeg_exe,
            "-y",
            *input_args,
            "-filter_complex", "".join(filter_complex),
            "-map", "[outv]",
            "-c:v", "libx264",
            "-preset", "veryfast",   # CHANGED: ultrafast -> veryfast, better quality/size for the extra time budget
            "-crf", "28",            # CHANGED: 30 -> 28, better visual quality
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            "-threads", "0",
            output_abs_path
        ]

        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout_seconds
        )
        return output_relative_path

    except subprocess.TimeoutExpired:
        print(f"SLIDESHOW GENERATION ERROR: ffmpeg timed out after {timeout_seconds}s")
        return None
    except subprocess.CalledProcessError as e:
        print("SLIDESHOW GENERATION ERROR (FFmpeg):", e.stderr)
        return None
    except Exception as e:
        print("SLIDESHOW GENERATION ERROR:", str(e))
        traceback.print_exc()
        return None