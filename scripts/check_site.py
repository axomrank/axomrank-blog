"""Validate local links and fragments in a generated site, without making requests."""
import argparse
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = set()
        self.links = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for name in ("href", "src"):
            if attrs.get(name):
                self.links.append((self.getpos()[0], attrs[name]))


def check(root, base_url):
    base = urlsplit(base_url.rstrip("/") + "/")
    pages = {p: Page(p) for p in root.rglob("*.html")}
    errors = []
    for file, page in pages.items():
        path = file.relative_to(root).as_posix()
        url = urljoin(base.geturl(), path.removesuffix("index.html"))
        for line, link in page.links:
            target = urlsplit(urljoin(url, link))
            if (target.scheme, target.netloc) != (base.scheme, base.netloc):
                continue
            if not target.path.startswith(base.path):
                continue  # Another GitHub Pages site may share this hostname.
            relative = unquote(target.path.removeprefix(base.path))
            relative_path = PurePosixPath(relative)
            if relative_path.is_absolute() or ".." in relative_path.parts:
                errors.append(f"{path}:{line}: {link}")
                continue
            dest = root / relative_path
            if dest.is_dir():
                dest /= "index.html"
            if not dest.is_file() or (target.fragment and dest in pages and unquote(target.fragment) not in pages[dest].ids):
                errors.append(f"{path}:{line}: {link}")
    return pages, errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_url")
    parser.add_argument("--root", type=Path, default=Path("_site"))
    args = parser.parse_args()
    pages, errors = check(args.root, args.base_url)
    if errors:
        raise SystemExit("\n".join(errors))
    if not pages:
        raise SystemExit(f"No HTML pages to check in {args.root}")
    print(f"Checked local links on {len(pages)} HTML pages")
