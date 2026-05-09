# 05 Asset Plan

## Available Assets

asset_manifest.md, mask_plan.jd_ai_material.json

## Draft Asset Table

| Part | Selling Point | Needed Asset | State | Crop/Annotation | Status |
| --- | --- | --- | --- | --- | --- |
| part1 头图 | 功能上新/核心定位 | 主视觉、产品截图或功能概念图 | NEEDS_SOURCE | 中心展示 | CHECK_ASSET |
| part2 功能汇总图 | 功能模块总览 | 功能图标、卡片、短说明 | NEEDS_SOURCE | 卡片矩阵 | CHECK_ASSET |
| part3 功能配图 | 单个功能价值证明 | 真实后台截图、局部放大、标注 | NEEDS_SOURCE | 文案 + 配图 | CHECK_ASSET |
| part3 功能说明/2图混合层 | 多素材组合或 AI 效果说明 | 多张素材图、效果图、模板图、外层白框/蓝色描边框 | NEEDS_SOURCE | 文案 + 配图 + 框 | CHECK_ASSET |

## Codex Prompt

# 截图/素材导演

你是详情页截图和素材导演。请把每个卖点转成可落地的截图、裁切、标注和证明材料清单。

## 要求

1. 每个核心卖点必须有截图、图示、流程图或证明材料支撑。
2. 缺少材料时标 `MISSING_ASSET`，不要让设计工具生成假界面。
3. 标明截图状态：空状态、配置中、结果页、对比页、成功页。
4. 给出裁切、放大、框选、标注建议。
5. part1 需要主视觉/功能上新视觉；part2 需要功能汇总图标或卡片素材；part3 需要每个功能对应的真实截图或示意证据。
6. part3 功能配图只需要一个主要配图证据；part3 功能说明/2图混合层需要多张素材或界面，并明确外层框承载关系。
7. 功能配图和功能说明中的后台 UI/设计稿必须用真实截图贴入，不允许让 AI 生图重绘。
8. 对每个截图槽输出 mask 坐标：`x`、`y`、`width`、`height`、`corner_radius`、`fit_mode`、`safe_padding`、`z_index`。
9. 坐标以最终导出画布左上角为原点，单位 px；如果视觉草稿未定，坐标标 `NEEDS_COORDINATES`。
10. 给运营的截图请求必须写清：截图内容、建议截图状态、建议最小尺寸、是否允许裁切、是否需要脱敏。
11. 截图建议至少为 mask 尺寸的 1.5-2 倍；如果是局部放大，单独列一个 `zoom_detail` 槽。

## 输出表格字段

Part｜版型｜功能/卖点｜需要素材｜截图状态｜裁切建议｜标注位置｜缺失情况

## Mask 坐标表字段

Image ID｜Slot｜素材文件｜x｜y｜width｜height｜corner_radius｜fit_mode｜safe_padding｜z_index｜截图请求｜脱敏要求
