# Brand Assets Directory

This directory stores core brand logo assets for **PPT Master Plus**, including official vector SVG logo files and reference raster images.

## Available Logo Assets

### 1. Aliyun Official Logos (阿里云官方 LOGO)

| File Name | Format | Dimensions / viewBox | Description |
|-----------|--------|----------------------|-------------|
| `阿里云官方-中文LOGO.svg` | SVG (Vector) | `0 0 900 200` | Official Alibaba Cloud Chinese logo mark & logotype (Alibaba Cloud Orange `#FF6A00`) |
| `aliyun-logo-zh.svg` | SVG (Vector) | `0 0 900 200` | English filename alias for `阿里云官方-中文LOGO.svg` |
| `阿里云官方-英文LOGO.svg` | SVG (Vector) | `0 0 1590 200` | Official Alibaba Cloud English logo mark & logotype (`#FF6A00`) |
| `aliyun-logo-en.svg` | SVG (Vector) | `0 0 1590 200` | English filename alias for `阿里云官方-英文LOGO.svg` |
| `阿里云官方-中文LOGO.png` | PNG (Bitmap) | `900 x 200` | Original source bitmap for Chinese logo |
| `阿里云官方-英文LOGO.png` | PNG (Bitmap) | `1590 x 200` | Original source bitmap for English logo |

### 2. Aliyun Flink Combined Logos (阿里云 Realtime Compute / Flink 联合 LOGO)

| File Name | Format | Dimensions / viewBox | Description |
|-----------|--------|----------------------|-------------|
| `aliyun-flink-logo-zh.svg` | SVG (Vector) | `0 0 1200 200` | Aliyun Chinese Logo + Apache Flink Logo combined vector asset |
| `aliyun-flink-logo-en.svg` | SVG (Vector) | `0 0 1890 200` | Aliyun English Logo + Apache Flink Logo combined vector asset |
| `aliyun-flink-logo.svg` | SVG (Vector) | `0 0 1200 200` | Primary Aliyun Flink combined logo alias |
| `阿里云-Flink-LOGO.svg` | SVG (Vector) | `0 0 1200 200` | Chinese filename alias for Aliyun Flink combined logo |

---

## SVG Embedding Usage in Presentations

To embed these vector SVG logos directly in presentation slides, use standard `<image>` or `<use>` elements:

```xml
<!-- Example: Aliyun Chinese SVG Logo -->
<image href="assets/aliyun-logo-zh.svg" x="60" y="40" width="180" height="40"/>

<!-- Example: Aliyun Flink Combined SVG Logo -->
<image href="assets/aliyun-flink-logo-zh.svg" x="60" y="40" width="240" height="40"/>
```

Vector SVGs offer subpixel precision, crisp rendering across all screen resolutions, and full independence from resolution constraints when exported to PPTX or PDF.
