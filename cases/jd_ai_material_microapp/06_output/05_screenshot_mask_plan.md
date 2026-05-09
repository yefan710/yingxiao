# 05 Screenshot Mask Plan

Source mask JSON:

`/Users/admin/Documents/Codex/2026-04-30/files-mentioned-by-the-user-48b5329b70bc31d0b293bdd91f90aad6/detail-page-workflow/cases/jd_ai_material_microapp/05_assets/mask_plan.jd_ai_material.json`

## Purpose

功能配图和功能说明里的京麦/京东微应用 UI 不走纯 AI 重绘。image2 负责生成整张图的视觉和中文文案排版，但真实产品截图槽必须留空；运营按 mask 坐标提供截图，再把真实截图贴入。

## Mask Coordinate Table

坐标以最终导出画布左上角为原点，单位 px。

| Image ID | Canvas | Type | Slot | Asset | x | y | width | height | fit_mode | corner_radius | safe_padding | Screenshot Request |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| part1-hero | 816 x 1054 | 头图 | hero_product_ui | screenshots/part1_hero_product_ui.png | 70 | 466 | 676 | 408 | cover_crop | 22 | 16 | 微应用默认首页或 agent 首页截图，建议导出宽度 >= 1352px，高度 >= 816px；避免上下留白 |
| part3-01-agent | 816 x 982 | 功能说明/2图混合层 | agent_home | screenshots/part3-01_agent_home.png | 72 | 430 | 672 | 270 | cover_crop | 18 | 12 | agent 首页/对话框组件，包含商品主体图、场景参考图、风格、比例，建议截图 >= 1344 x 624 |
| part3-01-agent | 816 x 982 | 功能说明/2图混合层 | agent_result | screenshots/part3-01_agent_result.png | 142 | 724 | 532 | 154 | cover_crop | 16 | 10 | 对话生成结果区，能看到生成图片、引用或继续修改等安全可用操作，建议截图 >= 1064 x 380 |
| part3-02-batch | 816 x 982 | 功能配图 | batch_generate | screenshots/part3-02_batch_generate.png | 70 | 430 | 676 | 360 | cover_crop | 18 | 12 | 选择商品批量设计页，包含商品筛选和素材类型：白底图、透图、场景图、卖点图、搜索推荐图，建议截图 >= 1352 x 772 |
| part3-03-confirm | 816 x 982 | 功能配图 | task_detail | screenshots/part3-03_task_detail.png | 64 | 430 | 688 | 287 | cover_crop | 18 | 12 | 生图详情页，展示成功/失败/跳过/执行中 tab、商品维度 AI 图和失败处理，建议截图 >= 1376 x 574；不要截入确认发布或回填商品按钮 |

## Handoff SOP

1. image2 阶段生成完整视觉和中文文案排版，包含标题、bullet、功能卡片、图标、底部说明和截图容器。
2. 所有后台 UI/产品 UI 槽位必须保持空白或浅色占位，不生成伪 UI。
3. 运营按上表导出真实截图，放入 `05_assets/screenshots/`。
4. 截图建议为 mask 尺寸的 1.5-2 倍，避免贴入后模糊。
5. 合成阶段只做裁切、缩放、圆角遮罩、阴影、描边和必要脱敏，不重排文案。
6. 如果没有真实截图，最终稿停在 image2 base，不进入发布稿。

## Draft Prompt Add-on

```text
本图包含真实截图区域。请用 image2 生成完整视觉和中文文案排版，但不要生成、重绘或虚构京麦/京东后台 UI。
截图槽只生成空白浅色容器、圆角、阴影和描边；槽内不要画具体表格、按钮、数据、商品、店铺信息或随机中文。
每个 mask 占位必须输出坐标：x、y、width、height、corner_radius、fit_mode、safe_padding。
```
