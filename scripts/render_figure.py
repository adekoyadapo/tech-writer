#!/usr/bin/env python3
"""Render Opus-authored SVG figures to PNG/WebP or assemble SVG frames into a GIF."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def which(cmd: str) -> str | None:
    return shutil.which(cmd)


def rasterize_svg(svg: Path, dest: Path, width: int | None = None) -> None:
    """Rasterize SVG using rsvg-convert, ImageMagick, or cairosvg."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    rsvg = which("rsvg-convert")
    magick = which("magick") or which("convert")

    if rsvg:
        cmd = [rsvg, "-f", dest.suffix.lstrip("."), "-o", str(dest), str(svg)]
        if width:
            cmd[1:1] = ["-w", str(width)]
        # rsvg-convert uses -f png|pdf|... ; webp may not be supported
        fmt = dest.suffix.lstrip(".").lower()
        if fmt == "webp":
            png_tmp = dest.with_suffix(".png")
            cmd = [rsvg, "-f", "png", "-o", str(png_tmp), str(svg)]
            if width:
                cmd = [rsvg, "-w", str(width), "-f", "png", "-o", str(png_tmp), str(svg)]
            subprocess.run(cmd, check=True)
            _png_to_webp(png_tmp, dest)
            png_tmp.unlink(missing_ok=True)
            return
        if width:
            cmd = [rsvg, "-w", str(width), "-f", fmt, "-o", str(dest), str(svg)]
        else:
            cmd = [rsvg, "-f", fmt, "-o", str(dest), str(svg)]
        subprocess.run(cmd, check=True)
        return

    if magick:
        cmd = [magick, str(svg)]
        if width:
            cmd += ["-resize", f"{width}x"]
        cmd.append(str(dest))
        subprocess.run(cmd, check=True)
        return

    try:
        import cairosvg  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "No SVG rasterizer found. Install one of:\n"
            "  brew install librsvg\n"
            "  brew install imagemagick\n"
            "  pip install cairosvg\n"
            "SVG source was kept; raster output skipped."
        ) from exc

    output_width = width
    if dest.suffix.lower() == ".webp":
        png_tmp = dest.with_suffix(".png")
        cairosvg.svg2png(url=str(svg), write_to=str(png_tmp), output_width=output_width)
        _png_to_webp(png_tmp, dest)
        png_tmp.unlink(missing_ok=True)
    else:
        cairosvg.svg2png(url=str(svg), write_to=str(dest), output_width=output_width)


def _png_to_webp(png: Path, webp: Path) -> None:
    magick = which("magick") or which("convert")
    if magick:
        subprocess.run([magick, str(png), str(webp)], check=True)
        return
    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit("WebP conversion needs ImageMagick or Pillow.") from exc
    Image.open(png).save(webp, "WEBP", quality=85)


def cmd_still(args: argparse.Namespace) -> None:
    svg = Path(args.input).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(svg, out_dir / svg.name)
    fmt = args.format.lower().lstrip(".")
    dest = out_dir / f"{svg.stem}.{fmt}"
    try:
        rasterize_svg(svg, dest, width=args.width)
        print(f"SVG: {out_dir / svg.name}")
        print(f"RASTER: {dest}")
    except SystemExit as exc:
        print(f"SVG: {out_dir / svg.name}")
        print(f"RASTER: unavailable ({exc})")
        raise


def cmd_gif(args: argparse.Namespace) -> None:
    frames_dir = Path(args.frames_dir).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    svgs = sorted(frames_dir.glob("*.svg"))
    if len(svgs) < 2:
        raise SystemExit("Need at least 2 SVG frames in --frames-dir")

    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit("GIF assembly requires Pillow: pip install pillow") from exc

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        pngs: list[Path] = []
        for i, svg in enumerate(svgs):
            png = tmp_path / f"frame-{i:02d}.png"
            rasterize_svg(svg, png, width=args.width)
            pngs.append(png)
            # Keep SVG copies in out_dir/frames
            frame_out = out_dir / "frames"
            frame_out.mkdir(exist_ok=True)
            shutil.copy2(svg, frame_out / svg.name)

        images = [Image.open(p).convert("RGBA") for p in pngs]
        # Quantize with adaptive palette via Pillow
        gif_path = out_dir / (args.name or "figure.gif")
        base = images[0].convert("P", palette=Image.ADAPTIVE, colors=256)
        rest = [im.convert("P", palette=Image.ADAPTIVE, colors=256) for im in images[1:]]
        base.save(
            gif_path,
            save_all=True,
            append_images=rest,
            duration=args.duration_ms,
            loop=0,
            optimize=True,
        )
        size_mb = gif_path.stat().st_size / (1024 * 1024)
        print(f"GIF: {gif_path} ({size_mb:.2f} MiB)")
        if size_mb > 2.0:
            print("WARNING: GIF exceeds 2 MiB target; reduce frames or width.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    still = sub.add_parser("still", help="Rasterize one SVG")
    still.add_argument("--input", required=True)
    still.add_argument("--out-dir", required=True)
    still.add_argument("--format", default="webp", choices=["png", "webp"])
    still.add_argument("--width", type=int, default=1200)
    still.set_defaults(func=cmd_still)

    gif = sub.add_parser("gif", help="Assemble SVG frames into a GIF")
    gif.add_argument("--frames-dir", required=True)
    gif.add_argument("--out-dir", required=True)
    gif.add_argument("--width", type=int, default=800)
    gif.add_argument("--duration-ms", type=int, default=400)
    gif.add_argument("--name", default="figure.gif")
    gif.set_defaults(func=cmd_gif)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
