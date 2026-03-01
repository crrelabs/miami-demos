#!/usr/bin/env python3
"""Update all demo sites to point to the checkout app instead of raw Stripe link."""

import os, re, sys
from pathlib import Path

DEMOS_DIR = Path(__file__).parent
CHECKOUT_BASE = "https://checkout-zeta-seven.vercel.app"
OLD_STRIPE_LINK = "https://buy.stripe.com/test_fZu28kbVF7yGeE89zb33W00"

def update_site(site_dir: Path) -> bool:
    index = site_dir / 'index.html'
    if not index.exists():
        return False
    
    content = index.read_text()
    if OLD_STRIPE_LINK not in content:
        return False
    
    slug = site_dir.name
    checkout_url = f"{CHECKOUT_BASE}/{slug}"
    
    content = content.replace(OLD_STRIPE_LINK, checkout_url)
    index.write_text(content)
    return True

def main():
    dirs = sorted([
        d for d in DEMOS_DIR.iterdir()
        if d.is_dir() and (d / 'index.html').exists()
    ])
    
    updated = 0
    for d in dirs:
        if update_site(d):
            updated += 1
            print(f'✅ {d.name}')
    
    print(f'\n--- Done: {updated} updated ---')

if __name__ == '__main__':
    main()
