"""Ders notu için (a), (b), (c) etiketi ekleyen yardımcı.

Görsel önce çizime göre kırpılır, sonra altına etiket satırı eklenir. Kırpma
payı (PAY) etiketin çizime olan uzaklığını belirler: pay kadar beyazlık
bırakılır, etiket onun hemen altına yazılır. Böylece etiket satırı çizime
yapışmaz ama arada gereksiz boşluk da kalmaz (hafta 8'in üç yanıltma
şemasında bu aralık eşitlenir).
"""

from PIL import Image, ImageChops, ImageDraw, ImageFont

YAZI = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
RENK = (31, 56, 100)
PAY = 8   # çizim ile etiket satırı arasındaki boşluk (piksel)
BANT = 40  # etiket satırının yüksekliği


def etiketle(kaynak, hedef):
    im = Image.open(kaynak).convert("RGB")

    # çizimin dışındaki beyaz alanı at; pay kadar beyaz bırak
    zemin = Image.new("RGB", im.size, (255, 255, 255))
    kutu = ImageChops.difference(im, zemin).getbbox()
    if kutu:
        kutu = (max(0, kutu[0] - PAY), max(0, kutu[1] - PAY),
                min(im.width, kutu[2] + PAY), min(im.height, kutu[3] + PAY))
        im = im.crop(kutu)

    gen, yuk = im.size
    tuval = Image.new("RGB", (gen, yuk + BANT), "white")
    tuval.paste(im, (0, 0))

    cizim = ImageDraw.Draw(tuval)
    yazi = ImageFont.truetype(YAZI, 27)
    for i, etiket in enumerate(("(a)", "(b)", "(c)")):
        x = gen * (1 / 6 + i / 3)
        kutu = cizim.textbbox((0, 0), etiket, font=yazi)
        # kutu[1] yazının kendi üst boşluğudur; çıkarınca metin tam yuk'ta başlar
        cizim.text((x - (kutu[2] - kutu[0]) / 2, yuk - kutu[1]), etiket, font=yazi, fill=RENK)

    tuval.save(hedef)
    print(f"yazıldı: {hedef}")
