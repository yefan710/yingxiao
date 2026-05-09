# 06 Production Prompts

## Master Prompt

```text
为电商服务市场 SaaS 产品「JD-AI商品素材微应用」生成详情页视觉稿。

必须遵守：
- 内置 image2 生成参数必须为：resolution=2k，quality=high。
- 若通过对话式 image2 生成，每张图提示词开头必须写明“生成 2k 分辨率、高质量图”。
- 使用已确认的屏幕规划、文案和视觉规范。
- 详情页结构固定为 part1 头图、part2 功能汇总图、part3 各个功能配图。
- part1/part2 参考《详情页-功能介绍头图》，part3 参考《详情页-功能介绍》，旧版 1500 x 1125 参考《欢乐逛功能配图-1》。
- part3 必须先判断版型：功能配图 = 文案 + 配图；功能说明/2图混合层 = 文案 + 配图 + 框。
- image2 必须生成完整视觉和中文文案排版，包括标题、正文、功能卡片、图标、底部说明、截图容器和整体留白。
- 产品界面和功能截图必须使用真实截图/设计稿贴入；image2 只生成空白截图槽，不允许重绘后台 UI。
- 缺素材时标 MISSING_ASSET，不生成假后台、假数据、假客户案例。
- 每张图只有一个主要沟通任务。
- 标题、副标题和模块文案不能溢出。
- 风格保持浅色服务市场功能说明风，卡片、截图框、图标风格统一。
- 禁止把 image2 只当背景图后再用脚本重排文案；合成阶段只能贴真实截图。
```

## Required Palettes

- 详情页-功能介绍头图：#c3d3e4、#e3e2db、#e1f6eb、#fafbfc、#2652f6
- 详情页-功能介绍：#d1d5d6、#c2d7f6、#1b44f0、#142ff0、#3763f3
- 欢乐逛功能配图-1：#c1d5ed、#8f9498、#fbfbfb、#e5e8fe、#bee2d6

## Screen Prompt Skeleton

```text
生成 {part} 详情页配图。

生成设置：内置 image2，resolution=2k，quality=high。
Part：{part}
版型：{image_type}
画布：{canvas_size}
图的任务：{image_task}
主标题：{main_title}
副标题：{subtitle}
模块文案：{module_copy}
需要素材：{asset_list}
精确文案：{exact_copy}

布局要求：
{layout_rules}

视觉要求：
{visual_rules}

版型规则：
- 如果是功能配图，只使用文案 + 一个主要界面/结果配图，保持简洁。
- 如果是功能说明/2图混合层，必须使用文案 + 多图组合 + 外层白色卡片或蓝色描边框。

image2 生成规则：
- 直接生成完整中文文案排版，不要用灰条或占位文字代替标题、bullet、卡片文案。
- 保持中文可读、无错字、无随机中文、无重叠。
- 功能卡片、图标、标题层级、底部说明全部由 image2 一次完成。
- 截图槽之外不要留多余占位条。

真实截图规则：
- 对所有后台 UI/设计稿区域，只生成空白浅色截图容器、圆角、阴影和坐标，不生成槽内 UI。
- 输出每个 mask 的 x、y、width、height、corner_radius、fit_mode、safe_padding。
- 等运营提供对应尺寸截图后，再贴入真实截图。

负向约束：
- 不要生成假后台数据
- 不要混用图标风格
- 不要让文字溢出
- 不要脱离对应 part 的指定色板
- 不要偏离已批准视觉规范
- 不要在截图槽内画伪 UI
```

## Composite Rule

```text
合成阶段只贴真实截图：
- 读取 image2 文案版底稿。
- 读取 mask 坐标。
- 按坐标裁切、缩放、圆角遮罩、阴影、描边。
- 不再压中文文案。
- 不重画卡片、标题、图标或装饰。
```

当前项目合成命令：

```bash
python3 bin/compose_jd_ai_image2_text_finals.py
```

## Codex Prompt

# 提示词工程师

你是详情页生产提示词工程师。请把已确认的结构、文案、视觉方向和素材需求，组装成可交给视觉生成工具的屏幕级提示词。

## 要求

1. 每张图一个提示词，按 part1 头图、part2 功能汇总图、part3 各个功能配图组织。
2. 每个提示词必须包含 part 类型、画布尺寸、精确文案、布局、素材、风格、负向约束，并要求 image2 直接完成文案排版。
3. 如果缺少素材，不要生成替代假素材，标记为 `MISSING_ASSET`。
4. 同时输出常见返修提示词。
5. 色板必须写入每个提示词：part1/part2 用 `#c3d3e4`、`#e3e2db`、`#e1f6eb`、`#fafbfc`、`#2652f6`；part3 用 `#d1d5d6`、`#c2d7f6`、`#1b44f0`、`#142ff0`、`#3763f3`；旧版 1500 x 1125 功能配图用 `#c1d5ed`、`#8f9498`、`#fbfbfb`、`#e5e8fe`、`#bee2d6`。
6. part3 提示词必须写清版型：功能配图是“文案 + 配图”；功能说明/2图混合层是“文案 + 配图 + 框”。
7. 涉及后台 UI、产品截图、设计稿的区域，只能生成空白截图槽和坐标，禁止让生图工具重绘真实界面。
8. 每个 mask 必须输出 `x/y/width/height/corner_radius/fit_mode/safe_padding`，并写明后续要贴入的真实截图文件名。
9. image2 提示词和最终贴图步骤要分开：image2 生成完整视觉和文案排版，合成阶段只贴入真实截图。

## 输出格式

- Master prompt
- Screen prompts
- Mask coordinate table
- Screenshot request list
- Composite instructions
- Revision prompts
- Missing asset list
