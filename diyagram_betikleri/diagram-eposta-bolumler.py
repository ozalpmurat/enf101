# 6. hafta: e-posta bölümleri — pencere şeması (Alıcı / Bilgi / Gizli / Konu / Gövde / Ek).
# Kullanım: python3 diyagram_betikleri/diagram-eposta-bolumler.py
# Çıktı:    hafta-06-internet-eposta-edevlet/gorseller/diagram-eposta-bolumler.png

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-06-internet-eposta-edevlet" / "gorseller"

LAC = "#1F3864"
ACIK = "#DCE7F5"
ZEMIN = "#EDF2F9"
GRI = "#595959"

plt.rcParams["font.family"] = "DejaVu Sans"

fig, ax = plt.subplots(figsize=(8.6, 5.4), dpi=170)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.6)
ax.axis("off")

ax.add_patch(FancyBboxPatch((0.25, 0.25), 9.5, 6.1,
             boxstyle="round,pad=0.02,rounding_size=0.12",
             linewidth=0, facecolor=ZEMIN, zorder=0))

# pencere gövdesi
ax.add_patch(FancyBboxPatch((1.0, 1.0), 8.0, 4.6,
             boxstyle="round,pad=0.02,rounding_size=0.06",
             linewidth=1.6, edgecolor=LAC, facecolor="#FFFFFF", zorder=1))
# başlık şeridi
ax.add_patch(FancyBboxPatch((1.0, 5.14), 8.0, 0.46,
             boxstyle="round,pad=0.02,rounding_size=0.06",
             linewidth=1.6, edgecolor=LAC, facecolor=LAC, zorder=2))
ax.text(1.25, 5.37, "Yeni Mesaj", ha="left", va="center", fontsize=11,
        color="#FFFFFF", zorder=3, fontweight="bold")

satirlar = [
    ("Alıcı (To)", "Mesajın asıl muhatabı"),
    ("Bilgi (CC)", "Bilgilendirilen, yanıt beklenmeyen kişiler"),
    ("Gizli (BCC)", "Adresleri diğer alıcılara görünmeyen kişiler"),
    ("Konu", "Kısa ve açıklayıcı başlık"),
]
y = 4.62
for ad, aciklama in satirlar:
    ax.plot([1.15, 8.85], [y, y], color="#C9D3E0", linewidth=1, zorder=2)
    ax.text(1.3, y - 0.19, ad, ha="left", va="center", fontsize=9.5,
            color=LAC, fontweight="bold", zorder=3)
    ax.text(3.55, y - 0.19, aciklama, ha="left", va="center", fontsize=8.5,
            color=GRI, zorder=3)
    y -= 0.5

# gövde
ax.plot([1.15, 8.85], [y, y], color="#C9D3E0", linewidth=1, zorder=2)
ax.text(1.3, y - 0.2, "Gövde", ha="left", va="center", fontsize=9.5,
        color=LAC, fontweight="bold", zorder=3)
ax.text(3.55, y - 0.2, "Hitap, mesaj, kapanış, imza", ha="left", va="center",
        fontsize=8.5, color=GRI, zorder=3)

# ek
ax.text(1.3, 1.3, "Ek (attachment)", ha="left", va="center", fontsize=9.5,
        color=LAC, fontweight="bold", zorder=3)
ax.text(3.55, 1.3, "Gönderilen dosyalar", ha="left", va="center",
        fontsize=8.5, color=GRI, zorder=3)
# ataç ikonu yerine küçük kutu
ax.add_patch(FancyBboxPatch((8.35, 1.12), 0.35, 0.36,
             boxstyle="round,pad=0.01,rounding_size=0.03",
             linewidth=1.2, edgecolor=LAC, facecolor=ACIK, zorder=3))

fig.tight_layout(pad=0.2)
cikti = HEDEF / "diagram-eposta-bolumler.png"
fig.savefig(cikti, dpi=170, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
