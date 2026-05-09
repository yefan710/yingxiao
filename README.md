# 营销推广物料工作流

这个仓库沉淀了「京麦微应用 / 稿定生图」服务市场详情页、京麦服务市场主图、功能推广 banner、弹窗等物料的生产依赖。内容包括设计规范、参考案例、可复用脚本、成图案例、草图与 image2 生产流程说明。

## 目录结构

| 目录 | 用途 |
| --- | --- |
| `skills/` | 可复制到 Codex Skills 的工作流说明。 |
| `references/` | 设计规范原始文件、参考案例图、京麦微应用截图、图标素材。 |
| `config/` | banner、弹窗、详情页等规格配置。 |
| `scripts/` | 详情页与京麦服务市场主图的本地合成脚本。 |
| `cases/` | 已执行过的完整案例，包括需求、草图、文案、mask 计划、成图。 |
| `outputs/` | 可直接查看的最终推广物料输出。 |
| `docs/` | 工作流项目文档和线程启动提示词。 |
| `templates/` | 详情页工作流模板。 |

## 当前包含的核心案例

1. `cases/jd_ai_material_microapp/`
   - 京麦微应用「稿定生图 / AI 商品素材」详情页完整案例。
   - 包含 UI 截图、image2 base、mask 计划、竖版详情页成图、京麦服务市场 1580x890 主图。

2. `cases/ai-product-image-optimization-module2-banner-popup/`
   - 「AI 商品图优化」功能推广 banner 和弹窗案例。
   - 包含 brief、文案包、规格解析、草图、最终 2K 图和标准尺寸图。

3. `references/banner规范/`
   - 稿定/欢乐逛功能推广 banner 规范及示例素材。

4. `references/弹窗规范/`
   - 稿定/欢乐逛弹窗规范、`tbgr落地版` 参考视觉。

5. `references/详情页规范/`
   - 服务市场详情页功能配图规范原始网页存档与示例素材。

## 推荐工作流

### 1. 先整理需求

先把物料拆成以下字段：

- 产品/功能名称
- 使用场景
- 目标物料：服务市场主图、详情页、banner、弹窗
- 平台规范：尺寸、文件大小、文字限制、张数限制
- 可用素材：产品截图、原始商品图、效果图、参考案例
- 核心利益点：商家为什么要点进去、为什么要试用

### 2. 先出草图，不直接做最终视觉

草图需要确认三件事：

- 文案：主标题、副标题、利益点、CTA
- 构图：左右结构、上下结构、图片槽数量、是否叠放
- 图片区域：哪些位置放原图、哪些位置放效果图、哪些位置需要 mask 截图

确认草图后再进入 image2 或本地合成阶段，避免反复重做完整视觉。

### 3. image2 生产原则

- banner / 弹窗 / 详情页头图都应该是完整视觉，不是低保真工程草图。
- 如果有真实产品截图，优先用真实截图 mask 到画面里。
- 如果用户给的是多张详情图/主图，不要机械全部塞进弹窗；弹窗篇幅有限时，要重新判断素材数量和展示结构。
- 对「优化多套主图」类功能，要表达“一个商品的多个位置，生成多张效果图”，避免让用户误解成只能生成一张。

### 4. 导出前 QA

每张图至少检查：

- 尺寸是否符合规范。
- 文案是否被截图、按钮、卡片遮挡。
- 标题和副标题是否足够醒目。
- 图片槽比例是否符合真实业务，比如主图通常应是 1:1。
- 平台限制是否满足，比如京麦主图 `1580x890`、单张建议 `3M` 内、主图总数不超过 `15` 张。

## 常用脚本

### 京麦服务市场主图

```bash
python3 scripts/detail-page-workflow/render_jd_service_market_main_images.py
```

默认读取：

- `cases/jd_ai_material_microapp/05_assets/screenshots/`

默认输出：

- `cases/jd_ai_material_microapp/06_output/final_comps/service_market_main_*.jpg`

规格：

- `1580 x 890`
- JPG
- 单张控制在 `3M` 内

### 详情页合成

```bash
python3 scripts/detail-page-workflow/compose_jd_ai_image2_finals.py
python3 scripts/detail-page-workflow/compose_jd_ai_image2_text_finals.py
```

用于把 image2 生成底图、文字底图和真实截图按 mask 计划合成到最终详情页模块。

## 服务简介参考

推荐版：

> 稿定生图是一款面向京麦商家的AI商品素材生成工具，支持对话生图与批量出图，可生成主图、白底图、透图、场景图、卖点图等素材，帮助商家快速完善店铺素材内容，提升商品展示效率。

精简版：

> 稿定生图支持AI对话生图与批量出图，可生成主图、白底图、透图、场景图、卖点图等商品素材，帮助商家快速完善店铺素材。

## 给新使用者的最短路径

1. 先读 `skills/marketing-material-image2-workflow/SKILL.md`。
2. 再看 `cases/jd_ai_material_microapp/06_output/11_image2_production_workflow.md`。
3. 参考 `references/banner规范/`、`references/弹窗规范/`、`references/详情页规范/`。
4. 复制一个 `cases/` 里的案例目录，替换 brief、截图和 mask 计划。
5. 出草图给业务确认。
6. 确认后生成最终视觉，并按平台规范 QA。

