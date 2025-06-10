import os
import asyncio
import httpx  # 用于发送 HTTP 请求，功能类似 requests，但支持异步
from telegram import Bot

# --- 从 GitHub Secrets 读取敏感信息 ---
# 多个 GLaDOS Cookie，用换行符分隔
GLADOS_COOKIES = os.getenv("GLADOS_COOKIES", "")
# Telegram Bot 的 Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
# 你的 Telegram Chat ID
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

async def checkin(cookie: str) -> list[str]:
    """使用单个 Cookie 进行签到，并返回结果消息列表。"""
    checkin_url = "https://glados.rocks/api/user/checkin"
    status_url = "https://glados.rocks/api/user/status"
    headers = {
        'cookie': cookie,
        'referer': 'https://glados.rocks/console/checkin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    try:
        async with httpx.AsyncClient() as client:
            # 1. 进行签到
            checkin_res = await client.post(checkin_url, headers=headers, json={"token": "glados.one"})
            checkin_data = checkin_res.json()

            # 2. 获取账户状态
            status_res = await client.get(status_url, headers=headers)
            status_data = status_res.json()

        # 3. 组合通知消息
        if checkin_data.get("code") == 0:
            days_left = int(float(status_data.get("data", {}).get("leftDays", "0")))
            return [
                "✅ GLaDOS 签到成功",
                f"💬 签到消息: {checkin_data.get('message', '未知')}",
                f"⏳ 剩余天数: {days_left} 天"
            ]
        else:
            return [
                "❌ GLaDOS 签到失败",
                f"💬 错误信息: {checkin_data.get('message', '未知错误')}"
            ]
            
    except Exception as e:
        return ["💥 签到脚本异常", f"错误详情: {e}"]

async def send_telegram_message(message: str):
    """使用 Telegram Bot 发送消息。"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram 的 Token 或 Chat ID 未设置，跳过发送。")
        return
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

async def main():
    """主函数，遍历所有 Cookie 并执行签到和通知。"""
    if not GLADOS_COOKIES:
        print("未找到 GLADOS_COOKIES，程序退出。")
        return

    # 分割多个 cookie
    cookie_list = [c.strip() for c in GLADOS_COOKIES.split("\n") if c.strip()]
    
    final_messages = ["**GLaDOS 签到报告**\n"]
    
    for i, cookie in enumerate(cookie_list, 1):
        result = await checkin(cookie)
        # 为多账号添加分隔符
        if len(cookie_list) > 1:
            final_messages.append(f"\n--- 账号 {i} ---")
        final_messages.extend(result)

    # 发送整合后的消息到 Telegram
    await send_telegram_message("\n".join(final_messages))
    # 也在控制台打印一份，方便在 GitHub Actions 日志中查看
    print("\n".join(final_messages))


if __name__ == "__main__":
    asyncio.run(main())