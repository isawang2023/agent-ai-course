#!/bin/bash
# ============================================================
#  双击运行：重建网站 → 提交 → 推送到 GitHub → 同步发布分支
#  （改了 md 之后，双击这一个文件就够了）
# ============================================================
cd "$(dirname "$0")" || exit 1
ROOT="$(pwd)"

pause_exit() {
  echo ""
  read -n 1 -s -r -p "按任意键关闭窗口…"
  exit "${1:-0}"
}

# ---------- 1. 找 python3 ----------
PY=""
for p in python3 /usr/bin/python3 /usr/local/bin/python3 /opt/homebrew/bin/python3; do
  if command -v "$p" >/dev/null 2>&1; then PY="$p"; break; fi
done
if [ -z "$PY" ]; then
  echo "❌ 没找到 python3，请先安装：https://www.python.org/downloads/"
  pause_exit 1
fi

echo "===== 1/4 重建网站 ====="
echo "使用 $PY"
if ! "$PY" build.py; then
  echo "❌ 构建失败，请把上面的报错发给小元。"
  pause_exit 1
fi

# ---------- 2. 提交 ----------
echo ""
echo "===== 2/4 提交改动 ====="
NAME="$(git config user.name)"
EMAIL="$(git config user.email)"
[ -z "$NAME" ] && { NAME="isawang2023"; git config user.name "$NAME"; }
[ -z "$EMAIL" ] && { EMAIL="138577286+isawang2023@users.noreply.github.com"; git config user.email "$EMAIL"; }

git add -A
if git diff --cached --quiet; then
  echo "没有新改动，跳过提交。"
else
  git commit -q -m "更新学习内容 $(date '+%Y-%m-%d %H:%M')" && echo "已提交：$(git log --oneline -1)"
fi

# ---------- 3. 推到主分支 ----------
echo ""
echo "===== 3/4 推送到 GitHub（main）====="
if GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no -o ConnectTimeout=25" git push origin main; then
  echo "✅ main 已推送"
else
  echo "⚠️ main 推送失败（网络问题？）。内容已保存在本地，稍后重试即可。"
  pause_exit 1
fi

# ---------- 4. 同步发布分支 gh-pages ----------
# GitHub Pages 从这个分支取网站，所以每次都要把最新的 index.html 同步过去
echo ""
echo "===== 4/4 同步发布分支（gh-pages）====="
REMOTE="$(git remote get-url origin)"
TMP="$(mktemp -d)"
cp "$ROOT/index.html" "$TMP/index.html" || { echo "❌ 没找到 index.html"; pause_exit 1; }
touch "$TMP/.nojekyll"
(
  cd "$TMP" || exit 1
  git init -q -b gh-pages
  git config user.name "$NAME"
  git config user.email "$EMAIL"
  git add -A
  git commit -q -m "发布站点 $(date '+%Y-%m-%d %H:%M')"
  git remote add origin "$REMOTE"
  GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no -o ConnectTimeout=25" git push -f origin gh-pages
)
RC=$?
rm -rf "$TMP"

echo ""
if [ $RC -eq 0 ]; then
  echo "✅ 全部完成！网站约 1 分钟后自动更新："
  echo "   https://isawang2023.github.io/agent-ai-course/"
  echo ""
  echo "（本地也可以直接双击 index.html 查看）"
else
  echo "⚠️ 发布分支同步失败，主分支已推送成功，稍后重试即可。"
fi
pause_exit 0
