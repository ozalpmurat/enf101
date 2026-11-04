#!/usr/bin/env python3
"""Üç kritik yanıltma örneği — tek figür (8. hafta).

Üç sütun, her sütunda doğru (üst) ve yanıltıcı (alt) grafik:
kesilmiş eksen, alan ve hacim yanılsaması, seçilmiş zaman aralığı.
Şemanın içine başlık yazılmaz; başlık ders notunda şekil künyesi, sunumda slayt başlığıdır.

Çıktı: hafta-08-hesap-tablosu/gorseller/diagram-yaniltma-3-ornek.png
"""

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image, ImageChops

CM = 1 / 2.54
GENISLIK_CM, YUKSEKLIK_CM = 13.4, 6.2

LACIVERT = "#1F3864"
MAVI = "#2E74B5"
GRI = "#8C8C8C"
YANILTICI = "#EB4034"

SOL = [1 / 6 - 0.115, 0.5 - 0.115, 5 / 6 - 0.115]

VERI_KESIK = [96, 98, 97, 99]
SERI = [52, 55, 54, 58, 60, 57, 58, 56, 62, 64, 65]


def susle(ax, yticks, ylim, xticks=None, xsize=6):
    if xticks is None:
        ax.set_xticks([])
    else:
        ax.set_xticks(xticks)
        ax.set_xticklabels([str(t) for t in xticks], fontsize=xsize)
    ax.set_yticks(yticks)
    ax.set_ylim(*ylim)
    ax.tick_params(axis="y", labelsize=6, colors=LACIVERT, length=2)
    ax.tick_params(axis="x", colors=LACIVERT, length=2, pad=1.5)
    for kenar in ("top", "right", "left"):
        ax.spines[kenar].set_visible(False)
    ax.spines["bottom"].set_color(GRI)


def kesik_eksen(fig):
    """1. sütun: eksen 0'dan başlarken ve 95'ten başlarken aynı dört değer."""
    ust = fig.add_axes([SOL[0], 0.618, 0.23, 0.30])
    alt = fig.add_axes([SOL[0], 0.18, 0.23, 0.30])

    ust.bar(range(len(VERI_KESIK)), VERI_KESIK, color=MAVI, width=0.6)
    susle(ust, [0, 100], (0, 105))

    alt.bar(range(len(VERI_KESIK)), VERI_KESIK, color=YANILTICI, width=0.6)
    susle(alt, [95, 99], (94.4, 99.6))

    return ust, alt


def alan_hacim(fig):
    """2. sütun: dairelerin alanı mı çapı mı değerle orantılı?"""
    ust = fig.add_axes([SOL[1], 0.618, 0.23, 0.30])
    alt = fig.add_axes([SOL[1], 0.18, 0.23, 0.30])

    deger = [10, 20, 30]
    x = [-0.88, 0, 0.88]

    for eksen, oran, renk in ((ust, "alan", MAVI), (alt, "cap", YANILTICI)):
        for xi, d in zip(x, deger):
            r = 0.26 * math.sqrt(d / 10) if oran == "alan" else 0.14 * (d / 10)
            eksen.add_patch(Circle((xi, 0.12), r, color=renk))
            eksen.text(xi, -0.80, str(d), ha="center", fontsize=6, color=LACIVERT)
        eksen.set_xlim(-1.42, 1.42)
        eksen.set_ylim(-0.95, 0.75)
        eksen.set_aspect("equal")
        eksen.axis("off")
        eksen.text(-1.40, 0.62, "alanla orantılı" if oran == "alan" else "çapla orantılı",
                   fontsize=5.2, color=GRI)

    return ust, alt


def zaman_araligi(fig):
    """3. sütun: bütün seri yükselirken seçilen 4–7 aralığı düşüyor."""
    ust = fig.add_axes([SOL[2], 0.618, 0.23, 0.30])
    alt = fig.add_axes([SOL[2], 0.18, 0.23, 0.30])

    ust.plot(range(len(SERI)), SERI, color=MAVI, lw=1.3, marker="o", ms=1.6)
    susle(ust, [50, 55, 60, 65], (49, 66.5), xticks=range(len(SERI)), xsize=4.2)

    alt.plot(range(4, 8), SERI[4:8], color=YANILTICI, lw=1.3, marker="o", ms=1.6)
    susle(alt, [50, 55, 60, 65], (49, 66.5), xticks=range(4, 8), xsize=5)

    return ust, alt


def ciz(hedef):
    fig = plt.figure(figsize=(GENISLIK_CM * CM, YUKSEKLIK_CM * CM), dpi=300)
    ciftler = [kesik_eksen(fig), alan_hacim(fig), zaman_araligi(fig)]
    ipuclari = ["eksen 95'ten başlıyor", "çap 2 kat, alan 4 kat", "eğilim tersine çevrildi"]

    for (ust, alt), ipucu in zip(ciftler, ipuclari):
        ust.text(0.0, 1.04, "doğru", transform=ust.transAxes, fontsize=6.2, color=MAVI)
        alt.text(0.0, 1.04, "yanıltıcı", transform=alt.transAxes, fontsize=6.2, color=YANILTICI)
        alt.text(0.02, -0.17, ipucu, transform=alt.transAxes, fontsize=5.4,
                 color=YANILTICI, style="italic", va="top")

    fig.add_artist(plt.Line2D([0.035, 0.965], [0.549, 0.549], transform=fig.transFigure,
                              color="black", linewidth=1.0))
    fig.savefig(hedef, facecolor="white")
    plt.close(fig)

    # kenar boşluklarını kırp
    im = Image.open(hedef).convert("RGB")
    zemin = Image.new("RGB", im.size, (255, 255, 255))
    kutu = ImageChops.difference(im, zemin).getbbox()
    if kutu:
        pay = 8
        kutu = (max(0, kutu[0] - pay), max(0, kutu[1] - pay),
                min(im.width, kutu[2] + pay), min(im.height, kutu[3] + pay))
        im.crop(kutu).save(hedef)

    print(f"yazıldı: {hedef}")


if __name__ == "__main__":
    KOK = Path(__file__).resolve().parent.parent
    ciz(KOK / "hafta-08-hesap-tablosu" / "gorseller" / "diagram-yaniltma-3-ornek.png")
