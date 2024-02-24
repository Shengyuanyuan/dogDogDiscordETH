import os
from binance.client import Client
import discord
import asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()
discord_token = os.getenv('DISCORD_BOT_TOKEN_ETH')
CHANNEL_ID = os.getenv('CHANNEL_ID')
# 建立Binance API客戶端
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')
client = Client(api_key, api_secret)

# 建立Discord客戶端
intents = discord.Intents.default()
intents.message_content = True
# client_discord = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
# 設定通知閥值
THRESHOLD = 0.0001


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
# 定義監聽比特幣價格的函數
async def on_message(message):
    # 當收到!start指令時，開始監聽比特幣價格變化
    if message.content.startswith('!start_eth'):
        while True:
            print('開始監聽5分鐘的價格變化')
            # 取得比特幣最新的K線資料
            klines = client.get_klines(
                symbol='ETHUSDT', interval=Client.KLINE_INTERVAL_5MINUTE)
            # 取得最新的收盤價
            last_price = float(klines[-1][4])
            print(float(klines[-1][4]))
            # 取得前一分鐘的收盤價
            prev_price = float(klines[-2][4])
            print(float(klines[-2][4]))
            # 計算價格變動幅度
            price_change = (last_price - prev_price) / prev_price
            # 如果變動幅度超過閥值，就發送通知到Discord
            if abs(price_change) > THRESHOLD:
                if price_change > 0:
                    await message.channel.send(f'📈📈 ETH現在價格為: {last_price:.2f}, 5分鐘內上漲 {price_change*100:.2f}%')
                if price_change < 0:
                    await message.channel.send(f'🚨🚨 ETH現在價格為: {last_price:.2f}, 5分鐘內下跌 {price_change*100:.2f}%')
            print('監聽休息5分鐘')
            await asyncio.sleep(300)


# @bot.event
# # 定義監聽比特幣價格的函數
# async def on_message(message):
#     # 當收到!start指令時，開始監聽比特幣價格變化
#     if message.content.startswith('/monitor btc 5m'):
#         while True:
#             print('開始監聽5分鐘的價格變化')
#             # 取得比特幣最新的K線資料
#             klines = client.get_klines(
#                 symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_5MINUTE)
#             # 取得最新的收盤價
#             last_price = float(klines[-1][4])
#             print(float(klines[-1][4]))
#             # 取得前一分鐘的收盤價
#             prev_price = float(klines[-2][4])
#             print(float(klines[-2][4]))
#             # 計算價格變動幅度
#             price_change = (last_price - prev_price) / prev_price
#             # 如果變動幅度超過閥值，就發送通知到Discord
#             if abs(price_change) > THRESHOLD:
#                 if price_change > 0:
#                     await message.channel.send(f'📈 BTC現在價格為: {last_price:.2f}, 5分鐘內上漲 {price_change*100:.2f}%')
#                 if price_change < 0:
#                     await message.channel.send(f'🚨 BTC現在價格為: {last_price:.2f}, 5分鐘內下跌 {price_change*100:.2f}%')
#             print('監聽休息5分鐘')
#             await asyncio.sleep(300)
bot.run(discord_token)
# client_discord.run(discord_token)
