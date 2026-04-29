document.addEventListener('DOMContentLoaded', () => {
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
});
