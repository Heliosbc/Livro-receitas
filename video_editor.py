import os
import textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    ImageClip,
    CompositeVideoClip,
    concatenate_videoclips,
    vfx
)

FORMAT_DIMENSIONS = {
    "9:16": (1080, 1920),
    "16:9": (1920, 1080),
    "1:1": (1080, 1080)
}


def create_subtitle_image(text: str, width: int = 1080, height: int = 350, font_size: int = 48) -> Image.Image:
    """
    Renders styled subtitle text with dark semi-transparent background and yellow/white text using PIL.
    Returns PIL Image (RGBA).
    """
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Try loading default font or fallback
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except Exception:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

    # Wrap text based on width
    wrap_width = max(20, int(width / 38))
    wrapped_lines = textwrap.wrap(text, width=wrap_width)

    # Calculate line positions
    line_height = font_size + 10
    total_text_height = len(wrapped_lines) * line_height
    start_y = (height - total_text_height) // 2

    # Draw semi-transparent background box behind subtitles
    padding = 20
    box_top = max(0, start_y - padding)
    box_bottom = min(height, start_y + total_text_height + padding)
    draw.rounded_rectangle(
        [(40, box_top), (width - 40, box_bottom)],
        radius=15,
        fill=(0, 0, 0, 180)
    )

    # Render each line with stroke/outline
    for i, line in enumerate(wrapped_lines):
        line_y = start_y + i * line_height

        # Calculate text width for center alignment
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        text_x = (width - text_w) // 2

        # Draw outline
        stroke_color = (0, 0, 0, 255)
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2), (-2, 0), (2, 0), (0, -2), (0, 2)]:
            draw.text((text_x + dx, line_y + dy), line, font=font, fill=stroke_color)

        # Draw main text (Yellow for short punchy style)
        draw.text((text_x, line_y), line, font=font, fill=(255, 235, 59, 255))

    return img


def create_scene_clip(video_path: str, audio_path: str, narration_text: str, target_format: str = "9:16") -> CompositeVideoClip:
    """
    Creates a single scene clip combining background video, narration audio, and dynamic subtitle overlay.
    """
    target_width, target_height = FORMAT_DIMENSIONS.get(target_format, (1080, 1920))

    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    bg_clip = VideoFileClip(video_path)

    # Loop or trim background video to match narration duration
    if bg_clip.duration < duration:
        bg_clip = bg_clip.with_effects([vfx.Loop(duration=duration)])
    else:
        bg_clip = bg_clip.subclipped(0, duration)

    # Resize/Crop video to target aspect ratio
    bg_w, bg_h = bg_clip.size
    target_aspect = target_width / target_height
    current_aspect = bg_w / bg_h

    if current_aspect > target_aspect:
        # Video is wider -> crop left/right
        new_w = int(bg_h * target_aspect)
        x1 = (bg_w - new_w) // 2
        bg_clip = bg_clip.cropped(x1=x1, width=new_w, height=bg_h)
    else:
        # Video is taller or equal -> crop top/bottom
        new_h = int(bg_w / target_aspect)
        y1 = (bg_h - new_h) // 2
        bg_clip = bg_clip.cropped(y1=y1, width=bg_w, height=new_h)

    bg_clip = bg_clip.resized(new_size=(target_width, target_height))

    # Generate Subtitle Overlay
    sub_box_height = int(target_height * 0.2)
    pil_sub_img = create_subtitle_image(narration_text, width=target_width, height=sub_box_height)
    np_sub_img = np.array(pil_sub_img)

    sub_y_pos = target_height - sub_box_height - int(target_height * 0.1)
    subtitle_clip = (
        ImageClip(np_sub_img)
        .with_duration(duration)
        .with_position(("center", sub_y_pos))
    )

    composite = CompositeVideoClip([bg_clip, subtitle_clip], size=(target_width, target_height))
    composite = composite.with_audio(audio_clip).with_duration(duration)
    return composite


def assemble_final_video(scene_clips: list, output_filename: str) -> str:
    """
    Concatenates all scene clips into final video file.
    """
    os.makedirs(os.path.dirname(output_filename) if os.path.dirname(output_filename) else ".", exist_ok=True)
    final_clip = concatenate_videoclips(scene_clips, method="compose")
    final_clip.write_videofile(
        output_filename,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        preset="fast",
        logger="bar"
    )
    return output_filename


if __name__ == "__main__":
    print("Módulo de edição de vídeo configurado.")
