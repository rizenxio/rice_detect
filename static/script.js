// Membuat tombol navigasi responsif
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');

navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
});

// Membuat efek scrolling pada tombol "Periksa Komoditas Untuk Lahan Kamu"
const btn = document.querySelector('.btn');
const heroSection = document.querySelector('.hero');

btn.addEventListener('click', () => {
    heroSection.scrollIntoView({ behavior: 'smooth' });
});

// Membuat efek animasi pada teks hero
const heroText = document.querySelector('.hero-content h2');
const heroTextArray = heroText.textContent.split('');

heroText.textContent = '';

heroTextArray.forEach((char, index) => {
    const span = document.createElement('span');
    span.textContent = char;
    heroText.appendChild(span);
    span.style.animationDelay = `${index * 0.1}s`;
});

// Membuat efek animasi pada gambar hero
const heroImage = document.querySelector('.hero-image img');
heroImage.style.opacity = 0;

window.addEventListener('load', () => {
    heroImage.style.opacity = 1;
    heroImage.style.transform = 'scale(1)';
});