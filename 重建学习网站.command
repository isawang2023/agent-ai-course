#!/bin/bash
# 双击即可重建学习网站（Agent AI 学习）
cd "$(dirname "$0")" || exit 1

PY=""
for p in python3 /usr/bin/python3 /usr/local/bin/python3 /opt/homebrew/bin/python3; do
  if command -v "$p" >/dev/null 2>&1; then PY="$p"; break; fi
done

if [ -z "$PY" ]; then
  echo "❌ 没找到 python3，请先安装 Python 3：https://www.python.org/downloads/"
  read -n 1 -s -r -p "按任意键关闭…"
  exit 1
fi

echo "使用 $PY 构建…"
if ! "$PY" build.py; then
  echo ""
  echo "❌ 构建失败，请把上面的报错发给小元。"
  read -n 1 -s -r -p "按任意键关闭…"
  exit 1
fi

echo ""
echo "✅ 完成！窗口可以关闭。"
open "index.html"
