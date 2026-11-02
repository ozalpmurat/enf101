#!/usr/bin/env python3
"""Ölçek ve oran kaynaklı yanıltma örneği (8. hafta).

Üç sütun, her sütunda doğru (üst) ve yanıltıcı (alt) grafik:
alan/hacim yanılsaması, üç boyutlu efekt, çift eksen.

Çıktı: hafta-08-hesap-tablosu/gorseller/diagram-yaniltma-olcek.png
"""

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

CM = 1 / 2.54
GENISLIK_CM, YUKSEKLIK_CM = 13.4, 6.2

LACIVERT = "#1F3864"
MAVI = "#2E74B5"
GRI = "#8C8C8C"
YANILTICI = "#EB4034"
YESIL = "#2E7D32"

IPUCLARI = ["çap 2 kat, alan 4 kat", "eğik bakış dilimleri bozar", "iki ayrı eksen ilişki uydurur"]
SOL = [1 / 6 - 0.115, 0.5 - 0.115, 5 / 6 - 0.115]


def susle(ax, yticks, ylim):
    ax.set_xticks([])
    ax.set_yticks(yticks)
    ax.set_ylim(*ylim)
    ax.tick_params(labelsize=6, colors=LACIVERT, length=2)
    for kenar in ("top", "right", "left"):
        ax.spines[kenar].set_visible(False)
    ax.spines["bottom"].set_color(GRI)


def alan(fig):
    """Aynı üç değer, aynı daireler: üstte alan değerle, altta çap değerle orantılı."""
    ust = fig.add_axes([SOL[0], 0.618, 0.23, 0.30])
    alt = fig.add_axes([SOL[0], 0.18, 0.23, 0.30])

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


def uc_boyut(fig):
    ust = fig.add_axes([SOL[1], 0.618, 0.23, 0.30])
    alt = fig.add_axes([SOL[1], 0.18, 0.23, 0.30])

    for ax, egik in ((ust, False), (alt, True)):
        renkler = ([YANILTICI, "#F06A5A", "#F5A79C", "#FBD5CF"] if egik
                   else [MAVI, "#4A90D9", "#8FB8E8", "#C9DDF2"])
        ax.pie([25, 25, 25, 25], colors=renkler,
               startangle=90, counterclock=False, radius=0.92,
               wedgeprops=dict(linewidth=0.5, edgecolor="white"))
        ax.set_frame_on(False)
        ax.set_xticks([])
        ax.set_yticks([])
        if egik:
            ax.set_aspect(0.42)
            ax.set_ylim(-1.9, 1.9)
        else:
            ax.set_aspect("equal")
            ax.set_ylim(-1, 1)

    return ust, alt


def cift_eksen(fig):
    ust = fig.add_axes([SOL[2], 0.618, 0.23, 0.30])
    alt = fig.add_axes([SOL[2], 0.18, 0.23, 0.30])

    a = [10, 12, 14, 16, 18]
    b = [100, 150, 140, 215, 250]
    x = range(5)

    ust.plot(x, a, color=MAVI, lw=1.4, marker="o", ms=1.8)
    ust.plot(x, b, color=YESIL, lw=1.4, marker="s", ms=1.6)
    susle(ust, [0, 250], (0, 260))

    alt.plot(x, b, color=YESIL, lw=1.4, marker="s", ms=1.6)
    alt.set_ylim(0, 260)
    alt.set_xticks([])
    alt.set_yticks([0, 250])
    alt.tick_params(labelsize=6, colors=LACIVERT, length=2)
    for kenar in ("top", "right", "left"):
        alt.spines[kenar].set_visible(False)
    alt.spines["bottom"].set_color(GRI)
    ikiz = alt.twinx()
    ikiz.plot(x, a, color=YANILTICI, lw=1.4, marker="o", ms=1.8)
    ikiz.set_ylim(8, 20)
    ikiz.set_yticks([10, 18])
    ikiz.tick_params(labelsize=6, colors=YANILTICI, length=2)
    for kenar in ("top", "left", "bottom"):
        ikiz.spines[kenar].set_visible(False)
    ikiz.spines["right"].set_color(YANILTICI)

    return ust, alt


def ciz(hedef):
    fig = plt.figure(figsize=(GENISLIK_CM * CM, YUKSEKLIK_CM * CM), dpi=300)
    ciftler = [alan(fig), uc_boyut(fig), cift_eksen(fig)]

    for (ust, alt), ipucu in zip(ciftler, IPUCLARI):
        ust.text(0.0, 1.04, "doğru", transform=ust.transAxes, fontsize=6.2, color=MAVI)
        alt.text(0.0, 1.04, "yanıltıcı", transform=alt.transAxes, fontsize=6.2,
                 color=YANILTICI)
        alt.text(0.02, -0.17, ipucu, transform=alt.transAxes, fontsize=5.4,
                 color=YANILTICI, style="italic", va="top")

    fig.add_artist(plt.Line2D([0.035, 0.965], [0.549, 0.549], transform=fig.transFigure,
                              color="black", linewidth=1.0))
    fig.savefig(hedef, facecolor="white")
    print(f"yazıldı: {hedef}")


if __name__ == "__main__":
    KOK = Path(__file__).resolve().parent.parent
    ciz(KOK / "hafta-08-hesap-tablosu" / "gorseller" / "diagram-yaniltma-olcek.png")
