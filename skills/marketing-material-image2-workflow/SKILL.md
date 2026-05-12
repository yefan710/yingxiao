---
name: marketing-material-image2-workflow
description: Use when producing Gaoding/Jingmai marketing visuals such as service-market detail pages, service-market main images, function promotion banners, and popups. The workflow emphasizes design-spec compliance, wireframe confirmation before image2, screenshot masking, and final QA.
metadata:
  version: 1.0.0
---

# Marketing Material Image2 Workflow

这个 skill 用于生成稿定/欢乐逛/京麦服务市场相关营销物料，包括服务市场详情页、京麦主图、banner、弹窗。

## 核心原则

先确认草图，再做完整视觉。草图不是最终画面，而是文案、构图、图片区域、mask 区域的确认稿。只有当用户确认草图后，才进入 image2 视觉设计和截图覆盖。

视觉必须遵守对应物料规范。banner 看 banner 规范，弹窗看弹窗规范，详情页看详情页规范。规范优先于临时审美判断。

真实截图优先。只要有产品截图、原图、效果图，就优先作为核心视觉素材；必要时将截图 mask 到 image2 生成底图上，而不是凭空重绘 UI。

弹窗篇幅有限，不要机械承载所有素材。如果用户给了 5 张原图和 5 张效果图，详情页可以完整展示，弹窗则要重新判断展示数量、叠放结构和信息优先级。

## 输入检查

开始前确认：

- 目标物料类型：服务市场主图、详情页、banner、弹窗。
- 平台尺寸和限制：例如京麦主图为 `1580 x 890`，单张建议 `3M` 内。
- 必须出现的业务信息：功能名、利益点、免费额度、CTA、素材类型。
- 素材来源：商品原图、效果图、产品截图、参考案例、品牌图标。
- 是否需要 image2：完整视觉通常需要；纯尺寸调整或截图合成可用本地脚本。

## 草图阶段

草图必须说明：

- 主标题和副标题。
- 核心利益点。
- 构图方向。
- 图片槽数量和比例。
- 原图、效果图、截图分别放在哪里。
- 哪些区域需要后续 mask。

草图确认前不要直接进入最终视觉。

## 构图经验

### AI 商品图优化

要表达“选择一个商品的多个位置，生成多张主图/效果图”，不要只放 1 个原图槽和 1 个效果槽，否则用户容易误以为只能生成一张。

更合理的表达：

- 左侧放一个完整原商品概念。
- 标注可提取主图、详情页、标题、属性里的卖点。
- 右侧展示多张 1:1 主图结果，可用 2+3 或叠放结构。
- 明确体现“新用户可免费使用 5 张图”等关键权益。

### 弹窗

弹窗需要高完成度视觉，不能像低保真工程草图。可以参考 `references/弹窗规范/tbgr落地版 (1).png` 的完整感，但替换成当前功能的利益点，不照抄“一句话生成案例”等无关文案。

### banner

banner 要信息快速、视觉集中。不要加入突兀的分类标签框；CTA 可以只保留“立即体验”，由业务跳转到对应页面。

## image2 与 mask

推荐流程：

1. 先生成无截图或低信息量的完整视觉底图。
2. 为真实截图留出明确 mask 区域。
3. 用本地合成脚本把真实截图覆盖进去。
4. 输出后检查截图是否遮挡文案。

如果截图遮挡文案，优先调整截图区域，而不是缩小文案到不可读。

## QA 清单

交付前逐项检查：

- 尺寸正确。
- 文件大小符合平台限制。
- 主标题、副标题、利益点不被遮挡。
- 字体大小和粗细符合规范。
- 图片比例符合业务认知，比如主图结果应为 1:1。
- 文案不溢出卡片或按钮。
- 视觉不是单一色块堆叠，整体有完成度。
- 使用真实截图时，截图和背景融合自然。

## 字体规范

生成 banner / 弹窗时参考 `docs/BANNER_POPUP_TYPOGRAPHY.md`。

硬性优先级：

- 字体：优先 `"PingFang SC"`，不可用时用 `"Hiragino Sans GB"` 或 `STHeiti`。
- 主蓝：`#2254F4`。
- 主标题：`#222529`，字重 `600`。
- 正文：`#4C535C` 或 `#7F8792`，字重 `400`。
- Banner 主标题按 `32-34px` 显示尺寸；副标题按 `16-18px`。
- 弹窗主标题按 `34-40px` 显示尺寸；副标题按 `24-28px`；功能点正文按 `13-16px`。
- 2x 图按显示字号乘 2 生成。

## 参考路径

- `references/banner规范/`
- `references/弹窗规范/`
- `references/详情页规范/`
- `docs/BANNER_POPUP_TYPOGRAPHY.md`
- `cases/jd_ai_material_microapp/`
- `cases/ai-product-image-optimization-module2-banner-popup/`
- `config/promo-materials/material_specs/`
