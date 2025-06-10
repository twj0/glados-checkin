# Checkin

GitHub Actions 实现 [GLaDOS][glados] 自动签到

([GLaDOS][glados] 可用邀请码: `MW4DK-O0RSF-C7AOU-EN1MP`, 双方都有奖励天数)

## 使用说明

1. Fork 这个仓库

1. 登录 [GLaDOS][glados] 获取 Cookie

1. 添加 Cookie 到 Secret `GLADOS`

1. 启用 Actions, 每天北京时间 00:10 自动签到

## 高级功能

1. 如有多个帐号, 可以写为多行 Secret `GLADOS`, 每行写一个 Cookie

1. 如需修改时间, 可以修改文件 [run.yml](.github/workflows/run.yml#L7) 中的 `cron` 参数, 格式可参考 [crontab]

1. 如需推送通知, 可配置 Secret `NOTIFY`, 已支持:
    1. [WxPusher][wxpusher]: 格式 `wxpusher:{token}:{uid}`
    1. [PushPlus][pushplus]: 格式 `pushplus:{token}`
    1. Console: 格式 `console:log`, 作为日志输出, 一般用于调试
    1. 如需配置多个, 可以写为多行, 每行写一个

1. 注意: Cookie 以及接口输出数据, 包含帐号敏感信息, 因此不要随意公开

---

[glados]: https://github.com/glados-network/GLaDOS
[crontab]: https://crontab.guru/
[pushplus]: https://www.pushplus.plus/
[wxpusher]: https://wxpusher.zjiecode.com/


---

# Checkin

## Python 改版

此版本由原版 Fork 而来，将核心逻辑迁移到了 Python，并**增加了对 Telegram 推送的支持**。代码更清晰，方便后续维护和功能扩展。

### 使用说明 (Python 版)

#### 步骤 1: 准备 Python 相关文件

请确保你的仓库根目录下包含以下三个文件：

1.  **签到脚本 `checkin.py`**:
    *   这是执行签到和推送的核心脚本。

2.  **依赖文件 `requirements.txt`**:
    *   文件内容应包含 `python-telegram-bot` 和 `httpx`。

3.  **工作流文件 `.github/workflows/run.yml`**:
    *   此文件调用 Python 环境来执行脚本。


#### 步骤 2: 获取 Telegram 推送所需信息

1.  **获取 Bot Token**:
    *   在 Telegram 中搜索并与 **@BotFather** 对话，发送 `/newbot` 命令创建你自己的机器人，你将获得一串 Bot Token。
2.  **获取 Chat ID**:
    *   在 Telegram 中搜索并与 **@userinfobot** 对话，它会直接返回你的 Chat ID。
3.  **激活机器人**:
    *   **重要**: 搜索你刚刚创建的机器人，并给它发送一条消息（例如 `/start`），以授权它向你发送消息。

#### 步骤 3: 在 GitHub 添加 Secrets

进入你的 GitHub 仓库 -> **Settings** -> **Secrets and variables** -> **Actions**，点击 **New repository secret** 添加以下三个机密信息：

1.  **`GLADOS_COOKIES`**:
    *   **值**: 你的 GLaDOS Cookie。如果你有多个账号，每个 Cookie **占一行**。Cookie按F12后可以获取，比如可以在“网络”中，过滤“user”，一般都可以找到cookie的。大概是这样的：koa:sess=; koa:sess.sig=

1.  **`TELEGRAM_BOT_TOKEN`**:
    *   **值**: 你从 @BotFather 获取的机器人 Token。

2.  **`TELEGRAM_CHAT_ID`**:
    *   **值**: /start后，在这个网站  https://api.telegram.org/bot114514:bilibili/getUpdates  获取的 Chat ID。可能是十位数字吧。

> **注意**: Python 版本不再使用原版的 `GLADOS` 和 `NOTIFY` 这两个 Secrets。

#### 步骤 4: 启用并测试 Actions

1.  进入仓库的 **Actions** 标签页，如果 workflow 是禁用的，请先启用它。
2.  在左侧选择 **GLaDOS Checkin** 工作流。
3.  点击 **Run workflow** 下拉菜单，再点击绿色的 **Run workflow** 按钮，即可手动触发一次签到任务。
4.  稍等片刻，检查 Actions 日志，并留意你的 Telegram 是否收到了签到报告。

### 安全提示

*   Cookie 以及接口输出数据，包含帐号敏感信息，请勿在任何地方公开你的仓库 Secrets 或日志中的敏感数据。

---

[glados]: https://github.com/glados-network/GLaDOS
[crontab]: https://crontab.guru/
[pushplus]: https://www.pushplus.plus/
[wxpusher]: https://wxpusher.zjiecode.com/
[telegram-bot-api]: https://core.telegram.org/bots/api