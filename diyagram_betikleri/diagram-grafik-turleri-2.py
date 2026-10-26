# 8. hafta: yaygın grafik türleri (2/2) — histogram, kutu grafiği ve saçılım.
# Üç kart: türün adı, ne işe yaradığı ve küçük bir örnek grafik.
#
# Kullanım:
#   python3 diyagram_betikleri/diagram-grafik-turleri-2.py            # PNG üretir
#   python3 diyagram_betikleri/diagram-grafik-turleri-2.py --kontrol  # yazı taşması denetimi
#
# Çıktı: hafta-08-hesap-tablosu/gorseller/diagram-grafik-turleri-2.png

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-08-hesap-tablosu" / "gorseller"

NAVY = "#1F3864"
BLUE = "#2E74B5"
SCATTER = "#6297C7"
LIGHT = "#EDF2F9"
GREY = "#595959"
RULE = "#C9D6E8"

plt.rcParams["font.family"] = "DejaVu Sans"

# Kart yerleşimi: üç eşit sütun (merkezler ve genişlik figür oranı olarak).
MERKEZLER = (0.165, 0.50, 0.835)
GENISLIK = 0.25
ALT, UST = 0.13, 0.63

TURLER = [
    ("Histogram", "Dağılımı görme"),
    ("Kutu grafiği", "Yayılım ve uç değerler"),
    ("Saçılım grafiği", "İki değişkenin ilişkisi"),
]


def eksen_ayari(ax):
    """Grafik alanını sadeleştir: üst/sağ çerçeve yok, sol/alt ince çizgi."""
    for kenar in ("top", "right"):
        ax.spines[kenar].set_visible(False)
    for kenar in ("left", "bottom"):
        ax.spines[kenar].set_color(RULE)
    ax.tick_params(colors=GREY, labelsize=7, length=0)
    ax.set_facecolor("white")


def kartlar(fig):
    """Her kart için grafik eksenini ve başlık metinlerini yerleştir."""
    eksenler = []
    basliklar = []
    for i, (tur, aciklama) in enumerate(TURLER):
        cx = MERKEZLER[i]
        ax = fig.add_axes([cx - GENISLIK / 2, ALT, GENISLIK, UST - ALT])
        eksenler.append(ax)
        b1 = fig.text(cx, 0.99, tur, ha="center", va="top",
                      fontsize=10.5, fontweight="bold", color=NAVY)
        b2 = fig.text(cx, 0.86, aciklama, ha="center", va="top",
                      fontsize=8, color=BLUE)
        basliklar += [b1, b2]
    return eksenler, basliklar


def ciz_histogram(ax):
    # 30–70 arasında çan eğrisine yakın bir dağılım; yalnızca sınıf sınırları yazılır.
    merkezler = [22, 27, 32, 37, 42, 47, 52, 57, 62, 67, 72]
    yukseklikler = [2, 4, 7, 10, 13, 14, 12, 9, 6, 3, 1]
    ax.bar(merkezler, yukseklikler, width=4.4, color=BLUE, linewidth=0)
    ax.set_xlim(18, 76)
    ax.set_ylim(0, 16)
    ax.set_yticks([])
    ax.set_xticks([30, 50, 70])
    eksen_ayari(ax)


def ciz_kutu(ax):
    birinci = [52, 60, 66, 70, 72, 74, 78, 80, 88]
    ikinci = [58, 64, 70, 75, 78, 82, 85, 90, 96]
    kutu = ax.boxplot(
        [birinci, ikinci],
        widths=0.42,
        patch_artist=True,
        medianprops={"color": NAVY, "linewidth": 1.6},
        boxprops={"facecolor": LIGHT, "edgecolor": BLUE, "linewidth": 1.3},
        whiskerprops={"color": BLUE, "linewidth": 1.2},
        capprops={"color": BLUE, "linewidth": 1.2},
        flierprops={"marker": "o", "markersize": 3,
                    "markerfacecolor": BLUE, "markeredgecolor": BLUE},
    )
    for parca in kutu["boxes"]:
        parca.set_zorder(2)
    ax.set_ylim(45, 105)
    ax.set_yticks([])
    ax.set_xticks([1, 2])
    ax.set_xticklabels(["1. sınav", "2. sınav"])
    eksen_ayari(ax)


def ciz_sacilim(ax):
    x = [1.0, 1.6, 2.1, 2.7, 3.2, 3.8, 4.3, 4.9, 5.4, 6.0, 6.6, 7.1]
    y = [2.1, 3.0, 2.7, 4.0, 4.6, 4.9, 5.7, 5.3, 6.5, 6.9, 7.2, 7.9]
    ax.scatter(x, y, s=18, color=SCATTER, edgecolors="none", alpha=0.95)
    ax.set_xlim(0.6, 7.5)
    ax.set_ylim(1.5, 8.5)
    ax.set_xticks([])
    ax.set_yticks([])
    eksen_ayari(ax)


def olustur():
    fig = plt.figure(figsize=(1181 / 200, 354 / 200), dpi=200)
    fig.patch.set_facecolor("white")
    eksenler, basliklar = kartlar(fig)
    ciz_histogram(eksenler[0])
    ciz_kutu(eksenler[1])
    ciz_sacilim(eksenler[2])
    return fig, eksenler, basliklar


def kontrol():
    """PNG üretmeden yazıların figür ve grafik alanlarıyla çakışmadığını denetle."""
    fig, eksenler, basliklar = olustur()
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    fig_bb = fig.bbox
    sorun = 0

    for t in basliklar:
        bb = t.get_window_extent(renderer)
        if bb.x0 < fig_bb.x0 - 1 or bb.x1 > fig_bb.x1 + 1:
            print(f"TAŞMA (yatay): '{t.get_text()}'")
            sorun += 1
        if bb.y0 < fig_bb.y0 - 1 or bb.y1 > fig_bb.y1 + 1:
            print(f"TAŞMA (dikey): '{t.get_text()}'")
            sorun += 1

    for i, ax in enumerate(eksenler):
        abb = ax.get_window_extent(renderer)
        for t in basliklar[2 * i:2 * i + 2]:
            bb = t.get_window_extent(renderer)
            kesisim = (bb.x0 < abb.x1 and bb.x1 > abb.x0 and
                       bb.y0 < abb.y1 and bb.y1 > abb.y0)
            if kesisim:
                print(f"ÇAKIŞMA: '{t.get_text()}' grafik alanıyla üst üste")
                sorun += 1

    plt.close(fig)
    if sorun:
        print(f"{sorun} sorun bulundu")
        return 1
    print("Yazı taşması yok.")
    return 0


def main(argv):
    if "--kontrol" in argv:
        return kontrol()
    fig, _, _ = olustur()
    cikti = HEDEF / "diagram-grafik-turleri-2.png"
    fig.savefig(cikti, dpi=200, facecolor="white")
    plt.close(fig)
    print(f"{cikti.relative_to(KOK)} üretildi")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
