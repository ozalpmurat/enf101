# ENF101 — Temel Bilgi Teknolojileri Ders Materyali

Bilecik Şeyh Edebali Üniversitesi'nde tüm fakültelerin 1. sınıf öğrencilerine verilen
**ENF101 Temel Bilgi Teknolojileri** dersi için hazırlanmış, 14 haftalık ders materyali.
İçerik Türkçedir.

Materyal [Quarto](https://quarto.org) ile üretilir. Depoda hem kaynak (`.qmd`, `.tex`) hem de
üretilmiş **PDF** çıktıları birlikte tutulur.

## İçerik

- **`izlence.qmd` / `izlence.pdf`** — ders izlencesi.
- **`hafta-NN/`** — her haftanın paketi: `ders-notu.qmd`+`.pdf`, `sunum.qmd`+`.pdf`,
  `alistirma.qmd`+`.pdf` ve `gorseller/` klasörü (NN = 01 … 14).
- **`tema/notlar.tex` ve `tema/sunum.tex`** — ders notu ve sunumun ortak görünüm dosyaları.
- **`ornekler/`** — Quarto özelliklerine ilişkin başvuru belgeleri (ders içeriği değildir).
- **`KILAVUZ_Quarto_Kurulum_ve_Kullanim.qmd` / `.pdf`** — Quarto kurulum ve kullanım kılavuzu.
- **`AGENTS.md`** — proje kuralları, üretim talimatları ve geçmiş hatalardan çıkarılan uyarılar.

**Katkı yapmadan veya üretim komutunu çalıştırmadan önce `AGENTS.md` okunmalıdır.** Klasörün nasıl
derlendiği, hangi dosyalara dokunulmaması gerektiği ve hangi tuzaklara düşülmemesi gerektiği orada yazılıdır.

## Gereksinimler

- **Quarto 1.10.18** (materyal bu sürümle üretildi)
- **XeLaTeX / TeX Live** (TeX Live 2026 ile üretildi)
- Mermaid veya Graphviz şemaları PDF'e gömülecekse **Chrome Headless**

Sürümleri olabildiğince sabit tutun: PDF çıktısı TeX sürümüne göre ufak görsel farklar gösterebilir
(örn. madde imi glifleri). Böylece herkesin ürettiği PDF aynı görünür.

## Derleme

Proje kökünde:

```bash
quarto render hafta-03        # bir haftanın üç belgesini üretir
quarto render izlence.qmd     # tek dosya
```

`quarto render` yalnızca **tek yol** alır; `quarto render hafta-01 hafta-03` çalışmaz. Tüm projeyi
tek komutta derlemek uzun sürdüğü için hafta hafta derlemek gerekir. Ayrıntı: `AGENTS.md`.

## PDF'ler hakkında

PDF'ler aslında birer derleme çıktısıdır, ama bu depoda bilinçli olarak takip edilir: böylece
Quarto/TeX kurulu olmayan hocalar depoyu indirip PDF'leri doğrudan kullanabilir. Bir kaynağı
düzenlediğinizde, yeniden ürettiğiniz PDF'i de aynı commit'te göndermeniz beklenir.
`.gitattributes` PDF'leri ikili dosya olarak işaretler; Git bunlar üzerinde satır satır fark almaya çalışmaz.

## Katkı

1. Depoyu forklayın ya da bir dal (branch) açın.
2. Hafta bazında çalışın; bir haftayı düzenlerken diğer haftaları etkilemeyin.
3. Düzenlediğiniz `.qmd` dosyasını ve yeniden ürettiğiniz ilgili PDF'i birlikte commit'leyin.
4. `tema/` altındaki dosyalar kritiktir; silmeyin, taşımayın, adını değiştirmeyin (AGENTS.md §4).
5. Göndermeden önce `AGENTS.md`'nin sonundaki teslim öncesi doğrulama listesini çalıştırın.

## GitHub'a yükleme

```bash
git init -b main
git add -A
git commit -m "İlk sürüm: ENF101 ders materyali"
git remote add origin <depo-adresi>
git push -u origin main
```

## Lisans

Depoda henüz bir lisans dosyası yoktur. Materyalin başka kurum ve hocalarca kullanılıp
düzenlenebilmesi amaçlandığından, uygun bir lisans (örneğin eğitim içerikleri için **CC BY-SA**)
seçilip `LICENSE` dosyası eklenmesi önerilir. Bu, yeniden kullanım koşullarını netleştirir.
