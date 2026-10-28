# 6. hafta: e-posta bölümleri — pencere şeması (Alıcı / Bilgi / Gizli / Konu / Gövde / Ek).
# Kullanım: python3 diyagram_betikleri/diagram-eposta-bolumler.py
# Çıktı:    hafta-06-internet-eposta-edevlet/gorseller/diagram-eposta-bolumler.png

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-06-internet-eposta-edevlet" / "gorseller"

LAC = "#1F3864"
GRI = "#595959"

plt.rcParams["font.family"] = "DejaVu Sans"

fig, ax = plt.subplots(figsize=(5.73, 3.38), dpi=170)
# kırpma: çizim pencereyle sınırlı; dışarıda açık renk çerçeve yok
ax.set_xlim(0.85, 9.15)
ax.set_ylim(0.85, 5.75)
ax.axis("off")

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
# gövdenin dört öğesi alt alta
for i, oge in enumerate(["hitap", "mesaj", "kapanış", "imza"]):
    ax.text(3.55, y - 0.2 - i * 0.24, oge, ha="left", va="center",
            fontsize=8.5, color=GRI, zorder=3)

# ek
ax.plot([1.15, 8.85], [1.56, 1.56], color="#C9D3E0", linewidth=1, zorder=2)
ax.text(1.3, 1.3, "Ek (attachment)", ha="left", va="center", fontsize=9.5,
        color=LAC, fontweight="bold", zorder=3)
ax.text(3.55, 1.3, "Gönderilen dosyalar", ha="left", va="center",
        fontsize=8.5, color=GRI, zorder=3)
# ataç simgesi: tek bir tel gibi — iç kol, üst kavis, sağ kol, alt kavis, sol kol
ATAÇ = dict(linewidth=1.6, edgecolor=LAC, facecolor="none", zorder=4)
xl, xr, xm = 8.38, 8.70, 8.48          # dış sol, dış sağ, iç kol
yb = 1.10                               # ikonun en alt noktası
r_alt, r_üst = (xr - xl) / 2, (xr - xm) / 2
y_alt, y_üst = yb + r_alt, 1.40         # kavislerin uç noktalarının yüksekliği

ax.plot([xm, xm], [y_üst, y_alt + 0.04], color=LAC,
        linewidth=1.6, solid_capstyle="round", zorder=4)          # iç kol
ax.add_patch(Arc(((xm + xr) / 2, y_üst), 2 * r_üst, 2 * r_üst,
                 theta1=0, theta2=180, **ATAÇ))                   # üst kavis
ax.plot([xr, xr], [y_üst, y_alt], color=LAC,
        linewidth=1.6, solid_capstyle="round", zorder=4)          # sağ kol
ax.add_patch(Arc(((xl + xr) / 2, y_alt), 2 * r_alt, 2 * r_alt,
                 theta1=180, theta2=360, **ATAÇ))                 # alt kavis
ax.plot([xl, xl], [y_alt, y_üst + r_üst - 0.07], color=LAC,
        linewidth=1.6, solid_capstyle="round", zorder=4)          # sol kol

fig.tight_layout(pad=0.2)
cikti = HEDEF / "diagram-eposta-bolumler.png"
fig.savefig(cikti, dpi=170, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
