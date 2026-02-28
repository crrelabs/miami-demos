# CRRE Labs Demo Site Framework v2

> Follow this pipeline for EVERY demo site build. The goal: sites that look like $5K custom builds, not templates.

---

## Pipeline Overview

Each demo site goes through 5 phases. Don't skip any.

### Phase 1: Architecture & Content Strategy

Before writing any HTML, plan the site structure for this specific business.

**Think through:**
- What does this business type need? (booking? menu? gallery? services list?)
- What are the 3 most likely user journeys? (e.g., "find hours" → "see services" → "call/book")
- What sections make sense? Not every business needs the same layout.

**Section inventory (pick what fits):**
- Hero with value proposition (NOT just the business name)
- Services/menu/offerings grid
- About/story section (even 2 sentences of personality helps)
- Social proof (Google rating, review count, testimonials)
- Gallery/portfolio (if visual business)
- Location + hours + contact
- FAQ (if service business)
- CTA section

**Key rule:** The hero headline should be a VALUE PROPOSITION, not just the business name.
- ❌ "Acqua Nails & Wax"
- ✅ "Miami's Premier Nail Experience — Walk-Ins Welcome"

### Phase 2: Design System (Per Business Category)

Use a CONSISTENT design system based on business category. Don't randomly pick colors.

**Design tokens by category:**

#### Restaurants / Food
- Primary: warm tones (amber, terracotta, deep red)
- Font pairing: Display serif (Playfair/Cormorant) + clean sans (Inter/DM Sans)
- Mood: warm, inviting, appetizing
- Hero style: full-bleed food photography with dark overlay

#### Beauty / Wellness / Salon
- Primary: soft luxe (rose gold, champagne, soft pink, deep plum)
- Font pairing: Elegant serif (Cormorant Garamond) + light sans (Nunito/Poppins)
- Mood: luxurious, clean, relaxing
- Hero style: gradient or soft image with generous whitespace

#### Auto / Mechanical / Trade Services
- Primary: bold industrial (deep blue, orange, charcoal, red)
- Font pairing: Bold sans (Montserrat/Raleway 800) + body sans (Inter)
- Mood: trustworthy, professional, strong
- Hero style: angled/geometric sections, bold typography

#### Retail / Shopping
- Primary: clean modern (black/white + one accent color from their branding if known)
- Font pairing: Modern sans (DM Sans/Plus Jakarta Sans) + mono accent
- Mood: curated, browsable, contemporary
- Hero style: product-forward, minimal

#### Professional Services (Insurance, Legal, Finance)
- Primary: corporate trust (navy, forest green, gold accents)
- Font pairing: Professional serif (Source Serif) + clean sans (Source Sans/Inter)
- Mood: established, credible, expert
- Hero style: subtle gradient, professional photography or pattern background

#### Health / Medical / Veterinary
- Primary: clinical calm (teal, soft blue, white, green accents)
- Font pairing: Friendly sans (Nunito/Rubik) + body (Inter)
- Mood: caring, professional, reassuring
- Hero style: light and airy, soft imagery

**Universal design rules:**
- 8px spacing grid (all spacing in multiples of 8)
- Typography scale: 0.875rem, 1rem, 1.125rem, 1.25rem, 1.5rem, 2rem, 2.5rem, 3rem, clamp() for hero
- Border radius: 12-16px for cards, 50px for buttons/badges
- Shadows: 0 4px 24px rgba(0,0,0,.06) for cards, 0 8px 32px rgba(0,0,0,.12) for elevated
- Max content width: 1200px (not 900px — use the space)
- Dark mode: not required for demos, but use dark sections for visual rhythm

### Phase 3: Conversion-Focused Copy

**Every section needs purposeful copy, not filler.**

**Hero formula:**
- Headline (6-8 words): Lead with what the customer gets
- Subheadline (12-18 words): Expand with specificity (location, specialty, differentiator)
- CTA: Action-oriented ("Book Your Appointment" not "Contact Us")

**Services section:**
- Don't just list services — add a one-line benefit for each
- Use icons or emojis as visual anchors

**Social proof section:**
- Pull real Google rating + review count
- If 4.5+, make it prominent. If lower, downplay but don't hide.
- Add "Trusted by X+ customers" or "Serving [area] since [year]" if known

**CTA section:**
- Create urgency or lower friction: "Same-Day Appointments Available" / "Free Estimates" / "Walk-Ins Welcome"
- Phone number should be tap-to-call on mobile
- If they have Google Maps presence, link to directions

### Phase 4: Animations & Interactions

**Every site MUST include these micro-interactions:**

**Scroll reveal (use IntersectionObserver):**
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.1 });
document.querySelectorAll('.animate-in').forEach(el => observer.observe(el));
```

**Required interactions:**
- Hero content: fade-up on load (0.6s, stagger title/subtitle/CTA by 0.15s)
- Cards: fade-up on scroll, stagger by 0.1s each
- Cards: subtle lift on hover (translateY(-6px), box-shadow increase)
- Buttons: scale(1.05) on hover with color shift
- Navigation: sticky header that shrinks on scroll (80px → 60px)
- Phone numbers: pulse/glow animation on CTA buttons
- Images: subtle scale on hover (1.02-1.05)

**Nice-to-have (for higher-value businesses with 200+ reviews):**
- Parallax on hero background
- Counter animation for stats (review count, years in business)
- Smooth scroll between sections
- Typed text effect on hero headline

### Phase 5: Responsive Behavior

**Breakpoints:**
- Mobile: 375px (primary — design mobile-first)
- Tablet: 768px
- Desktop: 1024px+

**Rules:**
- Hero headline: clamp(2rem, 6vw, 4.5rem)
- Navigation: hamburger on mobile, full horizontal on desktop
- Card grids: 1 col mobile → 2 col tablet → 3 col desktop
- Section padding: 3rem 1.5rem mobile → 5rem 2rem desktop
- CTA buttons: full width on mobile, auto on desktop
- Phone number: prominent sticky bottom bar or floating button on mobile
- Tap targets minimum 44px
- FAQ: accordion on mobile

---

## Quality Checklist (Before Deploying)

- [ ] Hero has a value proposition headline (not just business name)
- [ ] Design system matches business category (colors, fonts, mood)
- [ ] At least 3 distinct sections with visual rhythm (alternate backgrounds)
- [ ] Scroll animations on all cards and sections
- [ ] Sticky navigation with shrink effect
- [ ] Tap-to-call on all phone numbers
- [ ] Google Maps embed with styled container
- [ ] CTA section with action-oriented button text
- [ ] Mobile responsive — tested at 375px
- [ ] Page loads fast (vanilla CSS/JS only — no frameworks)
- [ ] Google Fonts loaded with display=swap
- [ ] Proper meta tags (title, description, viewport)
- [ ] "Website by CRRE Labs" footer link

---

## Anti-Patterns (Don't Do These)

- ❌ Same color scheme for every site
- ❌ "Welcome to [Business Name]" as the hero headline
- ❌ Generic descriptions that could apply to any business
- ❌ No animations (static pages feel cheap)
- ❌ Tiny max-width that wastes screen space
- ❌ Contact section without tap-to-call
- ❌ Missing mobile hamburger menu
- ❌ All sections same white background (no visual rhythm)
- ❌ Stock photos when Google Places photos are available
