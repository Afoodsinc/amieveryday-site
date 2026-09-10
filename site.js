(() => {
  const button = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.primary-nav');
  if (button && nav) {
    const close = (focus = false) => {
      nav.classList.remove('open');
      button.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('menu-open');
      if (focus) button.focus();
    };
    button.addEventListener('click', () => {
      const open = !nav.classList.contains('open');
      nav.classList.toggle('open', open);
      button.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('menu-open', open);
    });
    nav.addEventListener('click', (event) => { if (event.target.closest('a')) close(); });
    document.addEventListener('keydown', (event) => { if (event.key === 'Escape' && nav.classList.contains('open')) close(true); });
    window.addEventListener('resize', () => { if (window.innerWidth > 820) close(); });
  }

  const items = document.querySelectorAll('[data-reveal]');
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    items.forEach((item) => item.classList.add('is-visible'));
  } else {
    const observer = new IntersectionObserver((entries, instance) => entries.forEach((entry) => {
      if (entry.isIntersecting) { entry.target.classList.add('is-visible'); instance.unobserve(entry.target); }
    }), { rootMargin: '0px 0px -8% 0px' });
    items.forEach((item) => observer.observe(item));
  }

  const catalog = document.getElementById('product-grid');
  const search = document.getElementById('catalog-search');
  if (catalog && search) {
    const cards = [...catalog.querySelectorAll('[data-product]')];
    const filters = [...document.querySelectorAll('[data-filter]')];
    const status = document.getElementById('catalog-status');
    const empty = document.getElementById('catalog-empty');
    const clear = document.getElementById('catalog-clear');
    const normalize = (value) => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
    let category = 'all';
    const apply = () => {
      const term = normalize(search.value);
      let visible = 0;
      cards.forEach((card) => {
        const matchesText = !term || normalize(card.dataset.product).includes(term);
        const matchesCategory = category === 'all' || card.dataset.category === category;
        card.hidden = !(matchesText && matchesCategory);
        if (!card.hidden) visible += 1;
      });
      if (status) {
        const suffix = document.documentElement.lang === 'es' ? status.dataset.templateEs : status.dataset.templateEn;
        status.textContent = `${visible} ${suffix}`;
      }
      if (empty) empty.hidden = visible !== 0;
    };
    filters.forEach((filter) => filter.addEventListener('click', () => {
      category = filter.dataset.filter;
      filters.forEach((item) => item.setAttribute('aria-pressed', String(item === filter)));
      apply();
    }));
    search.addEventListener('input', apply);
    clear?.addEventListener('click', () => { search.value = ''; category = 'all'; filters.forEach((item) => item.setAttribute('aria-pressed', String(item.dataset.filter === 'all'))); apply(); search.focus(); });
    const params = new URLSearchParams(window.location.search);
    search.value = params.get('q') || '';
    const requestedCategory = params.get('category');
    if (requestedCategory && filters.some((item) => item.dataset.filter === requestedCategory)) {
      category = requestedCategory;
      filters.forEach((item) => item.setAttribute('aria-pressed', String(item.dataset.filter === category)));
    }
    apply();
  }
})();
