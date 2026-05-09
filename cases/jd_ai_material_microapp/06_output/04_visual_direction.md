# 04 Visual Direction

## Visual Norm Sources

visual_norm_summary.md

## Required Palette

| Token | Hex |
| --- | --- |
| function_image_mist_blue | #c1d5ed |
| function_image_cool_gray | #8f9498 |
| function_image_near_white | #fbfbfb |
| function_image_lavender_blue | #e5e8fe |
| function_image_mint_green | #bee2d6 |
| summary_header_blue_gray | #c3d3e4 |
| summary_header_warm_gray | #e3e2db |
| summary_header_mint | #e1f6eb |
| summary_header_near_white | #fafbfc |
| summary_header_primary_blue | #2652f6 |
| function_explain_gray | #d1d5d6 |
| function_explain_light_blue | #c2d7f6 |
| function_explain_primary_blue | #1b44f0 |
| function_explain_deep_blue | #142ff0 |
| function_explain_accent_blue | #3763f3 |

## Required Page Structure

- part1: 头图，通常为功能上新图
- part2: 功能汇总图
- part3: 各个功能配图

## Default Direction From Design Spec

- 整体为浅色服务市场功能说明风，不能做成红黄大促海报
- part1 头图和 part2 功能汇总图优先参考《详情页-功能介绍头图》规范，使用 #c3d3e4、#e3e2db、#e1f6eb、#fafbfc、#2652f6
- part3 各功能配图优先参考《详情页-功能介绍》规范，使用 #d1d5d6、#c2d7f6、#1b44f0、#142ff0、#3763f3
- part3 需要先判断版型：功能配图 = 文案 + 配图；功能说明/2图混合层 = 文案 + 配图 + 框
- 功能配图适合后台工具类功能，以单个主要界面截图为视觉主体，不额外套大框
- 功能说明/2图混合层适合 AI、素材组合、模板效果、前后对比类功能，必须有外层白色卡片或蓝色描边框承载多图混合
- 旧版欢乐逛功能配图或需要兼容 1500 x 1125 时，使用 #c1d5ed、#8f9498、#fbfbfb、#e5e8fe、#bee2d6
- 功能卡片、截图框、标注框保持统一圆角、统一阴影、统一图标风格
- 必须保留足够留白，避免一张图塞太多功能说明
- 真实后台截图必须可读，不能用 AI 生成假数据、假界面、假客户案例

## Negative Rules

- 不要使用深色背景
- 不要使用红黄大促风
- 不要生成不存在的后台数据
- 不要混用写实图标、线性图标、3D 图标
- 不要让标题、副标题、功能卡片文字溢出
- 不要脱离指定色板

## Codex Prompt

# 视觉总监

你是详情页视觉总监。请基于已确认的屏幕规划、文案和视觉规范样例，生成统一视觉方向。

## 要求

1. 严格遵守视觉规范，不重新发明风格。
2. 详情页结构必须匹配：part1 头图、part2 功能汇总图、part3 各个功能配图。
3. part1/part2 优先参考《详情页-功能介绍头图》，色板：`#c3d3e4`、`#e3e2db`、`#e1f6eb`、`#fafbfc`、`#2652f6`。
4. part3 优先参考《详情页-功能介绍》，色板：`#d1d5d6`、`#c2d7f6`、`#1b44f0`、`#142ff0`、`#3763f3`。
5. 旧版 1500 x 1125 功能配图可参考《欢乐逛功能配图-1》，色板：`#c1d5ed`、`#8f9498`、`#fbfbfb`、`#e5e8fe`、`#bee2d6`。
6. part3 需要区分两类：功能配图 = 文案 + 配图；功能说明/2图混合层 = 文案 + 配图 + 框。
7. 功能配图不要额外套大框，重点是一个清晰产品界面/结果图。
8. 功能说明/2图混合层必须有外层白色卡片或蓝色描边框，用来承载多图组合、效果图或前后对比。
9. 明确颜色、字体层级、卡片、截图、图标、背景、装饰元素的使用规则。
10. 为每个 part 给出视觉重点和排版建议。
11. 输出负向约束，防止 AI 生成跑偏。
12. 字体层级必须匹配 `00_design_spec.md` 的 `Font Size Rules`：标题短而大，bullet 可读，标签短小但清楚。
13. 如果文案超过该版型字数上限，先退回文案助手改短，不要靠缩小字号硬塞。

## 输出格式

- 总体视觉原则
- 色彩规则
- 字体层级
- 字号参考和缩放规则
- 组件规则
- 截图处理规则
- part1 / part2 / part3 视觉建议
- part3 版型判断：功能配图 / 功能说明2图混合层
- 禁止出现的风格/元素
