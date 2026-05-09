# Detail Page Workflow

Codex 驱动的电商服务市场 SaaS 详情页生产工作流。

这个工具包把已批准的设计方案落成可执行材料：任务目录、角色提示词、QA 评分表、返修路由，以及一个本地脚本，用来初始化详情页任务并生成第一版生产包。

## 适用场景

- 新平台：从 0 到 1 生成整套详情图
- 老平台：新增功能时迭代原详情页

## 固定详情页结构

- `part1`：头图，通常为功能上新图，参考 `/Users/admin/Desktop/运营推广材料/服务市场详情页/设计规范/功能汇总头图.html`
- `part2`：功能汇总图，同样参考功能汇总头图规范
- `part3`：各个功能配图，参考 `/Users/admin/Desktop/运营推广材料/服务市场详情页/设计规范/功能说明.html`

`part3` 需要继续分两种版型：

- 功能配图：文案 + 配图。适合后台工具、检测、导出、监控、批量操作等单界面证明型功能。
- 功能说明 / 2图混合层：文案 + 配图 + 框。适合 AI、素材组合、模板效果、前后对比、多图展示。

旧版 1500 x 1125 功能配图兼容参考：`/Users/admin/Desktop/运营推广材料/服务市场详情页/设计规范/功能配图设计规范.html`

指定色板已经写入 `config/design_spec.json`，生成包会输出 `00_design_spec.md`。

## 文案和字号规范

`config/design_spec.json` 已加入服务市场参考图的文字规范，生成包会同步输出到 `03_copy_draft.md`：

- 头图：主标题 4-8 字优先，最长 12 字；副标题 12-22 字优先；功能卡片标题 3-6 字。
- 功能汇总图：主标题 8-14 字优先；bullet 标签 4-6 字，正文 18-32 字；标签 4-7 字。
- 功能配图：标题 4-7 字优先；2 条 bullet 优先，最多 3 条；每条 24-36 字；截图标注 4-8 字。
- 功能说明 / 2图混合层：标题 4-8 字；副标题 10-20 字；功能块标题 4-8 字；检查项 6-14 字。

字号按 1632px 宽参考图估算，并在 816px 宽画布中等比缩放：大标题必须最强，bullet 可读，截图标注不抢主标题层级。

## 真实截图贴图流程

功能配图和功能说明里的后台界面、产品截图、设计稿不走纯 AI 重绘，避免出现假 UI、假数据和界面变形。

推荐流程：

1. Codex/视觉工具先出草稿：只生成背景、标题、bullet、截图容器、装饰和灰色 mask 占位。
2. 输出 `05_screenshot_mask_plan.md`：每个截图槽给出 `x/y/width/height/corner_radius/fit_mode/safe_padding`。
3. 运营按坐标表截图：截图尺寸建议至少为 mask 的 1.5-2 倍；需要局部放大时单独截图。
4. Codex/设计工具合成：把真实截图按 mask 裁切、缩放、圆角、阴影、描边贴入。
5. 质检：检查截图是否真实、清晰、未拉伸、未重绘，并完成必要脱敏。

没有真实截图或设计稿时，最终图只能停在 layout draft，不能进入发布稿。

本地贴图可以用：

```bash
python3 bin/composite_screenshots.py \
  --draft path/to/layout_draft.png \
  --mask-json path/to/mask_plan.json \
  --assets-dir path/to/05_assets \
  --out path/to/final_composite.png
```

`05_assets/mask_plan.example.json` 是坐标文件模板。

## 快速开始

```bash
python3 bin/detail_page_workflow.py init-case cases/huanleguang_new --mode new_page --product-name 欢乐逛
```

把资料放进生成的目录：

- `01_product_doc.md`: 产品文档、功能说明、服务说明
- `02_user_pain_points.md`: 人群痛点、购买顾虑、使用场景
- `03_original_page.md`: 原详情页链接、截图说明、旧页面结构
- `04_visual_norms/`: 视觉规范截图、模板、色彩说明
- `05_assets/`: 产品截图、功能截图、图标、证明材料

生成结构化生产包：

```bash
python3 bin/detail_page_workflow.py build-package cases/huanleguang_new
```

输出会写入：

```text
cases/huanleguang_new/06_output/
```

## 工作流闸门

1. 需求结构化
2. 主流程设计
3. 文案生成
4. 视觉总监
5. 截图/素材导演
6. 提示词组装
7. 质检员

每个阶段的输出都是下一个角色的输入。缺资料时统一标 `NEEDS_SOURCE`，禁止 AI 编造痛点、数据、案例或功能。

## 产物说明

`build-package` 会生成：

- `workflow_package.md`: 全量生产包索引
- `00_design_spec.md`: 当前设计规范、来源文件、尺寸和色板
- `01_requirement_brief.md`: 标准需求包
- `02_screen_plan.md`: 画布和屏幕规划
- `03_copy_draft.md`: 分屏文案稿
- `04_visual_direction.md`: 视觉统一指令
- `05_asset_plan.md`: 截图和素材清单
- `05_screenshot_mask_plan.md`: 功能配图/功能说明的真实截图 mask 坐标和截图请求
- `06_production_prompts.md`: 屏幕级生成提示词
- `07_qa_scorecard.md`: 发布前质检表
- `08_revision_routing.md`: 问题退回角色表

## 推荐运行方式

第一轮不要直接追求自动化出终图。先选两个真实任务试跑：

- 一个新平台详情页
- 一个老平台功能迭代

确认闸门能抓住真实问题后，再把提示词和目录结构固化进内部 Codex 命令或你们自己的视觉工具流程。
