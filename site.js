(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const forcedColors = window.matchMedia('(forced-colors: active)');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');

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
  try {
    if (!('IntersectionObserver' in window) || reducedMotion.matches) {
      items.forEach((item) => item.classList.add('is-visible'));
    } else {
      const observer = new IntersectionObserver((entries, instance) => entries.forEach((entry) => {
        if (entry.isIntersecting) { entry.target.classList.add('is-visible'); instance.unobserve(entry.target); }
      }), { rootMargin: '0px 0px -8% 0px' });
      items.forEach((item) => observer.observe(item));
    }
    document.documentElement.classList.add('motion-ready');
  } catch (error) {
    items.forEach((item) => item.classList.add('is-visible'));
    document.documentElement.classList.remove('motion-ready');
  }

  const films = [...document.querySelectorAll('.brand-film')];
  films.forEach((film) => {
    const video = film.querySelector('[data-cinema-video]');
    const toggle = film.querySelector('[data-cinema-toggle]');
    if (!video || !toggle) return;

    const playLabel = toggle.dataset.playLabel || 'Play film';
    const pauseLabel = toggle.dataset.pauseLabel || 'Pause film';
    const labelNode = toggle.querySelector('[data-cinema-label], span:last-child');
    let restrictedAutoplay = reducedMotion.matches || forcedColors.matches || navigator.connection?.saveData === true;
    let loaded = video.readyState > 0;
    let inView = false;
    let userPaused = false;

    const setToggleState = (playing) => {
      const label = playing ? pauseLabel : playLabel;
      toggle.setAttribute('aria-label', label);
      toggle.setAttribute('title', label);
      toggle.setAttribute('aria-pressed', String(playing));
      if (labelNode) labelNode.textContent = label;
      film.classList.toggle('is-playing', playing);
    };

    const loadVideo = () => {
      if (loaded) return;
      video.querySelectorAll('source[data-src]').forEach((source) => {
        source.src = source.dataset.src;
        source.removeAttribute('data-src');
      });
      if (video.dataset.src) {
        video.src = video.dataset.src;
        video.removeAttribute('data-src');
      }
      loaded = true;
      video.load();
    };

    const playVideo = async () => {
      loadVideo();
      try {
        await video.play();
      } catch (error) {
        setToggleState(false);
      }
    };

    const playWhenEligible = () => {
      if (!restrictedAutoplay && inView && !userPaused && !document.hidden) playVideo();
    };

    const syncPlaybackPreference = () => {
      restrictedAutoplay = reducedMotion.matches || forcedColors.matches || navigator.connection?.saveData === true;
      if (restrictedAutoplay) video.pause(); else playWhenEligible();
    };

    video.autoplay = false;
    video.addEventListener('play', () => setToggleState(true));
    video.addEventListener('pause', () => setToggleState(false));
    video.addEventListener('canplay', () => film.classList.add('is-ready'));
    video.addEventListener('error', () => {
      film.classList.add('has-video-error');
      setToggleState(false);
    });
    toggle.addEventListener('click', () => {
      if (video.paused || video.ended) {
        userPaused = false;
        playVideo();
      } else {
        userPaused = true;
        video.pause();
      }
    });
    setToggleState(false);

    if ('IntersectionObserver' in window) {
      if (!restrictedAutoplay) {
        const preloadObserver = new IntersectionObserver(([entry], instance) => {
          if (!entry.isIntersecting) return;
          loadVideo();
          instance.disconnect();
        }, { rootMargin: '240px 0px' });
        preloadObserver.observe(film);
      }
      const filmObserver = new IntersectionObserver(([entry]) => {
        inView = entry.isIntersecting && entry.intersectionRatio >= .35;
        if (inView) playWhenEligible(); else video.pause();
      }, { threshold: [0, .35, .75] });
      filmObserver.observe(film);
    } else if (!restrictedAutoplay) {
      inView = true;
      playWhenEligible();
    }

    document.addEventListener('visibilitychange', () => {
      if (document.hidden) video.pause(); else playWhenEligible();
    });
    reducedMotion.addEventListener?.('change', syncPlaybackPreference);
    forcedColors.addEventListener?.('change', syncPlaybackPreference);
    navigator.connection?.addEventListener?.('change', syncPlaybackPreference);
  });

  const motionTargets = [...document.querySelectorAll('.product-card, .category-card, .range-montage, .range-pack, .pdp-stage, .recipe-card, .identity-product, .split-media')]
    .filter((target) => !target.matches('.range-montage') || !target.querySelector('.range-pack'));
  if (finePointer.matches && !reducedMotion.matches && !forcedColors.matches) {
    motionTargets.forEach((target) => {
      const limit = target.matches('.pdp-stage, .range-montage') ? 8 : target.matches('.range-pack') ? 5 : target.matches('.recipe-card, .identity-product, .split-media') ? 4 : 6;
      const scale = target.matches('.range-pack') ? 1.025 : target.matches('.recipe-card, .identity-product, .split-media') ? 1.012 : 1.035;
      let frame = 0;
      let point = null;

      const render = () => {
        frame = 0;
        if (!point) return;
        const bounds = target.getBoundingClientRect();
        const xRatio = ((point.x - bounds.left) / bounds.width) * 2 - 1;
        const yRatio = ((point.y - bounds.top) / bounds.height) * 2 - 1;
        target.style.setProperty('--motion-x', `${(xRatio * limit).toFixed(2)}px`);
        target.style.setProperty('--motion-y', `${(yRatio * limit).toFixed(2)}px`);
        target.style.setProperty('--motion-rx', `${(-yRatio * 1.4).toFixed(2)}deg`);
        target.style.setProperty('--motion-ry', `${(xRatio * 1.4).toFixed(2)}deg`);
        target.style.setProperty('--motion-scale', scale);
      };

      const schedule = (event) => {
        point = { x: event.clientX, y: event.clientY };
        if (!frame) frame = requestAnimationFrame(render);
      };
      const reset = () => {
        point = null;
        if (frame) cancelAnimationFrame(frame);
        frame = 0;
        target.style.removeProperty('--motion-x');
        target.style.removeProperty('--motion-y');
        target.style.removeProperty('--motion-rx');
        target.style.removeProperty('--motion-ry');
        target.style.removeProperty('--motion-scale');
      };

      target.classList.add('has-pointer-motion');
      target.addEventListener('pointermove', schedule, { passive: true });
      target.addEventListener('pointerleave', reset);
      target.addEventListener('pointercancel', reset);
      target.addEventListener('blur', reset, true);
    });
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
      if (status) status.textContent = document.documentElement.lang === 'es' ? status.dataset.statusEs : status.dataset.statusEn;
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
    cards.forEach((card, index) => {
      card.classList.add('catalog-card-reveal');
      card.style.setProperty('--catalog-order', index % 8);
    });
    if ('IntersectionObserver' in window && !reducedMotion.matches) {
      const cardRevealObserver = new IntersectionObserver((entries, instance) => entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-catalog-visible');
        instance.unobserve(entry.target);
      }), { rootMargin: '0px 0px -6% 0px', threshold: .08 });
      cards.forEach((card) => cardRevealObserver.observe(card));
    } else {
      cards.forEach((card) => card.classList.add('is-catalog-visible'));
    }
  }

  const productDialog = document.getElementById('product-dialog');
  if (productDialog) {
    const quickProducts = [...document.querySelectorAll('[data-quick-product]')];
    const dialogImage = document.getElementById('product-dialog-image');
    const dialogCategory = document.getElementById('product-dialog-category');
    const dialogTitle = document.getElementById('product-dialog-title');
    const dialogSize = document.getElementById('product-dialog-size');
    const dialogFull = document.getElementById('product-dialog-full');
    const productContact = productDialog.querySelector('a[href*="#product-question"]');
    const productContactBase = productContact?.getAttribute('href') || '';
    let opener = null;
    quickProducts.forEach((product) => product.addEventListener('click', () => {
      opener = product;
      if (dialogImage) { dialogImage.src = product.dataset.image; dialogImage.alt = `ami ${product.dataset.name}, ${product.dataset.size}`; }
      if (dialogCategory) dialogCategory.textContent = product.dataset.categoryLabel;
      if (dialogTitle) dialogTitle.textContent = product.dataset.name;
      if (dialogSize) dialogSize.textContent = product.dataset.size;
      if (productContact && productContactBase) {
        const path = productContactBase.split('#')[0];
        productContact.href = `${path}?product=${encodeURIComponent(`${product.dataset.name}, ${product.dataset.size}`)}#product-question`;
      }
      if (dialogFull) {
        dialogFull.hidden = !product.dataset.full;
        if (product.dataset.full) dialogFull.href = product.dataset.full;
      }
      productDialog.showModal();
      productDialog.classList.remove('is-opening');
      void productDialog.offsetWidth;
      productDialog.classList.add('is-opening');
    }));
    productDialog.addEventListener('click', (event) => {
      if (event.target === productDialog) productDialog.close();
    });
    productDialog.addEventListener('close', () => {
      productDialog.classList.remove('is-opening');
      opener?.focus();
    });
  }

  const mapFrame = document.querySelector('.market-map-frame');
  const marketFeature = document.querySelector('.market-feature');
  if (mapFrame && marketFeature) {
    const markers = [...mapFrame.querySelectorAll('.market-marker')];
    const cards = [...document.querySelectorAll('[data-market-card]')];
    const filters = [...document.querySelectorAll('[data-market-filter]')];
    const number = marketFeature.querySelector('.market-index');
    const name = marketFeature.querySelector('h3');
    const status = marketFeature.querySelector(':scope > strong');
    const body = marketFeature.querySelector(':scope > p');
    const marketApply = marketFeature.querySelector('.market-apply');
    const marketApplyBase = marketApply?.getAttribute('href') || '';
    const selectMarket = (marker) => {
      markers.forEach((item) => item.setAttribute('aria-pressed', String(item === marker)));
      cards.forEach((card) => {
        const active = card.dataset.marketCard === marker.dataset.market;
        card.classList.toggle('is-active', active);
        if (active) card.setAttribute('aria-current', 'true'); else card.removeAttribute('aria-current');
      });
      if (number) number.textContent = marker.querySelector('span')?.textContent.padStart(2, '0') || '';
      if (name) name.textContent = marker.dataset.name;
      if (status) status.textContent = marker.dataset.status;
      if (body) body.textContent = marker.dataset.body;
      if (marketApply && marketApplyBase) {
        const path = marketApplyBase.split('#')[0];
        marketApply.href = `${path}?market=${encodeURIComponent(marker.dataset.name)}#distribution-inquiry`;
      }
      if (!reducedMotion.matches) {
        marketFeature.classList.remove('market-updating');
        void marketFeature.offsetWidth;
        marketFeature.classList.add('market-updating');
        const activeCard = cards.find((card) => card.dataset.marketCard === marker.dataset.market);
        activeCard?.classList.remove('selection-pop');
        if (activeCard) {
          void activeCard.offsetWidth;
          activeCard.classList.add('selection-pop');
        }
      }
    };
    markers.forEach((marker) => marker.addEventListener('click', () => selectMarket(marker)));
    cards.forEach((card) => card.addEventListener('click', (event) => {
      event.preventDefault();
      const marker = markers.find((item) => item.dataset.market === card.dataset.marketCard);
      if (!marker) return;
      selectMarket(marker);
      if (window.matchMedia('(max-width: 560px)').matches) {
        marketFeature.focus({ preventScroll: true });
        marketFeature.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
      }
    }));
    filters.forEach((filter) => filter.addEventListener('click', () => {
      const region = filter.dataset.marketFilter;
      filters.forEach((item) => item.setAttribute('aria-pressed', String(item === filter)));
      markers.forEach((marker) => { marker.hidden = region !== 'all' && marker.dataset.region !== region; });
      cards.forEach((card) => { card.hidden = region !== 'all' && card.dataset.region !== region; });
      const visibleSelected = markers.find((marker) => !marker.hidden && marker.getAttribute('aria-pressed') === 'true');
      if (!visibleSelected) {
        const firstVisible = markers.find((marker) => !marker.hidden);
        if (firstVisible) selectMarket(firstVisible);
      }
    }));
    const selected = markers.find((marker) => marker.getAttribute('aria-pressed') === 'true') || markers[0];
    if (selected) selectMarket(selected);
  }

  const pdpContact = document.querySelector('.pdp-copy a[href*="#product-question"]');
  if (pdpContact) {
    const productName = document.querySelector('.pdp-copy h1')?.textContent.trim();
    const productSize = document.querySelector('.pdp-proof strong')?.textContent.trim();
    if (productName && productSize) {
      const path = pdpContact.getAttribute('href').split('#')[0];
      pdpContact.href = `${path}?product=${encodeURIComponent(`${productName}, ${productSize}`)}#product-question`;
    }
  }

  const contactParams = new URLSearchParams(window.location.search);
  const isSpanish = document.documentElement.lang === 'es';
  const contextRoutes = [
    { key: 'product', route: 'product-question', subject: isSpanish ? 'Consulta sobre un producto ami' : 'ami product question' },
    { key: 'market', route: 'distribution-inquiry', subject: isSpanish ? 'Alianza de distribución ami' : 'ami distribution partnership' },
  ];
  contextRoutes.forEach(({ key, route, subject }) => {
    const value = contactParams.get(key)?.trim();
    const card = document.getElementById(route);
    const link = card?.querySelector('a[href^="mailto:"]');
    if (!value || !card || !link) return;
    const mailbox = link.getAttribute('href').split('?')[0];
    link.href = `${mailbox}?subject=${encodeURIComponent(`${subject} — ${value}`)}`;
    const context = document.createElement('span');
    context.className = 'contact-context';
    context.textContent = `${isSpanish ? 'Selección' : 'Selected'}: ${value}`;
    link.before(context);
  });
})();
