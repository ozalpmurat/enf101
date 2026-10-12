# 2. hafta: HDD (dönen disk) ile SSD (flash yonga) karşılaştırması.
# Kullanım: python3 diyagram_betikleri/diagram-hdd-ssd.py
# Çıktı:    hafta-02-bilgisayar-donanim/gorseller/diagram-hdd-ssd.png

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-02-bilgisayar-donanim" / "gorseller"

NAVY = "#1F3864"
ACCENT = "#2E74B5"
LIGHT = "#EDF2F9"
GREY = "#595959"

plt.rcParams["font.family"] = "DejaVu Sans"


def kutu(ax, x, y, w, h, text, fc=LIGHT, ec=NAVY, fs=11, tc=NAVY, bold=True, round_=0.05):
    b = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.015,rounding_size={round_}",
                       fc=fc, ec=ec, lw=1.5)
    ax.add_patch(b)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fs,
            color=tc, fontweight="bold" if bold else "normal")
    return b


def zemin(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


fig, ax = plt.subplots(figsize=(8.6, 3.4), dpi=200)
zemin(ax, (0, 10), (0, 4.0))
# HDD
kutu(ax, 0.5, 0.5, 4.2, 3.0, "", fc=LIGHT, ec=NAVY, round_=0.07)
ax.text(2.6, 3.05, "HDD", ha="center", fontsize=12, color=NAVY, fontweight="bold")
disk = Circle((2.6, 1.9), 0.75, fc="white", ec=GREY, lw=2)
ax.add_patch(disk)
ax.text(2.6, 1.9, "disk", ha="center", va="center", fontsize=8, color=GREY)
ax.add_patch(FancyArrowPatch((2.6, 1.9), (3.15, 2.4), arrowstyle="-", color=GREY, lw=2.5))
ax.text(2.6, 0.8, "Dönen disk + okuyucu kafa\n(mekanik, yavaş)", ha="center", fontsize=9, color=GREY)
# SSD
kutu(ax, 5.3, 0.5, 4.2, 3.0, "", fc="#F4F7FB", ec=ACCENT, round_=0.07)
ax.text(7.4, 3.05, "SSD", ha="center", fontsize=12, color=NAVY, fontweight="bold")
for i, cx in enumerate([6.6, 7.4, 8.2]):
    c = FancyBboxPatch((cx-0.32, 1.55), 0.64, 0.55, boxstyle="round,pad=0.01,rounding_size=0.06",
                       fc="white", ec=ACCENT, lw=1.5)
    ax.add_patch(c)
ax.text(7.4, 0.8, "Flash bellek yongaları\n(elektronik, hızlı)", ha="center", fontsize=9, color=GREY)

cikti = HEDEF / "diagram-hdd-ssd.png"
fig.savefig(cikti, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
