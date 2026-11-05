#!/usr/bin/env python3
"""Bir sununun üç bölümünü gösteren akış şeması.

Çıktı: hafta-09-sunum-uygulamalari/gorseller/diagram-sunumyapi.png

Şemaya başlık gömülmez; başlık ders notunda şekil altyazısı, sunumda slayt
başlığıdır. Ayrıntılı açıklama ve süre payları tabloda verilir; şema yalnızca
sırayı gösterir.

Kullanım:
    python3 diyagram_betikleri/diagram-sunumyapi.py
    python3 diyagram_betikleri/diagram-sunumyapi.py --kontrol
"""

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / "hafta-09-sunum-uygulamalari" / "gorseller" / "diagram-sunumyapi.png"

LACIVERT = "#1F3864"
MAVI = "#2E74B5"
ACIK = "#EDF2F9"
GRI = "#595959"


def kutu(ax, x, baslik, sayi):
    y, genislik, yukseklik = 0.7, 4.9, 3.2
    kutu = FancyBboxPatch(
        (x, y),
        genislik,
        yukseklik,
        boxstyle="round,pad=0.02,rounding_size=0.25",
        linewidth=2,
        edgecolor=LACIVERT,
        facecolor=ACIK,
    )
    ax.add_patch(kutu)
    ax.add_patch(
        FancyBboxPatch(
            (x, y + yukseklik - 1.0),
            genislik,
            1.0,
            boxstyle="round,pad=0.02,rounding_size=0.25",
            linewidth=0,
            facecolor=LACIVERT,
        )
    )
    metinler = [
        (
            f"{baslik}-başlık",
            ax.text(
                x + genislik / 2,
                y + yukseklik - 0.5,
                baslik,
                ha="center",
                va="center",
                fontsize=24,
                fontweight="bold",
                color="white",
            ),
        ),
        (
            f"{baslik}-sayı",
            ax.text(
                x + genislik / 2,
                y + 0.95,
                sayi,
                ha="center",
                va="center",
                fontsize=34,
                fontweight="bold",
                color=GRI,
            ),
        ),
    ]
    return kutu, metinler


def ciz():
    fig = plt.figure(figsize=(18 / 2.54, 4.6 / 2.54), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 4.6)
    ax.axis("off")

    gruplar = []
    for x, baslik, sayi in (
        (0.4, "AÇILIŞ", "1"),
        (6.55, "GÖVDE", "2"),
        (12.7, "KAPANIŞ", "3"),
    ):
        gruplar.append(kutu(ax, x, baslik, sayi))

    for x0, x1 in ((5.4, 6.45), (11.55, 12.6)):
        ax.add_patch(
            FancyArrowPatch(
                (x0, 2.35),
                (x1, 2.35),
                arrowstyle="-|>",
                mutation_scale=24,
                linewidth=2.5,
                color=MAVI,
            )
        )

    return fig, gruplar


def kontrol(fig, gruplar):
    fig.canvas.draw()
    cizici = fig.canvas.get_renderer()
    sorun = False
    for kutu, metinler in gruplar:
        kb = kutu.get_window_extent(cizici)
        for ad, metin in metinler:
            mb = metin.get_window_extent(cizici)
            if mb.x0 < kb.x0 or mb.y0 < kb.y0 or mb.x1 > kb.x1 or mb.y1 > kb.y1:
                print(f"TAŞMA: {ad} kutusuna sığmıyor")
                sorun = True
            else:
                print(f"tamam: {ad}")
    return 1 if sorun else 0


def main():
    fig, gruplar = ciz()
    if "--kontrol" in sys.argv:
        kod = kontrol(fig, gruplar)
        plt.close(fig)
        return kod
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(CIKTI, dpi=200, facecolor="white")
    plt.close(fig)
    print(CIKTI.relative_to(KOK))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
