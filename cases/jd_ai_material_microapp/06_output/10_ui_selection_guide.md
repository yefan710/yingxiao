# UI Selection Guide

Source UI image:

`/Users/admin/Desktop/运营推广材料/服务市场详情页/京麦ai微应用/678203F1-F252-40D0-9359-9C0DC734F5AE.png`

Preview crops:

`/Users/admin/Documents/Codex/2026-04-30/files-mentioned-by-the-user-48b5329b70bc31d0b293bdd91f90aad6/detail-page-workflow/cases/jd_ai_material_microapp/06_output/ui_source_preview/crops/`

## Selection Principle

这张 PNG 是总流程图，不是最终可直接贴入的截图源。里面有黑底、灰色画布和蓝色流程线。终稿建议从 Figma/原型中按下面选中的 frame 干净导出，再贴到 mask 区域里。

如果只是快速试排，可以先用我裁出来的 crop 做临时素材；发布稿必须换成干净导出的 UI。

本轮已按产品真实能力移除 `回填商品 / 发布回商品` 部分，详情页只保留 5 张主闭环配图。

## Per-Image Selection

| Detail Image | Slot | Use This UI | Preview Crop | Why | Final Export Requirement |
| --- | --- | --- | --- | --- | --- |
| part1-hero 头图 | `hero_product_ui` | AI 商品素材首页，含 `agent一键设计`、`选择商品批量设计`、灵感卡片 | `01_agent_home_cards.jpg` | 首屏需要让商家一眼知道这是一个完整微应用，不是单个弹窗 | 只导出白色应用主界面，去掉黑底、灰边、流程线 |
| part2-summary 功能汇总 | none | 不放真实 UI，使用图标/卡片总结 6 个能力 | none | 汇总图承担导航作用，不需要截图抢信息 | 无需截图 |
| part3-01 对话生图 | `agent_home` | AI 商品素材首页/agent 输入区，最好包含大输入框和灵感卡片 | `01_agent_home_cards.jpg` | 证明“选图 + 提要求”的入口和对话式生图 | 干净导出完整 agent 首页局部，保证输入框和卡片可读 |
| part3-01 对话生图 | `agent_result` | 对话生成结果区，优先用 4 图结果 + 重新生成/引用/继续修改 | `03_agent_result_multi.jpg` | 比单图结果更能表达“套图生成”和“结果可回用” | 导出生成结果局部，保留安全可用的操作按钮，不要出现发布回商品 |
| part3-02 批量生图 | `batch_generate` | 选择商品批量设计页，含商品筛选、素材类型勾选、提交生图计划 | `08_batch_select_products.jpg` | 这张最能证明批量生成多类素材，不需要别的图补充 | 导出完整批量设计页面，底部按钮要出现 |
| part3-03 结果确认 | `task_detail` | 批量生图记录详情页，含成功/失败/跳过/执行中 tab、商品 AI 图、失败重试 | `10_task_detail_results.jpg` | 比任务列表更适合解释“结果分状态管理，失败可处理” | 导出详情页上半部分，保留统计和状态管理，不要出现确认发布/回填商品按钮 |

## Secondary / Not Used In Current 5 Images

| UI | Preview Crop | Current Decision |
| --- | --- | --- |
| 空白 agent 对话页 | `02_agent_blank_chat.jpg` | 不用。信息太空，证明力弱。 |
| 单图生成结果 | `05_agent_result_single.jpg` | 可作为备选，但当前优先用 4 图结果。 |
| 单图发布弹窗 | `06_publish_dialog_single.jpg` | 不用。当前产品不支持回填/发布回商品。 |
| 生成后引用/图片 #1 | `07_agent_edit_result.jpg` | 不单独使用，除非要突出“引用继续改图”。 |
| 批量生图记录列表 | `09_batch_task_list.jpg` | 不单独使用。可放进后续“计划管理”图，但当前只保留 5 张主图。 |
| 发布到商品弹窗 | `04_publish_dialog_multi.jpg` | 不用。当前产品不支持回填/发布回商品。 |

## File Naming For Final Exports

Put final clean exports here:

`cases/jd_ai_material_microapp/05_assets/screenshots/`

Use these names:

- `part1_hero_product_ui.png`
- `part3-01_agent_home.png`
- `part3-01_agent_result.png`
- `part3-02_batch_generate.png`
- `part3-03_task_detail.png`

## Crop Preview Files Generated

- `01_agent_home_cards.jpg`
- `03_agent_result_multi.jpg`
- `08_batch_select_products.jpg`
- `10_task_detail_results.jpg`

These previews are for selection only. They are not clean final screenshot assets.
