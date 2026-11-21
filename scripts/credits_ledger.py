#!/usr/bin/env python3
"""free-ai-credits 台账脚本：记录已领取的 AI 免费额度，提醒到期。

用法:
    python credits_ledger.py add <平台> <token数> [--expires YYYY-MM-DD] [--note 备注] [--file 路径]
    python credits_ledger.py list [--file 路径]
    python credits_ledger.py due [--days 7] [--file 路径]
    python credits_ledger.py used <行号> [--file 路径]

台账为 CSV（无依赖，Python 3.8+）。行号即 list 显示的 No.。
"""
from __future__ import annotations
import argparse, csv, os, sys
from datetime import date, datetime, timedelta

FIELDS = ["no", "platform", "tokens", "claimed_on", "expires", "note", "status"]

def _read(fpath: str) -> list[dict]:
    if not os.path.exists(fpath):
        return []
    with open(fpath, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def _write(fpath: str, rows: list[dict]):
    tmp = fpath + ".tmp"
    with open(tmp, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for i, r in enumerate(rows, 1):
            r["no"] = str(i)
            w.writerow(r)
    os.replace(tmp, fpath)

def _fmt_tokens(t: str) -> str:
    try:
        n = float(t)
        if n >= 1e8: return f"{n/1e8:.1f}亿"
        if n >= 1e4: return f"{n/1e4:.0f}万"
        return str(int(n)) if n == int(n) else str(n)
    except ValueError:
        return t

def cmd_add(a):
    rows = _read(a.file)
    rows.append({
        "no": "", "platform": a.platform, "tokens": str(a.tokens),
        "claimed_on": date.today().isoformat(),
        "expires": a.expires or "", "note": a.note or "", "status": "active",
    })
    _write(a.file, rows)
    print(f"已记录：{a.platform} {_fmt_tokens(str(a.tokens))} token，"
          f"到期 {a.expires or '未填(请按平台页面补填！)'}，台账共 {len(rows)} 笔")

def cmd_list(a):
    rows = _read(a.file)
    if not rows:
        print("台账为空。领取第一个额度后运行 add 记录。")
        return
    print(f"{'No.':>4}  {'平台':<14}{'额度':<10}{'领取日':<12}{'到期':<12}{'状态':<8}备注")
    for r in rows:
        print(f"{r['no']:>4}  {r['platform']:<14}{_fmt_tokens(r['tokens']):<10}"
              f"{r['claimed_on']:<12}{r['expires'] or '-':<12}{r['status']:<8}{r['note']}")

def cmd_due(a):
    rows = _read(a.file)
    today = date.today()
    limit = today + timedelta(days=a.days)
    hits, total = [], 0
    for r in rows:
        if r["status"] != "active" or not r["expires"]:
            continue
        try:
            exp = datetime.strptime(r["expires"], "%Y-%m-%d").date()
        except ValueError:
            print(f"⚠ 台账第 {r['no']} 行日期格式错误：{r['expires']}（应为 YYYY-MM-DD）", file=sys.stderr)
            continue
        if exp <= limit:
            left = (exp - today).days
            hits.append((r, left)); total += int(float(r["tokens"] or 0))
    if not hits:
        print(f"未来 {a.days} 天内没有到期额度。")
        return
    print(f"未来 {a.days} 天内到期 {len(hits)} 笔，合计约 {_fmt_tokens(str(total))} token：")
    for r, left in hits:
        when = "今天过期！" if left == 0 else (f"已过期 {abs(left)} 天" if left < 0 else f"还剩 {left} 天")
        print(f"  [{r['no']}] {r['platform']}（{_fmt_tokens(r['tokens'])}）— {when} → 尽快消耗或标记 used")

def cmd_used(a):
    rows = _read(a.file)
    for r in rows:
        if r["no"] == str(a.no):
            r["status"] = "used"
            _write(a.file, rows)
            print(f"已标记：[{r['no']}] {r['platform']} → used")
            return
    print(f"没找到行号 {a.no}，先运行 list 查看台账。", file=sys.stderr); sys.exit(1)

def main():
    ap = argparse.ArgumentParser(description="AI 免费额度领取台账")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--file", default=os.path.join(os.path.dirname(__file__), "ledger.csv"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add", parents=[common]); p.add_argument("platform"); p.add_argument("tokens", type=float)
    p.add_argument("--expires", default=None); p.add_argument("--note", default=None)
    sub.add_parser("list", parents=[common])
    p = sub.add_parser("due", parents=[common]); p.add_argument("--days", type=int, default=7)
    p = sub.add_parser("used", parents=[common]); p.add_argument("no")
    args = ap.parse_args()
    {"add": cmd_add, "list": cmd_list, "due": cmd_due, "used": cmd_used}[args.cmd](args)

if __name__ == "__main__":
    main()
