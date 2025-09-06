// Modern Website JavaScript Animations and Interactions

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all animations and interactions
    initAnimations();
    initScrollEffects();
    initFormInteractions();
    initParticleEffect();
});

// Initialize entrance animations
function initAnimations() {
    // Stagger animation for form groups
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach((group, index) => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        setTimeout(() => {
            group.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            group.style.opacity = '1';
            group.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Animate section headers
    const sectionHeaders = document.querySelectorAll('.card h4');
    sectionHeaders.forEach((header, index) => {
        header.style.opacity = '0';
        header.style.transform = 'translateX(-20px)';
        setTimeout(() => {
            header.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
            header.style.opacity = '1';
            header.style.transform = 'translateX(0)';
        }, 500 + index * 200);
    });
}

// Initialize scroll effects
function initScrollEffects() {
    // Parallax effect for background
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const background = document.body;

        if (background.style.backgroundPosition) {
            background.style.backgroundPosition = `0% ${scrolled * 0.5}px`;
        }
    });

    // Fade in elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe cards for scroll animations
    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });
}

// Initialize form interactions
function initFormInteractions() {
    // Enhanced input focus effects
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });

        // Check if input has value on load
        if (input.value) {
            input.parentElement.classList.add('focused');
        }
    });

    // Password toggle functionality
    const passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);

            // Animate toggle icon
            this.style.transform = 'translateY(-50%) scale(1.2)';
            setTimeout(() => {
                this.style.transform = 'translateY(-50%) scale(1)';
            }, 200);
        });
    });

    // Button ripple effect
    const buttons = document.querySelectorAll('.btn, .apply-btn, .admin-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple-effect');

            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// Initialize particle effect
function initParticleEffect() {
    // Create floating particles
    const particleContainer = document.createElement('div');
    particleContainer.className = 'particle-container';
    document.body.appendChild(particleContainer);

    for (let i = 0; i < 50; i++) {
        createParticle(particleContainer);
    }
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';

    // Random properties
    const size = Math.random() * 6 + 2;
    const left = Math.random() * 100;
    const animationDelay = Math.random() * 20;
    const animationDuration = Math.random() * 10 + 10;

    particle.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        left: ${left}%;
        bottom: -10px;
        animation: float ${animationDuration}s linear infinite;
        animation-delay: ${animationDelay}s;
        pointer-events: none;
    `;

    container.appendChild(particle);

    // Remove particle after animation
    setTimeout(() => {
        particle.remove();
    }, (animationDuration + animationDelay) * 1000);
}

// Add CSS for additional animations
const additionalCSS = `
<style>
@keyframes float {
    to {
        transform: translateY(-100vh);
        opacity: 0;
    }
}

.animate-in {
    animation: slideInUp 0.8s ease-out forwards;
}

.ripple-effect {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: scale(0);
    animation: ripple 0.6s linear;
    pointer-events: none;
}

@keyframes ripple {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

.form-group.focused label {
    color: var(--primary-color);
    transform: translateY(-2px);
}

.form-group.focused input,
.form-group.focused select {
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
}

.particle-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
}

/* Loading states */
.btn.loading {
    pointer-events: none;
    position: relative;
}

.btn.loading::after {
    content: '';
    position: absolute;
    width: 20px;
    height: 20px;
    margin: auto;
    border: 2px solid transparent;
    border-top-color: white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

/* Hover effects for cards */
.card:hover .card h4::after {
    width: 100px;
    transition: width 0.3s ease;
}

/* Smooth transitions for all elements */
* {
    transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
}

/* Enhanced focus states */
input:focus, select:focus, button:focus {
    outline: 2px solid var(--primary-color);
    outline-offset: 2px;
}

/* Success animation */
.success-animation {
    animation: successPulse 0.6s ease-in-out;
}

@keyframes successPulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}
</style>
`;

// Inject additional CSS
document.head.insertAdjacentHTML('beforeend', additionalCSS);

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add loading state to forms
function addLoadingState(button) {
    button.classList.add('loading');
    button.disabled = true;
    button.innerHTML = '<span class="loading"></span> Processing...';
}

// Remove loading state
function removeLoadingState(button, originalText) {
    button.classList.remove('loading');
    button.disabled = false;
    button.innerHTML = originalText;
}

// Enhanced form submission
document.addEventListener('submit', function(e) {
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"], .btn');

    if (submitBtn) {
        const originalText = submitBtn.innerHTML;
        addLoadingState(submitBtn);

        // Simulate processing (remove this in production)
        setTimeout(() => {
            removeLoadingState(submitBtn, originalText);
        }, 2000);
    }
});

// Add success animation to successful actions
function showSuccessAnimation(element) {
    element.classList.add('success-animation');
    setTimeout(() => {
        element.classList.remove('success-animation');
    }, 600);
}

// Export functions for global use
window.WebsiteUtils = {
    addLoadingState,
    removeLoadingState,
    showSuccessAnimation,
    debounce
};
