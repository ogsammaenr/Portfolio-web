# XanthCommands

**XanthCommands**, Paper sunucuları için geliştirilmiş modüler ve özelleştirilebilir bir Minecraft eklentisidir. Oyunculara kullanışlı araç komutları, bekleme süresine (cooldown) dayalı yetkiler ve özel büyü masası konumlarıyla entegrasyon sunar.

## Özellikler

- `/fly`: Oyuncu için uçuş modunu açar veya kapatır.
- `/repairhand`: Oyuncunun ana elindeki eşyayı tamir eder (bekleme süresi ve yetki seviyeleri ile).
- `/repairall`: Oyuncunun envanterindeki hasarlı tüm eşyaları tamir eder (bekleme süresi ve yetki seviyeleri ile).
- `/enchant`: Dünyalara özel konumlara dayalı, yapılandırılabilir bir büyü masası sistemine erişim sağlar.
- `/craft`: Sanal bir çalışma masası (crafting table) açar.
- `/anvil`: Sanal bir örs (anvil) açar.
- `/xanthcommands reload`: Eklenti yapılandırmasını (config) yeniden yükler.
- `/xanthcommands version`: Mevcut eklenti sürümünü gösterir.
- `/xanthcommands setenchantingtable`: Oyuncunun bulunduğu konumu, o anki dünya için büyü masası konumu olarak kaydeder.
- SQLite tabanlı kalıcı bekleme süresi (cooldown) sistemi.
- Yapılandırılabilir bekleme sürelerine sahip çoklu yetki (permission) seviyeleri.
- Dünya başına (per-world) büyü masası desteği.

## Yapılandırma (Config) Örneği

'''yaml
cooldowns:
  repairhand:
    level1:
      permission: "xanthcommands.cooldown.repairhand1"
      duration: 60
    level2:
      permission: "xanthcommands.cooldown.repairhand2"
      duration: 180
    level3:
      permission: "xanthcommands.cooldown.repairhand3"
      duration: 360
'''
