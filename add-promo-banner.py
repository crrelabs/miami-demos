#!/usr/bin/env python3
"""
Add promo banner to all v2 demo sites.
Inserts a sticky top banner with countdown timer + Stripe checkout link.
"""

import os, re, sys
from pathlib import Path

DEMOS_DIR = Path(__file__).parent
STRIPE_LINK = "https://buy.stripe.com/test_fZu28kbVF7yGeE89zb33W00"

BANNER_CSS = """
/* === PROMO BANNER === */
.promo-banner{position:fixed;top:0;left:0;right:0;z-index:200;background:linear-gradient(135deg,#dc2626 0%,#b91c1c 50%,#991b1b 100%);color:#fff;text-align:center;padding:.65rem 1rem;font-size:.95rem;font-weight:600;display:flex;align-items:center;justify-content:center;gap:.75rem;flex-wrap:wrap;box-shadow:0 2px 12px rgba(0,0,0,.2)}
.promo-banner .price-old{text-decoration:line-through;opacity:.7;font-size:.9rem}
.promo-banner .price-new{font-size:1.15rem;font-weight:800;color:#fbbf24}
.promo-banner .countdown{background:rgba(0,0,0,.25);padding:.25rem .6rem;border-radius:6px;font-family:'Courier New',monospace;font-size:.85rem;letter-spacing:1px}
.promo-banner .promo-btn{background:#fbbf24;color:#1a1a2e;padding:.4rem 1.2rem;border-radius:50px;text-decoration:none;font-weight:700;font-size:.85rem;transition:all .2s;white-space:nowrap}
.promo-banner .promo-btn:hover{background:#f59e0b;transform:scale(1.05)}
@media(max-width:600px){.promo-banner{font-size:.8rem;padding:.5rem .75rem;gap:.5rem}.promo-banner .promo-btn{padding:.35rem 1rem;font-size:.8rem}}
"""

BANNER_HTML = f"""
<!-- Promo Banner -->
<div class="promo-banner">
  <span>🚀 Launch Your Website — <span class="price-old">$39.99/mo</span> <span class="price-new">$19.99/mo</span></span>
  <span class="countdown" id="countdown">48:00:00</span>
  <a href="{STRIPE_LINK}" class="promo-btn" target="_blank">Claim This Deal →</a>
</div>
"""

BANNER_JS = """
// Promo countdown timer
(function(){
  const key = 'promo_end_' + location.pathname;
  let end = localStorage.getItem(key);
  if (!end) {
    end = Date.now() + 48 * 60 * 60 * 1000;
    localStorage.setItem(key, end);
  }
  end = parseInt(end);
  const el = document.getElementById('countdown');
  function update() {
    const diff = Math.max(0, end - Date.now());
    const h = Math.floor(diff / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    const s = Math.floor((diff % 60000) / 1000);
    el.textContent = String(h).padStart(2,'0') + ':' + String(m).padStart(2,'0') + ':' + String(s).padStart(2,'0');
    if (diff > 0) requestAnimationFrame(update);
    else el.textContent = 'EXPIRED';
  }
  update();
  setInterval(update, 1000);
})();
"""

def add_banner(site_dir: Path) -> bool:
    index = site_dir / 'index.html'
    if not index.exists():
        return False
    
    content = index.read_text()
    
    # Skip if already has promo banner
    if 'promo-banner' in content:
        return False
    
    # Skip if not v2 (no nav)
    if '<nav class="nav">' not in content:
        return False
    
    # 1. Add CSS before closing </style>
    content = content.replace('</style>', BANNER_CSS + '\n</style>', 1)
    
    # 2. Adjust nav top to account for banner (push nav down ~40px)
    content = content.replace(
        '.nav{position:fixed;top:0;',
        '.nav{position:fixed;top:40px;'
    )
    # Adjust hero padding to account for nav + banner
    content = content.replace(
        'padding:6rem 2rem 4rem',
        'padding:7rem 2rem 4rem'
    )
    # Mobile nav adjustment
    content = content.replace(
        '.nav-links{position:fixed;top:0;',
        '.nav-links{position:fixed;top:40px;'
    )
    
    # 3. Add banner HTML right after <body>
    content = content.replace('<body>', '<body>\n' + BANNER_HTML, 1)
    
    # 4. Add countdown JS before closing </script>
    content = content.replace('</script>', BANNER_JS + '\n</script>', 1)
    
    index.write_text(content)
    return True

def main():
    dirs = sorted([
        d for d in DEMOS_DIR.iterdir()
        if d.is_dir() and (d / 'index.html').exists()
    ])
    
    if len(sys.argv) > 1:
        targets = set(sys.argv[1:])
        dirs = [d for d in dirs if d.name in targets]
    
    added = 0
    skipped = 0
    
    for d in dirs:
        try:
            if add_banner(d):
                added += 1
                print(f'✅ {d.name}')
            else:
                skipped += 1
                print(f'⏭️  {d.name}')
        except Exception as e:
            print(f'❌ {d.name}: {e}')
    
    print(f'\n--- Done: {added} updated, {skipped} skipped ---')

if __name__ == '__main__':
    main()
