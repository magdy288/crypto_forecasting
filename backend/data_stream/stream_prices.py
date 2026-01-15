import httpx  

# Get the last price and pct_change function 
async def get_price_and_pct_change(symbol: str, interval: str = "1s", limit: int = 2):
    KLINE_URL = f"https://api.binance.com/api/v3/ticker?symbol={symbol}" # for pct_change values
    TICKER_URL = "https://api.binance.com/api/v3/ticker/price" # for last price
    
    async with httpx.AsyncClient() as client:
        # Fetch current price
        ticker_resp = await client.get(TICKER_URL, params={"symbol": symbol})
        ticker_data = ticker_resp.json()
        current_price = float(ticker_data["price"])

        # Fetch klines for pct_change
        kline_resp = await client.get(KLINE_URL)
        klines = kline_resp.json()

        pct_change = float(klines['priceChangePercent'])
        change = float(klines['priceChange'])
            
        return {
            "symbol": symbol,
            "current_price": current_price,
            "pct_change": pct_change,
            "change": change
        }