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

    // Animaciones al hacer scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    // Observar elementos para animaciones
    const animatedElements = document.querySelectorAll('.card, .alert, .btn-lg');
    animatedElements.forEach(el => observer.observe(el));

    // Auto-hide alerts después de 5 segundos
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
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

    // Loading state for buttons
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            if (form && form.checkValidity()) {
                this.disabled = true;
                this.innerHTML = '<span class="loading"></span> Enviando...';
            }
        });
    });

    // Match form enhancements
    const matchForm = document.querySelector('#match-form');
    if (matchForm) {
        const selects = matchForm.querySelectorAll('select');
        selects.forEach(select => {
            select.addEventListener('change', function() {
                // Auto-submit cuando se cambia cualquier filtro
                setTimeout(() => {
                    matchForm.submit();
                }, 500);
            });
        });
    }

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
