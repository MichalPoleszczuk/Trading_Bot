# Trading_Bot

This repository contains a Python-based Discord bot designed to fetch and analyze K-line data for the SOL/USDT trading pair from Bybit. The bot calculates the Relative Strength Index (RSI) based on closing prices and sends alerts to a Discord channel when RSI values indicate overbought or oversold conditions.

## Features

-   **Data Fetching:** Periodically fetches K-line data for the SOL/USDT trading pair.
-   **RSI Calculation:** Computes the RSI using the `ta` technical analysis library.
-   **Discord Integration:** Sends alerts to a Discord channel if the RSI value is over 70 or below 30.

## How It Works

1.  **Initialization:** The bot is initialized with your Discord bot token and Bybit API keys.
2.  **Data Fetching:** The bot fetches K-line data for the SOL/USDT trading pair from Bybit at 1-hour intervals.
3.  **RSI Calculation:** It calculates the RSI based on the closing prices of the fetched K-line data.
4.  **Discord Alerts:** If the RSI value is over 70 or below 30, an alert is sent to a specified Discord channel.

## Requirements

-   Python 3.11
-   Libraries:
    -   discord.py
    -   pandas
    -   ta
    -   pybit

## Setup

### Configuration

There is a `config.py` file in repository with placeholders for your Bybit API keys and Discord bot token. Use the following template:

``` python
# config.py

api_key = "YOUR_BYBIT_API_KEY"
api_secret = "YOUR_BYBIT_API_SECRET"
discord_token = "YOUR_DISCORD_BOT_TOKEN"
discord_channel_id = "YOUR_DISCORD_CHANNEL_ID"
```

### Installation

1.  **Clone the repository:** git clone <https://github.com/MichalPoleszczuk/Trading_Bot.git>
2.  **Install the required packages:** pip install -r requirements.txt

If you want to run the bot locally, use:

``` bash
python3 bot_source.py
```

### Running the Bot in Docker

1.  **Build the Docker Image:**

``` bash
docker build -t discord-rsi-bot .
```

2.  **Run the Docker Container:**

``` bash
docker run -d --name discord-rsi-bot discord-rsi-bot
```

3.  **View the logs to confirm the bot is running:**

``` bash
docker logs -f discord-rsi-bot
```
