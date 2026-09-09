(() => {
  const nav = document.getElementById('nav');
  const toggle = nav && nav.querySelector('.burger');
  const activePage = nav && nav.querySelector('.menu a.on');
  if (activePage) activePage.setAttribute('aria-current', 'page');
  if (!nav || !toggle) return;

  const closeMenu = returnFocus => {
    if (!nav.classList.contains('open')) return;
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    if (returnFocus) toggle.focus();
  };

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeMenu(true);
  });
  nav.querySelectorAll('.menu a').forEach(link => {
    link.addEventListener('click', () => closeMenu(false));
  });
})();
