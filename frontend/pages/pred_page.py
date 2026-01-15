from fasthtml.common import *  
from monsterui.all import *
from fh_plotly import plotly2fasthtml


# Add parent directory to path
module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)
    
from frontend.components.layout import page_layout
from backend.predict_ml.pred_chart import plot_predictions
from backend.predict_ml.model.pipeline.collection import get_data
from backend.predict_ml.model.model_service import ModelService
from frontend.components.pred_table import create_prediction_series

def pred_route(rt):
    @rt('/prediction')
    def get():
        form = Form(
            Div(
                LabelInput("Crypto Symbol:", name="symbol", placeholder="e.g., BTCUSDT",
                        cls='w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500'),
                    
                    Br(),
                    
                    LabelSelect(
                    Option("1m", value="1m"),
                    Option("5m", value="5m"),
                    Option("15m", value="15m"),
                    Option("30m", value="30m"),
                    Option("1h", value="1h"),
                    Option("4h", value="4h"),
                    Option("1d", value="1d"),
                    label="Interval:",
                    name="interval",
                    cls = 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500',
                    ),

                    Br(),
                    
                    LabelInput('Forecast Numbers', name='forecast_period', placeholder='30',
                            cls='w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500'),
                    
                    Br(),
                    
                    Div(Button('View Prediction', type='submit',
                        cls=('center-button' + ButtonT.primary), hx_indicator='#loading'),
                        cls='text-center')
            ),
            Div(Loading((LoadingT.bars, LoadingT.lg), htmx_indicator=True, id='loading'),
                cls='text-center'),
            
            hx_target='#prediction-area',
            hx_post='/prediction/chart'
        )
        
        content = [
            form,
            Br(),
            Div(id='prediction-area',
                hx_swap='true')
        ]
        
        return page_layout(
            'Predction Analysis',
            *content
        )
        
        
    @rt('/prediction/chart')
    def post(symbol: str, interval: str, forecast_period: int):
        df = get_data(symbol, interval, forecast_period)
        X_future = df.drop(['Prediction'], axis=1)[-forecast_period:]
        
        ml_svc = ModelService(df, forecast_period)
        model = ml_svc.load_model()
        
        prediction = model.predict(X_future)
        
        fig = plot_predictions(df, forecast_period, prediction, symbol, interval)
        plot_div = plotly2fasthtml(fig)
        
        # Prepare the prediction series table
        pred_series = create_prediction_series(df, interval, forecast_period, prediction)
        table_rows = [Tr(Td(f"{row['Price']:.2f}"), Td(str(row['Date']))) for _, row in pred_series.iterrows()]
        table_html = Div(Table('',
                            Thead(Tr(Th('Price'), Th('Date'))),
                            Tbody(*table_rows)),
                            cls='overflow-x-auto max-h-96 border border-gray-300 rounded-md p-2 bg-white shadow-sm centered-table')
        
        return Div(
            H3('Prediction Results'),
            Br(),
            plot_div,
            Br(),
            table_html,
        )
        
        
        
        
        