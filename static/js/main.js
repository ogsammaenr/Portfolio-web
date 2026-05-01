document.addEventListener('DOMContentLoaded', () => {
    // --- Parallax Yıldız (Box-Shadow) Üretici ---
    // CSS dosyasını şişirmemek (bloat-free) için yıldızları dinamik üretiyoruz.
    const generateStars = (count) => {
        let shadows = [];
        for(let i = 0; i < count; i++) {
            // 2000px x 2000px bir alan içine rastgele yıldızlar dağıt
            shadows.push(`${Math.floor(Math.random() * 2000)}px ${Math.floor(Math.random() * 2000)}px #FFF`);
        }
        return shadows.join(', ');
    };

    // Her katman için farklı sayıda yıldız üret ve CSS değişkenlerine ata
    const starsContainer = document.getElementById('stars-container');
    if(starsContainer) {
        starsContainer.style.setProperty('--shadows-small', generateStars(700));
        starsContainer.style.setProperty('--shadows-medium', generateStars(200));
        starsContainer.style.setProperty('--shadows-big', generateStars(100));
    }

    // --- FARE PARALLAX EFEKTİ (MOUSE TRACKING) ---
    const heroBg = document.querySelector('.hero-bg-layer');
    
    if (heroBg) {
        let targetX = 0, targetY = 0;   // Farenin gitmek istediği hedef
        let currentX = 0, currentY = 0; // Arka planın şu anki konumu
        const friction = 0.04;          // Kayma yumuşaklığı (Düşük = Daha akışkan/tembel)

        // Tarayıcının render döngüsüyle uyumlu 60 FPS animasyon motoru
        const animateParallax = () => {
            // Hedef ile mevcut konum arasındaki farkı sürtünme ile yumuşat
            currentX += (targetX - currentX) * friction;
            currentY += (targetY - currentY) * friction;
            
            // Hem parallax hareketini yap hem de kenar yırtılmasını önleyen scale'i koru
            heroBg.style.transform = `translate(${currentX}px, ${currentY}px) scale(1.05)`;
            
            requestAnimationFrame(animateParallax);
        };

        // Fare hareketini dinle
        document.addEventListener('mousemove', (e) => {
            // Ekranın neresinde olduğuna göre -1 ile 1 arası bir oran bul ve max kayma pikseli ile çarp
            const moveX = (e.clientX / window.innerWidth - 0.5) * -120; // Max 20px sağa/sola
            const moveY = (e.clientY / window.innerHeight - 0.5) * -120; // Max 20px yukarı/aşağı
            
            targetX = moveX;
            targetY = moveY;
        });

        // Motoru çalıştır
        animateParallax();
    }
    
    // --- Reveal Animasyonu (Aşağı Kaydırma Efektleri İçin Aynı Kalıyor) ---
    const modernCards = document.querySelectorAll('.modern-card:not(.carousel-card-3d), .section-title');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target); 
            }
        });
    }, { threshold: 0.1 });

    modernCards.forEach(card => {
        card.classList.add('reveal');
        observer.observe(card);
    });

    // --- Yeni Odaklı (Center-Focused) Karusel Mantığı ---
    const cards = document.querySelectorAll('.carousel-card-3d');
    const container = document.querySelector('.carousel-container');
    
    // Yeterli kart varsa karuseli başlat
    if (cards.length > 0) {
        let currentIndex = 0;
        let isPaused = false;
        let carouselInterval;

        function updateCarousel() {
            // Önce tüm eski durumları temizle
            cards.forEach(card => {
                card.classList.remove('center', 'left', 'right');
            });

            const total = cards.length;
            
            // Sonsuz döngü için modulo (%) matematiği kullanıyoruz
            const leftIndex = (currentIndex - 1 + total) % total;
            const rightIndex = (currentIndex + 1) % total;

            // Sınıfları ilgili kartlara dağıt
            cards[currentIndex].classList.add('center');
            
            // En az 3 kart varsa sağı ve solu göster (Eğer 2 kart varsa tasarım bozulmasın diye)
            if (total >= 3) {
                cards[leftIndex].classList.add('left');
                cards[rightIndex].classList.add('right');
            } else if (total === 2) {
                cards[rightIndex].classList.add('right');
            }
        }

        function nextSlide() {
            if (!isPaused) {
                currentIndex = (currentIndex + 1) % cards.length;
                updateCarousel();
            }
        }

        // Başlangıçta kartları yerleştir
        updateCarousel();

        // Fare üzerine gelince otomatik kaymayı durdur
        container.addEventListener('mouseenter', () => isPaused = true);
        container.addEventListener('mouseleave', () => isPaused = false);

        // 3.5 saniyede bir kartları kaydır
        carouselInterval = setInterval(nextSlide, 3500);
    }


    // --- FORM GENİŞLETME (ACCORDION) VE OTOMATİK KAYDIRMA ---
    const toggleBtn = document.getElementById('toggle-form-btn');
    const formWrapper = document.getElementById('expandable-form-wrapper');

    if (toggleBtn && formWrapper) {
        toggleBtn.addEventListener('click', () => {
            // Sınıfları ekle/çıkar ve durumu (açık/kapalı) bir değişkene ata
            const isOpen = formWrapper.classList.toggle('is-open');
            toggleBtn.classList.toggle('is-active');

            // İŞTE SİHİR BURADA: Form açılıyorsa sayfayı aşağı kaydır
            if (isOpen) {
                // CSS genişleme animasyonu (0.5s) ile senkronize olması için küçük bir gecikme ekliyoruz
                setTimeout(() => {
                    formWrapper.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'nearest' // Sadece görünmeyen kısmı ekrana sokacak kadar kaydırır
                    });
                }, 350); // Animasyonun ortasında (250ms) kaymayı başlatır, çok akıcı hissettirir
            }
        });
    };


    //=============================================
    

    // --- PROJE MODAL (POPUP) MOTORU ---
    const modal = document.getElementById('project-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');
    const modalClose = document.getElementById('modal-close');
    const modalBackdrop = document.getElementById('modal-backdrop');
    const modalGithubWrapper = document.getElementById('modal-github-wrapper');
    const modalGithubLink = document.getElementById('modal-github-link');

    // /project/ ile başlayan tüm linkleri bul
    const projectLinks = document.querySelectorAll('a[href^="/project/"]');

    const openModal = () => {
        modal.classList.add('is-active');
        document.body.style.overflow = 'hidden'; // Ana sayfanın arkada kaymasını engelle
    };

    const closeModal = () => {
        modal.classList.remove('is-active');
        document.body.style.overflow = ''; 
        
        // Modal kapanırken içeriği sıfırla ki bir sonraki açılışta eski proje görünmesin
        setTimeout(() => {
            modalTitle.textContent = 'Bağlantı Kuruluyor...';
            modalBody.innerHTML = '<div class="terminal-loader">Arşiv verileri çekiliyor..._</div>';
            modalGithubWrapper.style.display = 'none';
        }, 300);
    };

    // Kapatma Eventleri (Butona basınca, boşluğa tıklayınca veya ESC tuşuna basınca)
    if(modalClose) modalClose.addEventListener('click', closeModal);
    if(modalBackdrop) modalBackdrop.addEventListener('click', closeModal);
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('is-active')) closeModal();
    });

    // Proje Tıklama Motoru
    projectLinks.forEach(link => {
        link.addEventListener('click', async (e) => {
            e.preventDefault(); // Sayfanın değişmesini engelle!
            openModal();

            // Linkten slug'ı çıkar (Örn: /project/arch-setup -> arch-setup)
            const slug = link.getAttribute('href').split('/').pop();

            try {
                // Arka planda Python API'mıza istek at
                const response = await fetch(`/api/project/${slug}`);
                if (!response.ok) throw new Error('Ağ hatası');
                
                const data = await response.json();
                
                // Verileri Modal içine yerleştir
                modalTitle.textContent = data.name;
                modalBody.innerHTML = data.content;
                
                if (data.github) {
                    modalGithubLink.href = data.github;
                    modalGithubWrapper.style.display = 'block';
                }

            } catch (error) {
                modalBody.innerHTML = '<p style="color: #ef4444;">Sistem Hatası: Arşiv verisi çekilemedi. Veri tabanı bağlantısını kontrol edin.</p>';
            }
        });
    });

})
