#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent AI 学习网站生成器
========================
把本目录下的所有 .md（Obsidian 笔记）渲染成一个自包含的单文件学习网站：
index.html

用法（任选其一）：
  1. 双击本目录下的「重建学习网站.command」
  2. 终端运行:  python3 build.py

维护规则：
  - 直接在 Obsidian 里改 md，然后重新运行本脚本即可，网站进度保存在浏览器本地，不会丢
  - 新增的 md 文件会自动出现在侧边栏「其他」分组
  - 想给新文件归组 / 排序，改下面的 KNOWN_ORDER 和 GROUPS 即可
"""

import os
import re
import json
import html as H
import hashlib
import datetime

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(SRC_DIR, "index.html")

# 搜索引擎收录开关：True = 站点加 noindex（有链接才能看、搜不到）
#                    False = 允许搜索引擎收录
NOINDEX = True

# ---------------------------------------------------------------------------
# 页面分组与排序（不在表里的 md 会自动进「其他」分组）
# ---------------------------------------------------------------------------
KNOWN_ORDER = [
    "00 · 学习总纲.md",
    "L1 · 语言层 · 能听懂.md",
    "L2 · 结构层 · 能选型.md",
    "L3 · 判断层 · 能评估.md",
    "L4 · 落地层 · 能交付.md",
    "卡A · 可靠性判断卡.md",
    "卡B · 成本与延迟判断卡.md",
    "卡C · 不该做清单.md",
    "卡D · 科研场景专项卡.md",
    "术语速查表.md",
    "书 · 深入理解 AI Agent · 导读.md",
    "课程框架评审 · 2026-09-30.md",
    "网站维护指南.md",
]

GROUPS = {
    "00 · 学习总纲.md": ("总纲", "🧭"),
    "L1 · 语言层 · 能听懂.md": ("四层主干", "🧱"),
    "L2 · 结构层 · 能选型.md": ("四层主干", "🧱"),
    "L3 · 判断层 · 能评估.md": ("四层主干", "🧱"),
    "L4 · 落地层 · 能交付.md": ("四层主干", "🧱"),
    "卡A · 可靠性判断卡.md": ("横切判断卡", "🃏"),
    "卡B · 成本与延迟判断卡.md": ("横切判断卡", "🃏"),
    "卡C · 不该做清单.md": ("横切判断卡", "🃏"),
    "卡D · 科研场景专项卡.md": ("横切判断卡", "🃏"),
    "术语速查表.md": ("参考与工具", "📚"),
    "书 · 深入理解 AI Agent · 导读.md": ("参考与工具", "📚"),
    "课程框架评审 · 2026-09-30.md": ("参考与工具", "📚"),
    "网站维护指南.md": ("参考与工具", "🛠"),
}

GROUP_ICONS = {"总纲": "🧭", "四层主干": "🧱", "横切判断卡": "🃏",
               "参考与工具": "📚", "其他": "🗂"}

# ---------------------------------------------------------------------------
# 首页课程架构 —— 首页讲什么、怎么讲，全部在这里改
# 想调整首页文案 / 卡片顺序 / 推荐路径，只改这一块即可
# ---------------------------------------------------------------------------
CURRICULUM = {
    "eyebrow": "科研助手 · Agent 产品学习体系",
    "title": "Agent AI 学习体系",
    "slogan": "从「能用」到「能判断」",
    "lead": "一套按能力层级组织的地图，而不是按周次排列的课程表。"
            "四层主干回答「该会什么」，四张判断卡回答「什么时候该喊停」。",
    "meta": ["产品 / UX 背景", "面向科研助手类 Agent", "总计 12–15h"],
    "start": "L2 · 结构层 · 能选型.md",
    "start_label": "从 L2 结构层开始",
    "start_note": "<b>起点校准</b>：你已有日常使用 AI 的体感，缺的是"
                  "<b>技术深度 / 整体评测 / 进阶路径</b>。"
                  "所以这套体系不从零开始，而是从你的真实缺口开始。",
    "path_hint": "建议路径 L2 → L3（最优先）→ L4，L1 随时查。"
                 "不必从 L1 顺着啃——已经会的东西不用再学一遍。",
    "layers": [
        {"file": "L1 · 语言层 · 能听懂.md", "code": "L1", "name": "语言层",
         "ability": "能听懂", "role": "给你词汇", "hours": "30min", "tag": "可略过",
         "desc": "在会上听懂研发说的每句话，并且能反问到点上。"},
        {"file": "L2 · 结构层 · 能选型.md", "code": "L2", "name": "结构层",
         "ability": "能选型", "role": "给你结构", "hours": "4–6h", "tag": "建议先学",
         "desc": "拿到「为什么这么选」的依据——够你做判断和提问，不必够你实现。"},
        {"file": "L3 · 判断层 · 能评估.md", "code": "L3", "name": "判断层",
         "ability": "能评估", "role": "给你判断力", "hours": "4–5h", "tag": "最优先",
         "desc": "在评审会上回答两个问题：这个方案好不好？该不该做？"},
        {"file": "L4 · 落地层 · 能交付.md", "code": "L4", "name": "落地层",
         "ability": "能交付", "role": "变成交付物", "hours": "3–4h", "tag": "中等",
         "desc": "把前三层认知，变成一份能过评审、能落地的产品方案。"},
    ],
    "cards": [
        {"file": "卡A · 可靠性判断卡.md", "code": "卡A", "name": "可靠性判断卡",
         "one": "步数越多越不可靠", "when": "评审多步方案前", "hours": "约 1h"},
        {"file": "卡B · 成本与延迟判断卡.md", "code": "卡B", "name": "成本与延迟判断卡",
         "one": "单次成本决定功能能不能活", "when": "立项前", "hours": "约 1h"},
        {"file": "卡C · 不该做清单.md", "code": "卡C", "name": "不该做清单",
         "one": "产品最贵的能力是 Say No", "when": "接到需求时", "hours": "约 20min"},
        {"file": "卡D · 科研场景专项卡.md", "code": "卡D", "name": "科研场景专项卡",
         "one": "科研要可溯源，不是看起来专业", "when": "做科研功能时", "hours": "约 1.5h"},
    ],
    "tools": [
        {"file": "术语速查表.md", "name": "术语速查表",
         "desc": "遇到不懂的词来这里", "hours": "随时查"},
        {"file": "书 · 深入理解 AI Agent · 导读.md", "name": "深入理解 AI Agent",
         "desc": "313 页工程实现视角，按需查", "hours": "8–10h"},
        {"file": "课程框架评审 · 2026-09-30.md", "name": "课程框架评审",
         "desc": "这套框架要不要改的体检报告", "hours": "约 20min"},
        {"file": "网站维护指南.md", "name": "网站维护指南",
         "desc": "这个网站怎么更新", "hours": ""},
    ],
}

CALLOUT_META = {
    "note":     ("📝", "note", "笔记"),
    "info":     ("ℹ️", "info", "信息"),
    "tip":      ("💡", "tip", "提示"),
    "hint":     ("💡", "tip", "提示"),
    "important":("💡", "tip", "重要"),
    "success":  ("✅", "success", "结论"),
    "check":    ("✅", "success", "检查"),
    "done":     ("✅", "success", "完成"),
    "question": ("❓", "question", "问题"),
    "help":     ("❓", "question", "求助"),
    "faq":      ("❓", "question", "FAQ"),
    "warning":  ("⚠️", "warning", "注意"),
    "caution":  ("⚠️", "warning", "谨慎"),
    "attention":("⚠️", "warning", "注意"),
    "danger":   ("🚨", "danger", "危险"),
    "failure":  ("🚨", "danger", "失败"),
    "bug":      ("🐞", "danger", "Bug"),
    "example":  ("🧪", "example", "示例"),
    "quote":    ("❝", "quote", "引用"),
    "cite":     ("❝", "quote", "引用"),
    "abstract": ("📄", "abstract", "摘要"),
    "summary":  ("📄", "abstract", "摘要"),
    "tldr":     ("📄", "abstract", "TL;DR"),
    "todo":     ("📌", "todo", "待办"),
}

# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def stable_id(*parts):
    return hashlib.md5("||".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:10]


def heading_slug(text):
    return "h-" + hashlib.md5(text.strip().encode("utf-8")).hexdigest()[:10]


def collect_md_files():
    files = []
    for name in sorted(os.listdir(SRC_DIR)):
        if not name.endswith(".md"):
            continue
        if name.startswith("."):
            continue
        full = os.path.join(SRC_DIR, name)
        if not os.path.isfile(full):
            continue
        files.append(name)
    ordered = [f for f in KNOWN_ORDER if f in files]
    others = [f for f in files if f not in KNOWN_ORDER]
    return ordered + others


def parse_frontmatter(text):
    meta = {}
    body = text
    if text.startswith("---"):
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
        if m:
            body = text[m.end():]
            for line in m.group(1).splitlines():
                mm = re.match(r"^(\S[^:]*):\s*(.*)$", line)
                if mm:
                    meta[mm.group(1).strip()] = mm.group(2).strip().strip("\"'")
    return meta, body


# ---------------------------------------------------------------------------
# 行内渲染
# ---------------------------------------------------------------------------

def inline(text, ctx):
    """ctx: {'page_keys': {name_or_title: slug}, 'headings': {text: id}}"""
    s = H.escape(text, quote=False)
    # 行内代码
    codes = []
    def _code(m):
        codes.append(m.group(1))
        return f"\x00{len(codes)-1}\x01"
    s = re.sub(r"`([^`]+)`", _code, s)
    # wikilink [[target|alias]] / [[target]]
    def _wiki(m):
        target = m.group(1).strip()
        alias = m.group(2).strip() if m.group(2) else None
        alias = alias or target
        alias = alias.replace("\\|", "|")
        target = target.replace("\\|", "|")
        # 页内锚点 [[#标题]]
        if target.startswith("#"):
            hid = ctx["headings"].get(target[1:].strip())
            if hid:
                disp = m.group(2).strip() if m.group(2) else target[1:].strip()
                return f'<a class="wl" href="#{hid}">{H.escape(disp)}</a>'
            return H.escape(alias)
        # PDF/epub 深链
        if re.search(r"\.(pdf|epub)(#|$)", target):
            fname = target.split("#")[0]
            frag = target.split("#", 1)[1] if "#" in target else ""
            href = fname + (("#" + frag) if frag else "")
            return (f'<a class="wl pdf-link" href="{H.escape(href, quote=True)}" '
                    f'target="_blank" title="打开本地文件">{H.escape(alias)} <span class="pdf-badge">📄</span></a>')
        # 站内页面
        slug = ctx["page_keys"].get(target) or ctx["page_keys"].get(target + ".md")
        if slug:
            return f'<a class="wl" href="#/{slug}">{H.escape(alias)}</a>'
        return H.escape(alias)
    s = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", _wiki, s)
    # markdown 链接
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
               lambda m: f'<a class="ext" href="{H.escape(m.group(2), quote=True)}" target="_blank" rel="noopener">{m.group(1)}</a>',
               s)
    # 粗体 / 斜体 / 删除线 / 高亮
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"~~(.+?)~~", r"<del>\1</del>", s)
    s = re.sub(r"==(.+?)==", r"<mark>\1</mark>", s)
    # 还原代码
    def _restore(m):
        return "<code>" + H.escape(codes[int(m.group(1))]) + "</code>"
    s = re.sub(r"\x00(\d+)\x01", _restore, s)
    return s


# ---------------------------------------------------------------------------
# 块级渲染
# ---------------------------------------------------------------------------

def is_table_sep(line):
    return bool(re.match(r"^\s*\|?[\s:\-|]+\|?\s*$", line) and "-" in line and "|" in line)


def split_row(line):
    line = line.strip().strip("|")
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line)]


def parse_blocks(lines, ctx, page_title):
    """lines: list[str]（不含尾部空行）→ html string"""
    out = []
    i = 0
    n = len(lines)
    cb_index = 0
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        # 代码块
        if stripped.startswith("```"):
            j = i + 1
            buf = []
            while j < n and not lines[j].strip().startswith("```"):
                buf.append(lines[j])
                j += 1
            out.append(f"<pre><code>{H.escape(chr(10).join(buf))}</code></pre>")
            i = j + 1
            continue
        # 标题
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            hid = heading_slug(text)
            ctx["headings"][text] = hid
            out.append(f'<h{level} id="{hid}">{inline(text, ctx)}</h{level}>')
            i += 1
            continue
        # 分隔线
        if re.match(r"^-{3,}$", stripped) or re.match(r"^\*{3,}$", stripped):
            out.append("<hr>")
            i += 1
            continue
        # 引用 / callout（收集连续 > 行）
        if stripped.startswith(">"):
            block = []
            while i < n and lines[i].strip().startswith(">"):
                # 去掉一层 >
                block.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append(render_quote(block, ctx, page_title))
            continue
        # 表格
        if stripped.startswith("|") and i + 1 < n and is_table_sep(lines[i + 1]):
            header = split_row(stripped)
            sep = split_row(lines[i + 1])
            aligns = []
            for c in sep:
                if c.startswith(":") and c.endswith(":"):
                    aligns.append("center")
                elif c.startswith(":"):
                    aligns.append("left")
                elif c.endswith(":"):
                    aligns.append("right")
                else:
                    aligns.append("")
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i].strip()))
                i += 1

            def cell(content, align, tag):
                if align:
                    return '<{t} style="text-align:{a}">{c}</{t}>'.format(
                        t=tag, a=align, c=inline(content, ctx))
                return "<{t}>{c}</{t}>".format(t=tag, c=inline(content, ctx))

            th = "".join(cell(c, a, "th") for c, a in zip(header, aligns))
            trs = []
            for r in rows:
                tds = "".join(cell(c, a, "td") for c, a in zip(r, aligns)) if r else ""
                trs.append(f"<tr>{tds}</tr>")
            out.append(f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>')
            continue
        # 列表（支持嵌套与 checkbox）
        if re.match(r"^(\s*)([-*+]|\d+[.)])\s+", line):
            items = []
            while i < n and re.match(r"^(\s*)([-*+]|\d+[.)])\s+", lines[i]):
                items.append(lines[i])
                i += 1
            out.append(render_list(items, ctx, page_title))
            continue
        # 普通段落
        para = [stripped]
        i += 1
        while i < n and lines[i].strip() and not re.match(
                r"^(#{1,6}\s|>|\||```|\s*[-*+]\s|\s*\d+[.)]\s|-{3,}$)", lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(para), ctx)}</p>")
    return "\n".join(out)


def render_list(items, ctx, page_title):
    """把缩进列表行渲染成嵌套 ul，带 checkbox 支持"""
    parsed = []
    for it in items:
        m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", it)
        indent = len(m.group(1).replace("\t", "    "))
        level = min(indent // 2, 4)
        content = m.group(3)
        checked = None
        cb = re.match(r"^\[( |x|X)\]\s+(.*)$", content)
        if cb:
            checked = cb.group(1).lower() == "x"
            content = cb.group(2)
        parsed.append({"level": level, "checked": checked, "text": content})

    html_parts = []
    stack = []  # 当前打开的层级号，如 [0, 1] 表示两层嵌套
    for item in parsed:
        # 关闭比当前更深的层级
        while stack and stack[-1] > item["level"]:
            html_parts.append("</li></ul>")
            stack.pop()
        if not stack:
            stack.append(item["level"])
            html_parts.append("<ul>")
        elif stack[-1] < item["level"]:
            for lv in range(stack[-1] + 1, item["level"] + 1):
                html_parts.append("<ul>")
                stack.append(lv)
        else:
            html_parts.append("</li>")  # 同级新条目
        if item["checked"] is None:
            html_parts.append(f"<li>{inline(item['text'], ctx)}")
        else:
            cbid = "cb-" + stable_id(page_title, item["text"])
            state = " checked" if item["checked"] else ""
            html_parts.append(
                f'<li><label class="task"><input type="checkbox" data-cb="{cbid}"{state}>'
                f'<span>{inline(item["text"], ctx)}</span></label>')
    while stack:
        html_parts.append("</li></ul>")
        stack.pop()
    return "".join(html_parts)


def render_quote(block, ctx, page_title):
    """block: 去掉一层 > 后的行。识别 [!type] callout"""
    first = ""
    for ln in block:
        if ln.strip():
            first = ln.strip()
            break
    m = re.match(r"^\[!(\w+)\]([+-]?)\s*(.*)$", first)
    if not m:
        body = parse_blocks([re.sub(r"^(\s*)>\s?", "", ln) if ln.startswith(">") else ln for ln in block], ctx, page_title)
        return f"<blockquote>{body}</blockquote>"
    ctype = m.group(1).lower()
    fold = m.group(2)
    title = m.group(2 + 1) if False else m.group(3).strip()
    # 去掉首行，剩余内容递归解析
    rest = []
    skipped_first = False
    for ln in block:
        if not skipped_first and ln.strip() == first:
            skipped_first = True
            continue
        rest.append(ln)
    body = parse_blocks(rest, ctx, page_title)
    icon, cls, default_title = CALLOUT_META.get(ctype, ("📌", "note", ctype))
    title_text = title if title else default_title
    if fold == "-":
        return (f'<details class="callout co-{cls}" data-fold><summary>'
                f'<span class="co-icon">{icon}</span><span class="co-title">{inline(title_text, ctx)}</span>'
                f'<span class="co-arrow">▸</span></summary>'
                f'<div class="co-body">{body}</div></details>')
    open_attr = " open" if fold == "+" else ""
    return (f'<details class="callout co-{cls}"{open_attr}><summary>'
            f'<span class="co-icon">{icon}</span><span class="co-title">{inline(title_text, ctx)}</span>'
            f'<span class="co-arrow">▸</span></summary>'
            f'<div class="co-body">{body}</div></details>')


# ---------------------------------------------------------------------------
# 页面构建
# ---------------------------------------------------------------------------

HELP_PAGE_SLUG = "how-to-update"


def build():
    md_files = collect_md_files()
    pages = []
    page_keys = {}
    for name in md_files:
        slug = "p-" + stable_id(name)
        page_keys[name[:-3]] = slug          # 文件名（去 .md）
        with open(os.path.join(SRC_DIR, name), encoding="utf-8") as f:
            raw = f.read()
        meta, _ = parse_frontmatter(raw)
        title = meta.get("title") or name[:-3]
        page_keys[title] = slug              # frontmatter title
        pages.append({"file": name, "slug": slug, "title": title, "meta": meta})

    for p in pages:
        with open(os.path.join(SRC_DIR, p["file"]), encoding="utf-8") as f:
            raw = f.read()
        meta, body = parse_frontmatter(raw)
        ctx = {"page_keys": page_keys, "headings": {}}
        # 预扫描标题，保证目录里的 [[#标题]] 链接在前文也能解析
        for ln in body.splitlines():
            hm = re.match(r"^(#{1,6})\s+(.*)$", ln.strip())
            if hm:
                ctx["headings"][hm.group(2).strip()] = heading_slug(hm.group(2).strip())
        body_html = parse_blocks(body.splitlines(), ctx, p["title"])
        group, icon = GROUPS.get(p["file"], ("其他", ""))
        p.update({
            "group": group,
            "icon": icon,
            "updated": meta.get("更新日期", ""),
            "invest": meta.get("预计投入", ""),
            "html": body_html,
        })

    # 分组顺序
    group_order = ["总纲", "四层主干", "横切判断卡", "参考与工具", "其他"]
    groups = {}
    for p in pages:
        groups.setdefault(p["group"], []).append(p)

    data = []
    for g in group_order:
        if g in groups:
            for p in groups[g]:
                plain = re.sub(r"<[^>]+>", " ", p["html"])
                plain = H.unescape(re.sub(r"\s+", " ", plain))
                data.append({
                    "slug": p["slug"], "title": p["title"], "group": p["group"],
                    "icon": p["icon"], "updated": p["updated"], "invest": p["invest"],
                    "html": p["html"], "search": plain[:20000],
                })

    # 使用说明页（自动追加）
    help_html = """
<p>这个网站是<strong>自动生成</strong>的，源文件是本目录下的 Obsidian 笔记（.md）。在 Obsidian 里改完 md，双击一次 <code>更新并发布.command</code> 就完成重建与上线。</p>
<div class="callout co-tip"><summary>…</summary></div>
"""
    help_body = """
<ol>
<li><strong>在 Obsidian 里随便改</strong>：编辑 L1–L4、判断卡、术语表……新增或删除 md 文件都行（<code>归档/</code> 里的不会被收录）。</li>
<li><strong>重建网站</strong>：双击本目录下的 <code>重建学习网站.command</code>（或在终端运行 <code>python3 build.py</code>）。</li>
<li><strong>刷新浏览器</strong>，完事。</li>
<li><strong>发布到线上</strong>：双击 <code>更新并发布.command</code>（= 重建 + 提交 + 推送 main + 同步 <code>gh-pages</code> 发布分支），约 1 分钟后线上更新。</li>
<li><strong>只想本地看看</strong>：双击 <code>重建学习网站.command</code> 即可，它不碰 GitHub。</li>
</ol>
<p>规则：</p>
<ul>
<li>勾选进度保存在浏览器本地（localStorage），重建不会丢失；换浏览器或清缓存会重置。</li>
<li>新加的 md 文件会自动出现在侧边栏「其他」分组；想归组 / 调顺序，改 <code>build.py</code> 顶部的 <code>KNOWN_ORDER</code> 和 <code>GROUPS</code>。</li>
<li>指向 <code>AI-Agents-in-Depth-zh-CN.pdf#page=N</code> 的链接会直接打开本地 PDF 并跳到对应页。</li>
<li>网站是单文件、离线可用，可以拷到任何地方双击打开（同目录保留 PDF 即可让深链生效）。</li>
<li>线上地址：<code>https://isawang2023.github.io/agent-ai-course/</code>，已设 <code>noindex</code>，搜索引擎不会收录（可在 <code>build.py</code> 顶部用 <code>NOINDEX</code> 开关调整）。</li>
<li>GitHub Pages 从 <code>gh-pages</code> 分支取网站，所以<strong>只 push main 不会让线上更新</strong>——发布一定要用 <code>更新并发布.command</code>。</li>
</ul>
"""
    data.append({
        "slug": HELP_PAGE_SLUG, "title": "如何更新本站", "group": "参考与工具",
        "icon": "🛠", "updated": datetime.date.today().isoformat(), "invest": "",
        "html": help_body, "search": "如何更新本站 build.py 重建 学习网站 维护 github pages git 提交 推送",
    })

    groups_present = []
    for g in group_order:
        if any(p["group"] == g for p in data):
            groups_present.append(g)
    # 首页架构数据：把文件名解析成页面 slug
    cur = json.loads(json.dumps(CURRICULUM, ensure_ascii=False))
    cur["start_slug"] = page_keys.get(cur["start"][:-3], "")
    for it in cur["layers"] + cur["cards"] + cur["tools"]:
        it["slug"] = page_keys.get(it["file"][:-3], "")
        it.pop("file", None)
    cur.pop("start", None)

    payload = json.dumps({"pages": data, "groups": groups_present, "cur": cur},
                         ensure_ascii=False)

    template_path = os.path.join(SRC_DIR, "build.py")
    with open(template_path, encoding="utf-8") as f:
        src = f.read()
    m = re.search(r"(?ms)^HTML_TEMPLATE = r'''(.*)^'''\s*$", src)
    template = m.group(1)
    out_html = template.replace("/*__DATA__*/null", payload)
    out_html = out_html.replace(
        "__ROBOTS__",
        '<meta name="robots" content="noindex, nofollow">\n' if NOINDEX else "",
    )
    out_html = out_html.replace("__BUILD_DATE__", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write(out_html)
    print(f"✅ 已生成: {OUT_FILE}")
    print(f"   共 {len(data)} 个页面 · {os.path.getsize(OUT_FILE)/1024:.0f} KB")
    for p in data:
        n_cb = p["html"].count("data-cb=")
        if n_cb:
            print(f"   · {p['title']}（{n_cb} 个进度项）")


HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
__ROBOTS__
<title>Agent AI · 学习站</title>
<style>
:root{
  --bg:#0d1220; --bg2:#111830; --panel:#151d33; --panel2:#1a2340;
  --border:#253152; --text:#dbe3f4; --text-dim:#8b96b8; --accent:#6ea8fe;
  --accent2:#8be9c8; --radius:12px;
  --co-note:#5b8def; --co-info:#5b8def; --co-tip:#2fbfa4; --co-success:#3fbf6f;
  --co-question:#e0b13f; --co-warning:#e8963f; --co-danger:#e85f5f;
  --co-example:#a97ce0; --co-quote:#7c8aa5; --co-todo:#5b9fde; --co-abstract:#4fc3d9;
  --l1:#7c8aa5; --l2:#5b8def; --l3:#2fbfa4; --l4:#a97ce0;
}
body.light{
  --bg:#f4f6fb; --bg2:#eef1f8; --panel:#ffffff; --panel2:#f2f5fb;
  --border:#dfe4f0; --text:#252c3d; --text-dim:#6b7488; --accent:#2f6fe0;
  --accent2:#149d7c;
  --co-note:#2f6fe0; --co-info:#2f6fe0; --co-tip:#0e9c82; --co-success:#1d9e52;
  --co-question:#b98a10; --co-warning:#c87116; --co-danger:#d64545;
  --co-example:#8452c9; --co-quote:#6b7689; --co-todo:#2f6fe0; --co-abstract:#0f93aa;
  --l1:#6b7689; --l2:#2f6fe0; --l3:#0e9c82; --l4:#8452c9;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;font-size:15.5px;line-height:1.75}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
code{background:var(--panel2);border:1px solid var(--border);border-radius:5px;padding:1px 6px;font-size:.88em;font-family:"SF Mono",Menlo,Consolas,monospace}
pre{background:var(--panel2);border:1px solid var(--border);border-radius:10px;padding:14px 16px;overflow-x:auto;margin:12px 0}
pre code{background:none;border:none;padding:0}
#app{display:flex;min-height:100vh}
/* ---------- 侧边栏 ---------- */
#sidebar{width:290px;min-width:290px;background:var(--bg2);border-right:1px solid var(--border);height:100vh;position:sticky;top:0;overflow-y:auto;padding:20px 14px 40px;transition:margin .25s}
#sidebar.hidden{margin-left:-290px}
.logo{font-size:17px;font-weight:700;padding:6px 10px 16px;display:flex;align-items:center;gap:8px}
.logo .coin{font-size:20px}
.side-group{margin-top:14px}
.side-group-title{font-size:11.5px;letter-spacing:.12em;color:var(--text-dim);padding:4px 10px;text-transform:uppercase}
.side-link{display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:9px;color:var(--text);cursor:pointer;font-size:14px;line-height:1.45}
.side-link:hover{background:var(--panel)}
.side-link.active{background:var(--panel);color:var(--accent);font-weight:600}
.side-link .pg{margin-left:auto;font-size:10.5px;color:var(--text-dim);background:var(--panel2);border-radius:20px;padding:1px 7px;white-space:nowrap}
.side-link.all-done .pg{color:#fff;background:var(--co-success)}
/* ---------- 主区 ---------- */
#main{flex:1;min-width:0;display:flex;flex-direction:column}
#topbar{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--bg) 85%,transparent);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:12px;padding:10px 22px}
#btn-menu{background:none;border:1px solid var(--border);color:var(--text);border-radius:8px;width:34px;height:34px;cursor:pointer;font-size:15px}
#search-box{flex:1;max-width:520px;display:flex;align-items:center;gap:8px;background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:7px 12px}
#search-box input{flex:1;background:none;border:none;outline:none;color:var(--text);font-size:14px}
#search-box .kbd{font-size:11px;color:var(--text-dim);border:1px solid var(--border);border-radius:5px;padding:0 6px}
#global-progress{margin-left:auto;display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--text-dim);white-space:nowrap}
#gp-bar{width:110px;height:7px;background:var(--panel2);border-radius:10px;overflow:hidden;border:1px solid var(--border)}
#gp-fill{height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2));width:0%;transition:width .3s}
#btn-theme{background:none;border:1px solid var(--border);color:var(--text);border-radius:8px;width:34px;height:34px;cursor:pointer;font-size:14px}
#content{max-width:860px;width:100%;margin:0 auto;padding:34px 30px 90px}
.page-meta{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:6px}
.badge{font-size:11.5px;color:var(--text-dim);background:var(--panel2);border:1px solid var(--border);border-radius:20px;padding:2px 10px}
h1{font-size:27px;margin:4px 0 20px;line-height:1.4}
h2{font-size:21px;margin:34px 0 14px;padding-bottom:8px;border-bottom:1px solid var(--border)}
h3{font-size:17.5px;margin:26px 0 10px;color:var(--accent)}
h4{font-size:15.5px;margin:20px 0 8px}
p{margin:10px 0}
ul,ol{padding-left:24px;margin:10px 0}
li{margin:5px 0}
li ul{margin:4px 0}
blockquote{border-left:3px solid var(--border);padding:4px 16px;margin:12px 0;color:var(--text-dim)}
hr{border:none;border-top:1px solid var(--border);margin:28px 0}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:14.5px}
th,td{border:1px solid var(--border);padding:8px 12px;text-align:left;vertical-align:top}
th{background:var(--panel2);font-weight:600;white-space:nowrap}
tr:nth-child(even) td{background:color-mix(in srgb,var(--panel) 45%,transparent)}
.table-wrap{overflow-x:auto}
/* ---------- Callout ---------- */
.callout{border:1px solid;border-radius:var(--radius);margin:16px 0;overflow:hidden;background:var(--panel)}
.callout>summary{display:flex;align-items:center;gap:9px;padding:10px 15px;cursor:pointer;font-weight:600;font-size:14.5px;list-style:none;user-select:none}
.callout>summary::-webkit-details-marker{display:none}
.callout .co-arrow{margin-left:auto;transition:transform .2s;color:var(--text-dim);font-size:12px}
.callout[open]>summary .co-arrow{transform:rotate(90deg)}
.callout .co-body{padding:4px 16px 12px;border-top:1px dashed color-mix(in srgb,var(--text-dim) 30%,transparent)}
.callout .co-body>:first-child{margin-top:8px}
.callout .co-body>:last-child{margin-bottom:2px}
.callout.co-note{border-color:color-mix(in srgb,var(--co-note) 45%,transparent);background:color-mix(in srgb,var(--co-note) 9%,var(--panel))}
.callout.co-note>summary{color:var(--co-note)}
.callout.co-info{border-color:color-mix(in srgb,var(--co-info) 45%,transparent);background:color-mix(in srgb,var(--co-info) 9%,var(--panel))}
.callout.co-info>summary{color:var(--co-info)}
.callout.co-tip{border-color:color-mix(in srgb,var(--co-tip) 45%,transparent);background:color-mix(in srgb,var(--co-tip) 9%,var(--panel))}
.callout.co-tip>summary{color:var(--co-tip)}
.callout.co-success{border-color:color-mix(in srgb,var(--co-success) 45%,transparent);background:color-mix(in srgb,var(--co-success) 9%,var(--panel))}
.callout.co-success>summary{color:var(--co-success)}
.callout.co-question{border-color:color-mix(in srgb,var(--co-question) 45%,transparent);background:color-mix(in srgb,var(--co-question) 9%,var(--panel))}
.callout.co-question>summary{color:var(--co-question)}
.callout.co-warning{border-color:color-mix(in srgb,var(--co-warning) 45%,transparent);background:color-mix(in srgb,var(--co-warning) 9%,var(--panel))}
.callout.co-warning>summary{color:var(--co-warning)}
.callout.co-danger{border-color:color-mix(in srgb,var(--co-danger) 45%,transparent);background:color-mix(in srgb,var(--co-danger) 9%,var(--panel))}
.callout.co-danger>summary{color:var(--co-danger)}
.callout.co-example{border-color:color-mix(in srgb,var(--co-example) 45%,transparent);background:color-mix(in srgb,var(--co-example) 9%,var(--panel))}
.callout.co-example>summary{color:var(--co-example)}
.callout.co-quote{border-color:color-mix(in srgb,var(--co-quote) 45%,transparent);background:color-mix(in srgb,var(--co-quote) 8%,var(--panel))}
.callout.co-quote>summary{color:var(--co-quote)}
.callout.co-todo{border-color:color-mix(in srgb,var(--co-todo) 45%,transparent);background:color-mix(in srgb,var(--co-todo) 9%,var(--panel))}
.callout.co-todo>summary{color:var(--co-todo)}
.callout.co-abstract{border-color:color-mix(in srgb,var(--co-abstract) 45%,transparent);background:color-mix(in srgb,var(--co-abstract) 9%,var(--panel))}
.callout.co-abstract>summary{color:var(--co-abstract)}
/* ---------- 任务 checkbox ---------- */
label.task{display:flex;gap:9px;align-items:flex-start;cursor:pointer}
label.task input{margin-top:7px;accent-color:var(--co-success);width:15px;height:15px;flex-shrink:0;cursor:pointer}
label.task input:checked+span{color:var(--text-dim);text-decoration:line-through;text-decoration-color:color-mix(in srgb,var(--text-dim) 60%,transparent)}
/* ---------- 搜索结果 ---------- */
#search-overlay{display:none;position:fixed;inset:0;background:rgba(5,8,18,.6);backdrop-filter:blur(3px);z-index:100;padding:9vh 20px 20px}
#search-overlay.show{display:block}
#search-panel{max-width:680px;margin:0 auto;background:var(--panel);border:1px solid var(--border);border-radius:14px;overflow:hidden;max-height:76vh;display:flex;flex-direction:column;box-shadow:0 20px 60px rgba(0,0,0,.4)}
#search-input-lg{width:100%;background:none;border:none;outline:none;color:var(--text);font-size:16px;padding:16px 18px;border-bottom:1px solid var(--border)}
#search-results{overflow-y:auto;padding:8px}
.sr-item{padding:11px 14px;border-radius:9px;cursor:pointer}
.sr-item:hover,.sr-item.sel{background:var(--panel2)}
.sr-item .sr-title{font-weight:600;font-size:14px;display:flex;gap:8px;align-items:center}
.sr-item .sr-snip{font-size:12.5px;color:var(--text-dim);margin-top:3px;line-height:1.55}
.sr-item mark{background:color-mix(in srgb,var(--co-question) 45%,transparent);color:inherit;border-radius:3px;padding:0 2px}
.sr-empty{padding:26px;text-align:center;color:var(--text-dim);font-size:14px}
/* ---------- 仪表盘 ---------- */
#dashboard{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px;margin:6px 0 26px}
.dash-card{background:var(--panel);border:1px solid var(--border);border-radius:var(--radius);padding:14px 16px;cursor:pointer;transition:transform .15s,border-color .15s}
.dash-card:hover{transform:translateY(-2px);border-color:var(--accent)}
.dash-card .dc-title{font-size:13.5px;font-weight:600;display:flex;gap:7px;align-items:center}
.dash-card .dc-bar{height:6px;background:var(--panel2);border-radius:10px;margin-top:10px;overflow:hidden;border:1px solid var(--border)}
.dash-card .dc-fill{height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2));width:0%;transition:width .3s}
.dash-card .dc-num{font-size:11px;color:var(--text-dim);margin-top:6px}
/* ---------- 底部导航 ---------- */
#pager{display:flex;justify-content:space-between;gap:12px;margin-top:46px;padding-top:20px;border-top:1px solid var(--border)}
.pager-btn{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:10px 16px;color:var(--text);cursor:pointer;font-size:13.5px;max-width:46%;text-align:left}
.pager-btn:hover{border-color:var(--accent)}
.pager-btn .dir{display:block;font-size:11px;color:var(--text-dim)}
/* ---------- 面包屑（内页） ---------- */
.crumb{display:flex;align-items:center;gap:8px;font-size:12.5px;color:var(--text-dim);margin-bottom:14px}
.crumb a{cursor:pointer}
.crumb a:hover{color:var(--accent);text-decoration:none}
.crumb .sep{opacity:.45}
/* ---------- 首页（落地页） ---------- */
#content.wide{max-width:1120px;padding:0 34px 90px}
.home-hero{padding:52px 0 6px}
.eyebrow{font-size:12.5px;letter-spacing:.1em;color:var(--accent);font-weight:600;margin-bottom:16px}
.home-hero h1{font-size:clamp(30px,4.6vw,46px);line-height:1.2;letter-spacing:-.015em;margin:0 0 12px}
.slogan{font-size:clamp(16px,2vw,20px);color:var(--accent2);font-weight:600;margin-bottom:18px}
.lead{font-size:16px;line-height:1.85;color:var(--text-dim);max-width:640px}
.hero-meta{display:flex;gap:8px;flex-wrap:wrap;margin-top:22px}
.hero-cta{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-top:30px;padding-bottom:32px;border-bottom:1px solid var(--border)}
.btn-primary{background:var(--accent);color:#08101f;border:none;border-radius:11px;padding:13px 24px;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit;transition:transform .15s,filter .15s}
.btn-primary:hover{transform:translateY(-1px);filter:brightness(1.08)}
.btn-ghost{background:transparent;color:var(--text);border:1px solid var(--border);border-radius:11px;padding:12px 20px;font-size:14.5px;cursor:pointer;font-family:inherit;transition:border-color .15s,color .15s}
.btn-ghost:hover{border-color:var(--accent);color:var(--accent)}
.hero-progress{margin-left:auto;display:flex;align-items:center;gap:14px}
.hp-wrap{display:flex;flex-direction:column;gap:7px;align-items:flex-end}
.hp-label{font-size:11.5px;color:var(--text-dim);letter-spacing:.04em}
.hp-bar{width:160px;height:7px;background:var(--panel2);border:1px solid var(--border);border-radius:20px;overflow:hidden}
.hp-fill{height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2));width:0;transition:width .4s}
.hp-num{font-size:23px;font-weight:600;letter-spacing:-.01em;white-space:nowrap}
.hp-num small{font-size:14px;color:var(--text-dim);font-weight:400}
.start-note{display:flex;gap:12px;align-items:flex-start;background:var(--panel);border:1px solid var(--border);border-left:3px solid var(--accent2);border-radius:10px;padding:15px 18px;margin:30px 0 0;font-size:14.5px;line-height:1.75;color:var(--text-dim)}
.start-note .sn-dot{color:var(--accent2);font-size:11px;line-height:1.9}
.start-note b{color:var(--text);font-weight:600}
.section{margin-top:54px}
.sec-head{margin-bottom:20px}
.sec-head h2{font-size:22px;border:none;padding:0;margin:0 0 8px}
.sec-head p{font-size:14.5px;color:var(--text-dim);line-height:1.7;max-width:680px;margin:0}
.path-hint{display:inline-block;font-size:13.5px;line-height:1.6;color:var(--co-tip);background:color-mix(in srgb,var(--co-tip) 10%,var(--panel));border:1px solid color-mix(in srgb,var(--co-tip) 32%,transparent);border-radius:12px;padding:9px 15px;margin-bottom:22px}
/* 四层主干：时间线递进 */
.layer-list{position:relative;padding-left:46px}
.layer-list::before{content:"";position:absolute;left:16px;top:26px;bottom:26px;width:2px;border-radius:2px;opacity:.5;background:linear-gradient(180deg,var(--l1),var(--l2),var(--l3),var(--l4))}
.layer-card{position:relative;display:flex;align-items:center;gap:16px;background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:18px 22px;margin-bottom:14px;cursor:pointer;transition:transform .18s,border-color .18s,box-shadow .18s}
.layer-card:hover{transform:translateX(3px);border-color:var(--lc);box-shadow:0 8px 26px rgba(0,0,0,.16)}
.layer-card::before{content:"";position:absolute;left:-36px;top:50%;margin-top:-5.5px;width:11px;height:11px;border-radius:50%;background:var(--lc);box-shadow:0 0 0 4px color-mix(in srgb,var(--lc) 20%,var(--bg))}
.layer-card[data-accent="l1"]{--lc:var(--l1)}
.layer-card[data-accent="l2"]{--lc:var(--l2)}
.layer-card[data-accent="l3"]{--lc:var(--l3)}
.layer-card[data-accent="l4"]{--lc:var(--l4)}
.lc-num{font-size:25px;font-weight:600;color:var(--text-dim);opacity:.32;letter-spacing:-.02em;min-width:36px}
.lc-main{flex:1;min-width:0}
.lc-top{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:7px}
.lc-code{font-size:12px;font-weight:600;color:var(--lc);background:color-mix(in srgb,var(--lc) 14%,transparent);border:1px solid color-mix(in srgb,var(--lc) 38%,transparent);border-radius:6px;padding:2px 8px}
.lc-name{font-size:17px;font-weight:600}
.lc-ability{font-size:13.5px;color:var(--lc)}
.lc-tag{font-size:11.5px;color:var(--text-dim);border:1px solid var(--border);border-radius:20px;padding:1px 9px}
.lc-tag.hot{color:var(--co-warning);border-color:color-mix(in srgb,var(--co-warning) 42%,transparent);background:color-mix(in srgb,var(--co-warning) 10%,transparent)}
.lc-desc{font-size:14px;color:var(--text-dim);line-height:1.65}
.lc-foot{display:flex;align-items:center;gap:14px;margin-top:11px;font-size:12px;color:var(--text-dim)}
.lc-role{color:var(--lc);font-weight:600}
.lc-bar{flex:1;max-width:180px;height:5px;background:var(--panel2);border:1px solid var(--border);border-radius:20px;overflow:hidden}
.lc-fill{height:100%;background:var(--lc);width:0;transition:width .4s}
.lc-go{font-size:17px;color:var(--text-dim);transition:transform .18s,color .18s}
.layer-card:hover .lc-go{transform:translateX(4px);color:var(--lc)}
/* 横切判断卡 */
.tool-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.judge-card{background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:18px;cursor:pointer;transition:transform .18s,border-color .18s,box-shadow .18s}
.judge-card:hover{transform:translateY(-3px);border-color:var(--co-warning);box-shadow:0 8px 26px rgba(0,0,0,.16)}
.jc-top{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:11px}
.jc-code{font-size:11.5px;font-weight:600;color:var(--co-warning);background:color-mix(in srgb,var(--co-warning) 13%,transparent);border-radius:6px;padding:2px 8px}
.jc-when{font-size:11.5px;color:var(--text-dim)}
.jc-name{font-size:15.5px;font-weight:600;margin-bottom:6px}
.jc-one{font-size:13px;color:var(--text-dim);line-height:1.6;min-height:42px}
.jc-foot{display:flex;align-items:center;gap:10px;margin-top:12px;font-size:11.5px;color:var(--text-dim)}
.jc-bar{flex:1;height:4px;background:var(--panel2);border:1px solid var(--border);border-radius:20px;overflow:hidden}
.jc-fill{height:100%;background:var(--co-warning);width:0;transition:width .4s}
/* 参考与工具 */
.mini-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px}
.mini-card{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:15px 16px;cursor:pointer;transition:border-color .18s,transform .18s}
.mini-card:hover{border-color:var(--accent);transform:translateY(-2px)}
.mc-name{font-size:14.5px;font-weight:600;margin-bottom:5px}
.mc-desc{font-size:12.5px;color:var(--text-dim);line-height:1.6}
.mc-hours{font-size:11.5px;color:var(--text-dim);margin-top:8px;opacity:.75}
.home-footer{margin-top:58px;padding-top:22px;border-top:1px solid var(--border);display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;font-size:12.5px;color:var(--text-dim)}
.home-footer a{cursor:pointer}
.side-link.home-link{margin-bottom:8px}
mark.search-hl{background:color-mix(in srgb,var(--co-question) 50%,transparent);color:inherit;border-radius:3px}
.pdf-badge{font-size:.8em;opacity:.75}
@media (max-width:900px){
  #sidebar{position:fixed;left:0;top:0;z-index:60;box-shadow:8px 0 30px rgba(0,0,0,.35)}
  #sidebar.hidden{margin-left:-290px}
  #content{padding:24px 18px 80px}
  #content.wide{padding:0 18px 70px}
  #global-progress #gp-bar{width:60px}
  .home-hero{padding:28px 0 6px}
  .hero-cta{gap:10px}
  .hero-progress{margin-left:0;width:100%;justify-content:space-between}
  .hp-wrap{align-items:flex-start}
  .layer-list{padding-left:34px}
  .layer-list::before{left:12px}
  .layer-card::before{left:-28px}
  .layer-card{padding:15px 16px;gap:12px}
  .lc-num{font-size:18px;min-width:24px}
  .lc-foot{flex-wrap:wrap;gap:10px 14px}
  .lc-bar{max-width:none;flex-basis:100%;order:9}
}
</style>
</head>
<body>
<div id="app">
  <nav id="sidebar">
    <div class="logo" onclick="location.hash='#/home'" style="cursor:pointer"><span class="coin">🪙</span> Agent AI · 学习站</div>
    <div id="side-nav"></div>
  </nav>
  <div id="main">
    <header id="topbar">
      <button id="btn-menu" title="收起/展开目录">☰</button>
      <div id="search-box" onclick="openSearch()">
        <span style="opacity:.6;font-size:13px">🔍</span>
        <input id="search-mini" placeholder="搜索全部内容" readonly>
        <span class="kbd">/</span>
      </div>
      <div id="global-progress"><span id="gp-text">0 / 0</span><div id="gp-bar"><div id="gp-fill"></div></div></div>
      <button id="btn-theme" title="切换明暗主题">☀️</button>
    </header>
    <div id="content"></div>
  </div>
</div>
<div id="search-overlay">
  <div id="search-panel">
    <input id="search-input-lg" placeholder="搜索标题与正文…（Esc 关闭）" autocomplete="off">
    <div id="search-results"></div>
  </div>
</div>
<script>
const DATA = /*__DATA__*/null;

/* ---------------- 状态 ---------------- */
const LS_CB = "agentai-cb-";
const LS_THEME = "agentai-theme";
let currentSlug = null;
let PROGRESS = {};   // slug -> {total, done, ids:[]}

/* ---------------- 初始化 ---------------- */
function initProgress(){
  for(const p of DATA.pages){
    const parser = new DOMParser();
    const doc = parser.parseFromString(p.html, "text/html");
    const ids = [...doc.querySelectorAll("input[data-cb]")].map(i=>i.dataset.cb);
    const done = ids.filter(id=>localStorage.getItem(LS_CB+id)==="1").length;
    PROGRESS[p.slug] = {total: ids.length, done, ids};
  }
}
function refreshProgressUI(){
  let total=0, done=0;
  for(const s in PROGRESS){ total+=PROGRESS[s].total; done+=PROGRESS[s].done; }
  const gt = document.getElementById("gp-text");
  if(gt) gt.textContent = done+" / "+total;
  const gf = document.getElementById("gp-fill");
  if(gf) gf.style.width = total? (done/total*100)+"%" : "0%";
  for(const p of DATA.pages){
    const el = document.querySelector(`.side-link[data-slug="${p.slug}"] .pg`);
    const pr = PROGRESS[p.slug];
    if(el && pr.total){
      el.textContent = pr.done+"/"+pr.total;
      el.parentElement.classList.toggle("all-done", pr.done===pr.total);
    }
  }
  const hgp = document.getElementById("home-gp");
  if(hgp){
    hgp.querySelector(".hp-num").innerHTML = done+"<small> / "+total+"</small>";
    hgp.querySelector(".hp-fill").style.width = (total? done/total*100 : 0)+"%";
  }
  document.querySelectorAll("[data-pr]").forEach(el=>{
    const pr = PROGRESS[el.dataset.pr];
    if(!pr || !pr.total) return;
    const pct = Math.round(pr.done/pr.total*100);
    el.querySelectorAll(".js-fill").forEach(f=>f.style.width = pct+"%");
    el.querySelectorAll(".js-num").forEach(n=>n.textContent = pr.done+"/"+pr.total);
  });
}
function saveProgress(){ refreshProgressUI(); }
function onCbChange(e){
  const id = e.target.dataset.cb;
  localStorage.setItem(LS_CB+id, e.target.checked?"1":"0");
  const pr = PROGRESS[currentSlug];
  if(pr && pr.ids.includes(id)){
    pr.done += e.target.checked?1:-1;
  }
  saveProgress();
}

/* ---------------- 侧边栏 ---------------- */
function buildSidebar(){
  const nav = document.getElementById("side-nav");
  let html = `<div class="side-link home-link" data-slug="home"><span>🏠</span><span>首页</span></div>`;
  let lastGroup = null;
  for(const p of DATA.pages){
    if(p.slug==="how-to-update") continue;
    if(p.group!==lastGroup){
      html += `<div class="side-group"><div class="side-group-title">${p.group}</div>`;
      lastGroup = p.group;
    }
    const pr = PROGRESS[p.slug];
    const pg = pr.total? `<span class="pg">${pr.done}/${pr.total}</span>` : "";
    html += `<div class="side-link" data-slug="${p.slug}"><span>${p.icon||"📄"}</span><span>${p.title}</span>${pg}</div>`;
  }
    html += `<div class="side-group"><div class="side-group-title">🛠 帮助</div>
    <div class="side-link" data-slug="how-to-update"><span>🛠</span><span>如何更新本站</span></div></div>`;
  nav.innerHTML = html;
  nav.querySelectorAll(".side-link").forEach(el=>{
    el.addEventListener("click", ()=>{ location.hash = "#/"+el.dataset.slug; });
  });
}

/* ---------------- 渲染页面 ---------------- */
/* ---------------- 首页 ---------------- */
function renderHome(){
  const c = DATA.cur;
  const content = document.getElementById("content");
  currentSlug = "home";
  content.classList.add("wide");
  document.querySelectorAll(".side-link").forEach(el=>el.classList.toggle("active", el.dataset.slug==="home"));

  let total=0, done=0;
  for(const s in PROGRESS){ total+=PROGRESS[s].total; done+=PROGRESS[s].done; }
  const gpct = total? Math.round(done/total*100) : 0;
  const prOf = s => PROGRESS[s] || {done:0, total:0};

  const layers = c.layers.map((L,i)=>{
    const pr = prOf(L.slug);
    const pct = pr.total? Math.round(pr.done/pr.total*100) : 0;
    const hot = /最优先|建议先学/.test(L.tag)? " hot" : "";
    return `<div class="layer-card" data-accent="l${i+1}" data-pr="${L.slug}" onclick="location.hash='#/${L.slug}'">
      <div class="lc-num">0${i+1}</div>
      <div class="lc-main">
        <div class="lc-top">
          <span class="lc-code">${L.code}</span>
          <span class="lc-name">${L.name}</span>
          <span class="lc-ability">${L.ability}</span>
          <span class="lc-tag${hot}">${L.tag}</span>
        </div>
        <div class="lc-desc">${L.desc}</div>
        <div class="lc-foot">
          <span class="lc-role">${L.role}</span>
          <span>${L.hours}</span>
          <div class="lc-bar"><div class="lc-fill js-fill" style="width:${pct}%"></div></div>
          <span class="js-num">${pr.done}/${pr.total}</span>
        </div>
      </div>
      <div class="lc-go">→</div>
    </div>`;
  }).join("");

  const cards = c.cards.map(K=>{
    const pr = prOf(K.slug);
    const pct = pr.total? Math.round(pr.done/pr.total*100) : 0;
    return `<div class="judge-card" data-pr="${K.slug}" onclick="location.hash='#/${K.slug}'">
      <div class="jc-top"><span class="jc-code">${K.code}</span><span class="jc-when">${K.when}</span></div>
      <div class="jc-name">${K.name}</div>
      <div class="jc-one">${K.one}</div>
      <div class="jc-foot"><span>${K.hours}</span><div class="jc-bar"><div class="jc-fill js-fill" style="width:${pct}%"></div></div><span class="js-num">${pr.done}/${pr.total}</span></div>
    </div>`;
  }).join("");

  const tools = c.tools.map(T=>`
    <div class="mini-card" onclick="location.hash='#/${T.slug}'">
      <div class="mc-name">${T.name}</div>
      <div class="mc-desc">${T.desc}</div>
      ${T.hours? `<div class="mc-hours">${T.hours}</div>` : ""}
    </div>`).join("");

  content.innerHTML = `
  <div class="home-hero">
    <div class="eyebrow">${c.eyebrow}</div>
    <h1>${c.title}</h1>
    <div class="slogan">${c.slogan}</div>
    <p class="lead">${c.lead}</p>
    <div class="hero-meta">${c.meta.map(m=>`<span class="badge">${m}</span>`).join("")}</div>
    <div class="hero-cta">
      <button class="btn-primary" onclick="location.hash='#/${c.start_slug}'">${c.start_label}</button>
      <button class="btn-ghost" onclick="openSearch()">搜索全部内容</button>
      <div class="hero-progress" id="home-gp">
        <div class="hp-wrap">
          <div class="hp-bar"><div class="hp-fill" style="width:${gpct}%"></div></div>
          <div class="hp-label">整体完成度</div>
        </div>
        <span class="hp-num">${done}<small> / ${total}</small></span>
      </div>
    </div>
  </div>

  <div class="start-note"><span class="sn-dot">◆</span><div>${c.start_note}</div></div>

  <div class="section">
    <div class="sec-head">
      <h2>四层主干</h2>
      <p>L1 给你词汇，L2 给你结构，L3 给你判断力，L4 把前三样变成交付物。</p>
    </div>
    <div class="path-hint">${c.path_hint}</div>
    <div class="layer-list">${layers}</div>
  </div>

  <div class="section">
    <div class="sec-head">
      <h2>横切判断卡</h2>
      <p>不占学习顺序，遇到对应问题就翻——它们是工具，不是课程。</p>
    </div>
    <div class="tool-grid">${cards}</div>
  </div>

  <div class="section">
    <div class="sec-head">
      <h2>参考与工具</h2>
      <p>随时查阅，不进学习路径。</p>
    </div>
    <div class="mini-grid">${tools}</div>
  </div>

  <div class="home-footer">
    <span>🪙 Agent AI 学习站 · 共 ${DATA.pages.length} 个页面</span>
    <span>构建于 __BUILD_DATE__ · <a onclick="location.hash='#/how-to-update'">如何更新本站</a></span>
  </div>`;

  window.scrollTo(0,0);
  refreshProgressUI();
}
function renderPage(slug){
  const p = DATA.pages.find(x=>x.slug===slug);
  const content = document.getElementById("content");
  content.classList.remove("wide");
  document.querySelectorAll(".side-link").forEach(el=>el.classList.remove("active"));
  const sideEl = document.querySelector(`.side-link[data-slug="${slug}"]`);
  if(sideEl){ sideEl.classList.add("active"); sideEl.scrollIntoView({block:"nearest"}); }
  if(!p){ content.innerHTML = "<h1>页面不存在</h1>"; return; }
  currentSlug = slug;
  let html = `<div class="crumb"><a onclick="location.hash='#/home'">首页</a><span class="sep">/</span><span>${p.group}</span></div>`;
  html += `<div class="page-meta">`;
  if(p.invest) html += `<span class="badge">⏱ ${p.invest}</span>`;
  if(p.updated) html += `<span class="badge">🗓 更新于 ${p.updated}</span>`;
  const pr = PROGRESS[slug];
  if(pr && pr.total) html += `<span class="badge">✅ 进度 ${pr.done}/${pr.total}</span>`;
  html += `</div><h1>${p.icon||""} ${p.title}</h1>${p.html}`;
  // 底部上一页 / 下一页
  const idx = DATA.pages.indexOf(p);
  const prev = DATA.pages[idx-1], next = DATA.pages[idx+1];
  html += `<div id="pager">`;
  html += prev? `<button class="pager-btn" onclick="location.hash='#/${prev.slug}'"><span class="dir">← 上一篇</span>${prev.title}</button>` : "<span></span>";
  html += next? `<button class="pager-btn" style="text-align:right" onclick="location.hash='#/${next.slug}'"><span class="dir">下一篇 →</span>${next.title}</button>` : "<span></span>";
  html += `</div>`;
  content.innerHTML = html;
  content.querySelectorAll("input[data-cb]").forEach(cb=>{
    cb.addEventListener("change", onCbChange);
  });
  content.querySelectorAll(".ext").forEach(a=>{a.target="_blank";a.rel="noopener";});
  window.scrollTo(0,0);
  refreshProgressUI();
}
function route(){
  const h = location.hash || "";
  // 页内锚点（标题跳转）
  if(h.startsWith("#h-")){
    const el = document.getElementById(h.slice(1));
    if(el){ el.scrollIntoView(); return; }
  }
  let slug = h.startsWith("#/") ? h.slice(2) : "home";
  // 无 hash / 未知页面 / 显式首页 → 落地页
  if(slug==="home" || !DATA.pages.find(p=>p.slug===slug)){
    if(currentSlug!=="home") renderHome();
    return;
  }
  if(slug!==currentSlug) renderPage(slug);
  else { const el = document.getElementById(h.slice(2)); if(el) el.scrollIntoView(); }
}

/* ---------------- 搜索 ---------------- */
function openSearch(){
  document.getElementById("search-overlay").classList.add("show");
  const inp = document.getElementById("search-input-lg");
  inp.value=""; inp.focus(); doSearch("");
}
function closeSearch(){ document.getElementById("search-overlay").classList.remove("show"); }
function escRe(s){ return s.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"); }
function doSearch(q){
  const box = document.getElementById("search-results");
  q = q.trim();
  if(!q){ box.innerHTML = `<div class="sr-empty">输入关键词，搜索全部 ${DATA.pages.length} 个页面</div>`; return; }
  const re = new RegExp(escRe(q), "gi");
  const results = [];
  for(const p of DATA.pages){
    const titleHit = re.test(p.title); re.lastIndex=0;
    let snip = "";
    const m = re.exec(p.search);
    if(m){
      const s = Math.max(0, m.index-45);
      snip = (s>0?"…":"") + p.search.slice(s, m.index+70).trim() + "…";
    }
    if(titleHit || m){
      let snipHtml = snip? snip.replace(re, t=>`<mark>${t}</mark>`) : "";
      results.push({p, titleHit, snipHtml});
    }
  }
  results.sort((a,b)=>(b.titleHit?1:0)-(a.titleHit?1:0));
  if(!results.length){ box.innerHTML = `<div class="sr-empty">没有找到「${q}」</div>`; return; }
  box.innerHTML = results.slice(0,30).map(r=>
    `<div class="sr-item" data-slug="${r.p.slug}">
       <div class="sr-title"><span>${r.p.icon||"📄"}</span><span>${r.p.title.replace(re,t=>`<mark>${t}</mark>`)}</span></div>
       ${r.snipHtml?`<div class="sr-snip">${r.snipHtml}</div>`:""}
     </div>`).join("");
  box.querySelectorAll(".sr-item").forEach(el=>{
    el.addEventListener("click", ()=>{
      closeSearch();
      location.hash = "#/"+el.dataset.slug;
      setTimeout(()=>highlightInPage(q), 80);
    });
  });
}
function highlightInPage(q){
  document.querySelectorAll("mark.search-hl").forEach(m=>{
    const parent = m.parentNode; parent.replaceChild(document.createTextNode(m.textContent), m); parent.normalize();
  });
  if(!q.trim()) return;
  const root = document.getElementById("content");
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
  const nodes = [];
  while(walker.nextNode()) nodes.push(walker.currentNode);
  const lower = q.toLowerCase();
  for(const node of nodes){
    const idx = node.textContent.toLowerCase().indexOf(lower);
    if(idx>=0){
      const range = document.createRange();
      range.setStart(node, idx); range.setEnd(node, idx+q.length);
      const mark = document.createElement("mark"); mark.className="search-hl";
      try{ range.surroundContents(mark); mark.scrollIntoView({block:"center"}); }catch(e){}
      break;
    }
  }
}

/* ---------------- 主题 ---------------- */
function applyTheme(){
  const t = localStorage.getItem(LS_THEME)||"dark";
  document.body.classList.toggle("light", t==="light");
  document.getElementById("btn-theme").textContent = t==="light"?"🌙":"☀️";
}

/* ---------------- 启动 ---------------- */
initProgress();
buildSidebar();
applyTheme();
saveProgress();
window.addEventListener("hashchange", route);
document.getElementById("btn-menu").addEventListener("click", ()=>document.getElementById("sidebar").classList.toggle("hidden"));
document.getElementById("btn-theme").addEventListener("click", ()=>{
  const t = localStorage.getItem(LS_THEME)==="light"?"dark":"light";
  localStorage.setItem(LS_THEME,t); applyTheme();
});
document.getElementById("search-overlay").addEventListener("click", e=>{ if(e.target.id==="search-overlay") closeSearch(); });
document.getElementById("search-input-lg").addEventListener("input", e=>doSearch(e.target.value));
document.addEventListener("keydown", e=>{
  if(e.key==="/" && !e.target.matches("input,textarea")){ e.preventDefault(); openSearch(); }
  if(e.key==="Escape") closeSearch();
});
route();
</script>
</body>
</html>
'''

if __name__ == "__main__":
    build()
