#!/usr/bin/env python3
"""
Convert WordPress HTML bodies in posts to Markdown.

Idempotent: leaves existing fenced code blocks, <figure class="image-gallery">,
and <aside class="info-block"> blocks untouched.

Per-post backup is written as `index.md.bak` on first conversion.
Front matter (JSON, unfenced) is preserved verbatim.

Usage:
    python scripts/html_to_markdown.py                       # convert every post
    python scripts/html_to_markdown.py --dry-run             # show what would change
    python scripts/html_to_markdown.py --report-langs        # print code-block language report
    python scripts/html_to_markdown.py path/to/index.md ...  # convert specific posts
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "content" / "posts"

# Placeholder format: must survive markdownify intact.
PLACEHOLDER = "\x00PLACEHOLDER-{idx}\x00"
PLACEHOLDER_RE = re.compile(r"\x00PLACEHOLDER-(\d+)\x00")


# --- language detection ----------------------------------------------------

LANG_RULES: list[tuple[str, str]] = [
    # PHP first (the only one with a distinctive opening tag)
    (r"<\?php\b", "php"),
    # PowerShell: cmdlet style, variable usage (any kind), execution policy, splatting
    (
        r"(?m)(^|\s)(Get-|Set-|Install-|New-|Add-|Remove-|Import-Module|Enable-|Disable-|Restart-Service|Start-Service|Stop-Service|Read-Host|Connect-VIServer|Find-Module|Update-Module|Import-VApp|Find-Module|Set-PSRepository|Set-PowerCLIConfiguration|Set-ExecutionPolicy|Test-Path|Set-DhcpServer|Add-DhcpServer|Install-AdcsCert|Install-WindowsFeature|Set-MacLearn|Get-MacLearn|Get-DnsClient|Install-ADDSForest|Set-Service|Get-Module)\w*",
        "powershell",
    ),
    (r"(?m)^\s*\$\w+(\.\w+)*\s*(=|\.)", "powershell"),  # $var = ... or $var.member access
    (r"(?m)^\s*\$\w+\s*$", "powershell"),  # bare $var (REPL inspect)
    # Apache config
    (
        r"(?m)^\s*<Directory\b|^\s*RewriteCond\b|^\s*RewriteRule\b|^\s*AllowOverride\b|^\s*Require\s+all\b",
        "apacheconf",
    ),
    # crontab
    (r"(?m)^\s*(\*|\d+(,\d+)*|\*/\d+)\s+(\*|\d+|\*/\d+)\s+\S+\s+\S+\s+\S+\s+\S", "crontab"),
    # ESXi-specific shell first (kept distinct from generic bash)
    (r"(?m)^\s*(esxcli|esxcfg-|vmkfstools|partedUtil|vdq|chkconfig)\b", "shell"),
    (r"(?m)^\s*/etc/init\.d/", "shell"),
    # Generic Linux/macOS shell
    (
        r"(?m)^\s*(sudo|apt-get|apt|yum|brew|curl|systemctl|chmod|chown|wget|tar|cp|mv|rm|ls|cat|cd|mkdir|crontab|phpenmod|a2enmod|a2ensite|mysql|mysql_secure_installation|vim|vi|nano|less|reboot|shutdown|echo|eval|tee|pwsh|ovpn-init|umount|mount|pwd|grep|sed|awk|find|export|source|\./)",
        "bash",
    ),
    (r"(?m)^\s*[A-Za-z]\S*\.(sh|pl)\b", "bash"),  # ./vmware-install.pl etc
    (r"(?m)^\s*get\s+logical-router", "bash"),  # NSX-T CLI
    # Windows batch / DOS — case-insensitive for the .EFI / .exe tools
    (r"(?im)^\s*(md|xcopy|del|ren|copy)\b", "batch"),
    (r"(?im)^\s*\w+\.(EFI|exe)\b", "batch"),
    (
        r"(?m)^\s*(AMIDEDOS|esentutl|ntdsutil|activate\s+instance|compact\s+to|files|quit)\b",
        "batch",
    ),
]

# Tags we treat as "recognised". Anything else we leave untagged and surface to the user.
RECOGNISED_LANGS = {
    "powershell",
    "bash",
    "shell",
    "batch",
    "php",
    "apacheconf",
    "crontab",
    "yaml",
    "ini",
    "properties",
    "json",
    "xml",
    "html",
    "css",
    "javascript",
    "python",
    "text",
}


def detect_lang(code: str) -> str:
    for pattern, lang in LANG_RULES:
        if re.search(pattern, code):
            return lang
    # Fallback: "text" renders as a plain monospace block (no highlighting).
    # Right call for command output, file paths, config snippets, vim keystrokes.
    return "text"


# --- HTML preprocessing ----------------------------------------------------


def post_process_md(text: str) -> str:
    """Final cleanup on the Markdown output: nbsp -> regular space."""
    return text.replace(" ", " ")


def split_frontmatter(content: str) -> tuple[str | None, str]:
    """Extract a JSON-object front matter from the start of the file."""
    if not content.startswith("{"):
        return None, content
    depth = 0
    in_str = False
    esc = False
    for i, c in enumerate(content):
        if esc:
            esc = False
            continue
        if in_str:
            if c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return content[: i + 1], content[i + 1 :]
    return None, content


# --- block protection ------------------------------------------------------


def protect_blocks(body: str) -> tuple[str, list[str]]:
    """Stash blocks we never want markdownify to touch.

    Stashed:
      * fenced code blocks (```lang ... ```), already-Markdown
      * <figure class="image-gallery">...</figure>
      * <aside class="info-block">...</aside>
      * top-level <figure>...</figure> wrappers (already-converted images)
    """
    stash: list[str] = []

    def replace(match: re.Match) -> str:
        stash.append(match.group(0))
        return PLACEHOLDER.format(idx=len(stash) - 1)

    # NOTE: order matters — fenced blocks first so we don't munge ``` inside HTML.
    body = re.sub(r"```[^\n]*\n.*?\n```", replace, body, flags=re.DOTALL)
    body = re.sub(
        r'<figure class="image-gallery">.*?</figure>',
        replace,
        body,
        flags=re.DOTALL,
    )
    body = re.sub(
        r'<aside class="(?:info-block|warning-block|note-block)">.*?</aside>',
        replace,
        body,
        flags=re.DOTALL,
    )
    return body, stash


def restore_blocks(body: str, stash: list[str]) -> str:
    def repl(m: re.Match) -> str:
        return stash[int(m.group(1))]

    return PLACEHOLDER_RE.sub(repl, body)


# --- markdownify customization --------------------------------------------


class WPConverter(MarkdownConverter):
    """Tighten markdownify output for the WP HTML we have."""

    def __init__(self, code_block_log: list[dict] | None = None, **opts):
        super().__init__(**opts)
        self._code_log = code_block_log

    def convert_pre(self, el, text, parent_tags):
        raw = el.get_text()
        raw = raw.replace("\r\n", "\n").rstrip("\n")
        lang = detect_lang(raw)
        if self._code_log is not None:
            self._code_log.append({"lang": lang, "code": raw})
        return f"\n\n```{lang}\n{raw}\n```\n\n"

    def convert_img(self, el, text, parent_tags):
        src = el.get("src", "")
        alt = (el.get("alt") or "").replace("\n", " ").strip()
        # markdown can't represent title sanely for our case; drop attrs
        return f"![{alt}]({src})"

    def convert_a(self, el, text, parent_tags):
        # Drop WP-style self-links to the same attachment
        # (`<a href="/uploads/x.png"><img src="/uploads/x.png">`).
        # Preserve outbound links (e.g., Credly badge → credly.com).
        href = el.get("href", "")
        imgs = el.find_all("img", recursive=False) or el.find_all("img")
        is_uploads_self_link = href.startswith(("/uploads/", "uploads/"))
        if len(imgs) == 1 and not el.get_text(strip=True) and is_uploads_self_link:
            return self.convert_img(imgs[0], "", parent_tags)
        return super().convert_a(el, text, parent_tags)

    def convert_blockquote(self, el, text, parent_tags):
        # Strip <p style="text-align: center;"> wrappers inside blockquotes
        for p in el.find_all("p"):
            if p.has_attr("style"):
                del p["style"]
        return super().convert_blockquote(el, text, parent_tags)


# --- driver ----------------------------------------------------------------


def is_already_markdown(body: str) -> bool:
    """Heuristic: if body has no raw HTML tags outside protected blocks, treat as done."""
    stripped, _ = protect_blocks(body)
    # any remaining HTML-ish tag suggests work to do
    return (
        re.search(r"<(p|h[1-6]|ul|ol|li|blockquote|strong|em|a|img|pre|figure|br|span)\b", stripped)
        is None
    )


def convert_body(body: str, code_log: list[dict] | None = None) -> str:
    body, stash = protect_blocks(body)

    converter = WPConverter(
        heading_style="ATX",
        bullets="-",
        code_language="",
        escape_asterisks=False,
        escape_underscores=False,
        code_block_log=code_log,
    )
    md = converter.convert(body)

    md = restore_blocks(md, stash)
    md = post_process_md(md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def process_file(path: Path, dry_run: bool, code_log: list[dict] | None) -> str:
    raw = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(raw)
    if fm is None:
        return f"[skip] {path.relative_to(REPO_ROOT)}: no JSON front matter"

    body_in = body.lstrip("\n")
    if is_already_markdown(body_in):
        return f"[skip] {path.relative_to(REPO_ROOT)}: already Markdown"

    body_out = convert_body(body_in, code_log=code_log)
    new = fm + "\n\n" + body_out

    if dry_run:
        return f"[dry-run] {path.relative_to(REPO_ROOT)}: would convert ({len(body_in)} -> {len(body_out)} chars)"

    backup = path.with_suffix(path.suffix + ".bak")
    if not backup.exists():
        backup.write_text(raw, encoding="utf-8")
    path.write_text(new, encoding="utf-8")
    return f"[ok]   {path.relative_to(REPO_ROOT)}: converted (backup -> {backup.name})"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("paths", nargs="*", help="specific post files to convert")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--report-langs",
        action="store_true",
        help="print detected language for every code block instead of converting",
    )
    args = ap.parse_args(argv)

    if args.paths:
        targets = [Path(p).resolve() for p in args.paths]
    else:
        targets = sorted(POSTS_DIR.glob("*/index.md"))

    if args.report_langs:
        rows: list[tuple[str, str, str]] = []  # (post, lang, first_line)
        for path in targets:
            raw = path.read_text(encoding="utf-8")
            _, body = split_frontmatter(raw)
            if body is None:
                continue
            soup = BeautifulSoup(body, "html.parser")
            for pre in soup.find_all("pre"):
                code = pre.get_text().strip()
                lang = detect_lang(code)
                first = code.splitlines()[0] if code else ""
                rows.append((path.parent.name, lang or "?", first[:80]))
            # also scan existing fenced blocks
            for m in re.finditer(r"```([a-zA-Z]*)\n(.*?)\n```", body, re.DOTALL):
                rows.append((path.parent.name, m.group(1) or "?", m.group(2).splitlines()[0][:80]))

        if not rows:
            print("no code blocks found")
            return 0
        width = max(len(r[0]) for r in rows)
        for post, lang, first in rows:
            flag = "  AMBIGUOUS" if lang not in RECOGNISED_LANGS else ""
            print(f"{post:<{width}}  [{lang:>11}]  {first}{flag}")
        amb = sum(1 for r in rows if r[1] not in RECOGNISED_LANGS)
        print(f"\n{len(rows)} code blocks, {amb} ambiguous")
        return 0

    code_log: list[dict] = []
    for path in targets:
        print(process_file(path, args.dry_run, code_log))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
