import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

import os
from django.conf import settings
from moviepy.editor import ImageClip, concatenate_videoclips

def generate_property_slideshow(image_paths, output_relative_path, seconds_per_image=2.5, fade_duration=0.5):
    """
    Shared video generator utility used across property listing modules 
    (Residential, Commercial, and PG/Co-living).
    """
    if not image_paths:
        return None

    clips = []
    try:
        for path in image_paths:
            if not os.path.exists(path):
                continue
            
            # Initialize ImageClip and standardize height
            clip = ImageClip(path).set_duration(seconds_per_image).resize(height=720)
            
            # Apply fades safely
            if fade_duration > 0 and seconds_per_image > (2 * fade_duration):
                clip = clip.fadein(fade_duration).fadeout(fade_duration)
                
            clips.append(clip)

        if not clips:
            return None

        # Concatenate clips using compose method with crossfade overlap padding
        final = concatenate_videoclips(clips, method="compose", padding=-fade_duration)
        
        output_abs_path = os.path.join(settings.MEDIA_ROOT, output_relative_path)
        os.makedirs(os.path.dirname(output_abs_path), exist_ok=True)
        
        final.write_videofile(
            output_abs_path, 
            fps=24, 
            codec="libx264", 
            audio=False, 
            preset="medium", 
            threads=2, 
            logger=None
        )
        
        return output_relative_path

    except Exception as e:
        print(f"SLIDESHOW GENERATION ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

    finally:
        # Resource cleanup to prevent handle leaks across listing modules
        for c in clips:
            try:
                c.close()
            except:
                pass
        try:
            if 'final' in locals() and final:
                final.close()
        except:
            pass