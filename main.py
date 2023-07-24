import tempfile
import os
import math
import moviepy.editor as mp
from PIL import Image
import numpy as np

def zoom_in_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        w, h = img.size
        new_w = int(w * (1 + (zoom_ratio * t)))
        new_h = int(new_w * (h / w))
        new_size = (new_w, new_h)

        img = img.resize(new_size, Image.LANCZOS)

        x = int(math.ceil((new_size[0] - base_size[0]) / 2))
        y = int(math.ceil((new_size[1] - base_size[1]) / 2))

        img = img.crop([x, y, new_size[0] - x, new_size[1] - y]).resize(base_size, Image.LANCZOS)

        result = np.array(img)
        img.close()

        return result

    return clip.fl(effect)

def resize_and_crop(img_path, size):
    img = Image.open(img_path)
    width, height = img.size
    scale = max(size[0]/width, size[1]/height)

    new_width, new_height = round(width*scale), round(height*scale)
    img = img.resize((new_width, new_height), Image.LANCZOS)

    left = (img.width - size[0]) / 2
    top = (img.height - size[1]) / 2
    right = (img.width + size[0]) / 2
    bottom = (img.height + size[1]) / 2

    img = img.crop((left, top, right, bottom))
    return img

def generate_video(image_files, output_file='output.mp4', song_file='song.mp3', resolution=(1080, 1920)):
    size = resolution

    clips = []
    temp_files = []  # List to store the temporary files
    for image in image_files:
        # Resize and crop the image
        img = resize_and_crop(image, size)

        # Create a temporary file and save the image
        temp = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        img.save(temp.name)
        img.close()
        temp_files.append(temp)  # Add the temporary file to the list

        # Load the image file as a clip
        img_clip = mp.ImageClip(temp.name).set_fps(30).set_duration(6)
        img_clip = zoom_in_effect(img_clip, 0.15)

        # Add 1 second fade-in and fade-out effect
        img_clip = img_clip.crossfadein(1).crossfadeout(1)

        clips.append(img_clip)

    # Concatenate the clips together
    video = mp.concatenate_videoclips(clips, method="compose")

    # Add audio
    audio = mp.AudioFileClip(song_file)
    audio = audio.subclip(0, video.duration)  # Cut the audio to the video length
    video = video.set_audio(audio)

    # Add text
    txt_clip1 = mp.TextClip("Get yours today!", fontsize=70, color='white')
    txt_clip1 = txt_clip1.set_pos(('center', 'center')).set_duration(2).fadein(1)

    txt_clip2 = mp.TextClip("Link in description!", fontsize=70, color='white')
    txt_clip2 = txt_clip2.set_pos(('center', video.size[1]//2 + 70)).set_duration(2).fadein(1)

    video = mp.CompositeVideoClip([video, txt_clip1.set_start(video.duration-2), txt_clip2.set_start(video.duration-2)])

    # Write the result to a file
    video.write_videofile(output_file, codec='libx264', fps=30)

    # Delete temporary files
    for temp in temp_files:
        temp.close()  # Make sure the file is no longer in use
        os.unlink(temp.name)

    return output_file