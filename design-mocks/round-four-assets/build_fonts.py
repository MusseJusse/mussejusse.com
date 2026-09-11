"""Rebuild round-four-assets/fonts.css as subsets of the exact characters used.

Run after build_round_four.py has produced round-four-directions.html:
    python3 design-mocks/round-four-assets/build_fonts.py
"""

import base64
import html
import pathlib
import re
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "round-four-directions.html"
OUT = ROOT / "round-four-assets" / "fonts.css"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126 Safari/537.36"
)

FAMILIES = [
    "family=Fraunces:opsz,wght@9..144,300..900",
    "family=Libre+Franklin:wght@100..900",
    "family=Instrument+Serif:ital@0;1",
    "family=Gloock",
    "family=Cormorant+Garamond:wght@300..700",
    "family=Archivo:wght@100..900",
    "family=Space+Mono:wght@400;700",
]


def charset() -> str:
    doc = DOC.read_text()
    doc = re.sub(r"<style>.*?</style>", "", doc, flags=re.S)
    doc = re.sub(r"<script>.*?</script>", "", doc, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", "", doc))
    chars = set(text) - set("\n\r\t")
    for c in "0123456789:;.,()[]{}&%+-/#'\"\u2013\u2014\u00b7\u00d7\u00b0\u221e":
        chars.add(c)
    return "".join(sorted(chars))


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req).read()


def main() -> None:
    chars = charset()
    print(f"{len(chars)} unique characters")
    blocks = []
    for query in FAMILIES:
        url = "https://fonts.googleapis.com/css2?" + query + "&text=" + urllib.parse.quote(chars)
        css = fetch(url).decode()
        for remote in set(re.findall(r"url\((https://[^)]+)\)", css)):
            data = base64.b64encode(fetch(remote)).decode()
            css = css.replace(
                f"url({remote}) format('woff2')",
                f"url(data:font/woff2;base64,{data}) format('woff2')",
            )
        name = re.search(r"font-family: '([^']+)'", css).group(1)
        weight = ",".join(re.findall(r"font-weight: ([\d ]+);", css))
        print(f"{name:20} {weight:12} {len(css) // 1024:3} KB")
        blocks.append(css.rstrip())
    OUT.write_text("\n".join(blocks) + "\n")
    print(f"{OUT} written, {OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
