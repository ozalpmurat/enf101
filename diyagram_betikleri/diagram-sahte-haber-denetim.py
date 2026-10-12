# IFLA'nın "How to Spot Fake News" listesinden uyarlanan sekiz maddelik
# denetim listesini ENF paletiyle yatay 4x2 kart düzeni olarak çizer.
# Başlık çizilmez: ders notunda altyazı, sunumda slayt başlığı kullanılır.
# Kullanım: python3 diyagram_betikleri/diagram-sahte-haber-denetim.py
# Çıktı:    hafta-06-internet-eposta-edevlet/gorseller/diagram-sahte-haber-denetim.png
#           (22 x 7,5 cm, 200 dpi)

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-06-internet-eposta-edevlet" / "gorseller"

NAVY = "#1F3864"
ACCENT = "#2E74B5"
LIGHT = "#EDF2F9"
GREY = "#595959"

MADDELER = [
    ("Kaynağı sorgula", "Siteyi ve kurumunu araştır"),
    ("Yazarı kontrol et", "Gerçek ve güvenilir mi?"),
    ("Tarihi kontrol et", "Güncel mi, eski mi?"),
    ("Önyargılarına bak", "Kendi inancını da sorgula"),
    ("Haberin tamamını oku", "Başlığa göre karar verme"),
    ("Destekleyici kaynak ara", "Kanıtlara tıkla, doğrula"),
    ("Şaka mı, ciddi mi?", "Abartılıysa mizah olabilir"),
    ("Uzmanlara sor", "Doğrulama sitesine danış"),
]


def ikiye_bol(metin):
    if len(metin) <= 14:
        return [metin]
    orta = len(metin) // 2
    solda = metin.rfind(" ", 0, orta)
    sagda = metin.find(" ", orta)
    if solda == -1 and sagda == -1:
        return [metin]
    kesim = solda if sagda == -1 or (solda != -1 and orta - solda <= sagda - orta) else sagda
    return [metin[:kesim], metin[kesim + 1:]]

CM = 1 / 2.54
fig = plt.figure(figsize=(22 * CM, 7.5 * CM))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 22)
ax.set_ylim(0, 7.5)
ax.axis("off")

x0, y0, w, h, gx, gy = 0.7, 0.6, 4.9, 2.9, 0.35, 0.55
for i, (baslik, aciklama) in enumerate(MADDELER):
    satir, kolon = divmod(i, 4)
    x = x0 + kolon * (w + gx)
    y = 4.05 - satir * (h + gy)
    kutu = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.12,rounding_size=0.22",
                          linewidth=1.4, edgecolor=ACCENT, facecolor=LIGHT)
    ax.add_patch(kutu)
    cx = x + w / 2
    daire = plt.Circle((cx, y + h - 0.52), 0.30,
                       linewidth=1.4, edgecolor=ACCENT, facecolor="white")
    ax.add_patch(daire)
    ax.text(cx, y + h - 0.52, str(i + 1), ha="center", va="center",
            fontsize=12, fontweight="bold", color=ACCENT)
    satirlar = ikiye_bol(baslik)
    for j, satir_metni in enumerate(satirlar):
        ysatir = y + h - 1.15 - j * 0.62
        ax.text(cx, ysatir, satir_metni, ha="center", va="center",
                fontsize=11.5, fontweight="bold", color=NAVY)
    ax.text(cx, y + 0.45, aciklama, ha="center", va="center",
            fontsize=9, color=GREY)

cikti = HEDEF / "diagram-sahte-haber-denetim.png"
fig.savefig(cikti, dpi=200, facecolor="white", bbox_inches=None)
print(f"{cikti.relative_to(KOK)} üretildi")
