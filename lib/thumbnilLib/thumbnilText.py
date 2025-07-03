from PIL import Image, ImageDraw, ImageFont
import sys, os
import logging

logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import globalVariables as gv

def draw_centered_text(
    draw,
    text,
    font,
    image_width,
    image_height,
    v_align=None,
    y_offset=None,
    fill=None,
    outline_color=None,
    outline_width=None,
    line_spacing=10  # spacing between lines
):
    v_align = v_align or "center"
    y_offset = y_offset if y_offset is not None else 0
    fill = fill or (255, 255, 255)
    outline_width = outline_width if outline_width is not None else 2

    # Auto-wrap text
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= image_width * 0.9:  # 90% of width for padding
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    # Calculate total height of all lines
    line_height = font.getbbox("Ay")[3]  # reliable height calculation
    total_text_height = len(lines) * (line_height + line_spacing) - line_spacing

    # Determine starting Y based on vertical alignment
    if v_align == "top":
        y = 0 + y_offset
    elif v_align == "bottom":
        y = image_height - total_text_height - y_offset
    else:  # center
        y = (image_height - total_text_height) // 2 + y_offset

    # Draw each line centered
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        x = (image_width - w) // 2

        # Draw outline
        if outline_color:
            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx != 0 or dy != 0:
                        draw.text((x + dx, y + dy), line, font=font, fill=outline_color)

        draw.text((x, y), line, font=font, fill=fill)
        y += line_height + line_spacing


def createThumbnailWithText(
    image_path=None,
    output_path=None,
    title_text=None,
    subtitle_text=None,
    font_path_bold=None,
    font_path_regular=None,
    title_font_size=None,
    subtitle_font_size=None,
    title_v_align=None,
    title_y_offset=None,
    title_fill=None,
    title_outline_color=None,
    title_outline_width=None,
    subtitle_v_align=None,
    subtitle_y_offset=None,
    subtitle_fill=None,
    subtitle_outline_color=None,
    subtitle_outline_width=None
):
    # Default values
    title_font_size = title_font_size if title_font_size is not None else getattr(gv, 'title_font_size', 60)
    subtitle_font_size = subtitle_font_size if subtitle_font_size is not None else getattr(gv, 'subtitle_font_size', 40)
    title_v_align = title_v_align if title_v_align is not None else getattr(gv, 'title_v_align', "bottom")
    title_y_offset = title_y_offset if title_y_offset is not None else getattr(gv, 'title_y_offset', 200)
    title_fill = title_fill if title_fill is not None else getattr(gv, 'title_fill', (152, 251, 74))
    title_outline_color = title_outline_color if title_outline_color is not None else getattr(gv, 'title_outline_color', (0, 0, 0))
    title_outline_width = title_outline_width if title_outline_width is not None else getattr(gv, 'title_outline_width', 3)

    subtitle_v_align = subtitle_v_align if subtitle_v_align is not None else getattr(gv, 'subtitle_v_align', "bottom")
    subtitle_y_offset = subtitle_y_offset if subtitle_y_offset is not None else getattr(gv, 'subtitle_y_offset', 150)
    subtitle_fill = subtitle_fill if subtitle_fill is not None else getattr(gv, 'subtitle_fill', (255, 255, 255))
    subtitle_outline_color = subtitle_outline_color if subtitle_outline_color is not None else getattr(gv, 'subtitle_outline_color', (0, 0, 0))
    subtitle_outline_width = subtitle_outline_width if subtitle_outline_width is not None else getattr(gv, 'subtitle_outline_width', 2)

    font_path_bold = font_path_bold if font_path_bold is not None else getattr(gv, 'font_path_bold', 'fonts/arialbd.ttf')
    font_path_regular = font_path_regular if font_path_regular is not None else getattr(gv, 'font_path_regular', 'fonts/arial.ttf')

    # Load image
    image = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # Load fonts
    title_font = ImageFont.truetype(font_path_bold, size=title_font_size)
    subtitle_font = ImageFont.truetype(font_path_regular, size=subtitle_font_size)

    # Draw title text
    draw_centered_text(
        draw=draw,
        text=title_text,
        font=title_font,
        image_width=width,
        image_height=height,
        v_align=title_v_align,
        y_offset=title_y_offset,
        fill=title_fill,
        outline_color=title_outline_color,
        outline_width=title_outline_width
    )

    # Draw subtitle text
    if subtitle_text:
        draw_centered_text(
            draw=draw,
            text=subtitle_text,
            font=subtitle_font,
            image_width=width,
            image_height=height,
            v_align=subtitle_v_align,
            y_offset=subtitle_y_offset,
            fill=subtitle_fill,
            outline_color=subtitle_outline_color,
            outline_width=subtitle_outline_width
        )

    image.save(output_path)
    logger.info(f"✅ Thumbnail saved at: {output_path}")
