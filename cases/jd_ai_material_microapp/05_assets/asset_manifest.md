# Asset Manifest

Source PRD: `/Users/admin/稿定/稿定/Clippings/JD-AI商品素材微应用- V1.0 - 欢乐逛：tiger - 稿定星球 1.md`

This manifest lists required screenshots/design frames. The PRD includes embedded remote images, but the production workflow should use exported clean screenshots in `05_assets/screenshots/`.

## Required Real Screenshots

| Asset ID | Screen / State | Source In PRD | Needed For | Status |
| --- | --- | --- | --- | --- |
| agent_home | 微应用默认首页，agent 一键设计 + 选择商品批量设计 | `image2026-3-25_15-26-37.png` | part3 Agent 生图能力 | NEEDS_EXPORT |
| agent_prompt_components | 默认对话框组件，商品主体图、场景参考图、风格、比例 | `image2026-3-25_16-36-28.png` and ratio dropdown | part3 Agent 生图能力 | NEEDS_EXPORT |
| upload_local | 本地上传 / 图片链接 / 拖拽上传 | `image2026-3-25_17-40-54.png` | Agent 选图说明 | NEEDS_EXPORT |
| upload_image_space | 从图片空间选择图片 | `image2026-3-25_17-40-22.png` | Agent 选图说明 | NEEDS_EXPORT |
| upload_product | 从商品选择图片 | `image2026-3-25_17-41-14.png` | Agent 选图说明 | NEEDS_EXPORT |
| agent_chat_result | 对话生成图片 + 历史对话 + 引用/发布 | `image2026-3-25_18-3-28.png` | part3 Agent 生成结果 | NEEDS_EXPORT |
| publish_dialog | 批量发布至商品，选择商品、位置、SPU/SKU | `image2026-4-10_14-1-27.png` | part3 发布至商品 | NEEDS_EXPORT |
| batch_generate | 选择商品批量设计，筛选商品，选择素材类型 | `image2026-1-26_19-41-37.png` | part3 批量生图能力 | NEEDS_EXPORT |
| task_success_failed_running | 生图详情，成功/失败/跳过/执行中 | `image2026-4-1_18-55-46.png` | part3 效果确认/计划管理 | NEEDS_EXPORT |
| rights_modal | 免费/付费权益不足弹窗 | `image2026-4-16_18-5-40.png` and related modals | 本轮不使用，后续如加权益说明再启用 | NOT_USED_IN_V1 |
| entry_product_edit | 京麦商品编辑/发布入口 | `商品编辑发布.png` | 本轮不单独成图，可作为头图/汇总图辅助信息 | OPTIONAL_REFERENCE |
| entry_product_list | 京麦商品列表入口 | `image2026-4-1_11-17-24.png` | 本轮不单独成图，可作为头图/汇总图辅助信息 | OPTIONAL_REFERENCE |
| entry_material_manage | 京麦素材管理入口 | `image2026-4-1_11-18-45.png` | 本轮不单独成图，可作为头图/汇总图辅助信息 | OPTIONAL_REFERENCE |

## Screenshot Naming

Put exported files in:

`05_assets/screenshots/`

Suggested names:

- `part3-01_agent_home.png`
- `part3-01_agent_result.png`
- `part3-02_batch_generate.png`
- `part3-03_task_detail.png`
- `part3-04_publish_dialog.png`

## Public-Use Warning

Before using screenshots in a public service-market page, confirm:

- No internal URLs.
- No real merchant private data.
- No phone numbers, order IDs, customer info, or sensitive amounts.
- JD/Jingmai UI can be shown in this context.
