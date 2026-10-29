import os
import shutil
import subprocess
import tempfile

import imageio_ffmpeg
from django.conf import settings

WIDTH, HEIGHT = 1280, 720
FPS = 30
SLIDE_DURATION = 3.5
FADE_DURATION = 0.8
ZOOM_AMOUNT = 0.08

SLIDE_FRAMES = int(SLIDE_DURATION * FPS)   # 105
FADE_FRAMES = int(FADE_DURATION * FPS)     # 24

# Small, predictable memory use (every extra ffmpeg thread allocates its own frame buffers,
# which hurts on many-core Windows machines).
LOW_MEM_ARGS = ["-threads", "2", "-filter_threads", "1", "-filter_complex_threads", "1"]

# All segments MUST be encoded with identical settings so they can be joined without re-encoding.
ENCODE_ARGS = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
               "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", str(FPS * 2), "-an"]


def _run(cmd, label):
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] FFmpeg failed during: {label}")
        print((e.stderr or "")[-2000:])
        return False


def _slide_chain(in_label, out_label, start_frame, count):
    """Filter chain: fit image on blurred background, then slow zoom.
    Produces `count` frames of the slide, beginning at frame `start_frame` of its 105-frame zoom,
    so any piece of a slide is identical to the same frames of the full slide."""
    z = f"(1+{ZOOM_AMOUNT}*(n+{start_frame})/{SLIDE_FRAMES})"
    return (
        f"[{in_label}]split=2[bg_s_{out_label}][fg_s_{out_label}];"
        f"[bg_s_{out_label}]scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
        f"crop={WIDTH}:{HEIGHT},boxblur=20:10[bg_b_{out_label}];"
        f"[fg_s_{out_label}]scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease[fg_f_{out_label}];"
        f"[bg_b_{out_label}][fg_f_{out_label}]overlay=(W-w)/2:(H-h)/2,format=yuv420p,"
        # image is decoded once, then repeated as lightweight 1280x720 frames
        f"loop=loop={count - 1}:size=1:start=0,setpts=N/({FPS}*TB),fps={FPS},"
        f"scale='w=2*trunc({WIDTH}*{z}/2):h=2*trunc({HEIGHT}*{z}/2):eval=frame',"
        f"crop={WIDTH}:{HEIGHT}:(iw-{WIDTH})/2:(ih-{HEIGHT})/2,setsar=1,format=yuv420p[{out_label}]"
    )


def _render_body(ffmpeg_exe, img, start_frame, end_frame, out_path):
    """The part of one slide that is NOT inside a crossfade."""
    count = end_frame - start_frame
    graph = _slide_chain("0:v", "outv", start_frame, count)
    cmd = [ffmpeg_exe, "-y", *LOW_MEM_ARGS, "-i", img, "-filter_complex", graph,
           "-map", "[outv]", "-frames:v", str(count), *ENCODE_ARGS, out_path]
    return _run(cmd, f"slide body {os.path.basename(img)}")


def _render_transition(ffmpeg_exe, img_a, img_b, out_path):
    """Crossfade between the last FADE_FRAMES of slide A and the first FADE_FRAMES of slide B."""
    graph = (
        _slide_chain("0:v", "a", SLIDE_FRAMES - FADE_FRAMES, FADE_FRAMES) + ";" +
        _slide_chain("1:v", "b", 0, FADE_FRAMES) + ";" +
        f"[a][b]xfade=transition=fade:duration={FADE_DURATION}:offset=0[outv]"
    )
    cmd = [ffmpeg_exe, "-y", *LOW_MEM_ARGS, "-i", img_a, "-i", img_b, "-filter_complex", graph,
           "-map", "[outv]", "-frames:v", str(FADE_FRAMES), *ENCODE_ARGS, out_path]
    return _run(cmd, f"transition {os.path.basename(img_a)} -> {os.path.basename(img_b)}")


def _concat(ffmpeg_exe, segments, output_path, tmp_dir):
    list_file = os.path.join(tmp_dir, "segments.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        for s in segments:
            f.write("file '{}'\n".format(s.replace("\\", "/")))
    cmd = [ffmpeg_exe, "-y", "-f", "concat", "-safe", "0", "-i", list_file,
           "-c", "copy", "-movflags", "+faststart", output_path]
    return _run(cmd, "final concat")


def _is_valid_image(path):
    try:
        from PIL import Image
        with Image.open(path) as im:
            im.verify()
        return True
    except Exception:
        return False


def generate_property_slideshow(image_paths, output_relative_path):
    output_full_path = os.path.join(settings.MEDIA_ROOT, output_relative_path)
    os.makedirs(os.path.dirname(output_full_path), exist_ok=True)

    print("=" * 60)
    print("[INFO] GENERATING PROPERTY SLIDESHOW VIDEO")

    valid_images = [p.replace("\\", "/") for p in image_paths if os.path.exists(p)]
    skipped = [p for p in valid_images if not _is_valid_image(p)]
    for p in skipped:
        print(f"[WARN] Skipping unreadable image: {p}")
    valid_images = [p for p in valid_images if p not in skipped]
    if not valid_images:
        print("[ERROR] No valid images found on disk.")
        return None

    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    tmp_dir = tempfile.mkdtemp(prefix="slideshow_")
    try:
        n = len(valid_images)
        segments = []
        for i, img in enumerate(valid_images):
            has_prev = i > 0
            has_next = i < n - 1
            start = FADE_FRAMES if has_prev else 0                 # first FADE_FRAMES were used by previous transition
            end = SLIDE_FRAMES - FADE_FRAMES if has_next else SLIDE_FRAMES  # last FADE_FRAMES go into next transition

            if has_prev:
                tr = os.path.join(tmp_dir, f"seg_{i:03d}_a_transition.mp4")
                if not _render_transition(ffmpeg_exe, valid_images[i - 1], img, tr):
                    return None
                segments.append(tr)

            body = os.path.join(tmp_dir, f"seg_{i:03d}_b_body.mp4")
            if not _render_body(ffmpeg_exe, img, start, end, body):
                return None
            segments.append(body)

        print("[INFO] Joining segments...")
        if not _concat(ffmpeg_exe, segments, output_full_path, tmp_dir):
            return None

        print("[SUCCESS] Property video rendered!")
        return output_relative_path
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)