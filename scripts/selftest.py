#!/usr/bin/env python3
"""快速自检：台账脚本四个子命令 + 注册表完整性。"""
import subprocess, sys, os

here = os.path.dirname(os.path.abspath(__file__))
py = sys.executable
led = os.path.join(here, "credits_ledger.py")
test_ledger = os.path.join(here, "_test_ledger.csv")

ok = True
def run(args, expect_fail=False):
    global ok
    r = subprocess.run([py, led] + args, capture_output=True, text=True, encoding="utf-8")
    good = (r.returncode == 0) != expect_fail
    print(("PASS" if good else "FAIL"), " ".join(args[:2]))
    if not good:
        print(r.stdout, r.stderr)
        ok = False

run(["add", "智谱AI", "20000000", "--expires", "2030-01-01", "--note", "测试", "--file", test_ledger])
run(["add", "讯飞星辰", "1000000000", "--expires", "2000-01-01", "--note", "测试过期", "--file", test_ledger])
run(["list", "--file", test_ledger])
run(["due", "--days", "7", "--file", test_ledger])
run(["used", "2", "--file", test_ledger])
run(["list", "--file", test_ledger])

# 注册表完整性
reg = os.path.join(here, "..", "references", "registry.md")
if os.path.exists(reg):
    text = open(reg, encoding="utf-8").read()
    for kw in ["阿里云百炼", "智谱", "Google AI Studio", "GLM-4.7-Flash"]:
        print(("PASS" if kw in text else "FAIL"), "registry contains", kw)
        ok = ok and kw in text
else:
    print("FAIL references/registry.md 不存在"); ok = False

if os.path.exists(test_ledger):
    os.remove(test_ledger)
print("\n自检结果:", "全部通过 ✅" if ok else "有失败项 ❌")
sys.exit(0 if ok else 1)
