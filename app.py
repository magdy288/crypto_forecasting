from fasthtml.common import *
from monsterui.all import *
from fh_plotly import plotly_headers


# Add parent directory to path
module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)
    
from frontend.pages.home_page import home_route
from frontend.pages.pred_page import pred_route

theme = Theme.yellow.headers(mode='light',font=ThemeFont.sm,
                             highlightjs=True, daisy=True)
app, rt = fast_app(

    hdrs=(
        Script(src="https://unpkg.com/htmx-ext-sse@2.2.1/sse.js"),
        theme,
        plotly_headers,
        Script(src='https://cdn.plot.ly/plotly-2.32.0.min.js'),
        Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        Meta(name='description', content=' My Website'),

    )
)

# Register route modules
home_route(rt)
pred_route(rt)

serve(host='0.0.0.0', port=8000, reload=False)