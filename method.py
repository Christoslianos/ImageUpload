from PIL import Image, ImageDraw
from webcolors import rgb_to_hex


def get_colors(filename):
    image = Image.open(filename)
    resize_image = image.resize((100, 100))
    result = resize_image.convert('P', palette=Image.ADAPTIVE, colors=10)

    # find colors
    palette = result.getpalette()
    number_of_colors = sorted(result.getcolors(), reverse=True)
    colors = []

    for j in range(10):
        palette_index = number_of_colors[j][1]
        dominant_color = palette[palette_index * 3: palette_index * 3 + 3]
        colors.append(tuple(dominant_color))

    return colors


def upload_image_process(filename, palette_division, numcolors=10):
    # palette width
    palette_width = 100

    uploaded_image = Image.open(filename)
    width, height = uploaded_image.size

    # palette height that placed under the picture
    img_palette_height = int(height / palette_division)
    img_palette_width = width / 10

    # empty canvas för the uploaded image and the palette
    processed_image = Image.new('RGB', (width, height + img_palette_height))

    palette_under_image = Image.new('RGB', (width, img_palette_height))

    # empty canvas for the palette
    new_palette = Image.new('RGB', (numcolors * palette_width, palette_width + 20), color="rgb(255, 255,255)")

    draw = ImageDraw.Draw(palette_under_image)
    draw2 = ImageDraw.Draw(new_palette)


    posx = 0
    posx2 = 0


    colors = get_colors(filename)
    # creating the palette
    for color in colors:
        draw.rectangle([posx, 0, posx + img_palette_width, img_palette_height], fill=color)

        # drawing each palette
        draw2.rectangle([posx2, 0, posx2 + palette_width, palette_width], fill=color)

        draw2.text((posx2 + 20, palette_width), rgb_to_hex(color[:3]), fill="rgb(0,0,0)")

        # move the pointer to the beginning of the next palette
        posx = posx + img_palette_width
        posx2 = posx2 + palette_width


    box = (0, height, width, height + img_palette_height)



    # pasting the image and the palette on the canvas
    processed_image.paste(uploaded_image)
    processed_image.paste(palette_under_image, box)

    return processed_image, palette_under_image
