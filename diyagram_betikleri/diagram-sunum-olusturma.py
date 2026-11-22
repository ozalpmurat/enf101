#!/usr/bin/env python3
"""Bir sunuyu baştan sona oluşturmanın altı adımını gösteren akış şeması.

Çıktı: hafta-09-sunum-uygulamalari/gorseller/diagram-sunum-olusturma.png

Şemaya başlık gömülmez; başlık ders notunda şekil altyazısı, sunumda slayt
başlığıdır. Adımlar ders notundaki "Bir sunuyu baştan sona oluşturma" listesiyle
birebir aynıdır; akış iki satırda yılan biçiminde ilerler (1-2-3, sonra 4-5-6
sağdan sola).

Kullanım:
    python3 diyagram_betikleri/diagram-sunum-olusturma.py
    python3 diyagram_betikleri/diagram-sunum-olusturma.py --kontrol
"""

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / "hafta-09-sunum-uygulamalari" / "gorseller" / "diagram-sunum-olusturma.png"

LACIVERT = "#1F3864"
MAVI = "#2E74B5"
ACIK = "#EDF2F9"
GRI = "#595959"

ADIMLAR = [
    "Uygulamayı aç,\nboş sunu",
    "Ekran oranını\nseç (16:9)",
    "Tema, ana slayt,\ndüzen seç",
    "Slayt ekle,\ndoldur",
    "Notları yaz,\nprova yap",
    "Göster, PDF\nolarak ver",
]

# Kart konumları: ilk satır soldan sağa, ikinci satır sağdan sola (yılan).
X = [0.7, 6.5, 12.3]
Y1, Y2 = 4.5, 0.8
W, H, BANT = 5.0, 3.0, 0.9

YER = {
    1: (X[0], Y1),
    2: (X[1], Y1),
    3: (X[2], Y1),
    4: (X[2], Y2),
    5: (X[1], Y2),
    6: (X[0], Y2),
}


def kart(ax, x, y, numara, etiket):
    kutu = FancyBboxPatch(
        (x, y),
        W,
        H,
        boxstyle="round,pad=0.02,rounding_size=0.2",
        linewidth=2,
        edgecolor=LACIVERT,
        facecolor=ACIK,
    )
    ax.add_patch(kutu)
    ax.add_patch(
        FancyBboxPatch(
            (x, y + H - BANT),
            W,
            BANT,
            boxstyle="round,pad=0.02,rounding_size=0.2",
            linewidth=0,
            facecolor=LACIVERT,
        )
    )
    metinler = [
        (
            f"{numara}-sayı",
            ax.text(
                x + W / 2,
                y + H - BANT / 2,
                str(numara),
                ha="center",
                va="center",
                fontsize=22,
                fontweight="bold",
                color="white",
            ),
        ),
        (
            f"{numara}-etiket",
            ax.text(
                x + W / 2,
                y + (H - BANT) / 2,
                etiket,
                ha="center",
                va="center",
                fontsize=16,
                color=GRI,
            ),
        ),
    ]
    return kutu, metinler


def ok(ax, p0, p1):
    ax.add_patch(
        FancyArrowPatch(
            p0, p1, arrowstyle="-|>", mutation_scale=18, linewidth=2.2, color=MAVI
        )
    )


def ciz():
    fig = plt.figure(figsize=(18 / 2.54, 8.1 / 2.54), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 8.1)
    ax.axis("off")

    gruplar = []
    for i, etiket in enumerate(ADIMLAR, start=1):
        x, y = YER[i]
        gruplar.append(kart(ax, x, y, i, etiket))

    orta1 = Y1 + H / 2
    orta2 = Y2 + H / 2
    ok(ax, (X[0] + W + 0.05, orta1), (X[1] - 0.05, orta1))
    ok(ax, (X[1] + W + 0.05, orta1), (X[2] - 0.05, orta1))
    ok(ax, (X[2] + W / 2, Y1 - 0.05), (X[2] + W / 2, Y2 + H + 0.05))
    ok(ax, (X[2] - 0.05, orta2), (X[1] + W + 0.05, orta2))
    ok(ax, (X[1] - 0.05, orta2), (X[0] + W + 0.05, orta2))

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
