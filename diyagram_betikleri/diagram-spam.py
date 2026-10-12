# 6. hafta: istenmeyen posta (spam) akışı.
# Kullanım: python3 diyagram_betikleri/diagram-spam.py
# Çıktı:    hafta-06-internet-eposta-edevlet/gorseller/diagram-spam.png

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-06-internet-eposta-edevlet" / "gorseller"

LAC = "#1F3864"
ACIK = "#DCE7F5"
ZEMIN = "#EDF2F9"
GRI = "#595959"

plt.rcParams["font.family"] = "DejaVu Sans"


def kutu(ax, x, y, w, h, metin, fc=ACIK, ec=LAC, fs=11, tc=LAC, bold=False):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                       linewidth=1.6, edgecolor=ec, facecolor=fc, zorder=2)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, metin, ha="center", va="center",
            fontsize=fs, color=tc, zorder=3,
            fontweight="bold" if bold else "normal", wrap=True)
    return (x, y, w, h)


def ok(ax, p1, p2, renk=LAC):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=14,
                                 linewidth=1.5, color=renk, zorder=1,
                                 shrinkA=2, shrinkB=2))


fig, ax = plt.subplots(figsize=(8.6, 3.2), dpi=170)
ax.set_xlim(0, 10)
ax.set_ylim(0, 3.8)
ax.axis("off")

ax.add_patch(FancyBboxPatch((0.25, 0.25), 9.5, 3.3,
             boxstyle="round,pad=0.02,rounding_size=0.12",
             linewidth=0, facecolor=ZEMIN, zorder=0))

adimlar = [
    ("Adresiniz bir\nformda paylaşılır", "#FFFFFF"),
    ("Adres listelere\neklenir", ACIK),
    ("İstenmeyen toplu\nposta gelmeye başlar", ACIK),
    ("Tıklamayın,\nsilin", "#FFFFFF"),
]
x0, w, gap = 0.7, 1.95, 0.42
for i, (m, fc) in enumerate(adimlar):
    x = x0 + i * (w + gap)
    kutu(ax, x, 1.4, w, 1.0, m, fc=fc, fs=9.5, bold=(i == 3))
    if i < len(adimlar) - 1:
        ok(ax, (x + w, 1.9), (x + w + gap, 1.9))

ax.text(5.0, 3.0, "İstenmeyen posta (spam) nasıl gelir?", ha="center",
        va="center", fontsize=9.5, color=GRI, style="italic")

fig.tight_layout(pad=0.2)
cikti = HEDEF / "diagram-spam.png"
fig.savefig(cikti, dpi=170, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
