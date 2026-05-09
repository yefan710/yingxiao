# Executed Workflow: JD-AI商品素材微应用

Generated: 2026-05-06
Source PRD: `/Users/admin/稿定/稿定/Clippings/JD-AI商品素材微应用- V1.0 - 欢乐逛：tiger - 稿定星球 1.md`

## 00 Current Scope

用户已确认：`回填商品 / 发布回商品坑位` 当前不支持，本轮详情页不做这一 part。

最终保留 5 张图：

1. part1 头图
2. part2 功能汇总图
3. part3-01 对话生图
4. part3-02 批量生图
5. part3-03 生成结果确认

详情页主线调整为：

`商品图来源 -> AI 对话生成/批量生成 -> 结果确认 -> 失败重试/计划管理`

## 01 Requirement Brief

### Product One-Liner

京东微应用内的 AI 商品素材生成工具，支持对话生成、批量生成、结果确认和失败重试。

### Target User

- 京东/京麦商家运营。
- 多 SKU 店铺运营。
- 没有设计师或设计资源不足的商家。

### Jobs To Be Done

1. 快速生成商品主图、白底图、透图、场景图、搜索推荐图、卖点图。
2. 从商品、图片空间、本地文件中选择素材，不用反复下载上传。
3. 对生成结果进行查看、确认、重试或移除。
4. 批量处理多个商品，并按成功/失败/执行中管理计划。

### Public Copy Risk

| Claim | Use In Detail Page | Risk |
| --- | --- | --- |
| 成本降低90%以上 | 暂不直接写 | NEEDS_SOURCE_FOR_PUBLIC_CLAIM |
| 效率提升100倍以上 | 暂不直接写 | NEEDS_SOURCE_FOR_PUBLIC_CLAIM |
| 30秒生成素材 | 可作为待确认卖点 | NEEDS_SOURCE_FOR_PUBLIC_CLAIM |
| 支持白底图、透图、场景图、搜索推荐图、卖点图 | 可以写 | PRD_SOURCE |
| 支持发布至商品 | 本轮不写 | USER_CONFIRMED_UNSUPPORTED |

## 02 Screen Plan

推荐 5 张图。第一版聚焦“生成 -> 批量 -> 结果确认/失败重试”的主闭环，不单独做入口、权益和回填商品说明图。

| Image ID | Part | Name | Type | Canvas | Task | Asset Need |
| --- | --- | --- | --- | --- | --- | --- |
| part1-hero | part1 | 头图 | 功能上新图 | 816 x 1054 | 让商家一眼知道这是京东 AI 商品素材工具 | 微应用首页或 agent 首页截图 |
| part2-summary | part2 | 功能汇总图 | 功能矩阵 | 816 x 1054 | 总览 6 个核心能力 | 图标/功能卡片即可 |
| part3-01-agent | part3 | 对话生成商品素材 | 功能说明/2图混合层 | 816 x 982 | 说明 agent 对话、选图、修改、生成结果 | agent 首页 + 生成结果 |
| part3-02-batch | part3 | 批量生成多类素材 | 功能配图 | 816 x 982 | 说明可批量生成多类商品图 | 批量生成页 |
| part3-03-confirm | part3 | 生成结果确认 | 功能配图 | 816 x 982 | 说明成功/失败/执行中、查看大图、失败重试 | 生图详情页 |

## 03 Copy Draft

### part1-hero

| Field | Copy | Check |
| --- | --- | --- |
| 品牌标签 | 欢乐逛出品 | 5 字 |
| 主标题 | AI商品素材 | 6 字 |
| 副标题 | 对话生成  批量生成商品素材 | 12 字 |
| 辅助标题 | 京东商家素材生成新方式 | 11 字 |
| 核心标签 | 主图 / 白底图 / 透图 / 场景图 / 卖点图 | 每个 2-3 字 |
| 风险 | 不写 90%、100倍、30秒 | safer |

### part2-summary

| Card | Title | Tags |
| --- | --- |
| 1 | 多来源选图 | 本地上传 / 图片空间 / 商品图 |
| 2 | 对话改图 | 换背景 / 换模特 / 改颜色 |
| 3 | 套图生成 | 主图 / 搜索图 / 规格图 |
| 4 | 批量生图 | 多商品 / 批量提交 / 计划生成 |
| 5 | 多类覆盖 | 白底图 / 透图 / 场景图 / 卖点图 |
| 6 | 结果可控 | 成功失败 / 查看原因 / 重新生成 |

### part3-01-agent

| Field | Copy |
| --- | --- |
| 主标题 | 对话生图 |
| 副标题 | 选图提要求  快速生成商品素材 |
| bullet 1 | 多来源选图｜本地 / 图片空间 / 商品图都能用 |
| bullet 2 | 对话式修改｜换背景 / 换模特 / 换颜色 |
| bullet 3 | 结果可回用｜引用结果 / 继续修改 |
| 标注 | 主体图 / 场景参考 / 比例选择 / 重新生成 |

### part3-02-batch

| Field | Copy |
| --- | --- |
| 主标题 | 批量生图 |
| 副标题 | 一次选择商品  多类素材批量生成 |
| bullet 1 | 多类型覆盖｜白底图 / 透图 / 场景图 |
| bullet 2 | 商品范围可选｜筛选商品后批量提交计划 |
| bullet 3 | 原图处理可控｜支持跳过或覆盖原商品图片 |
| 标注 | 选择商品 / 素材类型 / 提交计划 |

### part3-03-confirm

| Field | Copy |
| --- | --- |
| 主标题 | 结果确认 |
| 副标题 | 结果按状态管理  失败可重试 |
| bullet 1 | 结果分状态｜成功 / 失败 / 跳过 / 执行中 |
| bullet 2 | 失败可处理｜查看原因 / 单个重试 / 全部重试 |
| bullet 3 | 结果可查看｜按商品维度查看生成图片 |
| 标注 | 成功 / 失败 / 执行中 / 重新生成 |

## 04 Visual Direction

### Overall

浅色蓝白服务市场风。不要做成大促海报。不要用夸张 3D 机器人。重点是“可信的后台能力 + 真实截图证明”。

### Type Mapping

- Agent 生图：功能说明/2图混合层，因为需要多个截图层解释流程。
- 批量生图、结果确认：功能配图，因为用单个后台截图就能证明能力。

### Screenshot Policy

所有后台 UI、计划详情都必须真实截图贴入。最终确认的正确做法是：image2 生成完整视觉和中文文案排版，只把截图槽留空；本地合成阶段只贴入真实截图，不再重排文案或硬画卡片。

### Final Production Rule

`PRD/截图/设计规范 -> image2 生成完整视觉和文案排版 -> 本地按 mask 贴入真实截图 -> QA -> final_comps`

已验证不可采用的做法：

- 只用 image2 生成背景，再用脚本压标题、bullet、卡片。
- 用脚本硬画 part2 功能汇总卡片。
- 在合成阶段重新排文案。

以上做法会让成图变成工程稿，和服务市场设计规范差距明显。

## 05 Screenshot And Mask Plan

Mask JSON:

`/Users/admin/Documents/Codex/2026-04-30/files-mentioned-by-the-user-48b5329b70bc31d0b293bdd91f90aad6/detail-page-workflow/cases/jd_ai_material_microapp/05_assets/mask_plan.jd_ai_material.json`

| Image ID | Slot | x | y | w | h | Screenshot Needed |
| --- | --- | --- | --- | --- | --- | --- |
| part1-hero | hero_product_ui | 70 | 466 | 676 | 408 | 微应用首页或 agent 首页 |
| part3-01-agent | agent_home | 72 | 430 | 672 | 270 | agent 首页/对话框组件 |
| part3-01-agent | agent_result | 142 | 724 | 532 | 154 | 对话生成结果区 |
| part3-02-batch | batch_generate | 70 | 430 | 676 | 360 | 选择商品批量设计页 |
| part3-03-confirm | task_detail | 64 | 430 | 688 | 287 | 生图详情页 |

## 06 Production Prompt Skeleton

```text
生成服务市场详情页配图，产品：JD-AI商品素材微应用。

画布：{canvas}
图片 ID：{image_id}
版型：{function_image or function_explain_2_image_mix}
主标题：{main_title}
副标题：{subtitle}
bullet 文案：{bullets}
真实截图槽：{slot list with x/y/width/height}

视觉要求：
- 浅色蓝白服务市场风。
- 使用指定色板：part1/part2 用 #c3d3e4 #e3e2db #e1f6eb #fafbfc #2652f6，part3 用 #d1d5d6 #c2d7f6 #1b44f0 #142ff0 #3763f3。
- image2 直接生成完整中文文案排版：标题、subtitle、bullet、卡片、图标、底部说明都在画面里完成。
- 标题大、短、蓝色特粗；bullet 使用蓝点，关键词黑体。
- 后台 UI 区域只生成空白浅色截图槽，不画表格、按钮、数据、店铺信息。
- 每个 mask 输出坐标 x/y/width/height/corner_radius/fit_mode/safe_padding。

禁止：
- 不要重绘京麦后台 UI。
- 不要把 image2 当背景后再用脚本重排文案。
- 不要生成假数据、假店铺、假订单。
- 不要写未确认的 90%、100倍、30秒公开承诺。
- 不要写发布回商品、回填商品、发布到店铺。
```

当前最终合成脚本：

```bash
python3 bin/compose_jd_ai_image2_text_finals.py
```

该脚本读取 `05_assets/image2_text_bases/` 的 image2 文案版底稿，只按 `mask_plan.jd_ai_material.json` 贴入 `05_assets/screenshots/` 中的真实截图。

## 07 QA Checklist

| Check | PASS Standard |
| --- | --- |
| 结构 | 必须包含 part1 头图、part2 功能汇总、part3 功能展开 |
| image2 排版 | 文案、卡片、标题层级由 image2 一次生成，不能靠脚本补大段文字 |
| 文案 | 每张图一个主要任务，标题不超过对应字数上限，无随机中文和错字 |
| 真实性 | 所有后台 UI 都是真实截图贴入，不是 AI 重绘 |
| 截图质量 | 截图不糊、不拉伸、不遮挡核心操作 |
| 脱敏 | 无真实店铺隐私、手机号、订单号、客户信息 |
| 风险口径 | 90%、100倍、30秒未确认前不进入终稿 |
| 不支持能力 | 不出现发布回商品、回填商品、发布到店铺相关承诺 |
| 版型 | Agent 用 2图混合层；批量/确认用功能配图 |

## 08 Next Operator Actions

1. 已从 `/Users/admin/Desktop/运营推广材料/服务市场详情页/京麦ai微应用` 复制 5 个 UI 稿到 `05_assets/screenshots/`。
2. 已根据宽图比例调整 `batch_generate` 和 `task_detail` 的 mask 尺寸。
3. 已用 image2 生成包含中文文案排版的 5 张底稿，保存到 `05_assets/image2_text_bases/`。
4. 已用 `compose_jd_ai_image2_text_finals.py` 只贴入真实截图，生成 5 张草图和 5 张完成稿。
5. 跑 QA，任何 AI 重绘 UI、截图拉伸、随机中文、或出现不支持能力文案都退回。
