# 8. hafta: aynı verinin iki farklı dikey eksenle gösterimi.
# Solda eksen sıfırdan başlar, sağda 46'dan — veri aynı, izlenim farklı.
# Kullanım: python3 diyagram_betikleri/karsilastirma.py
# Çıktı:    hafta-08-elektronik-tablo/gorseller/karsilastirma.png

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-08-elektronik-tablo" / "gorseller"

NAVY = "#1F3864"
GREY = "#595959"
RULE = "#BFBFBF"

aylar = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu"]
deger = [48, 49, 50, 52, 51, 53, 54, 56]

plt.rcParams["font.family"] = "DejaVu Sans"


def stil(ax, baslik, ymin, ymax):
    ax.bar(aylar, deger, color=NAVY, width=0.62)
    ax.set_ylim(ymin, ymax)
    ax.set_title(baslik, color=NAVY, fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("Bin geçiş", color=GREY, fontsize=10)
    ax.tick_params(axis="both", labelsize=10, colors=GREY, length=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(RULE)
    ax.spines["bottom"].set_color(RULE)
    ax.grid(axis="y", color=RULE, linewidth=0.5, alpha=0.6)
    ax.set_axisbelow(True)
    ax.text(0.0, -0.22, "Kaynak: Örnek veri (ilçe bisiklet yolu sayımları)",
            transform=ax.transAxes, fontsize=8.5, color=GREY)


fig, eksenler = plt.subplots(1, 2, figsize=(11.4, 3.8), dpi=200)
stil(eksenler[0], "Grafik A", 0, 60)
stil(eksenler[1], "Grafik B", 46, 57)
fig.tight_layout()
cikti = HEDEF / "karsilastirma.png"
fig.savefig(cikti, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
