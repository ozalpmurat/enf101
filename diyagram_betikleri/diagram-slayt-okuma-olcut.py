#!/usr/bin/env python3
"""Slaytı okumayı önleyen pratik ölçüyü (karar) gösteren şema.

Çıktı: hafta-09-sunum-uygulamalari/gorseller/diagram-slayt-okuma-olcut.png

Şemaya başlık gömülmez.

Kullanım:
    python3 diyagram_betikleri/diagram-slayt-okuma-olcut.py
    python3 diyagram_betikleri/diagram-slayt-okuma-olcut.py --kontrol
"""

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / "hafta-09-sunum-uygulamalari" / "gorseller" / "diagram-slayt-okuma-olcut.png"

LACIVERT = "#1F3864"
MAVI = "#2E74B5"
KIRMIZI = "#A91818"
ACIK = "#EDF2F9"
GRI = "#595959"


def kutu(ax, x, y, w, h, kenar, metin, fontsize, yuz="white", renk=GRI):
    kutu = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.22",
        linewidth=2,
        edgecolor=kenar,
        facecolor=yuz,
    )
    ax.add_patch(kutu)
    metinler = [
        (
            metin[:18],
            ax.text(
                x + w / 2,
                y + h / 2,
                metin,
                ha="center",
                va="center",
                fontsize=fontsize,
                color=renk,
                fontweight="bold",
            ),
        )
    ]
    return kutu, metinler


def ciz():
    fig = plt.figure(figsize=(18 / 2.54, 5.6 / 2.54), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 5.6)
    ax.axis("off")

    gruplar = []
    gruplar.append(
        kutu(ax, 0.4, 1.7, 7.6, 2.2, LACIVERT, "Slayta bakmadan\nanlatabiliyor musun?", 16, ACIK, LACIVERT)
    )
    gruplar.append(
        kutu(ax, 10.6, 3.15, 7.0, 1.9, MAVI, "Evet  →  Slayt yeterli", 15, "white", MAVI)
    )
    gruplar.append(
        kutu(
            ax,
            10.6,
            0.55,
            7.0,
            1.9,
            KIRMIZI,
            "Hayır  →\nSlaytta fazla yazı var,\nsadeleştir",
            15,
            "white",
            KIRMIZI,
        )
    )

    ax.add_patch(
        FancyArrowPatch(
            (7.85, 2.8), (10.5, 4.1), arrowstyle="-|>", mutation_scale=18, linewidth=2.2, color=MAVI
        )
    )
    ax.add_patch(
        FancyArrowPatch(
            (7.85, 2.8), (10.5, 1.5), arrowstyle="-|>", mutation_scale=18, linewidth=2.2, color=KIRMIZI
        )
    )
    return fig, gruplar


def kontrol(fig, gruplar):
    fig.canvas.draw()
    cizici = fig.canvas.get_renderer()
    sorun = False
    for kutu_, metinler in gruplar:
        kb = kutu_.get_window_extent(cizici)
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
