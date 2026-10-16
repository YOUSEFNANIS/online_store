# Marketplace Website — Visual Identity

## Recommended Palette (Trust-first)

| Role | Color | Hex |
|------|-------|-----|
| Primary | Deep Blue | `#1A56DB` |
| CTA / Buy buttons | Orange | `#F97316` |
| Background | Off-white | `#F9FAFB` |
| Surface / Cards | White | `#FFFFFF` |
| Text (primary) | Near-black | `#111827` |
| Text (secondary) | Gray | `#6B7280` |
| Borders | Light gray | `#E5E7EB` |
| Success / Price drop | Green | `#16A34A` |
| Error / Urgency | Red | `#DC2626` |

## Alternative Palettes

### Warm (Amazon style)
- Header/Nav: `#131921`
- Accent/CTA: `#FF9900`

### Modern (Etsy style)
- Brand: `#E85D3D` (terracotta) or `#6D28D9` (violet)
- Everything else neutral grays

## Rules

1. Keep the UI ~90% neutral — let product images carry the color.
2. Use **one** CTA color, only for buy/cart actions.
3. Reserve green for success, red for errors — never as brand colors.
4. Minimum contrast ratio 4.5:1 for text (darken orange when used as text).

## CSS Variables

```css
:root {
  --color-primary: #1A56DB;
  --color-cta: #F97316;
  --color-bg: #F9FAFB;
  --color-surface: #FFFFFF;
  --color-text: #111827;
  --color-text-muted: #6B7280;
  --color-border: #E5E7EB;
  --color-success: #16A34A;
  --color-error: #DC2626;
}
```
