#!/usr/bin/env python3
"""4:3 ve 16:9 ekran oranlarını yan yana gösteren basit şema.

Çıktı: hafta-09-sunum-uygulamalari/gorseller/diagram-ekran-oranlari.png

Şemaya başlık gömülmez; başlık ders notunda şekil altyazısı, sunumda slayt
başlığıdır.

Kullanım:
    python3 diyagram_betikleri/diagram-ekran-oranlari.py
    python3 diyagram_betikleri/diagram-ekran-oranlari.py --kontrol
"""

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / "hafta-09-sunum-uygulamalari" / "gorseller" / "diagram-ekran-oranlari.png"

LACIVERT = "#1F3864"
MAVI = "#2E74B5"
ACIK = "#EDF2F9"
GRI = "#595959"


def ekran(ax, x, genislik, etiket, notu):
    y, yukseklik = 1.15, 4.2
    kutu = FancyBboxPatch(
        (x, y),
        genislik,
        yukseklik,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        linewidth=4,
        edgecolor=LACIVERT,
        facecolor=ACIK,
    )
    ax.add_patch(kutu)
    return [
        (
            f"{etiket}-etiket",
            ax.text(
                x + genislik / 2,
                y + yukseklik + 0.55,
                etiket,
                ha="center",
                va="center",
                fontsize=24,
                fontweight="bold",
                color=LACIVERT,
            ),
        ),
        (
            f"{etiket}-not",
            ax.text(
                x + genislik / 2,
                y - 0.55,
                notu,
                ha="center",
                va="center",
                fontsize=16,
                color=GRI,
            ),
        ),
    ]


def ciz():
    fig = plt.figure(figsize=(18 / 2.54, 7.0 / 2.54), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 7.0)
    ax.axis("off")

    metinler = []
    metinler += ekran(ax, 1.5, 5.6, "4:3", "daha dar")
    metinler += ekran(ax, 9.2, 7.47, "16:9", "daha geniş")
    return fig, metinler


def kontrol(fig, metinler):
    fig.canvas.draw()
    cizici = fig.canvas.get_renderer()
    sorun = False
    for ad, metin in metinler:
        mb = metin.get_window_extent(cizici)
        if mb.x0 < 0 or mb.y0 < 0 or mb.x1 > fig.bbox.x1 or mb.y1 > fig.bbox.y1:
            print(f"TAŞMA: {ad} figür sınırını aşıyor")
            sorun = True
        else:
            print(f"tamam: {ad}")
    return 1 if sorun else 0


def main():
    fig, metinler = ciz()
    if "--kontrol" in sys.argv:
        kod = kontrol(fig, metinler)
        plt.close(fig)
        return kod
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(CIKTI, dpi=200, facecolor="white")
    plt.close(fig)
    print(CIKTI.relative_to(KOK))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
