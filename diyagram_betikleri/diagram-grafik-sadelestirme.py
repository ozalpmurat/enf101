#!/usr/bin/env python3
"""Karmaşık ve sadeleştirilmiş grafiği karşılaştıran şema.

Çıktı: hafta-09-sunum-uygulamalari/gorseller/diagram-grafik-sadelestirme.png

Şemaya başlık gömülmez. İki panel: solda yoğun (KARMAŞIK), sağda tek mesaja
indirgenmiş (SADE) grafik.

Kullanım:
    python3 diyagram_betikleri/diagram-grafik-sadelestirme.py
    python3 diyagram_betikleri/diagram-grafik-sadelestirme.py --kontrol
"""

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / "hafta-09-sunum-uygulamalari" / "gorseller" / "diagram-grafik-sadelestirme.png"

LACIVERT = "#1F3864"
MAVI = "#2E74B5"
KIRMIZI = "#A91818"
YESIL = "#1E7B45"
TURUNCU = "#C77A00"
GRI = "#595959"
IZGARA = "#D6DCE5"
SOLUK = "#C9D6E6"

TABAN = 1.0
OLCEK = 1.5

SERI1 = [0.9, 1.4, 0.6, 1.8, 1.1, 2.4, 0.7, 1.6]
SERI2 = [1.3, 0.8, 1.7, 1.0, 2.0, 1.2, 2.2, 0.9]
SERI3 = [0.7, 1.9, 1.2, 1.5, 0.8, 1.7, 1.3, 2.1]


def panel(ax, x, w, baslik, kenar):
    y, h, bant = 0.6, 6.4, 0.85
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.2",
            linewidth=2,
            edgecolor=kenar,
            facecolor="white",
        )
    )
    ax.add_patch(
        FancyBboxPatch(
            (x, y + h - bant),
            w,
            bant,
            boxstyle="round,pad=0.02,rounding_size=0.2",
            linewidth=0,
            facecolor=kenar,
        )
    )
    ax.text(
        x + w / 2,
        y + h - bant / 2,
        baslik,
        ha="center",
        va="center",
        fontsize=22,
        fontweight="bold",
        color="white",
    )


def ciz():
    fig = plt.figure(figsize=(18 / 2.54, 7.6 / 2.54), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 7.6)
    ax.axis("off")

    # ---- KARMAŞIK ----
    panel(ax, 0.4, 8.3, "KARMAŞIK", KIRMIZI)
    tepe = TABAN + 3.9
    for i in range(5):
        y = TABAN + i * (tepe - TABAN) / 4
        ax.add_patch(Rectangle((0.95, y), 7.3, 0.03, facecolor=IZGARA))
    grup_w = 7.3 / 8
    for g in range(8):
        gx = 0.95 + g * grup_w
        for k, (seri, renk) in enumerate(
            ((SERI1, MAVI), (SERI2, YESIL), (SERI3, TURUNCU))
        ):
            bx = gx + 0.06 + k * 0.26
            ax.add_patch(
                Rectangle((bx, TABAN), 0.2, seri[g] * OLCEK, facecolor=renk, edgecolor="none")
            )
    # küçük eksen etiketleri (karmaşıklık göstergesi)
    for g in range(8):
        ax.text(0.95 + g * grup_w + grup_w / 2, TABAN - 0.22, "0", ha="center", va="top", fontsize=5, color=GRI)
    # gösterge (legend)
    ax.add_patch(Rectangle((6.4, 5.45), 1.9, 1.05, facecolor="white", edgecolor=GRI, linewidth=0.8))
    for k, renk in enumerate((MAVI, YESIL, TURUNCU)):
        ax.add_patch(Rectangle((6.55, 6.2 - k * 0.28), 0.16, 0.16, facecolor=renk))
        ax.add_patch(Rectangle((6.8, 6.24 - k * 0.28), 1.2, 0.08, facecolor=IZGARA))
    ax.add_patch(Rectangle((0.95, TABAN), 7.3, 0.04, facecolor=GRI))

    # ---- SADE ----
    panel(ax, 9.3, 8.3, "SADE", LACIVERT)
    bar_w = 1.3
    baslangic = 9.9 + (7.2 - (3 * bar_w + 2 * 0.8)) / 2
    yukseklikler = [2.5, 3.5, 2.0]
    renkler = [SOLUK, MAVI, SOLUK]
    for i in range(3):
        bx = baslangic + i * (bar_w + 0.8)
        ax.add_patch(
            Rectangle((bx, TABAN), bar_w, yukseklikler[i], facecolor=renkler[i], edgecolor="none")
        )
    ax.add_patch(Rectangle((baslangic, TABAN), 3 * bar_w + 2 * 0.8, 0.05, facecolor=GRI))
    ax.text(
        baslangic + (bar_w + 0.8) + bar_w / 2,
        TABAN + yukseklikler[1] + 0.28,
        "42%",
        ha="center",
        va="bottom",
        fontsize=24,
        fontweight="bold",
        color=MAVI,
    )
    return fig


def kontrol(fig):
    fig.canvas.draw()
    return 0


def main():
    fig = ciz()
    if "--kontrol" in sys.argv:
        kod = kontrol(fig)
        plt.close(fig)
        return kod
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(CIKTI, dpi=200, facecolor="white")
    plt.close(fig)
    print(CIKTI.relative_to(KOK))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
