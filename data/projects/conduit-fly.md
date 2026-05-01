# ConduitFly

**ConduitFly**, BentoBox tabanlı skyblock sunucuları için tasarlanmış bir Minecraft eklentisidir. Oyuncuların, yapılandırılabilir bir yarıçap içinde **geçici uçuş (flight)** sağlamak amacıyla adalarına özelleştirilebilir **Conduit (Boru/Kanal) blokları** yerleştirmelerine olanak tanır. Uçuş süresi, uçuş alanı ve düşme hasarı koruması tamamen oyuncunun **rütbesine (rank)** göre özelleştirilebilir.

---

## ✨ Özellikler

- 🔗 **BentoBox entegrasyonu**: Uçuş adaya özel olarak yönetilir
- 🌀 Menzil içinde uçuş sağlamak için **yerleştirilebilir Conduit blokları**
- 💸 **Rütbe (Rank) sistemi**: Oyuncular Vault ekonomisi ile rütbelerini yükseltebilir
- 🎯 **Görsel parçacık (particle) alan göstergesi**
- 🔧 **YAML** üzerinden tamamen yapılandırılabilir
- 💾 Hem **SQLite** hem de **MySQL** desteği
- 🔄 Değişiklikleri anında uygulamak (hot-reload) için `/conduitfly reload` komutu
- 🖱️ Rütbe etkileşimleri için sayfalandırılmış **GUI menüleri**

---

## 🔧 Bağımlılıklar

| Bağımlılık | Amacı |
|--------------|-------------------------------------------|
| BentoBox | Ada veri erişimi (depolama mantığı nedeniyle şu an için zorunlu; gelecekteki sürümlerde isteğe bağlı bağımlılık (soft-depend) olabilir) |
| Vault | Ekonomi entegrasyonu |
| Ekonomi Eklentisi | (EssentialsX, CMI vb.) |

> Eklenti, zorunlu bağımlılıklar eksikse yüklenmeyecektir.

---

## 💻 Kurulum

1. `ConduitFly.jar` dosyasını `plugins/` dizininize bırakın.
2. Sunucuyu başlatın. Aşağıdaki dosyalar oluşturulacaktır:
   - `config.yml`
3. Ayarları ihtiyaçlarınıza göre düzenleyin.
4. Değişiklikleri sunucuyu yeniden başlatmadan uygulamak için `/conduitfly reload` komutunu kullanın.

---

## 🏆 Rütbe Sistemi

Oyuncular, rütbelerini görmek ve yükseltmek için `/conduitfly rankup` komutuyla bir arayüz (GUI) açabilirler. Her rütbe şunları belirler:

- ✈️ **Uçuş süresi** (saniye cinsinden)
- 🌀 **Conduit yarıçapı**
- 🛡️ İsteğe bağlı **düşme hasarı koruması**
- 💰 **Yükseltme bedeli**

---

## 🛠️ Komutlar

| Komut | Açıklama |
|-----------------------|---------------------------------------------------|
| `/conduitfly reload` | Yapılandırmayı (config) yeniden yükler |
| `/conduitfly rankup` | Rütbeleri görmek/yükseltmek için arayüzü açar |
| `/conduitfly area` | Conduit'in aktif menzilini görsel olarak gösterir |

---

## 🧩 Destek ve Katkı

Bir hata mı buldunuz, yeni bir özellik mi istiyorsunuz veya sadece katkıda bulunmak mı istiyorsunuz?

📬 [GitHub'da bir issue açın veya pull request gönderin](https://github.com/ogsammaenr/ConduitFly/issues)

Tüm geri bildirimleri ve katkıları memnuniyetle karşılıyoruz!

## 📁 Yapılandırmaya (Config) Genel Bakış

- `conduit.material`: Hangi bloğun uçuş sağlayacağı (varsayılan: `CONDUIT`)
- `ranks`: Her rütbenin özelliklerini belirler
- `particles`: Conduit alanı içinde gösterilen görsel efekt
- `storage`: `sqlite` veya `mysql` arasında seçim yapın
- `rank-gui`: GUI düzenini ve ikonlarını özelleştirir

Tam dokümantasyon için `config.yml` dosyasına göz atın.

---

## ⚙️ Depolama (Storage) Seçenekleri

| Tür | Açıklama |
|---------|----------------------------------------------|
| SQLite | Varsayılan. Hafif ve kullanımı kolay |
| MySQL | Harici veya büyük ölçekli sunucu ağları için |

---

## 📜 Lisans

Bu proje **MIT Lisansı** altında lisanslanmıştır.  
Orijinal lisans ve telif hakkı bildiriminin dahil edilmesi şartıyla eklentiyi kullanmakta, değiştirmekte ve dağıtmakta özgürsünüz.

---
