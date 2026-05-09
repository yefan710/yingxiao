# 08 Revision Routing

| Problem Found | Send Back To | Fix Type |
| --- | --- | --- |
| 产品定位不清 | Requirement Structurer | Rebuild brief |
| 屏幕太多/太少 | Main-Flow Designer | Replan canvas |
| 文案超字数 | Copy Assistant | Rewrite within budget |
| 文案标点异常 / `、`、`，` 居中怪 | Copy Assistant + Quality Inspector | 改为空格、`｜`、` / ` 等安全分隔 |
| 风格跑偏 | Visual Director | Tighten style constraints |
| 色值突兀 / 高饱和蓝橙绿 | Visual Director | 回到指定色板，重新生成 image2 |
| 右上角装饰突兀或抢主体 | Visual Director | 降低装饰层级，重做 image2 构图 |
| image2 只生成背景，脚本补文案 | Production Prompt Assembler + Visual Director | 重新写提示词，让 image2 生成完整视觉和文案排版 |
| 脚本硬画卡片/标题导致工程稿感 | Production Prompt Assembler | 废弃脚本视觉层，只保留截图合成 |
| 功能配图文字被截图遮挡 | Quality Inspector + Screenshot / Asset Director | 调整 mask 或重生 image2 留白 |
| 截图不够证明卖点 | Screenshot / Asset Director | Add or recrop asset |
| 截图框上下留白过多 | Screenshot / Asset Director | 调整 mask 和截图裁切比例 |
| 头图 / 功能汇总图 / 功能配图 part 识别错 | Main-Flow Designer + Quality Inspector | 重新确认 part 身份和对应规范 |
| 出现回填商品/发布回商品等不支持能力 | Requirement Structurer + Copy Assistant | 删除该 part 和相关文案 |
| 提示词无法执行 | Production Prompt Assembler | Rewrite prompt |
| 多项发布风险 | Quality Inspector + Main-Flow Designer | Reopen page plan |
