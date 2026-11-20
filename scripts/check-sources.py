#!/usr/bin/env python3
"""Source-integrity check for Financial Poem posts.

Why this exists: on 2026-11-19 the FOMC minutes review was written from the
*2025* minutes (fomcminutes20251029.htm) and published as the 2026 review.
Every headline fact was a year off. This script makes that class of error
fail loudly before publishing:

1. Anachronism lint (all posts, offline): officeholders are checked against
   term windows. E.g. "パウエル議長" in a post dated after Powell's chair
   term ended (2026-05-22) is an error.
2. Source metadata (required for event posts tagged fomc/minutes/earnings):
   the post must carry a <!-- source-check --> block declaring the primary
   source URL, the event date, the source's own date text, the chair, and
   the key numbers/phrases the article relies on.
3. Consistency (offline): the date embedded in the source URL must equal
   the declared event date; the declared chair must be the officeholder on
   the event date; the event must be fresh relative to the post date
   (a minutes/earnings review cannot be based on an event >45 days old).
4. Fetch verification (default; --offline skips): the primary source is
   downloaded and must contain its own date text, the chair's name, every
   must_number and every must_phrase. If the author pointed the metadata
   at the wrong year's document, the declared 2026 date text / numbers
   will not be found in it.

Usage:
    python3 scripts/check-sources.py [--offline] [post.md ...]
With no file arguments, all non-draft posts are checked.
Exit code 0 = all checks passed, 1 = at least one failure.
"""

import re
import sys
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "src" / "content" / "posts"

# --- Officeholder term windows -------------------------------------------
# (pattern in article text, person, role valid from, role valid until)
# Dates are the days the person actually held the role.
CHAIR_WINDOWS = [
    ("パウエル議長", "Jerome Powell", date(2018, 2, 5), date(2026, 5, 22)),
    ("ウォーシュ議長", "Kevin Warsh", date(2026, 5, 22), date(2030, 1, 1)),
    ("ウォルシュ議長", "Kevin Warsh", date(2026, 5, 22), date(2030, 1, 1)),
]
CHAIR_BY_NAME = {
    "Jerome Powell": (date(2018, 2, 5), date(2026, 5, 22)),
    "Kevin Warsh": (date(2026, 5, 22), date(2030, 1, 1)),
}

EVENT_TAGS = {"fomc", "minutes", "earnings"}
MAX_EVENT_AGE_DAYS = 45
# The metadata requirement applies to event posts dated on/after the day
# this check was adopted. Earlier event posts are grandfathered (the
# anachronism lint above still applies to them).
METADATA_REQUIRED_FROM = date(2026, 11, 20)


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm


def parse_metadata(text):
    m = re.search(r"<!--\s*source-check\n(.*?)\n-->", text, re.S)
    if not m:
        return None
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta


def normalize(s):
    s = s.replace("–", "-").replace("—", "-").replace("’", "'").replace("‘", "'")
    s = s.replace("3-3/4", "3.75").replace("3¾", "3.75")
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.lower()


def number_variants(tok):
    tok = tok.strip()
    variants = {tok}
    if "." in tok:
        trimmed = tok.rstrip("0").rstrip(".")
        variants.add(trimmed)
        variants.add(trimmed + " percent")
        variants.add(tok + " percent")
    return variants


def fetch_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "financial-poem-check/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read().decode("utf-8", errors="replace")
    return normalize(raw)


def check_post(path, offline):
    errors = []
    text = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm.get("draft") == "true":
        return errors
    try:
        post_date = datetime.fromisoformat(fm["date"].replace("Z", "+00:00")).date()
    except Exception:
        return [f"{path.name}: cannot parse frontmatter date {fm.get('date')!r}"]

    # 1. Anachronism lint: chair titles vs term windows
    for pattern, person, start, end in CHAIR_WINDOWS:
        if pattern in text and not (start <= post_date < end):
            errors.append(
                f"{path.name}: '{pattern}' used but {person} was not Fed chair "
                f"on the post date {post_date} (term {start}..{end})"
            )

    tags = set(re.findall(r'"([^"]+)"', fm.get("tags", "")))
    meta = parse_metadata(text)

    # 2. Event posts must declare their primary source
    if tags & EVENT_TAGS and meta is None and post_date >= METADATA_REQUIRED_FROM:
        errors.append(
            f"{path.name}: event post (tags {sorted(tags & EVENT_TAGS)}) has no "
            "<!-- source-check --> metadata block; primary source is undeclared"
        )
        return errors
    if meta is None:
        return errors

    # 3. Offline consistency of the declared source
    try:
        event_date = date.fromisoformat(meta["event_date"])
    except Exception:
        errors.append(f"{path.name}: bad event_date {meta.get('event_date')!r}")
        return errors

    url = meta.get("primary_url", "")
    m = re.search(r"(\d{4})(\d{2})(\d{2})", url)
    if m:
        url_date = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if url_date != event_date:
            errors.append(
                f"{path.name}: source URL date {url_date} != declared event_date "
                f"{event_date} (wrong year's document?)"
            )
    age = (post_date - event_date).days
    if age > MAX_EVENT_AGE_DAYS or age < -2:
        errors.append(
            f"{path.name}: event_date {event_date} is {age} days from post date "
            f"{post_date}; a review must be based on a fresh event "
            f"(<= {MAX_EVENT_AGE_DAYS} days)"
        )
    chair = meta.get("chair", "")
    if chair in CHAIR_BY_NAME:
        start, end = CHAIR_BY_NAME[chair]
        if not (start <= event_date < end):
            errors.append(
                f"{path.name}: declared chair {chair} was not in office on "
                f"event_date {event_date}"
            )

    # Key numbers must at least appear in the article itself
    body = normalize(text)
    for tok in [t.strip() for t in meta.get("must_numbers", "").split(",") if t.strip()]:
        if not any(v in body for v in number_variants(tok)):
            errors.append(f"{path.name}: must_number {tok} not found in article body")

    if offline:
        return errors

    # 4. Fetch verification against the primary source itself
    try:
        src = fetch_text(url)
    except Exception as e:
        errors.append(f"{path.name}: cannot fetch primary source {url}: {e}")
        return errors
    date_text = normalize(meta.get("source_date_text", ""))
    if date_text and date_text not in src:
        errors.append(
            f"{path.name}: source does not contain its declared date text "
            f"{meta.get('source_date_text')!r} (wrong document?)"
        )
    if chair and normalize(chair) not in src:
        errors.append(f"{path.name}: source does not mention declared chair {chair!r}")
    for tok in [t.strip() for t in meta.get("must_numbers", "").split(",") if t.strip()]:
        if not any(v in src for v in number_variants(tok)):
            errors.append(f"{path.name}: must_number {tok} not found in primary source")
    for phrase in [p.strip() for p in meta.get("must_phrases", "").split(",") if p.strip()]:
        if normalize(phrase) not in src:
            errors.append(f"{path.name}: must_phrase {phrase!r} not found in primary source")
    return errors


def main():
    args = sys.argv[1:]
    offline = "--offline" in args
    files = [a for a in args if a != "--offline"]
    paths = [Path(f) for f in files] if files else sorted(POSTS_DIR.glob("*.md"))
    all_errors = []
    for p in paths:
        all_errors.extend(check_post(p, offline))
    if all_errors:
        print("SOURCE CHECK FAILED")
        for e in all_errors:
            print(" -", e)
        return 1
    print(f"SOURCE CHECK OK ({len(paths)} post(s), offline={offline})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
