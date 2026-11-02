#!/usr/bin/env python3
"""Seçme ve gizleme: seçilmiş karşılaştırma grubu vurgulu sürüm (8. hafta).

Üç sütun, her sütunda doğru (üst) ve yanıltıcı (alt) grafik:
seçilmiş zaman aralığı, "diğer" kovası, seçilmiş karşılaştırma grubu.

Çıktı: hafta-08-hesap-tablosu/gorseller/diagram-yaniltma-secme.png
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
from matplotlib.transforms import blended_transform_factory

CM = 1 / 2.54
GENISLIK_CM, YUKSEKLIK_CM = 13.4, 6.2

LACIVERT = "#1F3864"
MAVI = "#2E74B5"
GRI = "#8C8C8C"
YANILTICI = "#EB4034"
YESIL = "#2E7D32"

IPUCLARI = ["eğilim tersine çevrildi", "80 tane Evet/Hayır oyu\nüzerinden hesaplandı", "grup seçilerek fark büyütüldü"]
SOL = [1 / 6 - 0.115, 0.5 - 0.115, 5 / 6 - 0.115]

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


def pasta_etiketleri(ax, degerler, renkler, adlar):
    import math as _m
    dilimler, _ = ax.pie(degerler, colors=renkler, startangle=90, counterclock=False,
                         radius=0.95, wedgeprops=dict(linewidth=0.5, edgecolor="white"))
    ax.set_aspect("equal")
    ax.set_xlim(-1.34, 1.34)
    ax.set_ylim(-1.34, 1.34)
    ax.set_frame_on(False)
    ax.set_xticks([])
    ax.set_yticks([])
    for dilim, d, ad in zip(dilimler, degerler, adlar):
        aci = _m.radians((dilim.theta1 + dilim.theta2) / 2)
        r, g, b = (int(renkler[degerler.index(d)][i:i+2], 16) for i in (1, 3, 5))
        koyu = 0.299 * r + 0.587 * g + 0.114 * b > 170
        ax.text(0.44 * _m.cos(aci), 0.44 * _m.sin(aci), ad, ha="center", va="center",
                fontsize=4.6, color=LACIVERT if koyu else "white", fontweight="bold")
        ax.text(1.17 * _m.cos(aci), 1.17 * _m.sin(aci), str(d), ha="center", va="center",
                fontsize=5.0, color=LACIVERT, fontweight="bold")


def ciz(hedef):
    fig = plt.figure(figsize=(GENISLIK_CM * CM, YUKSEKLIK_CM * CM), dpi=300)
    ust = [fig.add_axes([s, 0.618, 0.23, 0.30]) for s in SOL]
    alt = [fig.add_axes([s, 0.18, 0.23, 0.30]) for s in SOL]

    # 1) seçilmiş zaman aralığı
    kesisme = blended_transform_factory(ust[0].transData, ust[0].transAxes)
    ust[0].add_patch(Rectangle((3.55, -0.17), 3.9, 0.92, transform=kesisme,
                               facecolor=YANILTICI, alpha=0.10, edgecolor="none",
                               clip_on=False, zorder=0.5))
    for kenar in (3.55, 7.45):
        ust[0].plot([kenar, kenar], [-0.17, 0.75], transform=kesisme,
                    color=YANILTICI, lw=0.9, clip_on=False, zorder=0.6)
    ust[0].plot(range(len(SERI)), SERI, color=MAVI, lw=1.3, marker="o", ms=1.6)
    susle(ust[0], [50, 55, 60, 65], (50, 65), xticks=range(len(SERI)), xsize=4.2)
    alt[0].plot(range(4, 8), SERI[4:8], color=YANILTICI, lw=1.3, marker="o", ms=1.6)
    susle(alt[0], [50, 55, 60, 65], (50, 65), xticks=range(4, 8), xsize=5)

    # 2) eksik cevaplar: sütun grafiği
    ust[1].bar(range(4), [55, 25, 10, 10], color=MAVI, width=0.62)
    for i, d in enumerate([55, 25, 10, 10]):
        ust[1].text(i, d + 1.5, str(d), ha="center", fontsize=5.0, color=LACIVERT)
    susle(ust[1], [0, 50], (0, 68), xticks=range(4), xsize=3.8)
    ust[1].set_xticklabels(["Evet", "Hayır", "Kararsız", "Cevap\nyok"], fontsize=3.8)

    alt[1].bar(range(2), [69, 31], color=YANILTICI, width=0.5)
    for i, d in enumerate([69, 31]):
        alt[1].text(i, d + 1.5, f"%{d}", ha="center", fontsize=5.0, color=YANILTICI)
    susle(alt[1], [0, 50], (0, 80), xticks=range(2), xsize=4.4)
    alt[1].set_xticklabels(["Evet", "Hayır"], fontsize=4.4)

    # 3) seçilmiş karşılaştırma grubu: seçilen iki çubuk işaretleniyor
    ust[2].bar(range(4), [70, 72, 75, 74], color=MAVI, width=0.62)
    for i, d in enumerate([70, 72, 75, 74]):
        ust[2].text(i, d + 3, str(d), ha="center", fontsize=5.2, color=LACIVERT)
    susle(ust[2], [0, 80], (0, 100), xticks=[])
    for i, d in ((0, 70), (2, 75)):
        ust[2].add_patch(Ellipse((i, d + 4.6), width=0.85, height=16,
                                 facecolor="none", edgecolor=YANILTICI, linewidth=1.1))

    alt[2].bar(range(2), [70, 75], color=YANILTICI, width=0.5)
    for i, d in enumerate([70, 75]):
        alt[2].text(i, d + 1.5, str(d), ha="center", fontsize=5.2, color=YANILTICI)
    susle(alt[2], [60, 70, 80], (60, 84), xticks=[])

    for i, (u, a, ipucu) in enumerate(zip(ust, alt, IPUCLARI)):
        u.text(0.0, 1.04, "doğru", transform=u.transAxes, fontsize=6.2, color=MAVI)
        a.text(0.0, 1.04, "yanıltıcı", transform=a.transAxes, fontsize=6.2, color=YANILTICI)
        dy = -0.20 if i == 1 else -0.17
        a.text(0.02, dy, ipucu, transform=a.transAxes, fontsize=5.4,
               color=YANILTICI, style="italic", va="top")

    fig.add_artist(plt.Line2D([0.035, 0.965], [0.549, 0.549], transform=fig.transFigure,
                              color="black", linewidth=1.0))
    fig.savefig(hedef, facecolor="white")
    print(f"yazıldı: {hedef}")


if __name__ == "__main__":
    KOK = Path(__file__).resolve().parent.parent
    ciz(KOK / "hafta-08-hesap-tablosu" / "gorseller" / "diagram-yaniltma-karsilastirma.png")
