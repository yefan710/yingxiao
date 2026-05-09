# 11 Image2 Production Workflow

## Final Rule

本项目最终确认的有效生产方式是：

`PRD/截图/设计规范 -> image2 生成完整视觉和文案排版 -> 本地按 mask 贴入真实截图 -> QA -> final_comps`

image2 负责整张图的视觉完成度，包括背景、标题、正文、功能卡片、图标、层级、留白、阴影和中文文案排版。本地脚本只负责把真实截图贴入 image2 预留的截图槽。

## Image2 Generation Settings

使用内置 image2 生成详情图时必须强制设置：

| Setting | Value |
| --- | --- |
| resolution | `2k` |
| quality | `high` |

如果调用入口支持显式参数，必须传 `resolution=2k` 和 `quality=high`；如果入口是对话式 image2，则必须在生成指令开头写明“生成 2k 分辨率、高质量图”。

## Why

上一轮验证证明：如果 image2 只生成背景，再由脚本补文案和卡片，画面会变成工程稿，和设计规范差距很大。服务市场详情页成图必须让 image2 一次性处理视觉和排版，只把产品 UI 截图区留给后期合成。

## Asset Folders

| Purpose | Path |
| --- | --- |
| image2 文案版底稿 | `05_assets/image2_text_bases/` |
| 真实产品截图 | `05_assets/screenshots/` |
| mask 坐标 | `05_assets/mask_plan.jd_ai_material.json` |
| 最终完成稿 | `06_output/final_comps/` |
| 草图/同版备份 | `06_output/sketches/` |

## Required Output

当前确认 5 张图：

1. `part1-hero_final.png`
2. `part2-summary_final.png`
3. `part3-01-agent_final.png`
4. `part3-02-batch_final.png`
5. `part3-03-confirm_final.png`

总览图：`contact_sheet.png`

## Image2 Prompt Rules

每张图单独生成。提示词必须包含：

- 画布比例和 part 类型。
- 精确中文文案，要求 image2 直接排版。
- 设计规范参考风格和色板。
- 截图槽坐标和尺寸。
- 明确说明截图槽必须为空白、浅色、无文字、无遮挡。
- 负向约束：不生成假后台 UI、不生成随机中文、不写未确认能力、不出现回填商品/发布回商品。

## Screenshot Slot Rule

截图槽只给真实截图使用。image2 可以生成截图容器、圆角、阴影和外框，但槽内必须保持空白或极浅占位，不能生成表格、按钮、商品、店铺名、假数据或伪后台。

合成阶段只允许做：

- 裁切
- 缩放
- 圆角 mask
- 阴影
- 白色描边
- 必要脱敏

合成阶段不允许做：

- 重排文案
- 重画功能卡片
- 改标题层级
- 在 image2 成图上重新压大段中文
- 用脚本硬画视觉装饰替代 image2

## Current Composite Command

```bash
python3 bin/compose_jd_ai_image2_text_finals.py
```

该脚本读取：

- `05_assets/image2_text_bases/*_image2_text_base.png`
- `05_assets/screenshots/*.png`
- `05_assets/mask_plan.jd_ai_material.json`

并输出：

- `06_output/final_comps/*_final.png`
- `06_output/final_comps/contact_sheet.png`
- `06_output/sketches/*_sketch.png`
- `06_output/sketches/contact_sheet.png`

## QA Gate

发布前必须检查：

| Check | Pass Standard |
| --- | --- |
| image2 排版 | 标题、正文、卡片、底部说明由 image2 统一排版，整体像规范成图 |
| 截图真实性 | 京麦/京东后台 UI 都是真实截图贴入 |
| 截图槽 | 截图不拉伸、不糊、不遮挡标题或 bullet |
| 文案 | 无随机中文、错字、重叠、标点异常 |
| 视觉 | 色板接近规范，不出现突兀强色块 |
| 能力口径 | 不出现回填商品、发布回商品、发布到店铺 |
| 隐私 | 截图中敏感信息已脱敏或可安全发布 |

任一项不通过，先回到 image2 重新生成该图，不能用脚本硬补视觉。
