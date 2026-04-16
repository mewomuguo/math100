"""
產生 PWA / Android App icon
- icon-192.png       (普通圖示, 192x192)
- icon-512.png       (普通圖示, 512x512)
- icon-maskable-512.png (Adaptive icon, 內容置中於 80% 安全區)
- favicon.png        (小型, 用於瀏覽器 tab)
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.dirname(os.path.abspath(__file__))

BG = "#3498db"        # 主藍色 (與網頁主色呼應)
ACCENT = "#27ae60"    # 綠色點綴
TEXT = "#ffffff"

def find_font(size):
    """找一個能顯示數字+符號的字體"""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def make_icon(size, maskable=False, filename=None):
    img = Image.new("RGBA", (size, size), BG)
    d = ImageDraw.Draw(img)

    # maskable 圖示需要把內容塞在中央 80% 區域 (Android Adaptive icon spec)
    inset = int(size * 0.10) if maskable else 0
    safe = size - 2 * inset
    cx = size // 2

    # 在背景畫淡淡的格子線(代表 100 格)
    grid_color = (255, 255, 255, 35)  # 半透明白
    grid_overlay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid_overlay)
    cell = safe // 10
    grid_origin = inset + (safe - cell * 10) // 2
    for i in range(11):
        x = grid_origin + i * cell
        gd.line([(x, grid_origin), (x, grid_origin + cell * 10)], fill=grid_color, width=2)
        gd.line([(grid_origin, x), (grid_origin + cell * 10, x)], fill=grid_color, width=2)
    img = Image.alpha_composite(img, grid_overlay)
    d = ImageDraw.Draw(img)

    # 主文字 "100"
    main_size = int(safe * 0.42)
    font_main = find_font(main_size)
    txt = "100"
    bbox = d.textbbox((0, 0), txt, font=font_main)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = cx - tw // 2 - bbox[0]
    ty = inset + safe // 2 - th // 2 - bbox[1] - int(safe * 0.05)
    # 文字陰影
    d.text((tx + 3, ty + 4), txt, fill=(0, 0, 0, 80), font=font_main)
    d.text((tx, ty), txt, fill=TEXT, font=font_main)

    # 下方一排小符號 + - × ÷
    sym_size = int(safe * 0.13)
    font_sym = find_font(sym_size)
    syms = "+−×÷"
    sym_y = inset + safe - int(safe * 0.18)
    spacing = safe // 5
    for i, s in enumerate(syms):
        sx = inset + spacing * (i + 1) - sym_size // 3
        d.text((sx, sym_y), s, fill=(255, 255, 255, 220), font=font_sym)

    if filename is None:
        suffix = "-maskable" if maskable else ""
        filename = f"icon{suffix}-{size}.png"
    out = os.path.join(OUT, filename)
    img.save(out, "PNG")
    print(f"  ✓ {filename}  ({size}x{size}{'  maskable' if maskable else ''})")

print("Generating icons:")
make_icon(192)
make_icon(512)
make_icon(512, maskable=True)
make_icon(64, filename="favicon.png")
print("Done.")
