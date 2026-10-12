# 3. hafta: yazdırma işinin katmanlar arası akışı (kelime işlemci → işletim sistemi → yazıcı).
# Kullanım: python3 diyagram_betikleri/diagram-ornek-yazdirma.py
# Çıktı:    hafta-03-yazilim-isletim-sistemleri/gorseller/diagram-ornek-yazdirma.png

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-03-yazilim-isletim-sistemleri" / "gorseller"

NAVY = "#1F3864"
FILL = "#EDF2F9"
GREY = "#595959"

W, H = 10.5, 11.0                      # cm
fig = plt.figure(figsize=(W/2.54, H/2.54), dpi=150)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect("equal")
ax.axis("off")


def box(y0, y1, label):
    ax.add_patch(FancyBboxPatch((0.6, y0), W-1.2, y1-y0,
                 boxstyle="round,pad=0,rounding_size=0.35",
                 linewidth=2.4, edgecolor=NAVY, facecolor=FILL))
    ax.text(W/2, (y0+y1)/2, label, ha="center", va="center",
            color=NAVY, fontsize=18, fontweight="bold")


def arrow(y0, y1, label):
    ax.add_patch(FancyArrowPatch((W/2, y0+0.10), (W/2, y1-0.10),
                 arrowstyle="<|-|>", mutation_scale=17, linewidth=2.0,
                 color=NAVY, shrinkA=0, shrinkB=0))
    ax.text(W/2+0.33, (y0+y1)/2, label, ha="left", va="center",
            color=NAVY, fontsize=13)


box(8.10, 10.10, "KELİME İŞLEMCİ")
arrow(6.70, 8.10, "yazdırma isteği")
box(4.70, 6.70, "İŞLETİM SİSTEMİ")
arrow(3.30, 4.70, "yazıcı sürücüsü")
box(1.30, 3.30, "YAZICI")
ax.text(W/2, 0.55, "Örnek: bir belgeyi yazdırma", ha="center", va="center",
        color=GREY, fontsize=13, style="italic")

cikti = HEDEF / "diagram-ornek-yazdirma.png"
fig.savefig(cikti, dpi=150, facecolor="white")
print(f"{cikti.relative_to(KOK)} üretildi")
