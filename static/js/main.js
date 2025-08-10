// JavaScript personalizado para Protectora Adán

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling para enlaces internos
    const scrollLinks = document.querySelectorAll('a[href^="#"]');
    scrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });


    // Auto-hide Bootstrap alerts después de 5 segundos (excepto las del carrusel y los mensajes de Django)
    const bootstrapAlerts = document.querySelectorAll('.alert:not(.alert-permanent):not(#carouselAvisos .alert):not([data-auto-hide])');
    bootstrapAlerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 500);
            }
        }, 5000);
    });

    // Inicializar carrusel de avisos - SIEMPRE VISIBLE
    const avisoCarousel = document.querySelector('#carouselAvisos');
    if (avisoCarousel) {
        // Asegurar que el carrusel SIEMPRE esté visible
        avisoCarousel.style.display = 'block !important';
        avisoCarousel.style.visibility = 'visible !important';
        avisoCarousel.style.opacity = '1 !important';
        
        // Remover todos los botones de cerrar del carrusel
        const closeButtons = avisoCarousel.querySelectorAll('.btn-close, [data-bs-dismiss="alert"]');
        closeButtons.forEach(btn => btn.remove());
        
        // Asegurar que todas las alertas del carrusel sean permanentes
        const carouselAlerts = avisoCarousel.querySelectorAll('.alert');
        carouselAlerts.forEach(alert => {
            alert.classList.remove('alert-dismissible');
            alert.classList.add('show');
            alert.style.display = 'block !important';
            alert.style.opacity = '1 !important';
            
            // Prevenir cualquier evento de cierre
            alert.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        });
        
        // Inicializar Bootstrap carousel con configuración mejorada
        const carousel = new bootstrap.Carousel(avisoCarousel, {
            interval: 6000,  // 6 segundos entre slides
            wrap: true,
            pause: 'hover',
            touch: true,
            keyboard: true
        });

        // Controles táctiles para móvil
        let startX = 0;
        let endX = 0;
        
        avisoCarousel.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;
        });
        
        avisoCarousel.addEventListener('touchend', function(e) {
            endX = e.changedTouches[0].clientX;
            const threshold = 50;
            
            if (startX - endX > threshold) {
                carousel.next();
            } else if (endX - startX > threshold) {
                carousel.prev();
            }
        });

        // Pausar solo en desktop al hacer hover
        if (window.innerWidth > 768) {
            avisoCarousel.addEventListener('mouseenter', function() {
                carousel.pause();
            });

            avisoCarousel.addEventListener('mouseleave', function() {
                carousel.cycle();
            });
        }
        
        // Asegurar que el carrusel no se pueda ocultar por JavaScript
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'attributes' && 
                    (mutation.attributeName === 'style' || mutation.attributeName === 'class')) {
                    if (avisoCarousel.style.display === 'none' || 
                        avisoCarousel.style.visibility === 'hidden' ||
                        avisoCarousel.style.opacity === '0') {
                        avisoCarousel.style.display = 'block';
                        avisoCarousel.style.visibility = 'visible';
                        avisoCarousel.style.opacity = '1';
                    }
                }
            });
        });
        
        observer.observe(avisoCarousel, {
            attributes: true,
            attributeFilter: ['style', 'class']
        });
    }

    // Form validation feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Loading state for buttons (exclude filter forms and donation forms)
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            // Skip filter forms - they should submit immediately
            if (form && form.action && form.action.includes('adopciones')) {
                return; // Don't interfere with adoption filter forms
            }
            // Skip donation forms - they need to redirect to WebPay
            if (form && form.action && form.action.includes('donaciones')) {
                return; // Don't interfere with donation forms
            }
            if (form && form.checkValidity()) {
                this.disabled = true;
                this.innerHTML = '<span class="loading"></span> Enviando...';
            }
        });
    });

    // Image lazy loading fallback
    const images = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for older browsers
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }

    // Social sharing buttons
    const shareButtons = document.querySelectorAll('.share-btn');
    shareButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.dataset.url || window.location.href;
            const text = this.dataset.text || document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: text,
                    url: url
                });
            } else {
                // Fallback: copy to clipboard
                navigator.clipboard.writeText(url).then(() => {
                    alert('¡Enlace copiado al portapapeles!');
                });
            }
        });
    });

    // WhatsApp contact button
    const whatsappButton = document.querySelector('#whatsapp-contact');
    if (whatsappButton) {
        whatsappButton.addEventListener('click', function() {
            const phone = this.dataset.phone;
            const message = this.dataset.message || 'Hola, me interesa obtener más información sobre la Protectora Adán.';
            const url = `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
            window.open(url, '_blank');
        });
    }

    // Donation amount quick select
    const donationAmounts = document.querySelectorAll('.donation-amount');
    const amountInput = document.querySelector('#id_cantidad');
    
    donationAmounts.forEach(amount => {
        amount.addEventListener('click', function() {
            const value = this.dataset.amount;
            if (amountInput) {
                amountInput.value = value;
                donationAmounts.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });

    // Card flip animation for dog details
    const dogCards = document.querySelectorAll('.dog-card');
    dogCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'rotateY(5deg) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'rotateY(0deg) scale(1)';
        });
    });

    // Search functionality
    const searchInput = document.querySelector('#search-dogs');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const dogCards = document.querySelectorAll('.dog-card');
            
            dogCards.forEach(card => {
                const dogName = card.querySelector('.dog-name').textContent.toLowerCase();
                const dogDescription = card.querySelector('.dog-description').textContent.toLowerCase();
                
                if (dogName.includes(searchTerm) || dogDescription.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
});

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

// Export for use in other scripts
window.ProtectoraAdan = {
    showNotification,
    formatCurrency
};




// Animaciones para formularios
const initFormAnimations = () => {
    const formInputs = document.querySelectorAll('input, textarea, select');
    
    formInputs.forEach(input => {
        // Animación al enfocar
        input.addEventListener('focus', function() {
            this.parentNode.classList.add('focused');
        });
        
        // Animación al desenfocar
        input.addEventListener('blur', function() {
            this.parentNode.classList.remove('focused');
            if (this.value) {
                this.parentNode.classList.add('filled');
            } else {
                this.parentNode.classList.remove('filled');
            }
        });
        
        // Estado inicial para campos con valor
        if (input.value) {
            input.parentNode.classList.add('filled');
        }
    });
    
    // Animación para botones de submit
    const submitButtons = document.querySelectorAll('button[type="submit"], input[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (!this.disabled) {
                this.classList.add('btn-loading');
                
                // Remover la animación después de 2 segundos
                setTimeout(() => {
                    this.classList.remove('btn-loading');
                }, 2000);
            }
        });
    });
};

// Animaciones para elementos de navegación
const initNavAnimations = () => {
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        // Efecto de hover mejorado
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Efecto de scroll en la navbar
    let lastScrollTop = 0;
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
};

// Animaciones para cards
const initCardAnimations = () => {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        // Efecto de hover con rotación sutil
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) rotateX(5deg)';
            this.style.transformStyle = 'preserve-3d';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) rotateX(0deg)';
        });
    });
};

// Inicializar animaciones cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        initFormAnimations();
        initNavAnimations();
        initCardAnimations();
    }, 100);
});

// Re-inicializar animaciones cuando se carga contenido dinámico
const reinitAnimations = () => {
    initFormAnimations();
    initCardAnimations();
};

// Exportar función para uso externo
window.ProtectoraAdan.reinitAnimations = reinitAnimations;
