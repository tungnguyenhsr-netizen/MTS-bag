#!/usr/bin/env python3
"""
validate-content-only.py — Guardrail cho MTS website (Hermes workers).
Chạy SAU khi worker sửa index.html. So sánh working tree vs HEAD (git diff).
Exit 0 = chỉ sửa text content (OK). Exit 1 = chạm code/CSS/attrs (VIOLATION).

Logic: parse từng dòng changed, tách PHẦN ATTRIBUTE (tag + class/src/href/style...)
và PHẦN TEXT (nội dung trong tag). Chỉ flag nếu PHẦN ATTRIBUTE thay đổi.
Sửa text trong cùng dòng với class= sẽ KHÔNG bị false-positive.

Dùng:  python validate-content-only.py
"""
import sys, os, subprocess, re

ATTR_FORBIDDEN = [
    (r'<style', 'sua CSS block'),
    (r'</style>', 'sua CSS block'),
    (r'<script', 'sua JS block'),
    (r'</script>', 'sua JS block'),
    (r':root', 'sua token :root'),
    (r'--color-[\w-]+', 'sua design token'),
    (r'--space-[\w-]+', 'sua design token'),
    (r'--radius-[\w-]+', 'sua design token'),
    (r'--motion-[\w-]+', 'sua design token'),
    (r'--elevation-[\w-]+', 'sua design token'),
]

def attr_part(line):
    """Trích phần attribute của 1 dòng HTML (bỏ text content).
    Giữ lại: <tag ...attrs...> và </tag>, bỏ nội dung giữa > và <."""
    # Bỏ phần text đứng giữa các tag
    s = re.sub(r'>([^<]*)<', '><', line)
    return s

def check_attrs(text):
    low = text.lower()
    hits = []
    for pat, desc in ATTR_FORBIDDEN:
        if re.search(pat, low):
            hits.append(desc)
    # Kiểm tra attribute cụ thể đổi giá trị
    for attr in ['class=', 'id=', 'src=', 'href=', 'style=', 'data-', 'loading=']:
        if attr in low:
            # attribute xuất hiện -> coi như candidate; chỉ flag nếu value đổi (xử lý ở pair)
            pass
    return hits

def get_diff(repo):
    try:
        out = subprocess.run(['git','-C',repo,'diff','HEAD','--','index.html'],
                             capture_output=True, text=True, timeout=30)
        if out.returncode != 0:
            print("[ERR] git diff failed"); sys.exit(2)
        return out.stdout
    except Exception as e:
        print(f"[ERR] {e}"); sys.exit(2)

def parse_pairs(diff):
    """Trả về list (old_line, new_line) cho các dòng changed."""
    lines = diff.splitlines()
    pairs = []
    old = None
    i = 0
    # Parse unified diff thành các hunk, ghép - và + thành pair
    buf_old = []
    buf_new = []
    for ln in lines:
        if ln.startswith('@@'):
            # flush previous
            while buf_old or buf_new:
                o = buf_old.pop(0) if buf_old else None
                n = buf_new.pop(0) if buf_new else None
                pairs.append((o, n))
            continue
        if ln.startswith('-') and not ln.startswith('---'):
            buf_old.append(ln[1:])
        elif ln.startswith('+') and not ln.startswith('+++'):
            buf_new.append(ln[1:])
        else:
            # context: flush aligned
            while buf_old or buf_new:
                o = buf_old.pop(0) if buf_old else None
                n = buf_new.pop(0) if buf_new else None
                pairs.append((o, n))
            pairs.append((ln[1:] if ln.startswith(' ') else ln, ln[1:] if ln.startswith(' ') else ln))
    while buf_old or buf_new:
        o = buf_old.pop(0) if buf_old else None
        n = buf_new.pop(0) if buf_new else None
        pairs.append((o, n))
    return pairs

def main():
    repo = os.path.dirname(os.path.abspath(__file__))
    diff = get_diff(repo)
    if not diff.strip():
        print("OK: no changes vs HEAD.")
        sys.exit(0)
    pairs = parse_pairs(diff)
    violations = []
    for old, new in pairs:
        if old is None and new is None:
            continue
        if old is None:  # added line
            a = check_attrs(attr_part(new))
            if a: violations.append((new[:60], a))
        elif new is None:  # removed line
            a = check_attrs(attr_part(old))
            if a: violations.append((old[:60], a))
        else:  # changed line
            ao = attr_part(old); an = attr_part(new)
            if ao != an:
                # attribute portion changed -> real code change
                # find which attr
                for attr in ['class=', 'id=', 'src=', 'href=', 'style=', 'data-', 'loading=']:
                    if (attr in ao.lower()) or (attr in an.lower()):
                        if attr_part(old).lower().count(attr) != attr_part(new).lower().count(attr) or \
                           re.search(attr+r'["\']?[^"\']*', ao.lower()) != re.search(attr+r'["\']?[^"\']*', an.lower()):
                            violations.append((new[:60], [f'sua {attr}']))
                # also CSS/token block changes
                v = check_attrs(an)
                if v: violations.append((new[:60], v))
    if violations:
        print("VIOLATION (code/attribute touched):")
        seen=set()
        for snippet, descs in violations:
            for d in descs:
                if d not in seen:
                    seen.add(d); print(f"  - {d}")
        sys.exit(1)
    print("OK: changes are content-text only (VI/EN). No code/attribute touched.")
    sys.exit(0)

if __name__ == '__main__':
    main()
