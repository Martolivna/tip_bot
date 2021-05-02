from io import BytesIO
import random

from PIL import Image, ImageDraw, ImageFont

TEMPLATE = Image.open("template.png").convert("RGBA")

FONT = ImageFont.truetype("radiance-regular.otf", 23)

PIC_SIZE = (141, 78)
TEXT_Y = 120+30
PIC_Y = 13+30

LEFT_PIC = (13, PIC_Y)
RIGHT_PIC = (262, PIC_Y)

LEFT_NAME = (LEFT_PIC[0] + 70, TEXT_Y)
RIGHT_NAME = (RIGHT_PIC[0] + 70, TEXT_Y)

COLORS = (
    (1, 68, 201),
    (88, 219, 165),
    (132, 2, 123),
    (195, 95, 9),
    (198, 86, 0),

    (185, 97, 145),
    (128, 142, 55),
    (80, 172, 195),
    (6, 104, 27),
    (119, 77, 5),
)


def make_image(l_name, l_photo, r_name, r_photo):
    img = _make_image(l_name, l_photo, r_name, r_photo)
    iob = BytesIO()
    img.save(iob, format='png')
    return iob.getvalue()


def _make_image(l_name, l_photo, r_name, r_photo):
    l_color, r_color = random.choices(COLORS, k=2)

    txt = Image.new("RGBA", TEMPLATE.size, (255, 255, 255, 0))
    d = ImageDraw.Draw(txt)

    d.text(LEFT_NAME, l_name, font=FONT, fill=l_color, anchor='mb')
    d.text(RIGHT_NAME, r_name, font=FONT, fill=r_color, anchor='mb')

    if l_photo:
        txt.paste(prepare_pic(l_photo), LEFT_PIC)
    if r_photo:
        txt.paste(prepare_pic(r_photo), RIGHT_PIC)

    out = Image.alpha_composite(TEMPLATE, txt)
    return out


def prepare_pic(pic):
    img = Image.open(pic)
    img = img.resize((PIC_SIZE[0], PIC_SIZE[0]))
    delta_size = (PIC_SIZE[0]-PIC_SIZE[1])/2
    img = img.crop((0, delta_size, PIC_SIZE[0], PIC_SIZE[1] + delta_size))  # crop to middle
    return img


if __name__ == "__main__":
    _make_image("Тест", None, "Тест", None).show()
