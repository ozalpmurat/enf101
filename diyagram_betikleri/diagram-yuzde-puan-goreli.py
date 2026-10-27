# 8. hafta: aynı 5 puanlık fark, farklı tabanlarda farklı göreli büyüme demektir.
# Üstte taban %20 (5 puan = %25 büyüme), altta taban %50 (5 puan = %10 büyüme).
# İki satır aynı ölçekte çizilir; 5 puanlık çubuk parçası gözle aynı görünür.
# Kullanım: python3 diyagram_betikleri/diagram-yuzde-puan-goreli.py [--kontrol]
# Çıktı:    hafta-08-hesap-tablosu/gorseller/diagram-yuzde-puan-goreli.png

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-08-hesap-tablosu" / "gorseller"
CIKTI = HEDEF / "diagram-yuzde-puan-goreli.png"

KIRMIZI = "#C0392B"   # taban (Excel'de A sütunu kırmızı)
MAVI = "#2E74B5"      # eklenen 5 puan ve sonuç (Excel'de B sütunu mavi)
GREY = "#595959"
RULE = "#BFBFBF"

SATIRLAR = [
    # (satır etiketi, taban, fark, hesap metni)
    ("Taban %20", 20, 5, "5 ÷ 20 = %25 büyüme"),
    ("Taban %50", 50, 5, "5 ÷ 50 = %10 büyüme"),
]

plt.rcParams["font.family"] = "DejaVu Sans"


def ciz(kontrol=False):
    fig, ax = plt.subplots(figsize=(10.6 / 2.54, 4.4 / 2.54), dpi=200)

    for i, (etiket, taban, fark, hesap) in enumerate(SATIRLAR):
        y = len(SATIRLAR) - 1 - i
        # renkler Excel görüntüsüyle aynı: taban (A sütunu) kırmızı, eklenen kısım (B) mavi
        ax.barh(y, taban, height=0.5, color=KIRMIZI, zorder=3)
        ax.barh(y, fark, left=taban, height=0.5, color=MAVI, zorder=3)

        ax.text(-2, y, etiket, ha="right", va="center", fontsize=8.5,
                color=GREY, fontweight="bold")
        ax.text(taban / 2, y, f"%{taban}", ha="center", va="center",
                fontsize=8, color="white", fontweight="bold", zorder=4)
        ax.text(taban + fark + 1.5, y, hesap, ha="left", va="center",
                fontsize=8, color=MAVI, fontweight="bold")

        # 5 puanlık farkın parantezi
        ax.annotate("", xy=(taban, y - 0.42), xytext=(taban + fark, y - 0.42),
                    arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.0))
        ax.text(taban + fark / 2, y - 0.55, f"{fark} puan", ha="center", va="top",
                fontsize=7.5, color=GREY)

    ax.set_xlim(0, 100)
    ax.set_ylim(-0.75, len(SATIRLAR) - 0.3)
    ax.set_yticks([])
    ax.set_xticks([])
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)

    # ortak ölçek: 5 puanlık parça iki satırda da aynı genişlikte
    ax.axvline(0, color=RULE, lw=0.8)
    fig.tight_layout()

    if kontrol:
        fig.canvas.draw()
        pencere = fig.bbox
        sorun = 0
        for t in ax.texts:
            kutu = t.get_window_extent(renderer=fig.canvas.get_renderer())
            if (kutu.x0 < pencere.x0 - 1 or kutu.x1 > pencere.x1 + 1
                    or kutu.y0 < pencere.y0 - 1 or kutu.y1 > pencere.y1 + 1):
                print(f"TAŞMA: {t.get_text()!r}")
                sorun += 1
        if sorun:
            print(f"{sorun} yazı figürün dışına taşıyor")
            return False
        print("--kontrol: bütün yazılar figür içinde")
        return True

    fig.savefig(CIKTI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"{CIKTI.relative_to(KOK)} üretildi")
    return True


if __name__ == "__main__":
    if "--kontrol" in sys.argv:
        sys.exit(0 if ciz(kontrol=True) else 1)
    ciz()
