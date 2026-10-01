#!/usr/bin/env bash
# ===============================================================
# ENF101 derleme sarmalayıcısı
#
# Ne yapar: `quarto render` çalıştırır; ardından son sayfasında
# "Sayfa n / N" altbilgisi bulunan belgelerde bu altbilgi TUTANA KADAR
# ek `xelatex` geçişi yapar.
#
# Neden gerekli: ders notu teması (tema/notlar.tex) altbilgiye toplam
# sayfa sayısını basar ve bu değer LaTeX'in belge sonunda yazdığı bir
# çapraz referanstan gelir. Belge tam sayfa sınırında bittiğinde
# Quarto'nun çalıştırdığı geçiş sayısı yetmez ve son sayfa
# "Sayfa 11 / 10" gibi **yanlış toplam** basar. Bu, bayat önbellekten
# değil, belgenin sınırda olmasından kaynaklanır; temiz bir derlemede
# de olur. Ayrıntı ve elenen diğer çözümler: AGENTS.md §3.
#
# Kullanım (depo kökünde):
#   bash araclar/derle.sh hafta-04-dosya-yonetimi-bulut
#   bash araclar/derle.sh hafta-04-dosya-yonetimi-bulut/04-ders-notu.qmd
#   bash araclar/derle.sh BASLIKLAR.qmd izlence.qmd
#   bash araclar/derle.sh .                 # bütün depo
#
# Gereksinimler: quarto, xelatex (TinyTeX), pdfinfo ve pdftotext (poppler-utils).
# Üretilen .tex/.aux/.log/.out dosyaları iş bitince silinir (.gitignore'da da yok sayılır).
# ===============================================================
set -euo pipefail

KOK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$KOK"

EK_GECIS=6      # belge başına en fazla ek xelatex geçişi

for arac in quarto xelatex pdfinfo pdftotext; do
  command -v "$arac" >/dev/null 2>&1 || { echo "HATA: '$arac' PATH'te bulunamadı." >&2; exit 1; }
done

# ---- hedefleri .qmd listesine aç ----
hedefler=()
for arg in "$@"; do
  if [ "$arg" = "." ]; then
    while IFS= read -r f; do hedefler+=("$f"); done \
      < <(find . -maxdepth 2 -name '*.qmd' -not -path './ornekler/*' | sort)
  elif [ -d "$arg" ]; then
    while IFS= read -r f; do hedefler+=("$f"); done \
      < <(find "$arg" -maxdepth 1 -name '*.qmd' | sort)
  else
    hedefler+=("$arg")
  fi
done
[ "${#hedefler[@]}" -gt 0 ] || { echo "Kullanım: bash araclar/derle.sh <klasör|dosya> [...]" >&2; exit 1; }

# ---- altbilgi yardımcıları (hiçbiri hata döndürmemeli: set -e) ----
sayfa_sayisi () { pdfinfo "$1" 2>/dev/null | awk '/^Pages/{print $2}' || true; }

altbilgi () {   # son sayfadaki "Sayfa n / N"; altbilgi yoksa boş döner
  local n
  n=$(sayfa_sayisi "$1")
  if [ -z "$n" ]; then echo ""; return 0; fi
  { pdftotext -layout -f "$n" -l "$n" "$1" - 2>/dev/null || true; } \
    | { grep -oE 'Sayfa [0-9]+ / [0-9]+' || true; } | head -1
}

# ---- derleme ----
for qmd in "${hedefler[@]}"; do
  if [ ! -f "$qmd" ]; then echo "atlandı (bulunamadı): $qmd" >&2; continue; fi
  dizin=$(dirname "$qmd"); taban=$(basename "$qmd" .qmd)
  pdf="$dizin/$taban.pdf"; tex="$dizin/$taban.tex"

  echo "==> $qmd"
  # .tex de üretilsin (ek geçiş gerekirse kullanılacak)
  quarto render "$qmd" -M keep-tex:true

  if [ ! -f "$tex" ]; then
    echo "    (uyarı: .tex üretilmedi, altbilgi kontrolü atlandı)" >&2
    continue
  fi

  n=$(sayfa_sayisi "$pdf"); s=$(altbilgi "$pdf")
  if [ -z "$s" ]; then
    echo "    altbilgi yok, ek geçiş gerekmez ($n sayfa)"
  elif [ "$s" = "Sayfa $n / $n" ]; then
    echo "    altbilgi doğru ($s)"
  else
    echo "    altbilgi tutmuyor ($s; gerçek $n sayfa) — ek geçişler yapılıyor"
    i=0
    while [ "$i" -lt "$EK_GECIS" ]; do
      ( cd "$dizin" && xelatex -interaction=nonstopmode "$taban.tex" >/dev/null 2>&1 || true )
      i=$((i + 1))
      n=$(sayfa_sayisi "$pdf"); s=$(altbilgi "$pdf")
      if [ "$s" = "Sayfa $n / $n" ]; then break; fi
    done
    if [ "$s" = "Sayfa $n / $n" ]; then
      echo "    altbilgi $i ek geçişte oturdu ($s)"
    else
      echo "    UYARI: altbilgi tutmuyor ($s; gerçek $n sayfa) — elle bakın" >&2
    fi
  fi

  rm -f "$tex" "$dizin/$taban.aux" "$dizin/$taban.log" "$dizin/$taban.out"
done

echo "bitti."
