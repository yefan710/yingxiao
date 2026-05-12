# Banner / 弹窗字体规范摘录

来源：

- `references/banner规范/稿定-功能推广banner规范.html`
- `references/弹窗规范/稿定-弹窗规范.html`
- 对应 `_files/index.min.css` 全局 design token

注意：HTML 里只明确给出了 PSD 尺寸和全局设计 token，没有单独标注“该图主标题必须几号字”。下面是从全局 token + 当前规范样张视觉层级整理出的可执行映射。

## 全局字体

CSS token：

```css
--font-family-body:
  "PingFang SC",
  "Microsoft YaHei",
  "Hiragino Sans GB",
  "WenQuanYi Micro Hei",
  Arial,
  sans-serif,
  Apple Color Emoji,
  Segoe UI Emoji;
```

本机生成时优先级：

1. `PingFang SC`，如果系统可用。
2. `Hiragino Sans GB`。
3. `STHeiti Medium / STHeiti Light`。
4. `Arial Unicode` 或 PIL 默认字体。

## 颜色

常用 token：

| 用途 | Token | 色值 |
| --- | --- | --- |
| 主蓝/强调色 | `--color-blue-600` | `#2254F4` |
| 主标题深色 | `--color-gray-900` | `#222529` |
| 正文深灰 | `--color-gray-800` | `#4C535C` |
| 辅助说明 | `--color-gray-700` | `#7F8792` |
| 白色 | `--color-static-white` | `#FFFFFF` |

## 字号 token

| Token | 字号 |
| --- | --- |
| `--font-size-950` | `48px` |
| `--font-size-900` | `46px` |
| `--font-size-800` | `42px` |
| `--font-size-750` | `40px` |
| `--font-size-700` | `38px` |
| `--font-size-650` | `36px` |
| `--font-size-600` | `34px` |
| `--font-size-550` | `32px` |
| `--font-size-500` | `30px` |
| `--font-size-450` | `28px` |
| `--font-size-400` | `26px` |
| `--font-size-350` | `24px` |
| `--font-size-300` | `22px` |
| `--font-size-250` | `20px` |
| `--font-size-200` | `18px` |
| `--font-size-150` | `16px` |
| `--font-size-100` | `14px` |
| `--font-size-50` | `12px` |

字重：

- Bold：`600`
- Regular：`400`
- 行高：标题 `1.3`，正文 `1.5`

## 物料映射

### Banner

规范尺寸：`1200 x 120`。

建议按最终显示尺寸理解。如果生成 2x 图 `2400 x 240`，字号乘 2。

| 层级 | 建议字号 | 字重 | 颜色 |
| --- | --- | --- | --- |
| 主标题 | `32-34px`，优先 `34px` | `600` | `#222529` |
| 副标题 / 正文说明 | `16-18px`，优先 `18px` | `400` | `#4C535C` 或 `#222529` |
| CTA 按钮文字 | `22-24px` | `600` | `#FFFFFF` |
| 强调词 | 同所在行字号 | `600` | `#2254F4` |

### 弹窗

规范尺寸：`700 x 550`。

建议按最终显示尺寸理解。如果生成 2x 图 `1400 x 1100` 或 `1500 x 1100`，字号按比例换算。当前 AI 商品图优化弹窗是 `1500 x 1100`，视觉上对应约 `750 x 550`，所以字号约等于显示字号 x2。

| 层级 | 建议字号 | 字重 | 颜色 |
| --- | --- | --- | --- |
| 主标题 | `34-40px`，优先 `38px` | `600` | `#222529` |
| 副标题 | `24-28px` | `600` | `#222529`，强调词用 `#2254F4` |
| 功能点标题 | `18-22px` | `600` | `#2254F4` |
| 功能点正文 | `13-16px` | `400` | `#7F8792` 或 `#4C535C` |
| CTA 按钮文字 | `24-28px` | `600` | `#FFFFFF` |
| 权益/提示文案 | `14-18px` | `400/600` | 普通 `#4C535C`，数字重点 `#2254F4` |

## 生成要求

后续生成 banner / 弹窗时：

1. 优先使用以上 token，不随意使用其他蓝色或灰色。
2. 标题默认 `600` 字重，不再使用过细字体。
3. 如果是 2x 输出，所有字号、线宽、圆角、间距按 2x 计算。
4. 最终交付前检查文案是否溢出、遮挡、过小或和规范层级不一致。

