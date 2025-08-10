// Confetti simple para donaciones exitosas
// https://www.kirilv.com/canvas-confetti/ (CDN)

function lanzarConfeti() {
    if (window.confetti) {
        window.confetti({
            particleCount: 150,
            spread: 70,
            origin: { y: 0.6 }
        });
    }
}

// Detectar si estamos en la página de gracias y si la donación fue exitosa
if (document.body && document.body.dataset.graciasDonacion === 'completada') {
    // Esperar a que todo cargue
    window.addEventListener('DOMContentLoaded', function() {
        setTimeout(lanzarConfeti, 600); // Pequeño delay para mejor UX
    });
}
