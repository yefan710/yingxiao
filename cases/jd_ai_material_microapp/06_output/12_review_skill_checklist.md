# 12 Review Skill Checklist

## Purpose

这份清单用于发布前审查，也用于复盘生成过程。它专门覆盖本轮实际暴露的问题，优先级高于通用审美判断。

## Review Order

必须按顺序审查：

1. Part 身份
2. image2 生产纪律
3. 视觉规范和色板
4. 文案和标点
5. 截图 mask 合成
6. 不支持能力
7. 最终输出路径

## 1. Part 身份

| Check | Blocking If |
| --- | --- |
| `part1-hero` 是头图/首屏功能上新图 | 把它当成唯一头图或功能汇总图 |
| `part2-summary` 是功能汇总头图 | 把它当成普通功能配图，或没有按功能汇总头图规范处理 |
| `part3-*` 才是功能配图/功能说明 | 用 part2 的规范套 part3，或反过来 |

## 2. Image2 Production Discipline

| Check | Blocking If |
| --- | --- |
| image2 生成完整视觉和中文文案排版 | image2 只生成背景，后续脚本压文案 |
| 功能卡片、标题、图标、底部说明由 image2 一次生成 | 脚本硬画卡片或标题 |
| 合成阶段只贴真实截图 | 合成阶段重排 bullet、标题或大段中文 |
| 截图槽保持空白/浅色占位 | image2 在槽内生成伪后台 UI、假数据或随机中文 |

## 3. Visual Norms

| Check | Blocking If |
| --- | --- |
| part1/part2 贴近功能汇总头图规范 | 大面积高饱和蓝、强橙、强绿突兀 |
| part3 贴近功能说明规范 | 功能配图像另一套品牌 |
| 装饰图形不抢主体 | 右上角大图形、白圈、折角抢过标题或截图 |
| 整体不像工程稿 | 视觉明显由脚本硬画，卡片/阴影/字体不自然 |

## 4. Copy And Punctuation

| Check | Blocking If |
| --- | --- |
| 标题、subtitle、bullet 由 image2 自然排版 | 文案重叠、遮挡或字号层级混乱 |
| 中文标点视觉自然 | `、`、`，` 居中异常或造成奇怪停顿 |
| 优先使用安全分隔 | 需要列表时使用 `｜`、` / `、空格 |
| 不出现随机中文 | image2 生成乱码、错别字、未确认词 |

## 5. Screenshot Mask

| Check | Blocking If |
| --- | --- |
| 真实截图按 mask 贴入 | UI 看起来是 AI 重绘 |
| 截图不遮挡文案 | 压住标题、bullet、底部说明 |
| 截图不糊、不拉伸 | 宽高比例明显变形 |
| 截图留白合理 | 上下留白过大，主体不够满 |
| 圆角、阴影、描边自然 | 贴图像硬贴，和 image2 容器割裂 |

## 6. Unsupported Capabilities

| Check | Blocking If |
| --- | --- |
| 不写回填商品 | 出现回填商品、发布回商品、发布到店铺 |
| 不写未经证明数据 | 出现 90%、100倍、30秒等未确认公开承诺 |
| 不新增 PRD 外能力 | 为了好看补了产品不支持的功能 |

## 7. Output Verification

审查完成后必须确认：

- `06_output/final_comps/part1-hero_final.png`
- `06_output/final_comps/part2-summary_final.png`
- `06_output/final_comps/part3-01-agent_final.png`
- `06_output/final_comps/part3-02-batch_final.png`
- `06_output/final_comps/part3-03-confirm_final.png`
- `06_output/final_comps/contact_sheet.png`

并打开 `contact_sheet.png` 做整体一致性检查。

## Review Verdict

只允许三种结论：

- `PASS`：无 blocking，无明显 important。
- `PASS WITH POLISH`：无 blocking，仅有可接受 polish。
- `FIX REQUIRED`：任一 blocking，或同类 important 重复出现。
