"""Generate portable, responsive WebP copies without changing catalog URLs."""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageOps

root = Path(__file__).resolve().parents[1]
source = root / "public/bijoux"
output = source / "responsive"
output.mkdir(exist_ok=True)
manifest = {}
original_bytes = 0
variant_bytes = 0
for path in sorted(source.rglob("*")):
    if not path.is_file() or output in path.parents or path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        continue
    url = "/" + path.relative_to(root / "public").as_posix()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    with Image.open(path) as opened:
        image = ImageOps.exif_transpose(opened)
        image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
        variants = []
        for width in sorted({min(image.width, size) for size in (160, 480, 800, 1200)}):
            height = max(1, round(image.height * width / image.width))
            name = f"{digest}-{width}.webp"
            target = output / name
            image.resize((width, height), Image.Resampling.LANCZOS).save(target, "WEBP", quality=80, method=6)
            variants.append({"src": f"/bijoux/responsive/{name}", "width": width, "height": height})
            if width == min(image.width, 480):
                variant_bytes += target.stat().st_size
        manifest[url] = variants
        original_bytes += path.stat().st_size
(root / "src/data/product-image-variants.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
print(f"{len(manifest)} images: originals {original_bytes:,} bytes; card variants {variant_bytes:,} bytes")