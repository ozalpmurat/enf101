# 6. hafta: e-posta adresinin yapısı — kullanıcı adı + @ + alan adı.
# Şemanın içine başlık yazılmaz: başlık ders notunda şekil altyazısı, sunumda slayt başlığıdır (AGENTS.md §8).
# Kullanım: python3 diyagram_betikleri/diagram-eposta.py
# Çıktı:    hafta-06-internet-eposta-edevlet/gorseller/diagram-eposta.png
#
# Kutu genişlikleri metin genişliğine göre ayarlanmıştır: yazı kutudan taşarsa
# (matplotlib yazıyı kırmaz, kutunun üstüne bindirir) şema bozuk görünür.
# Doğrulama: python3 diyagram_betikleri/diagram-eposta.py --kontrol

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-06-internet-eposta-edevlet" / "gorseller"

LAC = "#1F3864"
ACIK = "#DCE7F5"
GRI = "#595959"
CIZGI = "#C9D3E0"

PUNTO = 19  # adres yazısının punto büyüklüğü

# Ölçü birimi cm'dir; matplotlib figsize inç ister (AGENTS.md §8).
GENISLIK, YUKSEKLIK = 17.0, 3.6

KUTULAR = [
    # (kutu x, kutu genişliği, metin merkezi, metin, renk)
    (0.9, 5.2, 3.5, "kullanici", "#EDF2F9"),
    (9.0, 7.2, 12.6, "kurum.edu.tr", ACIK),
]
ETIKETLER = [(3.5, "kim?"), (12.6, "hangi sunucu?")]
AT = (7.55, "@")

KUTU_STIL = dict(boxstyle="round,pad=0.02,rounding_size=0.18",
                 linewidth=1.8, zorder=1)


def tuval():
    fig, ax = plt.subplots(figsize=(GENISLIK / 2.54, YUKSEKLIK / 2.54), dpi=200)
    ax.set_xlim(0, GENISLIK)
    ax.set_ylim(0, YUKSEKLIK)
    ax.axis("off")
    return fig, ax


def ciz(fig, ax):
    for x, g, mx, metin, zemin in KUTULAR:
        ax.add_patch(FancyBboxPatch((x, 1.85), g, 1.3,
                     facecolor=zemin, edgecolor=LAC, **KUTU_STIL))
        ax.text(mx, 2.5, metin, ha="center", va="center", fontsize=PUNTO,
                color=LAC, fontweight="bold", zorder=2)

    ax.text(AT[0], 2.5, AT[1], ha="center", va="center", fontsize=PUNTO + 2,
            color=LAC, fontweight="bold", zorder=2)

    for mx, etiket in ETIKETLER:
        ax.plot([mx, mx], [1.77, 1.35], color=CIZGI, linewidth=1.4, zorder=1)
        ax.text(mx, 0.95, etiket, ha="center", va="center", fontsize=12.5,
                color=GRI, zorder=2)


def kontrol():
    """Yazı kutusunun dışına taşıyor mu? Taşıyorsa non-zero ile çık."""
    fig, ax = tuval()
    ciz(fig, ax)
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    sorun = []
    for (x, g, mx, metin, _), (_, etiket) in zip(KUTULAR, ETIKETLER):
        olc = ax.text(mx, 0, metin, ha="center", va="center",
                      fontsize=PUNTO, fontweight="bold")
        bb = olc.get_window_extent(renderer=r).transformed(
            ax.transData.inverted())
        olc.remove()
        if bb.x0 < x + 0.15 or bb.x1 > x + g - 0.15:
            sorun.append(f"{metin!r}: {bb.x0:.2f}–{bb.x1:.2f} "
                         f"kutu {x:.2f}–{x + g:.2f}")
    plt.close(fig)
    if sorun:
        print("TAŞMA:\n  " + "\n  ".join(sorun))
        return 1
    print("kutular tamam: yazılar kutuların içinde")
    return 0


def uret():
    fig, ax = tuval()
    ciz(fig, ax)
    fig.tight_layout(pad=0.2)
    cikti = HEDEF / "diagram-eposta.png"
    fig.savefig(cikti, dpi=200, facecolor="white")
    plt.close(fig)
    print(f"{cikti.relative_to(KOK)} üretildi")
    return 0


if __name__ == "__main__":
    sys.exit(kontrol() if "--kontrol" in sys.argv else uret())
