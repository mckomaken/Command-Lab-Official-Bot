import os
import random

from PIL import Image, ImageDraw, ImageFont

img = Image.open("./assets/death_screen_bg.png").convert("RGBA")
filter_img = Image.new("RGBA", size=img.size, color=0xff0000ff)
img = Image.blend(img, filter_img, 0.2)

draw = ImageDraw.Draw(img)

def unifont(size: int):
    return ImageFont.truetype(os.path.join(os.getenv("BASE_DIR", "."), "assets/mcfont.ttf"), size)

msg = "akpcは殺された"
score = "スコア："

def drawtext(text: str, y: float, size: int):
    draw.text(((img.width / 2) - (draw.textlength(text, font=unifont(size)) / 2) + 1, y + 2), text, fill=0x42424201, font=unifont(size))
    draw.text(((img.width / 2) - (draw.textlength(text, font=unifont(size)) / 2) - 1, y), text, fill=0xffffffff, font=unifont(size))


drawtext("死んでしまった！", 256, 74)
drawtext(msg, 364, 32)
drawtext(f"{score}{random.randint(1, 9999)}", 428, 32)

respawn_button = Image.open("./assets/button-respawn.png").convert("RGBA")
title_button = Image.open("./assets/button-title.png").convert("RGBA")

img.paste(respawn_button, (560, 563))
img.paste(title_button, (560, 659))


img.show()