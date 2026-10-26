# 8. hafta: yaygın grafik türleri (1/2) — sütun, çizgi ve pasta grafiği.
# Üç kart: türün adı, ne işe yaradığı ve küçük bir örnek grafik.
#
# Kullanım:
#   python3 diyagram_betikleri/diagram-grafik-turleri-1.py            # PNG üretir
#   python3 diyagram_betikleri/diagram-grafik-turleri-1.py --kontrol  # yazı taşması denetimi
#
# Çıktı: hafta-08-hesap-tablosu/gorseller/diagram-grafik-turleri-1.png

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
MID = "#7FA6CC"
PALE = "#C9D6E8"
GREY = "#595959"
RULE = "#C9D6E8"

plt.rcParams["font.family"] = "DejaVu Sans"

# Kart yerleşimi: üç eşit sütun (merkezler ve genişlik figür oranı olarak).
MERKEZLER = (0.165, 0.50, 0.835)
GENISLIK = 0.25
ALT, UST = 0.13, 0.63

TURLER = [
    ("Sütun grafiği", "Kategorileri karşılaştırma"),
    ("Çizgi grafiği", "Zaman içindeki değişim"),
    ("Pasta grafiği", "Bütün içindeki pay"),
]


def eksen_ayari(ax):
    """Grafik alanını sadeleştir: üst/sağ çerçeve yok, sol/alt ince çizgi."""
    for kenar in ("top", "right"):
        ax.spines[kenar].set_visible(False)
    for kenar in ("left", "bottom"):
        ax.spines[kenar].set_color(RULE)
    ax.tick_params(colors=GREY, labelsize=7.5, length=0)
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


def ciz_sutun(ax):
    kategoriler = ["Müh.", "İkt.", "Eğt.", "Sağ."]
    degerler = [28, 39, 47, 56]
    ax.bar(kategoriler, degerler, color=BLUE, width=0.62)
    ax.set_ylim(0, 70)
    ax.set_yticks([])
    eksen_ayari(ax)


def ciz_cizgi(ax):
    aylar = ["Oca", "Şub", "Mar", "Nis", "May", "Haz"]
    degerler = [18, 24, 22, 33, 41, 50]
    ax.plot(aylar, degerler, color=BLUE, linewidth=2, marker="o",
            markersize=3.2, markerfacecolor="white", markeredgewidth=1.2)
    ax.set_ylim(0, 60)
    ax.set_yticks([])
    eksen_ayari(ax)
    ax.tick_params(axis="x", labelsize=6.8)


def ciz_pasta(ax):
    oranlar = [42, 27, 19, 12]
    renkler = [NAVY, BLUE, MID, PALE]
    ax.pie(oranlar, colors=renkler, startangle=90,
           wedgeprops={"edgecolor": "white", "linewidth": 1.4})
    ax.set_aspect("equal")


def olustur():
    fig = plt.figure(figsize=(1181 / 200, 354 / 200), dpi=200)
    fig.patch.set_facecolor("white")
    eksenler, basliklar = kartlar(fig)
    ciz_sutun(eksenler[0])
    ciz_cizgi(eksenler[1])
    ciz_pasta(eksenler[2])
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
    cikti = HEDEF / "diagram-grafik-turleri-1.png"
    fig.savefig(cikti, dpi=200, facecolor="white")
    plt.close(fig)
    print(f"{cikti.relative_to(KOK)} üretildi")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
