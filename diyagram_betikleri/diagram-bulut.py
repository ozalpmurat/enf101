# 4. hafta: bulut akış şeması (cihazlar → İnternet → bulut sunucuları).
# Kullanım: python3 diyagram_betikleri/diagram-bulut.py
# Çıktı:    hafta-04-dosya-yonetimi-bulut/gorseller/diagram-bulut.png

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-04-dosya-yonetimi-bulut" / "gorseller"

LACIVERT = "#1F3864"
ZEMIN = "#EDF2F9"
MAVI = "#2E75B6"
GRI = "#595959"

fig, ax = plt.subplots(figsize=(11.0, 4.3), dpi=200)
fig.patch.set_facecolor("white")
ax.set_xlim(0, 11.0)
ax.set_ylim(0, 4.3)
ax.axis("off")


def kutu(x, y, w, h, baslik, alt=None):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.18",
        linewidth=2.0, edgecolor=LACIVERT, facecolor=ZEMIN,
        mutation_aspect=1,
    ))
    if alt:
        ax.text(x + w/2, y + h*0.62, baslik, ha="center", va="center",
                fontsize=13, fontweight="bold", color=LACIVERT)
        ax.text(x + w/2, y + h*0.30, alt, ha="center", va="center",
                fontsize=11.5, color=LACIVERT)
    else:
        ax.text(x + w/2, y + h/2, baslik, ha="center", va="center",
                fontsize=13, fontweight="bold", color=LACIVERT)


# --- Sol: cihazlar ---
kutu(0.15, 2.55, 3.15, 1.35, "DİZÜSTÜ", "kendi cihazınız")
kutu(0.15, 1.05, 3.15, 1.35, "TELEFON / TABLET", "aynı dosyalara erişim")

# --- Orta: İnternet ---
kutu(3.85, 1.80, 2.7, 1.35, "İNTERNET", "veri yüklenir / indirilir")

# --- Sağ: bulut sunucuları ---
kutu(7.35, 1.80, 3.5, 1.35, "BULUT SUNUCULARI", "sağlayıcının uzak sunucuları")


# --- Oklar ---
def ok(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=22,
        linewidth=2.2, color=MAVI,
    ))


ok(3.33, 3.22, 3.82, 2.85)   # dizüstü -> internet
ok(3.33, 1.72, 3.82, 2.10)   # telefon -> internet
ok(6.58, 2.47, 7.32, 2.47)   # internet -> bulut
ax.add_patch(FancyArrowPatch(
    (7.32, 2.30), (6.58, 2.30),
    arrowstyle="-|>", mutation_scale=22,
    linewidth=2.2, color=MAVI,
))

# --- Alt not ---
ax.text(5.5, 0.35, "Dosyalar sizin diskinizde değil, sağlayıcının sunucularında durur.",
        ha="center", va="center", fontsize=13, style="italic", color=GRI)

cikti = HEDEF / "diagram-bulut.png"
fig.savefig(cikti, dpi=200, facecolor="white", bbox_inches="tight", pad_inches=0.12)
print(f"{cikti.relative_to(KOK)} üretildi")
