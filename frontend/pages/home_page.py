from asyncio import sleep, gather  
from fasthtml.common import *  
from monsterui.all import *

from backend.data_stream import get_price_and_pct_change
from backend.data_stream import fetch_ohlcv, create_ohlcv_chart
from frontend.components.crypto_cards import crypto_card
from frontend.components.layout import page_layout

shutdown_event = signal_shutdown()

def home_route(rt):
    
    @rt('/')
    def index():
        
        form = Form(hx_post="/chart-stream", hx_target="#chart-container")(  
            Input(name="symbol", placeholder="Symbol (e.g., BTC)"),  
            Input(name="interval", placeholder="Interval (e.g., 1m)"), 
            LabelSelect(
                    Option("RSI", value="rsi"),
                    Option("MACD", value="macd"),
                    Option("BBands", value="bbands"),
                    label="Indicator:",
                    name="indicator",
                    cls = 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500',
                    ),  
             
            Button("Start Streaming", type="submit")
            )
        
        content = [
            form,
            
            Br(),
            
            Div(
                hx_ext='sse',
                sse_connect='/crypto-stream',
                # hx_swap='true',
                sse_swap='message'
            ),
            
            Br(),
            
            Div(
                id='chart-container',
                hx_ext='sse',
                sse_connect='/chart-stream',
                # hx_swap='true',
                sse_swap='message'
            ),
            
            
            
        ]
        
        return page_layout(
            "Crypto Market Dashboard",
            *content
        )
    
    async def crypto_generator():
        symbols = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "SOLUSDT", "TRUMPUSDT", "TONUSDT", "DOGEUSDT", "XRPUSDT",
                   "DASHUSDT", "BNBUSDT", "LTCUSDT", "TRXUSDT", "BCHUSDT", "ZECUSDT", "XMRUSDT", "TONUSDT"]
        
        while not shutdown_event.is_set():
            try:
                tasks = [get_price_and_pct_change(symbol) for symbol in symbols]
                responses = await gather(*tasks)
                
                rows = []
                for response in responses:
                    symbol = response['symbol']
                    price = response['current_price']
                    pct_change = response['pct_change']
                    change = response['change']
                    
                    row = {
                        'symbol': symbol,
                        'price': price,
                        'pct_change': pct_change,
                        'change': change
                    }
                    rows.append(row)
                    
                crypto_row = Container(*[crypto_card(**row) for row in rows], cls=ContainerT.sm)
                
                yield sse_message(crypto_row)
                
            except Exception as e:
                yield sse_message(Article(f'Error:  {str(e)}'))
            await sleep(1)
            
        
                
    @rt('/crypto-stream')
    async def get():
        return EventStream(crypto_generator())
    
    
    
    @rt('/chart-stream')
    async def post(symbol: str = 'BTCUSDT', interval: str = '1m', indicator: str = 'rsi'):
        # Return a small div that instructs the client to open an SSE GET stream
        return Div(
            hx_ext='sse',
            sse_connect=f"/chart-stream/stream?symbol={symbol}&interval={interval}&indicator={indicator}",
            # hx_swap='true',
            sse_swap='message'
        )

    @rt('/chart-stream/stream')
    async def stream(symbol: str, interval: str, indicator: str ):
        async def crypto_data_generator():
            while not shutdown_event.is_set():
                try:
                    data = await fetch_ohlcv(symbol, interval)
                    if data:
                        chart_element = create_ohlcv_chart(symbol, data, indicator)
                        yield sse_message(chart_element)
                        
                except Exception as e:
                    yield sse_message(Article(f'Error: {str(e)}'))
                await sleep(1)

        return EventStream(crypto_data_generator())
    