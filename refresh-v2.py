#!/usr/bin/env python3
"""
Demo Site Refresh Script — v1 → v2 Framework
Reads existing index.html, extracts business data, generates v2 version.
"""

import os, re, sys, html
from pathlib import Path

DEMOS_DIR = Path(__file__).parent

# Category → design tokens mapping
CATEGORY_TOKENS = {
    'restaurant': {
        'keywords': ['restaurant', 'food truck', 'food', 'bakery', 'pizza', 'grill', 'cafe', 'coffee', 'bistro', 'taco', 'sushi', 'diner', 'barbecue', 'bbq', 'chicken', 'burger', 'seafood', 'ice cream', 'juice', 'smoothie', 'tea', 'pastry', 'catering', 'arepa', 'empanada'],
        'primary': '#c2410c',
        'primary_dark': '#9a3412',
        'primary_light': '#fed7aa',
        'gradient': 'linear-gradient(135deg, #1a0a00 0%, #7c2d12 50%, #c2410c 100%)',
        'hero_overlay': 'rgba(26,10,0,0.6)',
        'section_alt': '#fef3e2',
        'heading_font': "'Playfair Display', serif",
        'heading_weight': '700',
        'body_font': "'DM Sans', sans-serif",
        'google_fonts': 'Playfair+Display:wght@700&family=DM+Sans:wght@400;500;600;700',
        'hero_value_prop': 'Bold Flavors, Made Fresh Daily',
        'hero_sub': 'Serving Miami\'s favorite dishes with fresh ingredients and unforgettable taste.',
    },
    'beauty': {
        'keywords': ['nail', 'salon', 'spa', 'beauty', 'hair', 'barber', 'wax', 'lash', 'brow', 'makeup', 'skincare', 'tanning', 'massage', 'barbershop', 'tonsorial'],
        'primary': '#9f1239',
        'primary_dark': '#881337',
        'primary_light': '#fce7f3',
        'gradient': 'linear-gradient(135deg, #1a0a12 0%, #4a0520 50%, #9f1239 100%)',
        'hero_overlay': 'rgba(26,10,18,0.6)',
        'section_alt': '#fdf2f8',
        'heading_font': "'Cormorant Garamond', serif",
        'heading_weight': '600',
        'body_font': "'Nunito', sans-serif",
        'google_fonts': 'Cormorant+Garamond:wght@600;700&family=Nunito:wght@400;500;600;700',
        'hero_value_prop': 'Your Beauty, Elevated',
        'hero_sub': 'A luxurious experience designed to make you look and feel your absolute best.',
    },
    'auto': {
        'keywords': ['tire', 'auto', 'car', 'mechanic', 'body shop', 'towing', 'oil change', 'transmission', 'wheel', 'mobile tire', 'car wash', 'detailing', 'maintenance'],
        'primary': '#1d4ed8',
        'primary_dark': '#1e3a8a',
        'primary_light': '#dbeafe',
        'gradient': 'linear-gradient(135deg, #0c1929 0%, #1e3a8a 50%, #1d4ed8 100%)',
        'hero_overlay': 'rgba(12,25,41,0.65)',
        'section_alt': '#f0f4ff',
        'heading_font': "'Montserrat', sans-serif",
        'heading_weight': '800',
        'body_font': "'Inter', sans-serif",
        'google_fonts': 'Montserrat:wght@700;800&family=Inter:wght@400;500;600;700',
        'hero_value_prop': 'Expert Service You Can Trust',
        'hero_sub': 'Professional auto care with honest pricing — keeping Miami on the road.',
    },
    'retail': {
        'keywords': ['market', 'supermarket', 'store', 'shop', 'jewelry', 'boutique', 'thrift', 'supply', 'pet store', 'smoke shop', 'laundry', 'coin laundry'],
        'primary': '#0f172a',
        'primary_dark': '#020617',
        'primary_light': '#e2e8f0',
        'gradient': 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%)',
        'hero_overlay': 'rgba(15,23,42,0.6)',
        'section_alt': '#f8fafc',
        'heading_font': "'Plus Jakarta Sans', sans-serif",
        'heading_weight': '700',
        'body_font': "'Inter', sans-serif",
        'google_fonts': 'Plus+Jakarta+Sans:wght@600;700;800&family=Inter:wght@400;500;600;700',
        'hero_value_prop': 'Quality Selection, Everyday Value',
        'hero_sub': 'Your neighborhood destination for everything you need — curated with care.',
    },
    'professional': {
        'keywords': ['insurance', 'legal', 'lawyer', 'attorney', 'accountant', 'tax', 'finance', 'consulting', 'real estate', 'agency', 'notary'],
        'primary': '#0d4f4f',
        'primary_dark': '#064e3b',
        'primary_light': '#d1fae5',
        'gradient': 'linear-gradient(135deg, #022c22 0%, #064e3b 50%, #0d9488 100%)',
        'hero_overlay': 'rgba(2,44,34,0.65)',
        'section_alt': '#f0fdf4',
        'heading_font': "'Source Serif 4', serif",
        'heading_weight': '700',
        'body_font': "'Inter', sans-serif",
        'google_fonts': 'Source+Serif+4:wght@600;700&family=Inter:wght@400;500;600;700',
        'hero_value_prop': 'Trusted Expertise, Real Results',
        'hero_sub': 'Professional guidance you can count on — protecting what matters most.',
    },
    'health': {
        'keywords': ['dental', 'doctor', 'clinic', 'hospital', 'veterinary', 'vet', 'animal', 'medical', 'pharmacy', 'health', 'chiropractic', 'physical therapy', 'optician', 'eye'],
        'primary': '#0891b2',
        'primary_dark': '#155e75',
        'primary_light': '#cffafe',
        'gradient': 'linear-gradient(135deg, #0c1929 0%, #155e75 50%, #0891b2 100%)',
        'hero_overlay': 'rgba(12,25,41,0.6)',
        'section_alt': '#ecfeff',
        'heading_font': "'Nunito', sans-serif",
        'heading_weight': '700',
        'body_font': "'Inter', sans-serif",
        'google_fonts': 'Nunito:wght@600;700;800&family=Inter:wght@400;500;600;700',
        'hero_value_prop': 'Compassionate Care for Your Family',
        'hero_sub': 'Expert, personalized care in a warm and welcoming environment.',
    },
}

def detect_category(business_type: str) -> str:
    """Match business type to a design category."""
    bt = business_type.lower()
    for cat, tokens in CATEGORY_TOKENS.items():
        for kw in tokens['keywords']:
            if kw in bt:
                return cat
    return 'retail'  # default fallback

def make_value_prop(business_name: str, business_type: str, category: str, rating: str, review_count: str) -> tuple:
    """Generate a value proposition headline and subheadline."""
    tokens = CATEGORY_TOKENS[category]
    name_clean = html.unescape(business_name).strip()
    
    # Category-specific value props with business customization
    props = {
        'restaurant': [
            f'Bold Flavors, Made Fresh — Right Here in Miami',
            f'Authentic Taste That Keeps Miami Coming Back',
            f'Fresh Ingredients, Unforgettable Flavor',
        ],
        'beauty': [
            f'Your Beauty Experience, Elevated',
            f'Where Miami Comes to Look Amazing',
            f'Luxury Meets Artistry — Walk-Ins Welcome',
        ],
        'auto': [
            f'Expert Auto Service You Can Trust',
            f'Honest Repairs, Fair Prices — Every Time',
            f'Miami\'s Go-To for Reliable Auto Care',
        ],
        'retail': [
            f'Quality Selection, Everyday Value',
            f'Your Neighborhood Destination in Miami',
            f'Curated With Care, Priced to Please',
        ],
        'professional': [
            f'Trusted Expertise When It Matters Most',
            f'Professional Results, Personal Attention',
            f'Your Partner in Smart Decision-Making',
        ],
        'health': [
            f'Compassionate Care for Your Whole Family',
            f'Expert Care in a Warm, Welcoming Space',
            f'Where Your Health Comes First',
        ],
    }
    
    import hashlib
    idx = int(hashlib.md5(name_clean.encode()).hexdigest(), 16) % 3
    headline = props.get(category, props['retail'])[idx]
    
    # Build subheadline with specifics
    parts = []
    if rating and float(rating) >= 4.5:
        parts.append(f'Rated {rating}★ by {review_count}+ customers on Google')
    parts.append(f'{name_clean} — proudly serving the Miami community')
    subheadline = '. '.join(parts) + '.'
    
    return headline, subheadline

def extract_data(html_content: str) -> dict:
    """Extract business data from v1 index.html."""
    data = {}
    
    # Title / name
    m = re.search(r'<title>(.+?)(?:\s*—\s*(.+?))?</title>', html_content)
    if m:
        data['name'] = html.unescape(m.group(1).strip())
        data['type'] = html.unescape(m.group(2).strip()) if m.group(2) else 'Business'
    
    # Category tag
    m = re.search(r'category">\s*(.+?)\s*<', html_content)
    if m:
        data['type'] = html.unescape(m.group(1).strip())
    
    # Phone
    m = re.search(r'tel:\+(\d+)', html_content)
    if m:
        data['phone_raw'] = m.group(1)
        p = m.group(1)
        if len(p) == 11 and p.startswith('1'):
            data['phone_display'] = f'({p[1:4]}) {p[4:7]}-{p[7:]}'
            data['phone_tel'] = f'+{p}'
        else:
            data['phone_display'] = p
            data['phone_tel'] = f'+{p}'
    
    # Place ID
    m = re.search(r'place_id:([A-Za-z0-9_-]+)', html_content)
    if m:
        data['place_id'] = m.group(1)
    
    # Photo URL from hero background
    m = re.search(r"url\('(https://places\.googleapis\.com[^']+)'\)", html_content)
    if m:
        data['photo_url'] = m.group(1)
    
    # Rating and reviews
    m = re.search(r'(\d+\.?\d*)\s*(?:out of 5\s*·|·)\s*([\d,]+)\s*reviews?', html_content)
    if m:
        data['rating'] = m.group(1)
        data['review_count'] = m.group(2)
    
    # Address
    m = re.search(r'Address</h3>\s*<p>(.+?)</p>', html_content)
    if m:
        data['address'] = html.unescape(m.group(1).strip())
    
    # Description
    m = re.search(r'class="desc">(.+?)</p>', html_content, re.DOTALL)
    if m:
        data['desc'] = html.unescape(m.group(1).strip())
    
    # Google Maps API key
    m = re.search(r'key=([A-Za-z0-9_-]+)', html_content)
    if m:
        data['api_key'] = m.group(1)
    
    # Website URL if present
    m = re.search(r'Website</h3>\s*<p><a href="([^"]+)"', html_content)
    if m:
        data['website'] = m.group(1)
    
    # Hours
    hours = re.findall(r'<li>(.+?)</li>', html_content)
    if hours:
        data['hours'] = hours
    
    return data

def generate_v2(data: dict) -> str:
    """Generate v2 index.html from extracted data."""
    category = detect_category(data.get('type', 'Business'))
    tokens = CATEGORY_TOKENS[category]
    
    name = data.get('name', 'Business')
    btype = data.get('type', 'Business')
    phone_display = data.get('phone_display', '')
    phone_tel = data.get('phone_tel', '')
    address = data.get('address', '')
    rating = data.get('rating', '')
    review_count = data.get('review_count', '')
    place_id = data.get('place_id', '')
    photo_url = data.get('photo_url', '')
    api_key = data.get('api_key', 'AIzaSyAbieiBngZWDnF3Ol9q-Owg0ixVinSgSR0')
    website = data.get('website', '')
    
    headline, subheadline = make_value_prop(name, btype, category, rating, review_count)
    
    # Rating stars
    if rating:
        r = float(rating)
        full = int(r)
        half = 1 if r - full >= 0.3 else 0
        stars_html = '★' * full + ('½' if half else '') + '☆' * (5 - full - half)
    else:
        stars_html = '★★★★★'
    
    # Hours HTML
    hours_html = ''
    if data.get('hours'):
        hours_items = '\n'.join(f'              <li>{h}</li>' for h in data['hours'])
        hours_html = f'''
          <div class="info-card animate-in">
            <div class="icon">🕐</div>
            <h3>Hours</h3>
            <ul class="hours-list">
{hours_items}
            </ul>
          </div>'''
    
    # Website card
    website_html = ''
    if website:
        website_html = f'''
          <div class="info-card animate-in">
            <div class="icon">🌐</div>
            <h3>Website</h3>
            <p><a href="{website}" target="_blank">{website.replace("https://","").replace("http://","").rstrip("/")}</a></p>
          </div>'''
    
    # CTA text based on category
    cta_texts = {
        'restaurant': ('Hungry? Come Find Us', 'Fresh food is waiting — stop by today or give us a call to place your order.', 'Call to Order'),
        'beauty': ('Ready for a New Look?', 'Book your appointment today and experience the difference.', 'Book Now'),
        'auto': ('Need Service Today?', 'Call now for honest, fast auto service at fair prices.', 'Call for a Quote'),
        'retail': ('Come See Us Today', 'Visit our store and discover what makes us a neighborhood favorite.', 'Get Directions'),
        'professional': ('Let\'s Talk About Your Needs', 'Schedule a consultation and discover how we can help.', 'Schedule Consultation'),
        'health': ('Book Your Visit Today', 'Your health matters — call us or book online to get started.', 'Book Appointment'),
    }
    cta_h, cta_p, cta_label = cta_texts.get(category, cta_texts['retail'])
    
    # Phone CTA or email CTA
    if phone_tel:
        cta_btn = f'<a href="tel:{phone_tel}" class="cta-btn">{cta_label}: {phone_display} →</a>'
        mobile_cta = f'''<a href="tel:{phone_tel}" class="mobile-cta">📞 Call Now</a>'''
    else:
        cta_btn = f'<a href="mailto:carlos@crrelabs.com?subject=I want my website - {html.escape(name)}" class="cta-btn">Contact CRRE Labs →</a>'
        mobile_cta = ''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(name)} — {html.escape(btype)} | Miami, FL</title>
<meta name="description" content="{html.escape(name)} — {html.escape(btype)} in Miami. {html.escape(subheadline)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family={tokens['google_fonts']}&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{
  --primary:{tokens['primary']};
  --primary-dark:{tokens['primary_dark']};
  --primary-light:{tokens['primary_light']};
  --text:#1a1a2e;
  --text-muted:#64748b;
  --bg:#ffffff;
  --bg-alt:{tokens['section_alt']};
  --radius:14px;
  --radius-pill:50px;
  --shadow:0 4px 24px rgba(0,0,0,.06);
  --shadow-hover:0 12px 32px rgba(0,0,0,.12);
  --max-w:1200px;
  --font-heading:{tokens['heading_font']};
  --font-body:{tokens['body_font']};
}}
body{{font-family:var(--font-body);color:var(--text);line-height:1.6;overflow-x:hidden;background:var(--bg)}}

/* === NAV === */
.nav{{position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(255,255,255,.92);backdrop-filter:blur(12px);border-bottom:1px solid rgba(0,0,0,.06);transition:all .3s ease;height:72px;display:flex;align-items:center}}
.nav.scrolled{{height:56px;box-shadow:0 2px 20px rgba(0,0,0,.08)}}
.nav-inner{{max-width:var(--max-w);margin:0 auto;width:100%;padding:0 2rem;display:flex;align-items:center;justify-content:space-between}}
.nav-brand{{font-family:var(--font-heading);font-weight:{tokens['heading_weight']};font-size:1.15rem;color:var(--text);text-decoration:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:60%}}
.nav-links{{display:flex;gap:1.5rem;align-items:center}}
.nav-links a{{color:var(--text-muted);text-decoration:none;font-size:.9rem;font-weight:500;transition:color .2s}}
.nav-links a:hover{{color:var(--primary)}}
.nav-cta{{background:var(--primary);color:#fff!important;padding:.5rem 1.25rem;border-radius:var(--radius-pill);font-weight:600;transition:all .2s}}
.nav-cta:hover{{background:var(--primary-dark);transform:scale(1.05)}}
.hamburger{{display:none;flex-direction:column;gap:5px;cursor:pointer;padding:4px}}
.hamburger span{{width:24px;height:2.5px;background:var(--text);border-radius:2px;transition:all .3s}}

/* === HERO === */
.hero{{min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;color:#fff;padding:6rem 2rem 4rem;background:{tokens['hero_overlay']};position:relative}}
.hero::before{{content:'';position:absolute;inset:0;background:url('{photo_url}') center/cover no-repeat;z-index:-1}}
.hero-content{{max-width:720px}}
.hero-content .category{{font-size:.85rem;text-transform:uppercase;letter-spacing:4px;opacity:.7;margin-bottom:1rem;font-weight:600}}
.hero-content h1{{font-family:var(--font-heading);font-weight:{tokens['heading_weight']};font-size:clamp(2.5rem,6vw,4.5rem);margin-bottom:1rem;letter-spacing:-1px;line-height:1.1}}
.hero-content .sub{{font-size:1.15rem;opacity:.88;max-width:560px;margin:0 auto 2rem;line-height:1.7}}
.hero-content .hero-cta{{display:inline-block;background:var(--primary);color:#fff;padding:1rem 2.5rem;border-radius:var(--radius-pill);font-size:1.05rem;font-weight:600;text-decoration:none;transition:all .25s;border:2px solid var(--primary)}}
.hero-content .hero-cta:hover{{background:transparent;color:#fff;border-color:#fff;transform:scale(1.05)}}
.rating-badge{{display:inline-flex;align-items:center;gap:.5rem;background:rgba(255,255,255,.12);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.2);padding:.6rem 1.4rem;border-radius:var(--radius-pill);font-size:.95rem;margin-top:1.5rem}}
.rating-badge .stars{{color:#fbbf24;font-size:1.15rem}}

/* Hero animations */
.hero-content .category{{opacity:0;transform:translateY(20px);animation:fadeUp .6s ease .2s forwards}}
.hero-content h1{{opacity:0;transform:translateY(20px);animation:fadeUp .6s ease .35s forwards}}
.hero-content .sub{{opacity:0;transform:translateY(20px);animation:fadeUp .6s ease .5s forwards}}
.hero-content .hero-cta{{opacity:0;transform:translateY(20px);animation:fadeUp .6s ease .65s forwards}}
.rating-badge{{opacity:0;transform:translateY(20px);animation:fadeUp .6s ease .8s forwards}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:translateY(0)}}}}

/* === SECTIONS === */
section{{padding:5rem 2rem}}
section.alt{{background:var(--bg-alt)}}
.container{{max-width:var(--max-w);margin:0 auto}}
.section-header{{text-align:center;margin-bottom:3rem}}
.section-header h2{{font-family:var(--font-heading);font-weight:{tokens['heading_weight']};font-size:clamp(1.8rem,4vw,2.5rem);color:var(--text);margin-bottom:.75rem}}
.section-header p{{color:var(--text-muted);font-size:1.05rem;max-width:550px;margin:0 auto}}

/* === CARDS === */
.info-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.5rem}}
.info-card{{background:var(--bg);border-radius:var(--radius);padding:2rem;box-shadow:var(--shadow);transition:all .3s ease;text-align:center}}
.info-card:hover{{transform:translateY(-6px);box-shadow:var(--shadow-hover)}}
.info-card .icon{{font-size:2.5rem;margin-bottom:1rem}}
.info-card h3{{font-size:1.05rem;margin-bottom:.5rem;color:var(--text)}}
.info-card p,.info-card li{{color:var(--text-muted);font-size:.95rem}}
.info-card a{{color:var(--primary);text-decoration:none;font-weight:500}}
.info-card a:hover{{text-decoration:underline}}
.hours-list{{list-style:none;text-align:left;padding-left:.5rem}}
.hours-list li{{padding:.25rem 0;border-bottom:1px solid rgba(0,0,0,.04);font-size:.9rem}}

/* === MAP === */
.map-wrap{{border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);margin-top:2rem}}
.map-wrap iframe{{width:100%;height:400px;border:0}}

/* === REVIEWS === */
.review-highlight{{background:var(--bg);border-radius:var(--radius);padding:3rem;box-shadow:var(--shadow);text-align:center;max-width:500px;margin:0 auto}}
.review-highlight .big-rating{{font-size:4.5rem;font-weight:800;color:var(--text);line-height:1}}
.review-highlight .big-stars{{color:#fbbf24;font-size:2rem;margin:.75rem 0}}
.review-highlight .review-count{{color:var(--text-muted);font-size:1rem}}

/* === CTA === */
.cta-section{{background:{tokens['gradient']};color:#fff;text-align:center;padding:5rem 2rem}}
.cta-section h2{{font-family:var(--font-heading);font-weight:{tokens['heading_weight']};font-size:clamp(1.8rem,4vw,2.8rem);margin-bottom:1rem}}
.cta-section p{{opacity:.85;max-width:520px;margin:0 auto 2rem;font-size:1.1rem;line-height:1.7}}
.cta-btn{{display:inline-block;background:#fff;color:var(--primary-dark);padding:1rem 2.5rem;border-radius:var(--radius-pill);font-size:1.05rem;font-weight:700;text-decoration:none;transition:all .25s;box-shadow:0 4px 16px rgba(0,0,0,.15)}}
.cta-btn:hover{{transform:scale(1.05);box-shadow:0 8px 24px rgba(0,0,0,.2)}}

/* Pulse animation on CTA */
@keyframes pulse{{0%,100%{{box-shadow:0 0 0 0 rgba(255,255,255,.3)}}50%{{box-shadow:0 0 0 12px rgba(255,255,255,0)}}}}
.cta-btn{{animation:pulse 2.5s ease infinite}}

/* === FOOTER === */
footer{{text-align:center;padding:2.5rem;font-size:.85rem;color:var(--text-muted);border-top:1px solid rgba(0,0,0,.06)}}
footer a{{color:var(--primary);text-decoration:none;font-weight:500}}

/* === SCROLL ANIMATIONS === */
.animate-in{{opacity:0;transform:translateY(24px);transition:opacity .6s ease,transform .6s ease}}
.animate-in.visible{{opacity:1;transform:translateY(0)}}
.animate-in:nth-child(2){{transition-delay:.1s}}
.animate-in:nth-child(3){{transition-delay:.2s}}
.animate-in:nth-child(4){{transition-delay:.3s}}

/* === MOBILE === */
.mobile-cta{{display:none}}

@media(max-width:768px){{
  .nav-links{{position:fixed;top:0;right:-100%;width:280px;height:100vh;background:var(--bg);flex-direction:column;padding:5rem 2rem 2rem;box-shadow:-4px 0 24px rgba(0,0,0,.1);transition:right .3s ease;gap:1.5rem}}
  .nav-links.open{{right:0}}
  .nav-links a{{font-size:1.1rem}}
  .hamburger{{display:flex}}
  .hero{{min-height:90vh;padding:5rem 1.5rem 3rem}}
  .hero-content h1{{font-size:clamp(2rem,8vw,3rem)}}
  section{{padding:3.5rem 1.5rem}}
  .info-grid{{grid-template-columns:1fr}}
  .map-wrap iframe{{height:280px}}
  .mobile-cta{{display:flex;position:fixed;bottom:0;left:0;right:0;background:var(--primary);color:#fff;text-decoration:none;font-weight:700;font-size:1rem;justify-content:center;align-items:center;padding:1rem;z-index:99;gap:.5rem;box-shadow:0 -4px 16px rgba(0,0,0,.1)}}
}}
</style>
</head>
<body>

<!-- Nav -->
<nav class="nav">
  <div class="nav-inner">
    <a href="#" class="nav-brand">{html.escape(name)}</a>
    <div class="nav-links" id="navLinks">
      <a href="#about">About</a>
      <a href="#contact">Contact</a>
      <a href="#reviews">Reviews</a>
      {f'<a href="tel:{phone_tel}" class="nav-cta">Call Now</a>' if phone_tel else ''}
    </div>
    <div class="hamburger" id="hamburger" onclick="document.getElementById('navLinks').classList.toggle('open')">
      <span></span><span></span><span></span>
    </div>
  </div>
</nav>

<!-- Hero -->
<section class="hero">
  <div class="hero-content">
    <p class="category">{html.escape(btype)}</p>
    <h1>{html.escape(headline)}</h1>
    <p class="sub">{html.escape(subheadline)}</p>
    {f'<a href="tel:{phone_tel}" class="hero-cta">{cta_label}: {phone_display}</a>' if phone_tel else ''}
    {f'<div class="rating-badge"><span class="stars">{stars_html}</span><span>{rating} · {review_count} reviews on Google</span></div>' if rating else ''}
  </div>
</section>

<!-- About / Info -->
<section id="about">
  <div class="container">
    <div class="section-header animate-in">
      <h2>Visit {html.escape(name)}</h2>
      <p>{html.escape(btype)} proudly serving the Miami community.</p>
    </div>
    <div class="info-grid">
      {f"""<div class="info-card animate-in">
        <div class="icon">📍</div>
        <h3>Location</h3>
        <p>{html.escape(address)}</p>
      </div>""" if address else ''}
      {f"""<div class="info-card animate-in">
        <div class="icon">📞</div>
        <h3>Call Us</h3>
        <p><a href="tel:{phone_tel}">{phone_display}</a></p>
      </div>""" if phone_tel else ''}
      {f"""<div class="info-card animate-in">
        <div class="icon">⭐</div>
        <h3>Google Rating</h3>
        <p>{rating} out of 5 — {review_count} reviews</p>
      </div>""" if rating else ''}
      {hours_html}
      {website_html}
    </div>
  </div>
</section>

<!-- Map -->
<section class="alt" id="contact">
  <div class="container">
    <div class="section-header animate-in">
      <h2>Find Us</h2>
      <p>Stop by anytime — we'd love to see you.</p>
    </div>
    <div class="map-wrap animate-in">
      {f'<iframe src="https://www.google.com/maps/embed/v1/place?key={api_key}&q=place_id:{place_id}" allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>' if place_id else ''}
    </div>
  </div>
</section>

<!-- Reviews -->
{f"""<section id="reviews">
  <div class="container">
    <div class="section-header animate-in">
      <h2>What Customers Are Saying</h2>
      <p>Don't just take our word for it.</p>
    </div>
    <div class="review-highlight animate-in">
      <div class="big-rating">{rating}</div>
      <div class="big-stars">{stars_html}</div>
      <p class="review-count">Based on {review_count} Google reviews</p>
    </div>
  </div>
</section>""" if rating else ''}

<!-- CTA -->
<section class="cta-section">
  <h2 class="animate-in">{html.escape(cta_h)}</h2>
  <p class="animate-in">{cta_p}</p>
  {cta_btn}
</section>

<!-- Ready to Go Live -->
<section class="alt">
  <div class="container" style="text-align:center">
    <div class="section-header animate-in">
      <h2>Want a Website Like This?</h2>
      <p>This is a free demo from CRRE Labs. We build professional websites for Miami businesses — fast, affordable, and designed to bring in customers.</p>
    </div>
    <a href="mailto:carlos@crrelabs.com?subject=I want my website - {html.escape(name)}" class="cta-btn animate-in" style="background:var(--primary);color:#fff">Get Your Website →</a>
  </div>
</section>

<footer>
  <p>Website by <a href="https://crrelabs.com">CRRE Labs</a> · Miami, FL</p>
</footer>

{mobile_cta}

<script>
// Sticky nav shrink
const nav = document.querySelector('.nav');
window.addEventListener('scroll', () => {{
  nav.classList.toggle('scrolled', window.scrollY > 60);
}});

// Scroll reveal
const observer = new IntersectionObserver((entries) => {{
  entries.forEach(entry => {{
    if (entry.isIntersecting) {{
      entry.target.classList.add('visible');
    }}
  }});
}}, {{ threshold: 0.1 }});
document.querySelectorAll('.animate-in').forEach(el => observer.observe(el));

// Close mobile nav on link click
document.querySelectorAll('#navLinks a').forEach(a => {{
  a.addEventListener('click', () => document.getElementById('navLinks').classList.remove('open'));
}});

// Close mobile nav on outside click
document.addEventListener('click', (e) => {{
  const nav = document.getElementById('navLinks');
  const hamburger = document.getElementById('hamburger');
  if (!nav.contains(e.target) && !hamburger.contains(e.target)) {{
    nav.classList.remove('open');
  }}
}});
</script>
</body>
</html>'''

def refresh_site(site_dir: Path) -> bool:
    """Refresh a single site from v1 to v2."""
    index_path = site_dir / 'index.html'
    if not index_path.exists():
        return False
    
    content = index_path.read_text()
    
    # Skip if already v2 (has nav element)
    if '<nav class="nav">' in content:
        return False
    
    data = extract_data(content)
    if not data.get('name'):
        return False
    
    # Backup v1
    backup_path = site_dir / 'index.v1.html'
    if not backup_path.exists():
        backup_path.write_text(content)
    
    # Generate v2
    v2_html = generate_v2(data)
    index_path.write_text(v2_html)
    return True

def main():
    dirs = sorted([
        d for d in DEMOS_DIR.iterdir()
        if d.is_dir() and (d / 'index.html').exists()
    ])
    
    # If specific sites passed as args, only do those
    if len(sys.argv) > 1:
        targets = set(sys.argv[1:])
        dirs = [d for d in dirs if d.name in targets]
    
    refreshed = 0
    skipped = 0
    errors = []
    
    for d in dirs:
        try:
            if refresh_site(d):
                refreshed += 1
                print(f'✅ {d.name}')
            else:
                skipped += 1
                print(f'⏭️  {d.name} (already v2 or no data)')
        except Exception as e:
            errors.append((d.name, str(e)))
            print(f'❌ {d.name}: {e}')
    
    print(f'\n--- Done: {refreshed} refreshed, {skipped} skipped, {len(errors)} errors ---')

if __name__ == '__main__':
    main()
