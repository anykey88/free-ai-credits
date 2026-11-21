# 🌍 Free AI Credits Hunter｜全球 AI 免费额度猎手

> 把全世界能白嫖的 AI 额度做成一份**可执行、可追踪、可变现**的系统。
> 不是又一个"额度清单"——清单会过期，这套东西教你怎么**领、怎么记、怎么到期前用掉、怎么变成收入**。

**English**: A practical system for hunting free AI credits worldwide — claim, track, expire-proof, and monetize. See [references/registry.md](references/registry.md) for the full platform registry (Chinese; platform names are universal).

## 📦 这个仓库是什么

| 文件 | 作用 |
|---|---|
| `SKILL.md` | Skill 使用说明（可直接装进 AI 助手当技能用） |
| `references/registry.md` | **全球平台注册表**：注册赠送 / 每日签到 / 永久免费模型 / 海外免费层 四大类，含领取步骤、有效期、实名要求 |
| `references/monetization.md` | **变现指南**：5 条合规变现路径 + 30 天启动模型 |
| `scripts/credits_ledger.py` | **领取台账脚本**：记录领取、到期预警（零依赖，Python 3.8+） |

## 🚀 三分钟上手

```bash
# 1. 按注册表领额度（以智谱为例）：open.bigmodel.cn 注册 → 自动到账 2000 万 Token
# 2. 记台账
python scripts/credits_ledger.py add "智谱AI" 20000000 --expires 2030-01-01 --note "注册送,永久"
# 3. 每周跑一次到期巡检
python scripts/credits_ledger.py due --days 7
# 4. 用完了标记
python scripts/credits_ledger.py used 1
```

装进 AI 助手（WorkBuddy / Claude Code 等）：把本目录复制到技能目录，助手即可响应"白嫖 AI"、"免费 Token"、"免费额度"类请求，自动生成领取计划并维护台账。

## 🗺️ 额度全景（速览）

| 类型 | 代表平台 | 量级 | 价值 |
|---|---|---|---|
| 注册即送 | 阿里云百炼 7000 万 / 智谱 2000 万 / 讯飞星辰 10 亿 | 首轮合计 **>1 亿 Token** | 一次性，领完倒计时 |
| 每日签到 | 火山引擎 200 万/天、WorkBuddy 100 分/天 等 13 个 | 每天 >300 万 Token | **可自动化，长期价值最高** |
| 永久免费模型 | GLM-4.7-Flash / ERNIE-Speed / 混元 Lite / Doubao-Lite | 不限量 | 零成本产线的底座 |
| 海外免费层 | Google AI Studio / Groq / OpenRouter | 每天百万级 | 需网络条件，备用 |

## ⚠️ 五条限制（先读再用，都是踩过的坑）

1. **限时额度别囤**：90 天/31 天型过期清零，领完立即安排消耗。
2. **免费档≠旗舰**：多数免费层是 Lite/Flash 版，重任务该付费就付费。
3. **禁止多账号**：平台风控封号，账号资产全没收。
4. **禁止共享 Key**：不稳定＋数据安全风险；业务文件一律原厂直连。
5. **免费层不跑生产流量**：有 RPM/QPS 限制；平台政策随时会变（本仓库会更新，但以官方页面为准）。

## 💰 怎么变现（合规版）

> 铁律：变现的是**你的服务和内容**，不是转售平台额度（转售违反条款）。

1. **内容流量变现**（0 门槛）：把攻略做成图文/短视频，吃创作激励和广告
2. **自动化服务**：给个人账号做定时领取的技能/教程（绝不做多账号代刷）
3. **零成本产线**：免费额度跑自媒体代运营/文书服务/数据简报，卖给付费客户
4. **方法论课程**：跑通一条产线后，把过程打包成教程/训练营
5. **导航站**：注册表做成网站，吃广告位与云厂商邀请返佣

完整的 5 条路径 + 30 天启动模型（含真实公开参照案例）见 [references/monetization.md](references/monetization.md)。

## 🤝 贡献

发现新平台/政策变动？提 Issue 或 PR 更新 `references/registry.md`，注明来源链接。

## 📄 License

MIT. 本仓库仅汇总公开信息，不保证平台政策不变，不构成任何商业承诺。
