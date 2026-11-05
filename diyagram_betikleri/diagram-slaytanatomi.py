#!/usr/bin/env python3
"""Slayt metninde yanlış ve doğru örnekleri karşılaştıran şema.

Çıktı: hafta-09-sunum-uygulamalari/gorseller/diagram-slaytanatomi.png

Şemaya başlık gömülmez; başlık ders notunda şekil altyazısı, sunumda slayt
başlığıdır.

Kullanım:
    python3 diyagram_betikleri/diagram-slaytanatomi.py
    python3 diyagram_betikleri/diagram-slaytanatomi.py --kontrol
"""

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / "hafta-09-sunum-uygulamalari" / "gorseller" / "diagram-slaytanatomi.png"

LACIVERT = "#1F3864"
KIRMIZI = "#A91818"
GRI = "#595959"


def panel(ax, x, baslik, satirlar, renk):
    y, genislik, yukseklik = 0.5, 8.1, 6.2
    kutu = FancyBboxPatch(
        (x, y),
        genislik,
        yukseklik,
        boxstyle="round,pad=0.02,rounding_size=0.25",
        linewidth=2,
        edgecolor=renk,
        facecolor="white",
    )
    ax.add_patch(kutu)
    ax.add_patch(
        FancyBboxPatch(
            (x, y + yukseklik - 1.05),
            genislik,
            1.05,
            boxstyle="round,pad=0.02,rounding_size=0.25",
            linewidth=0,
            facecolor=renk,
        )
    )
    metinler = [
        (
            f"{baslik}-başlık",
            ax.text(
                x + genislik / 2,
                y + yukseklik - 0.53,
                baslik,
                ha="center",
                va="center",
                fontsize=24,
                fontweight="bold",
                color="white",
            ),
        )
    ]
    for i, satir in enumerate(satirlar):
        metinler.append(
            (
                f"{baslik}-{i + 1}",
                ax.text(
                    x + 0.45,
                    y + 4.35 - i * 0.88,
                    satir,
                    ha="left",
                    va="center",
                    fontsize=17,
                    color=GRI,
                ),
            )
        )
    return kutu, metinler


def ciz():
    fig = plt.figure(figsize=(18 / 2.54, 7.2 / 2.54), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 7.2)
    ax.axis("off")

    gruplar = []
    gruplar.append(
        panel(
            ax,
            0.4,
            "YANLIŞ",
            [
                "Uzun cümleler",
                "Paragraf metni",
                "Küçük punto",
                "Çok renk ve süsleme",
                "Slayt okunuyor",
            ],
            KIRMIZI,
        )
    )
    gruplar.append(
        panel(
            ax,
            9.5,
            "DOĞRU",
            [
                "Anahtar kelimeler",
                "Madde madde",
                "Büyük punto",
                "Sade tasarım",
                "Konuşmacı anlatır",
            ],
            LACIVERT,
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
