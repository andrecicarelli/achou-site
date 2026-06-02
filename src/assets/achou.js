window.addEventListener('DOMContentLoaded', () => {
  if (window.posthog) {
    posthog.init('phc_osQVVbRsX4P2BRKu4UD5ixb7BkNZX3QNphXriR3d8NDT', {
      api_host: 'https://us.i.posthog.com',
      defaults: '2026-05-30',
      person_profiles: 'identified_only',
    });
  }
});

const nav = document.getElementById('site-nav');
window.addEventListener('scroll', () => {
  nav.classList.toggle('nav--scrolled', window.scrollY > 80);
}, { passive: true });

const hamburger = document.getElementById('nav-hamburger');
const drawer    = document.getElementById('nav-drawer');

function closeDrawer() {
  drawer.classList.remove('nav-drawer--open');
  hamburger.classList.remove('nav-hamburger--open');
  nav.classList.remove('drawer-open');
  hamburger.setAttribute('aria-expanded', 'false');
  drawer.setAttribute('aria-hidden', 'true');
}

hamburger.addEventListener('click', () => {
  const open = drawer.classList.toggle('nav-drawer--open');
  hamburger.classList.toggle('nav-hamburger--open', open);
  nav.classList.toggle('drawer-open', open);
  hamburger.setAttribute('aria-expanded', String(open));
  drawer.setAttribute('aria-hidden', String(!open));
});

drawer.querySelectorAll('a').forEach(a => a.addEventListener('click', closeDrawer));

const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

document.querySelectorAll('.faq-question').forEach(btn => {
  btn.addEventListener('click', () => {
    const item   = btn.closest('.faq-item');
    const answer = item.querySelector('.faq-answer');
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(o => {
      o.classList.remove('open');
      o.querySelector('.faq-answer').style.maxHeight = '0';
    });
    if (!isOpen) {
      item.classList.add('open');
      answer.style.maxHeight = answer.scrollHeight + 'px';
    }
  });
});

document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
