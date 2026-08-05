---
brand_id: stripe
kind: brand
summary: Stripe brand identity - elegant diagonal color mesh gradients, clean light/dark interfaces, Indigo primary, premium commercial aesthetic.
primary_color: "#635BFF"
---

# Stripe Brand Specification

> Identity-only preset. No SVG page roster — pages are composed freely under these constraints.

## I. Brand Overview

| Property | Value |
|---|---|
| Brand Name | Stripe |
| Use Cases | Business plans, financial reports, developer API slides, startup pitch decks, marketing and product launches |
| Tone | Professional, elegant, premium, clean, commercial, developers-first |

## II. Color Scheme

Stripe style supports 3 primary palettes (light, dark, and deep indigo mesh). The Strategist should pick one and write it to `spec_lock.colors`.

### 1. Palette Options

| Palette | background | primary | secondary | accent | secondary_accent | body_text |
|---|---|---|---|---|---|---|
| **Stripe Light** (默认浅色) | `#F8F9FC` | `#0A2540` | `#4F5B66` | `#635BFF` | `#00D4B2` | `#3C4257` |
| **Stripe Indigo** (炫彩深蓝) | `#0A2540` | `#FFFFFF` | `#ADBDCC` | `#635BFF` | `#00D4B2` | `#E3E8EE` |
| **Stripe Midnight** (极深黑灰) | `#1A1F36` | `#F8F9FC` | `#A3ACD0` | `#635BFF` | `#FF5C93` | `#D9E2EC` |

### 2. Element Color Assignment
- `background`: Stripe Light off-white or Midnight Indigo.
- `primary`: Deep dark blue (`#0A2540`) or pure white, representing corporate trustworthiness.
- `secondary`: Slate gray for secondary typography.
- `accent`: Stripe Indigo (`#635BFF`) representing payments and technology.
- `body_text`: Neutral readable dark slate or light silver.

---

## III. Typography

| Role | Family | Weight | Notes |
|---|---|---|---|
| title | `"Inter", "Segoe UI", "Noto Sans SC", sans-serif` | 300 / 400 | Light weights for a modern tech feel |
| body | `"Inter", "Segoe UI", "Noto Sans SC", sans-serif` | 400 | Highly readable sans-serif |
| meta | `"JetBrains Mono", monospace` | 400 | Monospaced tags for APIs and data |

---

## IV. Voice & Tone

- **Style**: Clear, structured, data-driven narrative with precise numbers and units.
- **Visuals**: Beautiful card components (`rx="8"`, `box-shadow="0 4px 6px rgba(50,50,93,0.11)"`), diagonal dividers or slanted background mesh lines (10-15 degree angle).
- **Backgrounds**: Mesh gradients generated via background images.
