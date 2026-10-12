# 4. hafta: dosya ağacı görseli (C:\ kökünden başlayan ağaç yapısı).
# Görsel DejaVu Sans Mono ile dizildiği için bu yazı tipi gerekir.
# Kullanım: python3 diyagram_betikleri/diagram-dosya-agaci.py
# Çıktı:    hafta-04-dosya-yonetimi-bulut/gorseller/diagram-dosya-agaci.png

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-04-dosya-yonetimi-bulut" / "gorseller"

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
fp = FontProperties(fname=FONT)

lines = [
    "C:\\",
    "\u251c\u2500\u2500\u2500Users",          # ├───Users
    "\u2502   \u251c\u2500\u2500\u2500Ali",   # │   ├───Ali
    "\u2502   \u2502   \u251c\u2500\u2500\u2500Masa\u00fcst\u00fc",  # │   │   ├───Masaüstü
    "\u2502   \u2502   \u251c\u2500\u2500\u2500Belgeler",           # │   │   ├───Belgeler
    "\u2502   \u2502   \u2514\u2500\u2500\u2500...",                # │   │   └───...
    "\u2502   \u251c\u2500\u2500\u2500G\u00fcl",                     # │   ├───Gül
    "\u2502   \u2502   \u251c\u2500\u2500\u2500Masa\u00fcst\u00fc",  # │   │   ├───Masaüstü
    "\u2502   \u2502   \u2514\u2500\u2500\u2500...",                 # │   │   └───...
    "\u2502   \u2514\u2500\u2500\u2500...",                          # │   └───...
    "\u251c\u2500\u2500\u2500Program Files",                         # ├───Program Files
    "\u2502   \u2514\u2500\u2500\u2500...",                          # │   └───...
    "\u2514\u2500\u2500\u2500...",                                   # └───...
]
tree = "\n".join(lines)

# Boyut hesabı: DejaVu Sans Mono karakter genişliği ≈ 0.602 * fontsize
fontsize = 16.0
char_w = 0.602 * fontsize
max_chars = max(len(s) for s in lines)  # 20
line_h = 1.4 * fontsize
n_lines = len(lines)

pad = 18.0  # pt, her iki yan
w_pt = max_chars * char_w + 2 * pad
h_pt = n_lines * line_h + 2 * pad

fig = plt.figure(figsize=(w_pt / 72.0, h_pt / 72.0), dpi=300)
fig.patch.set_facecolor("#EDF2F9")

# Kenarlıklı, yuvarlak köşeli kart görünümü (arka planın kendisi zaten #EDF2F9)
ax = fig.add_axes([0, 0, 1, 1])
ax.axis("off")
ax.set_xlim(0, w_pt)
ax.set_ylim(0, h_pt)
ax.invert_yaxis()  # üstten alta çizim

# Metni sol üstten, monospace ile
ax.text(
    pad, pad, tree,
    fontproperties=fp,
    fontsize=fontsize,
    color="#1F3864",
    va="top",
    ha="left",
    linespacing=1.4,
)

cikti = HEDEF / "diagram-dosya-agaci.png"
fig.savefig(cikti, dpi=300, facecolor=fig.get_facecolor())
print(f"{cikti.relative_to(KOK)} üretildi ({n_lines} satır, en çok {max_chars} karakter)")
