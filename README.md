# Clip Generator

This project generates a video from a list of images. Each image is zoomed in gradually, and the video transitions between images with a fade effect. Text fades in at the end of the video.

## Requirements

- Python 3.7 or higher
- `ffmpeg`: This is required by the `moviepy` library for video processing.
- `moviepy`: This is used for video processing.
- `numpy`: This is used for numerical operations.
- `Pillow`: This is used for image processing.
- `ImageMagick`: This is used for adding text to the video. Make sure to have the `ImageMagick` binary installed and the path correctly set. For Windows users, this typically involves checking a box during the ImageMagick installation process to add it to your system path.

You can install the Python dependencies with pip by running:

```
pip install -r requirements.txt
```

## Usage

To generate a video, call the `generate_video` function with a list of image files as input. You can optionally specify an output file name and the resolution of the output video. The function returns the path to the output video file.

Here is an example of how to use the function:

```
from video_generator import generate_video

# List of image files
images = ['image1.jpg', 'image2.jpg', 'image3.jpg']

# Generate the video
output_file = generate_video(images, 'output.mp4')

print(f'Video saved to {output_file}')
```

This will generate a video where each image is shown for 6 seconds, with a 1-second fade effect between images. The text "Get yours today!" and "Link in description!" will fade in at the end of the video.
