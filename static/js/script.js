/**
 * Credit Card Approval Prediction - UI Interactivity & Particle Background
 */

// ===========================
// Particle Background Animation
// ===========================
(function initParticles() {
    const canvas = document.getElementById('particle-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let particles = [];
    let animFrameId = null;

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    // Color palettes: [main_color, glow_color]
    const COLORS = [
        { main: [255, 215, 0], glow: [255, 180, 50] },     // Gold
        { main: [100, 180, 255], glow: [50, 100, 255] },    // Blue
        { main: [60, 60, 85], glow: [90, 90, 110] }         // Charcoal/black
    ];

    class Particle {
        constructor() {
            this.colorSet = COLORS[Math.floor(Math.random() * COLORS.length)];
            this.reset();
        }

        reset() {
            this.x = Math.random() * canvas.width;
            this.y = canvas.height + Math.random() * 100;
            this.size = Math.random() * 3 + 0.8;
            this.speedY = -(Math.random() * 0.8 + 0.2);
            this.speedX = (Math.random() - 0.5) * 0.4;
            this.opacity = Math.random() * 0.6 + 0.2;
            this.pulseSpeed = Math.random() * 0.02 + 0.005;
            this.pulsePhase = Math.random() * Math.PI * 2;
            this.colorSet = COLORS[Math.floor(Math.random() * COLORS.length)];
        }

        update() {
            this.y += this.speedY;
            this.x += this.speedX;

            this.currentOpacity = this.opacity * (0.7 + 0.3 * Math.sin(this.pulsePhase));
            this.pulsePhase += this.pulseSpeed;

            if (this.y < -10) {
                this.reset();
                this.y = canvas.height + 10;
            }
            if (this.x < -10) this.x = canvas.width + 10;
            if (this.x > canvas.width + 10) this.x = -10;
        }

        draw() {
            const [mr, mg, mb] = this.colorSet.main;
            const [gr, gg, gb] = this.colorSet.glow;

            // Main particle
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${mr}, ${mg}, ${mb}, ${this.currentOpacity})`;
            ctx.fill();

            // Glow
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 3, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${gr}, ${gg}, ${gb}, ${this.currentOpacity * 0.1})`;
            ctx.fill();

            // Extra small bright core
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 0.4, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${this.currentOpacity * 0.5})`;
            ctx.fill();
        }
    }

    function initParticleSystem() {
        resizeCanvas();
        const count = Math.min(Math.floor(canvas.width * canvas.height / 6000), 250);
        particles = [];
        for (let i = 0; i < count; i++) {
            const p = new Particle();
            p.y = Math.random() * canvas.height;
            particles.push(p);
        }
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => {
            p.update();
            p.draw();
        });
        animFrameId = requestAnimationFrame(animate);
    }

    // Handle resize
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            resizeCanvas();
        }, 200);
    });

    initParticleSystem();
    animate();
})();

// ===========================
// Tab Switching
// ===========================
document.addEventListener('DOMContentLoaded', function() {
    window.switchTab = function(tabName) {
        const tabs = document.querySelectorAll('.tab-content');
        tabs.forEach(tab => tab.classList.remove('active'));

        const buttons = document.querySelectorAll('.tab-btn');
        buttons.forEach(btn => btn.classList.remove('active'));

        const selectedTab = document.getElementById('tab-' + tabName);
        if (selectedTab) {
            selectedTab.classList.add('active');
        }

        const activeBtn = document.querySelector(`.tab-btn[onclick*="${tabName}"]`);
        if (activeBtn) {
            activeBtn.classList.add('active');
        }

        if (selectedTab) {
            selectedTab.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    };

    // Form validation
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = 'Processing...';
            }
        });
    }

    // Animate progress bar on result display
    const progressFill = document.querySelector('.progress-fill');
    if (progressFill) {
        setTimeout(() => {
            progressFill.style.transition = 'width 1.5s ease-in-out';
        }, 100);
    }

    // Screenshot hover effects
    const screenshotItems = document.querySelectorAll('.screenshot-item');
    screenshotItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            const img = this.querySelector('img');
            if (img) img.style.transform = 'scale(1.05)';
        });
        item.addEventListener('mouseleave', function() {
            const img = this.querySelector('img');
            if (img) img.style.transform = 'scale(1)';
        });
    });

    console.log('Credit Card Approval UI initialized successfully!');
});
