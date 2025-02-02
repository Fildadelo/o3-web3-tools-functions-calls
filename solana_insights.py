#!/usr/bin/env python
import os
import json
import asyncio
import datetime
import click
import openai
import aiohttp
from rich.console import Console
from rich.table import Table

# Initialize Rich console for pretty printing
console = Console()

# Set your OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")

# ------------------------------------------------------------------------------
# Asynchronous helper functions to fetch data from external APIs.
# (Replace the placeholder URLs with your real endpoints as needed.)
# ------------------------------------------------------------------------------

# Placeholder API endpoint for market sentiment on a Solana memecoin.
SENTIMENT_API_URL = "https://api.example.com/solana/sentiment?coin={coin}"
# Solscan endpoints for token and trader info.
SOLSCAN_TOKEN_INFO_URL = "https://public-api.solscan.io/token/meta?tokenAddress={token_address}"
SOLSCAN_TRADER_INFO_URL = "https://public-api.solscan.io/account/tokens?account={wallet_address}"

async def fetch_market_sentiment(coin: str) -> dict:
    """Fetch market sentiment data for the given coin."""
    url = SENTIMENT_API_URL.format(coin=coin)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                else:
                    return {"error": f"Sentiment API returned status code {resp.status}"}
        except Exception as e:
            return {"error": str(e)}

async def fetch_token_info(token_address: str) -> dict:
    """Fetch token metadata from Solscan for the provided token address."""
    url = SOLSCAN_TOKEN_INFO_URL.format(token_address=token_address)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return {"error": f"Solscan API returned status code {resp.status}"}
        except Exception as e:
            return {"error": str(e)}

async def fetch_trader_info(wallet_address: str) -> dict:
    """Fetch trader (wallet) information from Solscan for the given wallet address."""
    url = SOLSCAN_TRADER_INFO_URL.format(wallet_address=wallet_address)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return {"error": f"Solscan API returned status code {resp.status}"}
        except Exception as e:
            return {"error": str(e)}

# ------------------------------------------------------------------------------
# OpenAI API utility function
# ------------------------------------------------------------------------------
async def query_openai(prompt: str, max_tokens: int = 200, temperature: float = 0.2, reasoning_effort: str = "medium") -> str:
    """Query the OpenAI o3-mini model and return the answer."""
    try:
        response = await openai.ChatCompletion.acreate(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "You are an expert assistant for Web3, blockchain, and coding."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            provider_options={"reasoningEffort": reasoning_effort}
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error querying OpenAI API: {str(e)}"

# ------------------------------------------------------------------------------
# Main function to generate an aggregated insight report.
# ------------------------------------------------------------------------------
async def generate_insights(coin: str, token_address: str, wallet_address: str, reasoning_effort: str) -> str:
    """Fetch data from various sources and generate a summary report using OpenAI."""
    # Gather data concurrently
    async with aiohttp.ClientSession() as session:
        sentiment_task = asyncio.create_task(fetch_market_sentiment(coin))
        token_task = asyncio.create_task(fetch_token_info(token_address))
        trader_task = asyncio.create_task(fetch_trader_info(wallet_address))
        sentiment_data, token_data, trader_data = await asyncio.gather(sentiment_task, token_task, trader_task)

    # Prepare a prompt for OpenAI with the aggregated data
    prompt = (
        f"Below is the aggregated data for a Solana asset:\n\n"
        f"Market Sentiment for {coin}:\n{json.dumps(sentiment_data, indent=2)}\n\n"
        f"Token Metadata for address {token_address}:\n{json.dumps(token_data, indent=2)}\n\n"
        f"Trader (Wallet) Data for address {wallet_address}:\n{json.dumps(trader_data, indent=2)}\n\n"
        "Provide a comprehensive summary report that describes the market sentiment, token details, and trader activity. "
        "Highlight any potential opportunities or risks. Use a professional tone and include actionable insights."
    )
    summary = await query_openai(prompt, max_tokens=300, reasoning_effort=reasoning_effort)
    return summary

# ------------------------------------------------------------------------------
# CLI Application using Click
# ------------------------------------------------------------------------------
@click.group()
def cli():
    """Solana Insights CLI: Fetch market data and generate AI-driven insights for Solana tokens and traders."""
    pass

@cli.command()
@click.argument("coin")
def sentiment(coin):
    """Fetch market sentiment for a Solana memecoin (by coin symbol)."""
    async def run():
        data = await fetch_market_sentiment(coin)
        console.print("[bold green]Market Sentiment Data:[/bold green]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Key")
        table.add_column("Value")
        for key, value in data.items():
            table.add_row(str(key), str(value))
        console.print(table)
    asyncio.run(run())

@cli.command()
@click.argument("token_address")
def token(token_address):
    """Fetch token metadata from Solana for the given token address."""
    async def run():
        data = await fetch_token_info(token_address)
        console.print("[bold green]Token Information:[/bold green]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Key")
        table.add_column("Value")
        for key, value in data.items():
            table.add_row(str(key), str(value))
        console.print(table)
    asyncio.run(run())

@cli.command()
@click.argument("wallet_address")
def trader(wallet_address):
    """Fetch trader (wallet) information from Solana for the given wallet address."""
    async def run():
        data = await fetch_trader_info(wallet_address)
        console.print("[bold green]Trader Information:[/bold green]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Key")
        table.add_column("Value")
        for key, value in data.items():
            table.add_row(str(key), str(value))
        console.print(table)
    asyncio.run(run())

@cli.command()
@click.option("--coin", prompt="Coin symbol", help="Solana memecoin symbol for market sentiment.")
@click.option("--token_address", prompt="Token address", help="Solana token address to fetch metadata.")
@click.option("--wallet_address", prompt="Wallet address", help="Trader (wallet) address to fetch information.")
@click.option("--reasoning", default="medium", type=click.Choice(["low", "medium", "high"], case_sensitive=False), help="Reasoning effort level.")
def summary(coin, token_address, wallet_address, reasoning):
    """
    Generate a comprehensive insights report for a Solana token.
    
    This command aggregates market sentiment, token metadata, and trader data,
    and uses OpenAI's o3-mini model to generate a summary report with actionable insights.
    """
    async def run():
        console.print("[bold blue]Generating aggregated insights report...[/bold blue]")
        report = await generate_insights(coin, token_address, wallet_address, reasoning)
        console.print("[bold green]Insights Report:[/bold green]")
        console.print(report)
    asyncio.run(run())

if __name__ == "__main__":
    cli()
