from fasthtml.common import *
from monsterui.all import *


def crypto_card(symbol, price, pct_change, change):
    """Reusable stock card components"""
    if float(pct_change) > 0:  
        change_class = "green"  
        change_symbol = "▲"  
    elif float(pct_change) < 0:
        change_class = "red"  
        change_symbol = "▼"  
    else:  
        change_class = "neutral"  
        change_symbol = "●" 
    return CardContainer(
        DivFullySpaced(
        CardTitle(H3(symbol, cls=TextPresets.bold_lg)),
        P(f"Last Price: ${price:.2f}", cls=TextPresets.bold_sm),
        P(Span(f'{change_symbol} ${change:.4f} - {abs(pct_change)}%', style=f'color: {change_class}'))
        
        ),
        cls=CardT.hover
    )