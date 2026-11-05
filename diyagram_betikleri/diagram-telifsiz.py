#!/usr/bin/env python3
"""Görsel kaynaklarına göre kullanım iznini gösteren akış şeması.

Çıktı: hafta-09-sunum-uygulamalari/gorseller/diagram-telifsiz.png

Şemaya başlık ve kapanış cümlesi gömülmez; bunlar ders notunda şekil altyazısı
ve metin içinde verilir.

Kullanım:
    python3 diyagram_betikleri/diagram-telifsiz.py
    python3 diyagram_betikleri/diagram-telifsiz.py --kontrol
"""

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / "hafta-09-sunum-uygulamalari" / "gorseller" / "diagram-telifsiz.png"

LACIVERT = "#1F3864"
MAVI = "#2E74B5"
ACIK = "#EDF2F9"
GRI = "#595959"
KIRMIZI = "#A91818"


def satir(ax, y, kaynak, aciklama, telifli=False):
    renk = KIRMIZI if telifli else LACIVERT
    zemin = "#F6E8E7" if telifli else ACIK
    kaynak_kutu = FancyBboxPatch(
        (0.4, y),
        6.0,
        1.45,
        boxstyle="round,pad=0.02,rounding_size=0.2",
        linewidth=2,
        edgecolor=renk,
        facecolor=zemin,
    )
    ax.add_patch(kaynak_kutu)
    ax.add_patch(
        FancyArrowPatch(
            (6.55, y + 0.72),
            (7.35, y + 0.72),
            arrowstyle="-|>",
            mutation_scale=22,
            linewidth=2,
            color=MAVI,
        )
    )
    aciklama_kutu = FancyBboxPatch(
        (7.5, y),
        10.1,
        1.45,
        boxstyle="round,pad=0.02,rounding_size=0.2",
        linewidth=1.5,
        edgecolor=MAVI,
        facecolor="white",
    )
    ax.add_patch(aciklama_kutu)
    k = ax.text(
        3.4,
        y + 0.72,
        kaynak,
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color=renk,
        linespacing=1.15,
    )
    a = ax.text(
        7.9,
        y + 0.72,
        aciklama,
        ha="left",
        va="center",
        fontsize=17,
        color=GRI,
        linespacing=1.15,
    )
    return [(kaynak_kutu, k), (aciklama_kutu, a)]


def ciz():
    fig = plt.figure(figsize=(18 / 2.54, 9.5 / 2.54), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 9.5)
    ax.axis("off")

    gruplar = []
    gruplar += satir(ax, 7.55, "KAMU MALI / CC0", "Serbest; atıf gerekmez")
    gruplar += satir(
        ax,
        5.55,
        "ÜCRETSİZ STOK\n(Pexels, Unsplash)",
        "Site lisansına uy;\nkamu malı değildir",
    )
    gruplar += satir(
        ax,
        3.55,
        "CREATIVE\nCOMMONS",
        "Lisansına uy;\ngenellikle atıf gerekir",
    )
    gruplar += satir(ax, 1.55, "TELİFLİ", "İzin gerekir; kullanma", telifli=True)
    return fig, gruplar


def kontrol(fig, gruplar):
    fig.canvas.draw()
    cizici = fig.canvas.get_renderer()
    sorun = False
    for kutu, metin in gruplar:
        kb = kutu.get_window_extent(cizici)
        mb = metin.get_window_extent(cizici)
        if mb.x0 < kb.x0 or mb.y0 < kb.y0 or mb.x1 > kb.x1 or mb.y1 > kb.y1:
            print(f"TAŞMA: {metin.get_text()!r} kutusuna sığmıyor")
            sorun = True
        else:
            print(f"tamam: {metin.get_text()!r}")
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
