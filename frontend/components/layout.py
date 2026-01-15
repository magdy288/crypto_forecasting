from fasthtml.common import *
from monsterui.all import *
from datetime import datetime



def page_layout(title, *content):
    """Main page layout with navigation"""
    nav = Header(
        Div(
            # A("Crypto Dashboard", href="/", cls=AT.classic),
            Div(
            Button('Pages 👇🏽', cls=ButtonT.primary),
            DropDownNavContainer(
                Li(A("Home", href="/", cls=AT.primary)),
                Li(A("Prediction", href="/prediction", cls=AT.primary)),
                # Li(A("AI", href="/ai", cls=AT.primary)),
                ),

        ),
        cls = 'container mx-auto flex items-center justify-between px-4 py-3'
        ),
    cls='bg-blue-200 shadow-md'
    )

    footer = Footer(
        Div(
            Div(
                P(f"© {datetime.now().year} Crypto Forecasting. All rights reserved.",
                  cls='text-gray-700'),

                cls = 'mb-4'
            ),

            Div(
                A('Privacy Policy', href='#', cls=AT.classic),
                A('Terms of Service', href='#', cls=AT.classic),

                cls = 'text-sm'
            ),

            cls = 'container mx-auto px-4 py-6 text-center'
        ),

        cls = 'bg-blue-100 mt-9'
    )

    body = Body(
            nav,
            Main(
                Div(*content, cls="container mx-auto px-4 py-8"),
                cls='min-h-screen'
            ))

    return Title(title), body, footer