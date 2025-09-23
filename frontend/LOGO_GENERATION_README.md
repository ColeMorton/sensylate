# Logo Generation System - Quick Start

## What We Built

✅ **Complete brand logo generation system** that creates pixel-perfect logo images identical to your h1 brand-text "Cole Morton" using your existing photo booth infrastructure.

## Key Features

- 🎨 **Perfect accuracy**: Uses exact same CSS, fonts (Paytone One), and colors as header
- 📱 **Multiple formats**: PNG (with transparency) and SVG (scalable vector)
- 🖥️ **Multiple resolutions**: 150 DPI (web), 300 DPI (print), 600 DPI (ultra)
- 🌓 **Theme variants**: Light (`#1A1A1A`) and dark (`#F9FAFB`) versions
- 📐 **Multiple aspect ratios**: 16:9 (standard), 3:4 (portrait/social)
- 🤖 **Automated generation**: Complete logo sets with one command

## Quick Start

### 1. Start Development Server
```bash
cd frontend
yarn dev
```

### 2. Generate All Logo Variants
```bash
# From project root
python3 scripts/generate_logos.py
```

### 3. Find Your Logos
```bash
ls data/outputs/logos/
```

You'll get organized files like:
- `cole_morton_logo_light_300dpi_16x9.png` (standard use)
- `cole_morton_logo_dark_300dpi_16x9.png` (dark theme)
- `cole_morton_logo_light_300dpi_16x9.svg` (scalable vector)

## Files Created

1. **📄 Dashboard**: `src/content/dashboards/logo-generation.mdx`
2. **⚛️ Component**: `src/layouts/components/LogoDisplay.tsx`
3. **⚙️ Configuration**: Updated `src/config/photo-booth.json`
4. **🚀 Helper Script**: `scripts/generate_logos.py`
5. **📚 Documentation**: `docs/LOGO_GENERATION.md`

## Usage Options

### Quick Generation (Recommended)
```bash
python3 scripts/generate_logos.py
```

### Specific Variants
```bash
# PNG only at 300 DPI
python3 scripts/generate_logos.py --formats png --sizes 300

# Dark theme only  
python3 scripts/generate_logos.py --themes dark

# High resolution only
python3 scripts/generate_logos.py --sizes 600
```

### Manual via Photo Booth UI
1. Visit `http://localhost:4321/photo-booth`
2. Select "Logo Generation Dashboard"
3. Choose format/resolution/theme
4. Click "Export Dashboard"

### Direct API Call
```bash
curl -X POST http://localhost:4321/api/export-dashboard \
  -H "Content-Type: application/json" \
  -d '{
    "dashboard_id": "logo_generation",
    "mode": "light",
    "aspect_ratio": "16:9",
    "format": "png",
    "dpi": 300,
    "scale_factor": 3
  }'
```

## What You Get

Each generation creates **10 logo variants**:

| Variant | Format | DPI | Use Case |
|---------|--------|-----|----------|
| Web Light/Dark | PNG | 150 | Website, digital use |
| Print Light/Dark | PNG | 300 | Business cards, documents |
| Ultra Light/Dark | PNG | 600 | Large format, professional print |
| Vector Light/Dark | SVG | - | Scalable, web icons |
| Portrait Light/Dark | PNG | 300 | Social media, mobile |

## Next Steps

1. **Test the system**: Run `python3 scripts/generate_logos.py`
2. **Use your logos**: Copy from `data/outputs/logos/` to needed locations
3. **Integrate if desired**: Update `Logo.astro` to use image logos instead of text
4. **Regenerate when needed**: Re-run script after any brand styling changes

## Troubleshooting

- **Server not responding?** Check port with `lsof -i :4321 :4322 :4323`
- **Generation fails?** Run with `--verbose` flag for detailed logging
- **Need help?** See full documentation in `docs/LOGO_GENERATION.md`

---

**🎉 Ready to generate professional brand logos identical to your current design!**