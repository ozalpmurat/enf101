#!/usr/bin/env python3
"""LibreOffice Impress ekran görüntüsü için yer tutucu kutu üretir.

Çıktı: hafta-09-sunum-uygulamalari/gorseller/ekran-yer-tutucu-libreoffice-impress.png

Kullanım:
    python3 diyagram_betikleri/ekran-yer-tutucu-libreoffice-impress.py
    python3 diyagram_betikleri/ekran-yer-tutucu-libreoffice-impress.py --kontrol
"""

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

KOK = Path(__file__).resolve().parent.parent
CIKTI = (
    KOK
    / "hafta-09-sunum-uygulamalari"
    / "gorseller"
    / "ekran-yer-tutucu-libreoffice-impress.png"
)

LACIVERT = "#1F3864"
MAVI = "#2E74B5"
ACIK = "#EDF2F9"
GRI = "#595959"


def ciz():
    fig = plt.figure(figsize=(18 / 2.54, 10 / 2.54), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10)
    ax.axis("off")

    kutu = FancyBboxPatch(
        (0.6, 0.6),
        16.8,
        8.8,
        boxstyle="round,pad=0.02,rounding_size=0.35",
        linewidth=2.5,
        edgecolor=MAVI,
        facecolor=ACIK,
        linestyle=(0, (6, 4)),
    )
    ax.add_patch(kutu)

    # Basit ekran simgesi: yer tutucunun ekran görüntüsü olduğunu sezdirir.
    ekran = FancyBboxPatch(
        (8.2, 8.0),
        3.6,
        1.1,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=2,
        edgecolor=LACIVERT,
        facecolor="white",
    )
    ax.add_patch(ekran)
    ax.add_patch(Rectangle((9.65, 7.72), 0.7, 0.28, facecolor=LACIVERT, edgecolor="none"))
    ax.add_patch(Rectangle((9.2, 7.58), 1.6, 0.14, facecolor=LACIVERT, edgecolor="none"))

    baslik = ax.text(
        9,
        6.85,
        "EKRAN GÖRÜNTÜSÜ YERİ",
        ha="center",
        va="center",
        fontsize=30,
        fontweight="bold",
        color=LACIVERT,
    )
    uygulama = ax.text(
        9,
        5.35,
        "LibreOffice Impress",
        ha="center",
        va="center",
        fontsize=28,
        color=MAVI,
    )
    aciklama = ax.text(
        9,
        3.45,
        "Slayt paneli, çalışma alanı\nve konuşmacı notları.",
        ha="center",
        va="center",
        fontsize=26,
        color=GRI,
        linespacing=1.25,
    )

    return fig, kutu, [("başlık", baslik), ("uygulama", uygulama), ("açıklama", aciklama)]


def kontrol(fig, kutu, metinler):
    fig.canvas.draw()
    cizici = fig.canvas.get_renderer()
    kb = kutu.get_window_extent(cizici)
    sorun = False
    for ad, metin in metinler:
        mb = metin.get_window_extent(cizici)
        if mb.x0 < kb.x0 or mb.y0 < kb.y0 or mb.x1 > kb.x1 or mb.y1 > kb.y1:
            print(f"TAŞMA: {ad} kutusuna sığmıyor")
            sorun = True
        else:
            print(f"tamam: {ad}")
    return 1 if sorun else 0


def main():
    fig, kutu, metinler = ciz()
    if "--kontrol" in sys.argv:
        kod = kontrol(fig, kutu, metinler)
        plt.close(fig)
        return kod
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(CIKTI, dpi=200, facecolor="white")
    plt.close(fig)
    print(CIKTI.relative_to(KOK))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
