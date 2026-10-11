"""Tách nhân vật khỏi nền trắng và cắt bảng nhân vật thành từng PNG trong suốt.

Cách dùng:
    python scripts/tach_nen.py anh.webp --grid 3x2 --names a,b,c,d,e,f --out assets/nhan-vat
Cần: pip install pillow numpy scipy
"""
import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage


def cutout(rgb: np.ndarray, diff_max=60, sat_max=14) -> np.ndarray:
    """Trả về alpha (0–255): nền trắng/xám nhạt nối với viền ảnh thành trong suốt."""
    r, g, b = (rgb[..., i].astype(int) for i in range(3))
    diff = 255 - np.minimum(np.minimum(r, g), b)          # độ xa so với màu trắng
    sat = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    # trắng, hoặc bóng đổ xám/nâu nhạt (độ bão hoà thấp; thân nhân vật bão hoà cao hơn nhiều)
    cand = ((diff < diff_max) & (sat < sat_max)) | ((diff < 80) & (sat < 30))
    labels, n = ndimage.label(cand)
    border = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    bg = np.isin(labels, border[border > 0])
    # khoảng trắng bị bao kín (vd. giữa tai nghe và đầu) cũng là nền, trừ đốm nhỏ như ánh mắt, răng
    if n:
        sizes = ndimage.sum(cand, labels, range(1, n + 1))
        mean_diff = ndimage.mean(diff, labels, range(1, n + 1))
        holes = 1 + np.flatnonzero((sizes > 250) & (mean_diff < 14))
        bg |= np.isin(labels, holes)
    fg = ~bg
    fg = ndimage.binary_opening(fg, iterations=1)          # bỏ đốm lẻ
    keep, n = ndimage.label(fg)                             # chỉ giữ các mảng đủ lớn
    if n:
        sizes = ndimage.sum(fg, keep, range(1, n + 1))
        fg = np.isin(keep, 1 + np.flatnonzero(sizes > 60))
    alpha = Image.fromarray((fg * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3))
    return np.array(alpha.filter(ImageFilter.GaussianBlur(0.8)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--grid", default="1x1", help="cột x hàng, ví dụ 3x2")
    ap.add_argument("--names", required=True, help="tên file, phân tách bằng dấu phẩy, theo thứ tự trái→phải, trên→dưới")
    ap.add_argument("--out", default=".")
    args = ap.parse_args()

    im = Image.open(args.image).convert("RGB")
    cols, rows = map(int, args.grid.lower().split("x"))
    names = args.names.split(",")
    W, H = im.size
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    for i, name in enumerate(names):
        c, r = i % cols, i // cols
        cell = im.crop((c * W // cols, r * H // rows, (c + 1) * W // cols, (r + 1) * H // rows))
        rgb = np.array(cell)
        rgba = np.dstack([rgb, cutout(rgb)])
        img = Image.fromarray(rgba, "RGBA")
        img = img.crop(img.getbbox())
        pad = 12
        canvas = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad))
        canvas.paste(img, (pad, pad))
        canvas.save(out / f"{name}.png")
        print("đã lưu", out / f"{name}.png", canvas.size)


if __name__ == "__main__":
    main()
