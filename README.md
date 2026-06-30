# Amazon RFM Analizi

Amazon sipariş verisi üzerinde, müşterileri **RFM (Recency, Frequency, Monetary)** metriklerine göre segmentlere ayıran bir analiz projesi. 
Müşteri davranışlarını anlamak ve pazarlama stratejilerini bu segmentlere göre yönlendirmek amacıyla geliştirildi.

## İçindekiler

- [RFM Nedir?](#rfm-nedir)
- [Kullanılan Teknolojiler](#kullanılan-teknolojiler)
- [Veri Seti](#veri-seti)
- [Analiz Adımları](#analiz-adımları)
- [Segmentler](#segmentler)
- [Kurulum ve Çalıştırma](#kurulum-ve-çalıştırma)
- [Çıktı](#çıktı)

## RFM Nedir?

RFM, müşterileri üç temel davranışsal metriğe göre puanlayan bir segmentasyon yöntemidir:

- **Recency (Yenilik):** Müşterinin son alışverişinden bu yana geçen gün sayısı. Düşük değer daha iyidir.
- **Frequency (Sıklık):** Müşterinin toplam alışveriş sayısı. Yüksek değer daha iyidir.
- **Monetary (Parasal Değer):** Müşterinin toplam harcaması. Yüksek değer daha iyidir.

Bu üç metrik 1-5 arasında puanlanır ve müşteriler anlamlı segmentlere (champions, at_risk, hibernating vb.) ayrılır.

## Kullanılan Teknolojiler

- **Python**
- **pandas** — veri işleme ve gruplama
- **numpy** — sayısal işlemler
- **matplotlib / seaborn** — görselleştirme

## Veri Seti

Analiz, Amazon sipariş kayıtlarını içeren bir CSV dosyası üzerinde çalışır. Kullanılan başlıca kolonlar:

| Kolon | Açıklama |
|-------|----------|
| `CustomerID` | Müşteri kimliği |
| `OrderID` | Sipariş kimliği |
| `OrderDate` | Sipariş tarihi |
| `OrderStatus` | Sipariş durumu (Delivered, Canceled vb.) |
| `TotalAmount` | Sipariş tutarı |

## Analiz Adımları

1. **Veri yükleme ve inceleme** — CSV okunur, eksik değerler ve sipariş durumları kontrol edilir.
2. **Filtreleme** — Yalnızca `Delivered` (teslim edilmiş) siparişler analize dahil edilir.
3. **Tarih dönüşümü** — `OrderDate` kolonu datetime tipine çevrilir.
4. **Analiz tarihi belirleme** — Recency hesabı için referans tarih olarak `2024-12-30` kullanılır (veri setindeki en son tarihten bir gün sonrası).
5. **RFM metriklerinin hesaplanması** — Her müşteri için recency, frequency ve monetary değerleri gruplanarak hesaplanır.
6. **Puanlama** — Her metrik `qcut` ile 1-5 arası beş eşit dilime ayrılır.
7. **Segmentasyon** — Recency ve Frequency puanları birleştirilerek (`RF_SCORE`) regex tabanlı bir harita üzerinden segmentlere atanır.
8. **Dışa aktarma** — Müşteri segment listesi `segment_list.csv` olarak kaydedilir.

## Segmentler

RF skoruna göre müşteriler şu segmentlere ayrılır:

| Segment | Açıklama |
|---------|----------|
| `champions` | En değerli, sık ve yakın zamanda alışveriş yapan müşteriler |
| `loyal_customers` | Sadık, düzenli alışveriş yapanlar |
| `potential_loyalists` | Sadık müşteriye dönüşme potansiyeli olanlar |
| `new_customers` | Yeni kazanılmış müşteriler |
| `promising` | Umut vaat eden yeni müşteriler |
| `need_attention` | İlgi gösterilmesi gereken ortalama müşteriler |
| `about_to_sleep` | Pasifleşmeye başlayan müşteriler |
| `at_Risk` | Kaybedilme riski yüksek, eskiden değerli müşteriler |
| `cant_loose` | Kaybedilmemesi gereken müşteriler |
| `hibernating` | Uzun süredir alışveriş yapmayan müşteriler |

## Kurulum ve Çalıştırma

Gerekli kütüphaneleri yükleyin:

```bash
pip install numpy pandas seaborn matplotlib  
```

Kod içindeki dosya yolunu kendi veri setinize göre güncelleyin:

```python
df_ = pd.read_csv("Amazon.csv")
```

Ardından script'i çalıştırın:

```bash
python amazon_rfm.py
```

## Çıktı

Analiz sonucunda her müşterinin atandığı segmenti içeren bir `segment_list.csv` dosyası üretilir. Bu çıktı, hedefli pazarlama kampanyaları, müşteri tutma stratejileri ve kişiselleştirilmiş kampanyalar için kullanılabilir.

---

*Bu proje öğrenme ve veri analizi pratiği amacıyla geliştirilmiştir.*
