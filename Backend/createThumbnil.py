from PIL import Image, ImageDraw, ImageFont

def draw_centered_text(draw, text, font, image_width, image_height,
                       v_align="center", y_offset=0,
                       fill=(255, 255, 255), outline_color=None, outline_width=2):
    # Get text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Horizontal center
    x = (image_width - text_width) // 2

    # Vertical alignment
    if v_align == "top":
        y = 0 + y_offset
    elif v_align == "bottom":
        y = image_height - text_height - y_offset
    else:  # default to center
        y = (image_height - text_height) // 2 + y_offset

    # Draw outline
    if outline_color:
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline_color)

    # Draw main text
    draw.text((x, y), text, font=font, fill=fill)



def create_thumbnail_with_text(
    image_path,
    output_path,
    title_text,
    subtitle_text,
    font_path_bold,
    font_path_regular,
    vAlign="bottom",
    yOffset=200,
    fill=(152, 251, 74),
    outlineColor=(0, 0, 0),
    outlineWidth=3
):
    # Load image and setup
    image = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # Fonts
    title_font = ImageFont.truetype(font_path_bold, size=60)
    subtitle_font = ImageFont.truetype(font_path_regular, size=40)

    # Draw title lower on the image
    draw_centered_text(draw, title_text, title_font, image_width=width, image_height=height,
                       v_align=vAlign, y_offset=yOffset, fill=fill,
                       outline_color=outlineColor, outline_width=outlineWidth)


    if subtitle_text:
        draw_centered_text(draw, subtitle_text, subtitle_font, image_width=width, image_height=height,
                        v_align="bottom", y_offset=150, fill=(255, 255, 255),
                        outline_color=(0, 0, 0), outline_width=2)

    image.save(output_path)
    print(f"Thumbnail saved at: {output_path}")

