import discord
from discord.ext import commands
import pandas as pd
import ta
import asyncio
from pybit.unified_trading import HTTP
import config  # This should contain your API keys and Discord bot token
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Any, Dict

# Initialize Discord bot and Bybit client
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)
session = HTTP(api_key=config.api_key, api_secret=config.api_secret)
print('Logged in')  # Confirm that the client has been initialized

def fetch_klines(symbol: str, interval: str, limit: int = 15) -> Optional[List[List[Any]]]:
    """
    Fetches K-line (candlestick) data for a given symbol and interval from Bybit.

    Args:
        symbol (str): The trading symbol (e.g., 'SOLUSDT').
        interval (str): The interval for K-line data (e.g., '60' for 1 hour).
        limit (int): The number of K-lines to fetch (default is 15).

    Returns:
        Optional[List[List[Any]]]: A list of K-lines, or None if an error occurs.
    """
    try:
        response = session.get_kline(
            category='linear',
            symbol=symbol,
            interval=interval,
            limit=limit
        )
        return response['result']['list']
    except Exception as e:
        print(f"Error fetching Kline data: {e}")
        return None

def extract_closing_prices(klines: List[List[Any]]) -> List[float]:
    """
    Extracts the closing prices from K-line data.

    Args:
        klines (List[List[Any]]): The K-line data.

    Returns:
        List[float]: A list of closing prices.
    """
    return [float(kline[4]) for kline in klines]

def calculate_rsi(prices: List[float], period: int = 14) -> float:
    """
    Calculates the Relative Strength Index (RSI) for a list of prices.

    Args:
        prices (List[float]): The list of closing prices.
        period (int): The period for the RSI calculation (default is 14).

    Returns:
        float: The RSI value.
    """
    df = pd.DataFrame(prices, columns=['close'])
    rsi = ta.momentum.RSIIndicator(df['close'], window=period).rsi()
    return rsi.iloc[-1]

async def send_rsi_alert() -> None:
    """
    Sends an RSI alert to a Discord channel if the RSI value is over 70 or below 30.
    This function runs indefinitely, checking the RSI at the end of each hourly bar.
    """
    await client.wait_until_ready()
    channel = client.get_channel(int(config.discord_channel_id.strip()))

    if channel is None:
        print("Channel not found. Please check the discord_channel_id.")
        for guild in client.guilds:
            for chan in guild.channels:
                print(f"Channel name: {chan.name}, Channel ID: {chan.id}")
        return

    print(f"Successfully connected to channel: {channel.name}")

    while not client.is_closed():
        symbol = 'SOLUSDT'
        interval = '60'  # 1 hour interval for Kline data
        period = 14

        klines = None
        while klines is None:
            klines = fetch_klines(symbol, interval, limit=period + 1)
            if klines is None:
                print("Waiting due to rate limits...")
                await asyncio.sleep(1)

        closing_prices = extract_closing_prices(klines)
        print(f"Closing prices: {closing_prices}")

        if len(closing_prices) >= period:
            last_rsi = calculate_rsi(closing_prices, period)
            print(f"Last RSI value: {last_rsi}")
            if last_rsi > 70:
                await channel.send(f"RSI Alert: Overbought! RSI is {last_rsi:.2f}")
            elif last_rsi < 30:
                await channel.send(f"RSI Alert: Oversold! RSI is {last_rsi:.2f}")
        else:
            print("Not enough closing prices for RSI calculation.")

        # Calculate time until next hour
        now = datetime.now(timezone.utc)
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        sleep_time = (next_hour - now).total_seconds() + 2  # Add a 2-second buffer

        await asyncio.sleep(sleep_time)

@client.event
async def on_ready() -> None:
    """
    Event handler called when the bot is ready. It starts the RSI alert loop.
    """
    print(f'Logged in as {client.user}')
    await send_rsi_alert()

# Run the Discord client
client.run(config.discord_token)

