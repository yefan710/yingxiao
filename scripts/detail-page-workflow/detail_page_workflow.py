#!/usr/bin/env python3
"""Detail-page workflow scaffold and package generator.

This script does not call an LLM. It creates the operating structure and
Codex-ready prompts so the workflow stays honest about missing source material.
"""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / "templates/detail-page-workflow/case").exists():
            return path
    raise RuntimeError("Cannot find repo root with templates/detail-page-workflow/case")


ROOT = find_repo_root(Path(__file__).resolve())
CASE_TEMPLATE = ROOT / "templates/detail-page-workflow/case"
ROLE_PROMPTS = ROOT / "templates/detail-page-workflow/role_prompts"
QA_CONFIG = ROOT / "config/detail-page-workflow/qa_scorecard.json"
DESIGN_SPEC = ROOT / "config/detail-page-workflow/design_spec.json"


DEFAULT_NEW_PAGE_SCREENS = [
    ("part1", "头图", "816 x 1054", "功能上新/首屏定位", "产品或功能一句话价值", "主视觉、功能名、适用场景", "标题 10 字内，副标题 20 字内"),
    ("part2", "功能汇总图", "816 x 1054", "集中展示功能模块", "功能全局认知", "功能卡片、统一图标、短说明", "功能名 4-8 字，说明 12 字内"),
    ("part3", "各个功能配图", "816 x 982", "逐个解释核心功能", "功能价值 + 使用证据", "真实截图、局部标注、场景说明", "标题 10 字内，标注 6-14 字"),
]

DEFAULT_ITERATION_SCREENS = [
    ("part1 头图", "保留", "原头图仍能承接本次功能上新", "只做轻量视觉统一或文案微调"),
    ("part1 头图", "重做", "新功能改变首屏承诺或购买理由", "重做功能上新图"),
    ("part2 功能汇总图", "替换", "功能列表、优先级或分组发生变化", "重做功能卡片矩阵"),
    ("part3 各个功能配图", "插入", "新增功能重要但不改变产品定位", "新增该功能的单独配图"),
    ("part3 各个功能配图", "替换", "原功能截图过时或证明不足", "用新版截图、标注和文案替换"),
]


@dataclass(frozen=True)
class CasePaths:
    root: Path
    product_doc: Path
    pain_points: Path
    original_page: Path
    visual_norms: Path
    assets: Path
    output: Path


def case_paths(case_dir: Path) -> CasePaths:
    return CasePaths(
        root=case_dir,
        product_doc=case_dir / "01_product_doc.md",
        pain_points=case_dir / "02_user_pain_points.md",
        original_page=case_dir / "03_original_page.md",
        visual_norms=case_dir / "04_visual_norms",
        assets=case_dir / "05_assets",
        output=case_dir / "06_output",
    )


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def has_real_content(path: Path) -> bool:
    text = read_text(path)
    meaningful = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and line.strip() != "NEEDS_SOURCE" and not line.lstrip().startswith("#")
    ]
    return bool(meaningful)


def excerpt(path: Path, limit: int = 900) -> str:
    text = read_text(path).strip()
    if not text:
        return "NEEDS_SOURCE"
    compact = "\n".join(line.rstrip() for line in text.splitlines() if line.strip())
    if len(compact) <= limit:
        return compact
    return compact[:limit].rstrip() + "\n..."


def list_dir(path: Path) -> list[str]:
    if not path.exists():
        return []
    ignored = {".DS_Store", "README.md", "mask_plan.example.json"}
    return sorted(str(p.relative_to(path)) for p in path.rglob("*") if p.is_file() and p.name not in ignored)


def init_case(args: argparse.Namespace) -> None:
    case_dir = Path(args.case_dir).resolve()
    if case_dir.exists() and any(case_dir.iterdir()) and not args.force:
        raise SystemExit(f"Case directory already exists and is not empty: {case_dir}")

    shutil.copytree(CASE_TEMPLATE, case_dir, dirs_exist_ok=True)
    meta = {
        "product_name": args.product_name,
        "mode": args.mode,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "intake",
    }
    write_text(case_dir / "workflow_case.json", json.dumps(meta, ensure_ascii=False, indent=2))
    print(f"Created case: {case_dir}")
    print("Next: fill 01_product_doc.md, 02_user_pain_points.md, and add visual norms/assets.")


def validate_case(paths: CasePaths) -> list[str]:
    issues: list[str] = []
    if not paths.product_doc.exists():
        issues.append("missing 01_product_doc.md")
    elif not has_real_content(paths.product_doc):
        issues.append("01_product_doc.md has no real source content")

    if not paths.pain_points.exists():
        issues.append("missing 02_user_pain_points.md")
    elif not has_real_content(paths.pain_points):
        issues.append("02_user_pain_points.md has no real source content")

    if not paths.original_page.exists():
        issues.append("missing 03_original_page.md")

    if not paths.visual_norms.exists():
        issues.append("missing 04_visual_norms/")
    elif not list_dir(paths.visual_norms):
        issues.append("04_visual_norms/ is empty")

    if not paths.assets.exists():
        issues.append("missing 05_assets/")
    elif not list_dir(paths.assets):
        issues.append("05_assets/ is empty")

    return issues


def load_case_meta(case_dir: Path) -> dict[str, str]:
    meta_path = case_dir / "workflow_case.json"
    if not meta_path.exists():
        return {"product_name": case_dir.name, "mode": "new_page"}
    return json.loads(read_text(meta_path))


def role_prompt(name: str) -> str:
    return read_text(ROLE_PROMPTS / name)


def load_design_spec() -> dict:
    return json.loads(read_text(DESIGN_SPEC))


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    head = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([head, sep, *body])


def table_cell(lines: list[str]) -> str:
    return "<br>".join(line.replace("|", "｜") for line in lines)


def render_design_spec() -> str:
    spec = load_design_spec()
    palette_rows = [[name, value] for name, value in spec["palette"].items()]
    type_rows = [
        [
            item["name"],
            item["structure"],
            item["description"],
            " / ".join(item["best_for"]),
            " / ".join(item["reference_examples"]),
        ]
        for item in spec["image_types"].values()
    ]
    source_rows = [
        [
            source["name"],
            source["canvas"],
            source["format"],
            " / ".join(source["palette"]),
            source["html"],
        ]
        for source in spec["design_sources"].values()
    ]
    structure_rows = [
        [
            item["part"],
            item["name"],
            item["default_canvas"],
            item["purpose"],
            " / ".join(item["required_content"]),
            item["copy_budget"],
        ]
        for item in spec["page_structure"]
    ]
    copy_rows = [
        [key, table_cell([f"{name}: {value}" for name, value in rules.items()])]
        for key, rules in spec["copy_rules"].items()
    ]
    font_rows = [
        [
            key,
            table_cell([f"{name}: {value}" for name, value in rules.items()])
            if isinstance(rules, dict)
            else str(rules),
        ]
        for key, rules in spec["font_size_rules"].items()
    ]
    composite_rows = [
        [
            key,
            " / ".join(value) if isinstance(value, list) else str(value),
        ]
        for key, value in spec["screenshot_composite_rules"].items()
    ]
    return f"""# 00 Design Spec

Spec: {spec["name"]}

## Source

- Source dir: `{spec["source_dir"]}`
- Reference root: `{spec["reference_root"]}`
- Reference images: `{spec["reference_images_dir"]}`

## Design Sources

{md_table(["Name", "Canvas", "Format", "Palette", "HTML"], source_rows)}

## Palette

{md_table(["Token", "Hex"], palette_rows)}

## Canvas

{md_table(["Type", "Size"], [
    ["part1 header", spec["canvas"]["part1_header"]],
    ["part2 summary", spec["canvas"]["part2_summary"]],
    ["part3 function explain", spec["canvas"]["part3_function_explain"]],
    ["legacy function image", spec["canvas"]["legacy_function_image"]],
    ["Reference output width", str(spec["canvas"]["reference_output_width"])],
])}

## Page Structure

{md_table(["Part", "Name", "Canvas", "Purpose", "Required Content", "Copy Budget"], structure_rows)}

## Part3 Image Types

{md_table(["Type", "Structure", "Description", "Best For", "Reference Examples"], type_rows)}

## Copy Rules

{md_table(["Part / Type", "Rules"], copy_rows)}

## Font Size Rules

{md_table(["Part / Type", "Reference Sizes"], font_rows)}

## Copy Style Rules

{chr(10).join(f"- {rule}" for rule in spec["copy_style_rules"])}

## Screenshot Composite Rules

{md_table(["Rule", "Value"], composite_rows)}

## Visual Rules

{chr(10).join(f"- {rule}" for rule in spec["visual_rules"])}

## Negative Rules

{chr(10).join(f"- {rule}" for rule in spec["negative_rules"])}
"""


def render_requirement_brief(meta: dict[str, str], paths: CasePaths, issues: list[str]) -> str:
    product = meta.get("product_name") or paths.root.name
    mode = meta.get("mode", "new_page")
    return f"""# 01 Requirement Brief

Product: {product}
Page mode: `{mode}`
Generated: {datetime.now().isoformat(timespec="seconds")}

## Source Status

{md_table(["Input", "Status"], [
    ["Product doc", "READY" if has_real_content(paths.product_doc) else "NEEDS_SOURCE"],
    ["Pain points", "READY" if has_real_content(paths.pain_points) else "NEEDS_SOURCE"],
    ["Original page", "READY" if has_real_content(paths.original_page) else "OPTIONAL_OR_NEEDS_SOURCE"],
    ["Visual norms", "READY" if list_dir(paths.visual_norms) else "NEEDS_SOURCE"],
    ["Assets", "READY" if list_dir(paths.assets) else "NEEDS_SOURCE"],
])}

## Draft Brief

- 产品一句话：NEEDS_SOURCE
- 目标用户：NEEDS_SOURCE
- 用户痛点：NEEDS_SOURCE
- 核心卖点：NEEDS_SOURCE
- 可用证明材料：{", ".join(list_dir(paths.assets)) if list_dir(paths.assets) else "NEEDS_SOURCE"}
- 缺失材料：{", ".join(issues) if issues else "None"}
- 合规风险：所有效果、增长、转化、收益类表达必须有来源证明。

## Product Doc Excerpt

```text
{excerpt(paths.product_doc)}
```

## Pain Points Excerpt

```text
{excerpt(paths.pain_points)}
```

## Codex Prompt

{role_prompt("01_requirement_structurer.md")}
"""


def render_screen_plan(meta: dict[str, str]) -> str:
    mode = meta.get("mode", "new_page")
    if mode == "feature_iteration":
        rows = [[part, change, when, action] for part, change, when, action in DEFAULT_ITERATION_SCREENS]
        body = md_table(["Part", "Change Type", "When To Use", "Action"], rows)
    else:
        rows = [
            [part, name, canvas, task, message, asset, budget]
            for part, name, canvas, task, message, asset, budget in DEFAULT_NEW_PAGE_SCREENS
        ]
        body = md_table(["Part", "Image Name", "Canvas", "Task", "Main Message", "Asset Need", "Copy Budget"], rows)

    return f"""# 02 Screen Plan

Page mode: `{mode}`

## Draft Plan

{body}

## Gate

运营确认 part1 头图、part2 功能汇总图、part3 各功能配图的数量、顺序、画布尺寸和模板方向后，才能进入文案阶段。

## Part3 Type Rule

- 功能配图：文案 + 配图，适合后台工具、检测、导出、批量操作等单界面证明型功能。
- 功能说明 / 2图混合层：文案 + 配图 + 框，适合 AI、素材组合、模板效果、前后对比等多图混合型功能。

## Codex Prompt

{role_prompt("02_main_flow_designer.md")}
"""


def render_copy_draft(meta: dict[str, str]) -> str:
    mode = meta.get("mode", "new_page")
    spec = load_design_spec()
    if mode == "feature_iteration":
        rows = [
            ["待定", "NEEDS_SOURCE", "NEEDS_SOURCE", "NEEDS_SOURCE", "NEEDS_SOURCE", "NEEDS_SOURCE", "NEEDS_SOURCE", "NEEDS_SOURCE"]
        ]
    else:
        rows = [
            [part, "NEEDS_SOURCE", "NEEDS_SOURCE", "NEEDS_SOURCE", "NEEDS_SOURCE", "NEEDS_SOURCE", "NEEDS_SOURCE", "NEEDS_SOURCE"]
            for part, *_ in DEFAULT_NEW_PAGE_SCREENS
        ]
    copy_rows = [
        [key, table_cell([f"{name}: {value}" for name, value in rules.items()])]
        for key, rules in spec["copy_rules"].items()
    ]
    font_rows = [
        [
            key,
            table_cell([f"{name}: {value}" for name, value in rules.items()])
            if isinstance(rules, dict)
            else str(rules),
        ]
        for key, rules in spec["font_size_rules"].items()
    ]
    return f"""# 03 Copy Draft

## Copy Budget By Part / Image Type

{md_table(["Part / Type", "Rules"], copy_rows)}

## Font Size Reference

{md_table(["Part / Type", "Reference Sizes"], font_rows)}

## Copy Style

{chr(10).join(f"- {rule}" for rule in spec["copy_style_rules"])}

## Draft Copy Table

{md_table(["Part", "Image Type", "Main Title", "Subtitle", "Module Copy", "Screenshot Annotation", "Source", "Risk"], rows)}

## Codex Prompt

{role_prompt("03_copy_assistant.md")}
"""


def render_visual_direction(paths: CasePaths) -> str:
    norms = list_dir(paths.visual_norms)
    spec = load_design_spec()
    return f"""# 04 Visual Direction

## Visual Norm Sources

{", ".join(norms) if norms else "NEEDS_SOURCE"}

## Required Palette

{md_table(["Token", "Hex"], [[name, value] for name, value in spec["palette"].items()])}

## Required Page Structure

- part1: 头图，通常为功能上新图
- part2: 功能汇总图
- part3: 各个功能配图

## Default Direction From Design Spec

{chr(10).join(f"- {rule}" for rule in spec["visual_rules"])}

## Negative Rules

{chr(10).join(f"- {rule}" for rule in spec["negative_rules"])}

## Codex Prompt

{role_prompt("04_visual_director.md")}
"""


def render_asset_plan(paths: CasePaths) -> str:
    assets = list_dir(paths.assets)
    rows = [
        ["part1 头图", "功能上新/核心定位", "主视觉、产品截图或功能概念图", "NEEDS_SOURCE", "中心展示", "MISSING_ASSET" if not assets else "CHECK_ASSET"],
        ["part2 功能汇总图", "功能模块总览", "功能图标、卡片、短说明", "NEEDS_SOURCE", "卡片矩阵", "MISSING_ASSET" if not assets else "CHECK_ASSET"],
        ["part3 功能配图", "单个功能价值证明", "真实后台截图、局部放大、标注", "NEEDS_SOURCE", "文案 + 配图", "MISSING_ASSET" if not assets else "CHECK_ASSET"],
        ["part3 功能说明/2图混合层", "多素材组合或 AI 效果说明", "多张素材图、效果图、模板图、外层白框/蓝色描边框", "NEEDS_SOURCE", "文案 + 配图 + 框", "MISSING_ASSET" if not assets else "CHECK_ASSET"],
    ]
    return f"""# 05 Asset Plan

## Available Assets

{", ".join(assets) if assets else "NEEDS_SOURCE"}

## Draft Asset Table

{md_table(["Part", "Selling Point", "Needed Asset", "State", "Crop/Annotation", "Status"], rows)}

## Codex Prompt

{role_prompt("05_asset_director.md")}
"""


def render_screenshot_mask_plan(paths: CasePaths) -> str:
    assets = list_dir(paths.assets)
    spec = load_design_spec()
    rules = spec["screenshot_composite_rules"]
    rows = [
        [
            "part3-01",
            "功能配图",
            "main_screenshot",
            "NEEDS_SOURCE",
            "NEEDS_COORDINATES",
            "NEEDS_COORDINATES",
            "NEEDS_COORDINATES",
            "NEEDS_COORDINATES",
            "cover_crop",
            "12-24",
            "8-16",
            "真实后台主界面；截图建议至少为 mask 的 1.5-2 倍",
        ],
        [
            "part3-01",
            "功能配图",
            "zoom_detail",
            "OPTIONAL",
            "NEEDS_COORDINATES",
            "NEEDS_COORDINATES",
            "NEEDS_COORDINATES",
            "NEEDS_COORDINATES",
            "contain_pad",
            "12-24",
            "6-12",
            "局部放大弹窗或重点字段；没有则删除该槽",
        ],
        [
            "part3-02",
            "功能说明/2图混合层",
            "image_mix_a",
            "NEEDS_SOURCE",
            "NEEDS_COORDINATES",
            "NEEDS_COORDINATES",
            "NEEDS_COORDINATES",
            "NEEDS_COORDINATES",
            "cover_crop",
            "12-24",
            "8-16",
            "多图组合第 1 张，必须是真实截图/设计稿/商品素材",
        ],
        [
            "part3-02",
            "功能说明/2图混合层",
            "image_mix_b",
            "NEEDS_SOURCE",
            "NEEDS_COORDINATES",
            "NEEDS_COORDINATES",
            "NEEDS_COORDINATES",
            "NEEDS_COORDINATES",
            "cover_crop",
            "12-24",
            "8-16",
            "多图组合第 2 张，必须是真实截图/设计稿/商品素材",
        ],
    ]
    return f"""# 05 Screenshot Mask Plan

## Purpose

功能配图和功能说明里的产品界面不走纯 AI 重绘。先生成 layout draft 和 mask 坐标，运营按坐标截图，再由 Codex/设计工具把真实截图贴入。

## Available Assets

{", ".join(assets) if assets else "NEEDS_SOURCE"}

## Composite Rules

{md_table(["Rule", "Value"], [[key, " / ".join(value) if isinstance(value, list) else str(value)] for key, value in rules.items()])}

## Mask Coordinate Table

坐标以最终导出画布左上角为原点，单位 px。`x/y/width/height` 必须在视觉草稿确认后填写，不能凭空估计。

{md_table(["Image ID", "Type", "Slot", "Asset", "x", "y", "width", "height", "fit_mode", "corner_radius", "safe_padding", "Screenshot Request"], rows)}

## Screenshot Handoff SOP

1. 视觉草稿阶段：只生成背景、标题、bullet、截图框、标注和 mask 占位。
2. Mask 输出阶段：为每个真实截图槽输出 `x/y/width/height/corner_radius/fit_mode/safe_padding`。
3. 运营截图阶段：按 `Screenshot Request` 提供真实截图或设计稿，实际截图尺寸建议大于 mask 1.5-2 倍。
4. 合成阶段：贴入真实截图，只做裁切、缩放、圆角遮罩、阴影、描边、局部标注和脱敏。
5. 质检阶段：检查截图是否真实、是否清晰、是否被 AI 重绘、是否有敏感信息。

## Draft Prompt Add-on

```text
本图包含真实截图区域。不要生成、重绘或虚构后台 UI。
请只生成 layout draft：背景、标题、bullet、装饰、截图容器和灰色 mask 占位。
每个 mask 占位必须输出坐标：x、y、width、height、corner_radius、fit_mode、safe_padding。
槽内写占位名，例如 main_screenshot，不要画具体表格、按钮、数据或店铺信息。
```
"""


def render_production_prompts(meta: dict[str, str]) -> str:
    product = meta.get("product_name", "NEEDS_SOURCE")
    spec = load_design_spec()
    source_palette_lines = [
        f"- {source['name']}：{'、'.join(source['palette'])}"
        for source in spec["design_sources"].values()
    ]
    return f"""# 06 Production Prompts

## Master Prompt

```text
为电商服务市场 SaaS 产品「{product}」生成详情页视觉稿。

必须遵守：
- 内置 image2 生成参数必须为：resolution=2k，quality=high。
- 若通过对话式 image2 生成，每张图提示词开头必须写明“生成 2k 分辨率、高质量图”。
- 使用已确认的屏幕规划、文案和视觉规范。
- 详情页结构固定为 part1 头图、part2 功能汇总图、part3 各个功能配图。
- part1/part2 参考《详情页-功能介绍头图》，part3 参考《详情页-功能介绍》，旧版 1500 x 1125 参考《欢乐逛功能配图-1》。
- part3 必须先判断版型：功能配图 = 文案 + 配图；功能说明/2图混合层 = 文案 + 配图 + 框。
- 产品界面和功能截图必须使用真实截图/设计稿贴入；生图阶段只允许生成 mask 占位，不允许重绘后台 UI。
- 缺素材时标 MISSING_ASSET，不生成假后台、假数据、假客户案例。
- 每张图只有一个主要沟通任务。
- 标题、副标题和模块文案不能溢出。
- 风格保持浅色服务市场功能说明风，卡片、截图框、图标风格统一。
```

## Required Palettes

{chr(10).join(source_palette_lines)}

## Screen Prompt Skeleton

```text
生成 {{part}} 详情页配图。

生成设置：内置 image2，resolution=2k，quality=high。
Part：{{part}}
版型：{{image_type}}
画布：{{canvas_size}}
图的任务：{{image_task}}
主标题：{{main_title}}
副标题：{{subtitle}}
模块文案：{{module_copy}}
需要素材：{{asset_list}}

布局要求：
{{layout_rules}}

视觉要求：
{{visual_rules}}

版型规则：
- 如果是功能配图，只使用文案 + 一个主要界面/结果配图，保持简洁。
- 如果是功能说明/2图混合层，必须使用文案 + 多图组合 + 外层白色卡片或蓝色描边框。

真实截图规则：
- 对所有后台 UI/设计稿区域，只生成 mask 占位和坐标，不生成槽内 UI。
- 输出每个 mask 的 x、y、width、height、corner_radius、fit_mode、safe_padding。
- 等运营提供对应尺寸截图后，再贴入真实截图。

负向约束：
- 不要生成假后台数据
- 不要混用图标风格
- 不要让文字溢出
- 不要脱离对应 part 的指定色板
- 不要偏离已批准视觉规范
```

## Codex Prompt

{role_prompt("06_prompt_assembler.md")}
"""


def render_qa_scorecard() -> str:
    config = json.loads(read_text(QA_CONFIG))
    rows = [
        [
            item["name"],
            str(item["weight"]),
            item["pass_standard"],
            " / ".join(item["blocking_examples"]),
        ]
        for item in config["dimensions"]
    ]
    return f"""# 07 QA Scorecard

## Scorecard

{md_table(["Dimension", "Weight", "PASS Standard", "Blocking Examples"], rows)}

## Release Rule

- 90-100: PASS
- 80-89: PASS WITH POLISH
- 70-79: FIX IMPORTANT ISSUES
- Below 70: FIX REQUIRED
- Any blocking issue: FIX REQUIRED

## Codex Prompt

{role_prompt("07_quality_inspector.md")}
"""


def render_revision_routing() -> str:
    return f"""# 08 Revision Routing

{md_table(["Problem Found", "Send Back To", "Fix Type"], [
    ["产品定位不清", "Requirement Structurer", "Rebuild brief"],
    ["屏幕太多/太少", "Main-Flow Designer", "Replan canvas"],
    ["文案超字数", "Copy Assistant", "Rewrite within budget"],
    ["风格跑偏", "Visual Director", "Tighten style constraints"],
    ["截图不够证明卖点", "Screenshot / Asset Director", "Add or recrop asset"],
    ["提示词无法执行", "Production Prompt Assembler", "Rewrite prompt"],
    ["多项发布风险", "Quality Inspector + Main-Flow Designer", "Reopen page plan"],
])}
"""


def render_workflow_package(meta: dict[str, str], issues: list[str]) -> str:
    return f"""# Workflow Package

Product: {meta.get("product_name", "NEEDS_SOURCE")}
Mode: `{meta.get("mode", "new_page")}`
Generated: {datetime.now().isoformat(timespec="seconds")}

## Status

{"FIX INTAKE FIRST" if issues else "READY FOR ROLE RUNS"}

## Intake Issues

{chr(10).join(f"- {issue}" for issue in issues) if issues else "- None"}

## Output Files

1. `00_design_spec.md`
2. `01_requirement_brief.md`
3. `02_screen_plan.md`
4. `03_copy_draft.md`
5. `04_visual_direction.md`
6. `05_asset_plan.md`
7. `05_screenshot_mask_plan.md`
8. `06_production_prompts.md`
9. `07_qa_scorecard.md`
10. `08_revision_routing.md`

## How To Use

1. Open `01_requirement_brief.md` and run the embedded Codex prompt with real source material.
2. Confirm the brief before opening `02_screen_plan.md`.
3. Continue one gate at a time.
4. Any `NEEDS_SOURCE` or `MISSING_ASSET` must be resolved or explicitly accepted before production.
"""


def build_package(args: argparse.Namespace) -> None:
    case_dir = Path(args.case_dir).resolve()
    paths = case_paths(case_dir)
    if not case_dir.exists():
        raise SystemExit(f"Case directory does not exist: {case_dir}")

    meta = load_case_meta(case_dir)
    issues = validate_case(paths)
    paths.output.mkdir(parents=True, exist_ok=True)

    outputs = {
        "workflow_package.md": render_workflow_package(meta, issues),
        "00_design_spec.md": render_design_spec(),
        "01_requirement_brief.md": render_requirement_brief(meta, paths, issues),
        "02_screen_plan.md": render_screen_plan(meta),
        "03_copy_draft.md": render_copy_draft(meta),
        "04_visual_direction.md": render_visual_direction(paths),
        "05_asset_plan.md": render_asset_plan(paths),
        "05_screenshot_mask_plan.md": render_screenshot_mask_plan(paths),
        "06_production_prompts.md": render_production_prompts(meta),
        "07_qa_scorecard.md": render_qa_scorecard(),
        "08_revision_routing.md": render_revision_routing(),
    }
    for filename, content in outputs.items():
        write_text(paths.output / filename, content)

    status = "FIX INTAKE FIRST" if issues else "READY FOR ROLE RUNS"
    print(f"Built package: {paths.output}")
    print(f"Status: {status}")
    if issues:
        print("Intake issues:")
        for issue in issues:
            print(f"- {issue}")


def validate_command(args: argparse.Namespace) -> None:
    paths = case_paths(Path(args.case_dir).resolve())
    issues = validate_case(paths)
    if not issues:
        print("READY")
        return
    print("FIX INTAKE FIRST")
    for issue in issues:
        print(f"- {issue}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Detail-page workflow toolkit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init-case", help="Create a new detail-page case folder")
    init.add_argument("case_dir")
    init.add_argument("--mode", choices=["new_page", "feature_iteration"], default="new_page")
    init.add_argument("--product-name", default="NEEDS_SOURCE")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=init_case)

    validate = subparsers.add_parser("validate-case", help="Check whether a case has source material")
    validate.add_argument("case_dir")
    validate.set_defaults(func=validate_command)

    build = subparsers.add_parser("build-package", help="Generate workflow output files")
    build.add_argument("case_dir")
    build.set_defaults(func=build_package)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
