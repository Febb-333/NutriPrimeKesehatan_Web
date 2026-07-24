// NutriPrimeKesehatan - main.js
// Interaksi ringan sisi client, tanpa library/framework tambahan.

document.addEventListener('DOMContentLoaded', function () {
  const navbar = document.querySelector('.navbar-nutriprime');

  // Tambahkan shadow pada navbar saat halaman di-scroll ke bawah
  function handleNavbarShadow() {
    if (!navbar) return;
    if (window.scrollY > 12) {
      navbar.classList.add('shadow-sm');
    } else {
      navbar.classList.remove('shadow-sm');
    }
  }
  handleNavbarShadow();
  window.addEventListener('scroll', handleNavbarShadow);

  // Smooth scroll untuk link anchor (#) di dalam landing page
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId.length > 1) {
        const target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    });
  });
});
