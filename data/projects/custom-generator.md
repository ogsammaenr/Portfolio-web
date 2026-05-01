# 🛠️ CustomGenerator

Ada sahiplerinin özel kırıktaş (cobblestone), taş (stone), bazalt veya derinrakım (deepslate) jeneratörleri satın almasını, yönetmesini ve aktifleştirmesini sağlamak için tasarlanmış, BentoBox uyumlu, tam özellikli bir jeneratör eklentisi. Tüm yapılandırmalar düzenlemesi kolay YAML dosyaları üzerinden yönetilir, böylece sunucu yöneticileri için özelleştirme işlemi basit ve esnektir.

---

## ✨ Özellikler

* Ada başına **satın alma ve aktifleştirme** iş akışı, yerleşik ekonomi ve ada seviyesi doğrulamaları ile
* Kategorilere ve bireysel jeneratör türlerine göz atmak için sezgisel **GUI menüleri**
* Gücünü `custom-generator-categories.yml` dosyasından alan **Özel Jeneratör Mantığı (Custom Generator Logic)**
* **YAML dosyaları** aracılığıyla tamamen özelleştirilebilir mesajlar, GUI düzenleri ve jeneratör ayarları
* Hızlı yanıt süreleri ve minimum sunucu yükü için verimli **önbellek öncelikli (cache-first)** tasarım
* Yapılandırma değişikliklerini sunucuyu yeniden başlatmadan anında uygulamak için kullanışlı **yenileme (reload)** komutu
* Klasik kırıktaş ve gelişmiş bazalt ile derinrakım türleri de dahil olmak üzere çoklu jeneratör kategorisi desteği
* Gelecekteki genişletmeleri kolaylaştırmak için modüler kod mimarisi ile net sorumluluk ayrımı (separation of concerns)
* Sorunsuz işlem yönetimi için Vault üzerinden ekonomi entegrasyonu
* Dengeli bir oynanış ilerlemesini korumak için BentoBox ada seviyesi kontrolleri

---

## 🔄 v1.1.0 Sürümündeki Yenilikler

### 🧪 Yeni Özellikler

- **`custom-generator-categories.yml` üzerinden Özel Jeneratör Kategorileri:**
  Sıvı akış koşulları, çevreleyen bloklar, biyomlar, Y ekseni (y-level) sınırları ve daha fazlasını kullanarak kendi jeneratör mantığınızı tanımlayın.

- **Geliştirilmiş Jeneratör Menüsü Arayüzü (UI):**
  Görsel iyileştirmeler, daha iyi bir düzen ve daha sezgisel kategori butonları.

- **GUI'de Sayfalandırma (Pagination) Desteği:**
  Menü artık **İleri** / **Geri** sayfa butonları ile gezilebilen sınırsız sayıda jeneratör türünü destekliyor.

---

## 📦 Zorunlu Bağımlılıklar (Hard Dependencies)

| Eklenti | Test Edilen Sürüm | Amacı |
|---------|------------------|-------------------------------------|
| **BentoBox** | 3.0.0+ | Ada verilerini ve dünya ayrımını yönetir |
| **Vault** | 1.7+ | İşlemler için ekonomi API'si sağlar |

> Eklentinin yüklenmesi ve çalışması için her iki bağımlılığın da kurulu ve etkin olması gerekir; aksi takdirde eklenti yüklenmez.

---

## 🚀 Hızlı Başlangıç

1. `CustomGenerator.jar` dosyasını **indirin** ve sunucunuzun `plugins/` dizinine yerleştirin.
2. Varsayılan yapılandırma dosyalarının oluşturulması için sunucuyu bir kez başlatın:
   * `messages.yml` — özelleştirilebilir mesaj metinleri
   * `generator-types.yml` — tüm jeneratör türleri için tanımlamalar
   * `custom-generator-categories.yml` — jeneratör davranışlarını tanımlar
3. YAML dosyalarını sunucunuzun ihtiyaçlarına ve tercihlerinize göre düzenleyin.
4. Özel ayarlarınızı yüklemek için `/generator reload` komutunu kullanın veya sunucuyu yeniden başlatın.
5. Oyuncuları, mevcut komutları ve kullanımı görmek için `/generator help` komutunu kullanmaya teşvik edin.

---

### Komutlar

| Komut | Açıklama |
|---------|-------------|
| `/generator` | Ana menüyü açar ve oyuncuya mevcut jeneratörleri gösterir. |
| `/generator buy <jeneratör>` | Belirtilen jeneratörü satın alır. Oyuncunun yeterli parası olmalıdır. |
| `/generator activate <jeneratör>` | Daha önce satın alınmış bir jeneratörü aktifleştirir. |
| `/generator list` | Sunucuda tanımlanmış tüm jeneratörleri listeler. |
| `/generator reload` | Tüm yapılandırma dosyalarını yeniden yükler. Yönetici (Admin) yetkisi gerektirir. |

## ⚙️ Temel Yapılandırma

### Jeneratör Türlerini Tanımlamak
Jeneratör türleri `generator-types.yml` dosyası içinde tanımlanır. Yeni türler ekleyebilir veya mevcut olanları değiştirebilirsiniz. Her bir girdi, jeneratörün nasıl davranacağını ve GUI'de nasıl görüneceğini belirler. İşte bir örnek:

'''yaml
generator-types:
  diamond:
    display-name: "&bElmas Jeneratörü"
    material: DIAMOND_ORE
    lore:
      - "&bNadir ve değerli kaynaklar içerir."
      - "&7%30 elmas ve %70 taş blokları üretir."
    generator-type: COBBLESTONE
    price: 5000
    required-island-level: 30
    blocks:
      STONE: 70
      DIAMOND_ORE: 30
'''

### Önemli notlar:

* `generator-type`, yerleşik kategorilerden birisi (COBBLESTONE, STONE, BASALT, DEEPSLATE) veya `custom-generator-categories.yml` dosyasında tanımlanan özel bir kategori olmalıdır.
* `blocks:` altındaki değerler göreceli ağırlık (relative weight) olarak işlev görür. Eklenti bunları kendi içinde normalleştirir, bu nedenle 70/30, 0.7/0.3 veya 7/3 kullanmanız fark etmez; davranış tutarlı olacaktır.
* Ekonomi eklentiniz izin veriyorsa `price` (fiyat) ondalık değerleri destekler.
* `material` (materyal), GUI ikonları için geçerli bir [Bukkit Materyali (Material)](https://hub.spigotmc.org/javadocs/bukkit/org/bukkit/Material.html) olmalıdır.
* `lore` (açıklama), jeneratörü tanımlamak için çoklu satırları ve renk kodlarını destekler.

### Özel Jeneratör Oluşturmak

Özel jeneratörler `custom-generator-categories.yml` dosyasında tanımlanır. Örnek:


```yaml
dirt_generator:
  category: DIRTGEN
  display-name: "&2Toprak"
  fluid: LAVA
  to: AIR

  conditions:
    sides: [ DIRT ]
    up: [ STONE ]
    down: [ COARSE_DIRT ]

  y-level:
    min: 10
    max: 64

  biomes:
    - minecraft:plains
    - minecraft:the_void
```

### Açıklama:
* **category**: Benzersiz kategori kimliği (ID). `generator-types.yml` dosyasındaki bir `generator-type` girdisi ile eşleşmelidir.
* **fluid**: Tetikleyici sıvı bloğu (örn. LAVA, WATER).
* **to**: Sıvının aktığı blok (AIR, WATER, POWDER_SNOW vb.).
* **conditions**: İsteğe bağlı blok gereksinimleri (sides [yanlar], up [üst], down [alt]).
* **y-level**: Jeneratörün aktif olması için isteğe bağlı Y ekseni aralığı.
* **biomes**: Jeneratörün çalışabileceği yerler için isteğe bağlı biyom beyaz listesi (whitelist).

**Bu sistemle şunları uygulayabilirsiniz:**

* Sadece Nether (Cehennem) ile sınırlandırılmış bazalt jeneratörleri.
* Y=100 seviyesinin üzerindeki altın jeneratörleri.
* Çevresinde belirli blokların bulunmasını gerektiren toprak jeneratörleri.
* Biyomlara özel jeneratörler (örneğin sadece Mantar Adalarında çalışanlar).
