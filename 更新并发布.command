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

# 如果 git 异常退出留下了 index.lock，就清掉它（先确认没有进程占用）
clean_stale_lock() {
  local L="$ROOT/.git/index.lock"
  [ -f "$L" ] || return 0
  # 有进程正开着这个锁文件 → 说明真的有 git 在跑，不能删
  if command -v lsof >/dev/null 2>&1 && lsof "$L" >/dev/null 2>&1; then
    echo "⚠️ 似乎有另一个 git 进程正在操作本仓库，请稍后重试。"
    return 1
  fi
  # 超过 3 秒且没人占用，视为残留
  local MTIME NOW AGE
  MTIME="$(stat -f %m "$L" 2>/dev/null || echo 0)"
  NOW="$(date +%s)"
  AGE=$(( NOW - MTIME ))
  if [ "$AGE" -gt 3 ]; then
    rm -f "$L" && echo "（已清理上次残留的 index.lock）"
  fi
  return 0
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

clean_stale_lock || pause_exit 1
if ! git add -A; then
  echo "❌ git add 失败（上面有报错），已中止。"
  echo "   可尝试：在终端运行  rm -f .git/index.lock  后重试。"
  pause_exit 1
fi

if git diff --cached --quiet; then
  echo "没有新改动，跳过提交。"
else
  if ! git commit -q -m "更新学习内容 $(date '+%Y-%m-%d %H:%M')"; then
    echo "❌ 提交失败（上面有报错），已中止。"
    pause_exit 1
  fi
  echo "已提交：$(git log --oneline -1)"
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
