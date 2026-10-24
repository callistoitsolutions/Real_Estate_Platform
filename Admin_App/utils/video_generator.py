import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

import os
import cv2
import numpy as np
from django.conf import settings

def generate_property_slideshow(image_paths, output_relative_path, seconds_per_image=2.5, fps=24):
    """
    Pure OpenCV property slideshow generator. Completely removes MoviePy and FFmpeg 
    filter graph overhead to prevent 'Cannot allocate memory' and 'xfade' crashes.
    """
    if not image_paths:
        return None

    valid_images = []
    processed_temp_files = []
    
    try:
        # 1. Preprocess and resize images to standard HD (1280x720) with letterboxing
        
        for path in image_paths:
            if not os.path.exists(path):
                continue
            try:
                with PIL.Image.open(path) as img:
                    img = img.convert('RGB')
                    
                    target_w, target_h = 1280, 720
                    img.thumbnail((target_w, target_h), PIL.Image.LANCZOS)
                    
                    # Create a dark slate background canvas and paste centered

                    new_img = PIL.Image.new("RGB", (target_w, target_h), (15, 23, 42))
                    paste_x = (target_w - img.size[0]) // 2
                    paste_y = (target_h - img.size[1]) // 2
                    new_img.paste(img, (paste_x, paste_y))
                    
                    temp_path = path + "_cv_opt.jpg"
                    new_img.save(temp_path, "JPEG", quality=90)
                    processed_temp_files.append(temp_path)
                    valid_images.append(temp_path)
            except Exception as img_err:
                print(f"IMAGE PREPROCESSING ERROR ({path}): {str(img_err)}")

        if not valid_images:
            return None

        output_abs_path = os.path.join(settings.MEDIA_ROOT, output_relative_path)
        os.makedirs(os.path.dirname(output_abs_path), exist_ok=True)

        # 2. Initialize OpenCV VideoWriter

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_abs_path, fourcc, fps, (1280, 720))

        if not video_writer.isOpened():
            print("ERROR: Failed to open OpenCV VideoWriter.")
            return None

        frames_per_image = int(fps * seconds_per_image)

        # 3. Write frames directly into video stream

        for img_path in valid_images:
            frame_bgr = cv2.imread(img_path)
            if frame_bgr is None:
                continue
            
            for _ in range(frames_per_image):
                video_writer.write(frame_bgr)

        video_writer.release()
        return output_relative_path

    except Exception as e:
        print(f"OPENCV SLIDESHOW GENERATION ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

    finally:
        # Clean up temporary processed image files
        for temp_path in processed_temp_files:
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except:
                pass