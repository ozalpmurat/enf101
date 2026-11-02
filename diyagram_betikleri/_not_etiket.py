"""Ders notu için (a), (b), (c) etiketi ekleyen yardımcı."""

from PIL import Image, ImageDraw, ImageFont

YAZI = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
RENK = (31, 56, 100)
BANT = 54


def etiketle(kaynak, hedef):
    im = Image.open(kaynak).convert("RGB")
    gen, yuk = im.size
    tuval = Image.new("RGB", (gen, yuk + BANT), "white")
    tuval.paste(im, (0, 0))

    cizim = ImageDraw.Draw(tuval)
    yazi = ImageFont.truetype(YAZI, 27)
    for i, etiket in enumerate(("(a)", "(b)", "(c)")):
        x = gen * (1 / 6 + i / 3)
        kutu = cizim.textbbox((0, 0), etiket, font=yazi)
        cizim.text((x - (kutu[2] - kutu[0]) / 2, yuk + 10), etiket, font=yazi, fill=RENK)

    tuval.save(hedef)
    print(f"yazıldı: {hedef}")
