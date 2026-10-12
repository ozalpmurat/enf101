# 2. hafta: RAM (çalışma belleği) ile depolamanın karşılaştırılması.
# Kullanım: python3 diyagram_betikleri/diagram-ram-depolama.py
# Çıktı:    hafta-02-bilgisayar-donanim/gorseller/diagram-ram-depolama.png

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

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


fig, ax = plt.subplots(figsize=(8.6, 3.2), dpi=200)
zemin(ax, (0, 10), (0, 3.6))
kutu(ax, 0.5, 0.6, 4.2, 2.4, "", fc=LIGHT, ec=ACCENT, round_=0.07)
ax.text(2.6, 2.5, "RAM — Çalışma Belleği", ha="center", fontsize=11, color=NAVY, fontweight="bold")
ax.text(2.6, 1.9, "Geçici · elektrik kesilince silinir", ha="center", fontsize=9.5, color=GREY)
ax.text(2.6, 1.3, "Masa benzetmesi", ha="center", fontsize=9, color=ACCENT, style="italic")
kutu(ax, 5.3, 0.6, 4.2, 2.4, "", fc="#F4F7FB", ec=NAVY, round_=0.07)
ax.text(7.4, 2.5, "Depolama — Disk", ha="center", fontsize=11, color=NAVY, fontweight="bold")
ax.text(7.4, 1.9, "Kalıcı · dosyalar saklanır", ha="center", fontsize=9.5, color=GREY)
ax.text(7.4, 1.3, "Çekmece benzetmesi", ha="center", fontsize=9, color=ACCENT, style="italic")

cikti = HEDEF / "diagram-ram-depolama.png"
fig.savefig(cikti, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
