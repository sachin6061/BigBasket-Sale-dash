import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import base64

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])
server = app.server
df = pd.read_csv('BigBasket Products.csv')
df['discount'] = df['market_price'] - df['sale_price']
df.dropna(inplace=True)

app.layout = dbc.Container([dcc.Location(id="url"), dbc.Row(
    [dbc.Col([dbc.Row(html.H2('BigBasket', style={'color': 'white'})),
              dbc.Row(html.H6('Products', style={'color': 'white', 'text-align': 'center', 'font-style': 'italic'})),
              html.Hr(style={'color': 'white'}),
              dbc.Row(dbc.Nav([
                  dbc.NavLink("Category Wise Discount", href="/", active="exact", style={'color': 'white'}),
                  dbc.NavLink("Sub Category Wise Discount", href="/sub_category_wise", active="exact", style={'color': 'white'}),
                  dbc.NavLink("Brand Wise Discount", href="/brand_wise", active="exact", style={'color': 'white'}),
                  dbc.NavLink("About Me", href="/about_me", active="exact", style={'color': 'white'})],
              )),
              ],
             width=2, style={"background-color": "#000000", 'padding': '10px'}),
     dbc.Col(html.Div(id="page-content"), width=10,
             style={'background-color': '#a6a6a6', 'padding': '10px'})], className='h-100'), ],
                           fluid=True, style={'padding': '20px', 'height': '100%', 'background-color': '#d9d9d9'})


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return dcc.Loading(fnCategorywise())
    elif pathname == "/sub_category_wise":
        return dcc.Loading(fnSubCategorywise())
    elif pathname == "/brand_wise":
        return dcc.Loading(fnBrandwise())
    elif pathname == "/about_me":
        return dcc.Loading(fnAboutMe(), type='cube')


def fnCategorywise():
    category_df = df.groupby(['category']).agg(
        {'sale_price': 'sum', 'market_price': 'sum', 'discount': 'sum'}).reset_index()
    grp_chart = go.Figure(data=[
        go.Bar(name='Sale Price', x=category_df['category'], y=category_df['sale_price'],
               text=category_df['sale_price']),
        go.Bar(name='Market Price', x=category_df['category'], y=category_df['market_price'],
               text=category_df['market_price']),
        go.Bar(name='Discount', x=category_df['category'], y=category_df['discount'], text=category_df['discount']),
    ])
    grp_chart.update_traces(texttemplate='%{text:.2s}', textposition='auto')
    grp_chart.update_layout(barmode='group', title='Market Price Vs Sale Price', template='plotly_dark',
                            xaxis_title="Category", yaxis_title="Price")
    dis_fig = px.bar(category_df, x="category", y='discount', title="Category Wise Discount",
                     template='plotly_dark', color='category', text_auto='.2s')
    dis_pie = px.pie(category_df, values='discount', names='category', template='plotly_dark', hole=.3,
                     title='Category wise Discount In Percentage')

    return [dbc.Row([
        dbc.Col([html.H5('Total Products', style={'text-align': 'center'}),
                 html.H4(str(df['category'].count()), style={'text-align': 'center'})], className='mx-1 p-3',
                style={'border-radius': '25px 0px 25px 0px', 'color': 'white', 'background-color': '#000000',
                       'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px'}),
        dbc.Col([html.H5('Total Market Price', style={'text-align': 'center'}),
                 html.H4('{:.2f} Rs.'.format(df['market_price'].sum()), style={'text-align': 'center'})],
                className='mx-1 p-3',
                style={'border-radius': '25px 0px 25px 0px', 'color': 'white', 'background-color': '#000000',
                       'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px'}),
        dbc.Col(
            [html.H5('Totsl Sale Price', style={'text-align': 'center'}),
             html.H4('{:.2f} Rs.'.format(df['sale_price'].sum()), style={'text-align': 'center'})],
            className='mx-1 p-3',
            style={'border-radius': '25px 0px 25px 0px', 'color': 'white', 'background-color': '#000000',
                   'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px'}
        ),
        dbc.Col([html.H5('Discount', style={'text-align': 'center'}),
                 html.H4('{:.2f} Rs.'.format(df['market_price'].sum() - df['sale_price'].sum()),
                         style={'text-align': 'center'})],
                className='mx-1 p-3',
                style={'border-radius': '25px 0px 25px 0px', 'color': 'white', 'background-color': '#000000',
                       'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px'})
    ], className='mx-auto'),

        dbc.Row(
            [dbc.Col(dcc.Graph(id='bar-chart-sale', figure=dis_fig), width=7, className='p-1 ',
                     style={'border-radius': '20px'}),
             dbc.Col(dcc.Graph(id='pie-chart-sale', figure=dis_pie), width=5, className='p-1')],
            className='my-2 mx-auto'),
        dbc.Row([dbc.Col(dcc.Graph(id='grp-bar-chart', figure=grp_chart), className='p-1')], className='my-2 mx-auto '),
    ]


def fnSubCategorywise():
    cat_lst = df['category'].unique()
    return [
        dbc.Row([dbc.Col(dcc.Dropdown(cat_lst, cat_lst[0], id='cat-value'), width=3, className='p-1'),
                 dbc.Col(html.H2('Result For ' + str(cat_lst[0]), id='cat-name',
                                 style={'text-align': 'center', 'color': '#000099'}))], className='my-2 mx-auto '),
        dbc.Row([
            dbc.Col([html.H5('Total Products', style={'text-align': 'center'}),
                     html.H4(id='ttl_product', style={'text-align': 'center'})], className='mx-1 p-3',
                    style={'border-radius': '25px 0px 25px 0px', 'color': 'white', 'background-color': '#000000',
                           'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px'}),
            dbc.Col([html.H5('Market Price', style={'text-align': 'center'}),
                     html.H4(id='ttl-market', style={'text-align': 'center'})], className='mx-1 p-3',
                    style={'border-radius': '25px 0px 25px 0px', 'color': 'white', 'background-color': '#000000',
                           'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px'}),
            dbc.Col(
                [html.H5('Sale Price', style={'text-align': 'center'}),
                 html.H4(id='ttl-sale', style={'text-align': 'center'})],
                className='mx-1 p-3',
                style={'border-radius': '25px 0px 25px 0px', 'color': 'white', 'background-color': '#000000',
                       'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px'}
            ),
            dbc.Col([html.H5('Discount', style={'text-align': 'center'}),
                     html.H4(id='ttl-dis-sub', style={'text-align': 'center'})], className='mx-1 p-3',
                    style={'border-radius': '25px 0px 25px 0px', 'color': 'white', 'background-color': '#000000',
                           'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px'}),

        ], className='mx-auto'),
        dbc.Row(
            [dbc.Col(dcc.Graph(id='bar-chart-sub', ), width=7, className='p-1 ',
                     style={'border-radius': '20px'}),
             dbc.Col(dcc.Graph(id='pie-chart-sub', ), width=5, className='p-1')],
            className='my-2 mx-auto'),
        dbc.Row([dbc.Col(dcc.Graph(id='grp-bar-chart-sub'), className='p-1')], className='my-2 mx-auto ')
    ]


@callback(
    [Output('cat-name', 'children'), Output('ttl_product', 'children'), Output('ttl-market', 'children'),
     Output('ttl-sale', 'children'), Output('ttl-dis-sub', 'children'),
     Output('bar-chart-sub', 'figure'),
     Output('pie-chart-sub', 'figure'), Output('grp-bar-chart-sub', 'figure'),
     ],
    Input('cat-value', 'value')
)
def fnUpdate(txt):
    cat_df = df[df['category'] == txt]
    subcategory_df = cat_df.groupby(['sub_category']).agg(
        {'sale_price': 'sum', 'market_price': 'sum', 'discount': 'sum'}).reset_index()
    grp_chart = go.Figure(data=[
        go.Bar(name='Sale Price', x=subcategory_df['sub_category'], y=subcategory_df['sale_price'],
               text=subcategory_df['sale_price']),
        go.Bar(name='Market Price', x=subcategory_df['sub_category'], y=subcategory_df['market_price'],
               text=subcategory_df['market_price']),
        go.Bar(name='Discount', x=subcategory_df['sub_category'], y=subcategory_df['discount'],
               text=subcategory_df['discount']),
    ])
    grp_chart.update_traces(texttemplate='%{text:.2s}', textposition='auto')
    grp_chart.update_layout(barmode='group', title='Market Price Vs Sale Price', template='plotly_dark',
                            xaxis_title="Category", yaxis_title="Price")
    dis_fig = px.bar(subcategory_df, x="sub_category", y='discount', title="Category Wise Discount",
                     template='plotly_dark', color='sub_category', text_auto='.2s')
    dis_pie = px.pie(subcategory_df, values='discount', names='sub_category', template='plotly_dark', hole=.3,
                     title='Category wise Discount In Percentage')
    return 'Result for ' + str(txt), '{:.0f}'.format(cat_df['category'].count()), '{:.2f} RS'.format(
        cat_df['market_price'].sum()), '{:.2f} RS'.format(
        cat_df['sale_price'].sum()), '{:.2f} RS'.format(cat_df['market_price'].sum() - cat_df[
        'sale_price'].sum()), dis_fig, dis_pie, grp_chart


def fnBrandwise():
    cat_lst = df['category'].unique()
    sub_cat = df[df['category'] == cat_lst[0]]
    sub_cat_lst = sub_cat['sub_category'].unique()
    return [
        dbc.Row([dbc.Col(dcc.Dropdown(cat_lst, cat_lst[0], id='cat-value-b'), width=3, className='p-1'),
                 dbc.Col(dcc.Dropdown(sub_cat_lst, sub_cat_lst[0], id='subcat-value-b'), width=3, className='p-1'),
                 dbc.Col(html.H2('Top 10 Discount And Brand', id='cat-name-b',
                                 style={'text-align': 'center', 'color': '#000099'}))
                 ], className='my-2 mx-auto '),
        dbc.Row([
            dbc.Col([html.H5('Total Products', style={'text-align': 'center'}),
                     html.H4(id='ttl_product-b', style={'text-align': 'center'})], className='mx-1 p-3',
                    style={'border-radius': '25px 0px 25px 0px', 'color': 'white', 'background-color': '#000000',
                           'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px'}),
            dbc.Col([html.H5('Market Price', style={'text-align': 'center'}),
                     html.H4(id='ttl-market-b', style={'text-align': 'center'})], className='mx-1 p-3',
                    style={'border-radius': '25px 0px 25px 0px', 'color': 'white', 'background-color': '#000000',
                           'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px'}),
            dbc.Col(
                [html.H5('Sale Price', style={'text-align': 'center'}),
                 html.H4(id='ttl-sale-b', style={'text-align': 'center'})],
                className='mx-1 p-3',
                style={'border-radius': '25px 0px 25px 0px', 'color': 'white', 'background-color': '#000000',
                       'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px'}
            ),
            dbc.Col([html.H5('Discount', style={'text-align': 'center'}),
                     html.H4(id='ttl-dis-b', style={'text-align': 'center'})], className='mx-1 p-3',
                    style={'border-radius': '25px 0px 25px 0px', 'color': 'white', 'background-color': '#000000',
                           'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px'}),

        ], className='mx-auto'),
        dbc.Row(
            [dbc.Col(dcc.Graph(id='bar-chart-b', ), width=7, className='p-1 ',
                     style={'border-radius': '20px'}),
             dbc.Col(dcc.Graph(id='pie-chart-b', ), width=5, className='p-1')],
            className='my-2 mx-auto'),
        dbc.Row([dbc.Col(dcc.Graph(id='grp-bar-chart-b'), className='p-1')], className='my-2 mx-auto ')
    ]


@callback(
    [Output('subcat-value-b', 'options'), Output('subcat-value-b', 'value')],
    Input('cat-value-b', 'value')
)
def fnUpDr(cat):
    cat_lst = df['category'].unique()
    sub_cat = df[df['category'] == cat]
    return sub_cat['sub_category'].unique(), sub_cat['sub_category'].unique()[0]


@callback(
    [Output('ttl_product-b', 'children'), Output('ttl-market-b', 'children'),
     Output('ttl-sale-b', 'children'), Output('ttl-dis-b', 'children'),
     Output('bar-chart-b', 'figure'),
     Output('pie-chart-b', 'figure'), Output('grp-bar-chart-b', 'figure'),
     ],
    [Input('cat-value-b', 'value'), Input('subcat-value-b', 'value')]
)
def fnUpdate(cat, sub_cat):
    cat_df = df[df['category'] == cat]
    sub_cat_df = cat_df[cat_df['sub_category'] == sub_cat]
    subcategory_df = sub_cat_df.groupby(['brand']).agg(
        {'sale_price': 'sum', 'market_price': 'sum', 'discount': 'sum'}).reset_index()
    # subcategory_df['discount'] = df['market_price'] - df['sale_price']

    subcategory_df = subcategory_df.nlargest(10, 'discount')

    grp_chart = go.Figure(data=[
        go.Bar(name='Sale Price', x=subcategory_df['brand'], y=subcategory_df['sale_price'],
               text=subcategory_df['sale_price']),
        go.Bar(name='Market Price', x=subcategory_df['brand'], y=subcategory_df['market_price'],
               text=subcategory_df['market_price']),
        go.Bar(name='Discount', x=subcategory_df['brand'], y=subcategory_df['discount'],
               text=subcategory_df['discount']),
    ])
    grp_chart.update_traces(texttemplate='%{text:.2s}', textposition='auto')
    grp_chart.update_layout(barmode='group', title='Market Price Vs Sale Price', template='plotly_dark',
                            xaxis_title="Category", yaxis_title="Price")
    dis_fig = px.bar(subcategory_df, x="brand", y='discount', title="Category Wise Discount",
                     template='plotly_dark', color='brand', text_auto='.2s')
    dis_pie = px.pie(subcategory_df, values='discount', names='brand', template='plotly_dark', hole=.3,
                     title='Category wise Discount In Percentage')
    return '{:.2f}'.format(sub_cat_df['category'].count()), '{:.2f} RS'.format(
        sub_cat_df['market_price'].sum()), '{:.2f} RS'.format(sub_cat_df['sale_price'].sum()), '{:.2f} RS'.format(
        sub_cat_df['market_price'].sum() - sub_cat_df[
            'sale_price'].sum()), dis_fig,dis_pie, grp_chart


def fnAboutMe():
    encoded_image = base64.b64encode(open('1657562494531.jpg', 'rb').read())
    return dbc.Row([dbc.Row(dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode("utf-8")),
                                             style={'height': '100%', 'width': '100%',
                                                    'border-radius': '30px 30px 30px 30px',
                                                    'box-shadow': 'rgb(38, 57, 77) 0px 20px 30px -10px'}),
                                    width=4), justify='center', className='my-2'),
                    dbc.Row(dbc.Col(html.H1('Sachin Halave', style={'text-align': 'center', 'color': 'white'})),
                            justify='center'),
                    dbc.Row(dbc.Col(dbc.NavLink("sdhalave6061@gmail.com", href="sdhalave6061@gmail.com",
                                                style={'text-align': 'center', 'color': '#000066', 'height': '20px'})),
                            justify='center'),
                    dbc.Row(dbc.Col(dbc.NavLink("https://www.linkedin.com/in/sachin-halave-6061",
                                                href='https://www.linkedin.com/in/sachin-halave-6061',
                                                style={'text-align': 'center', 'color': '#000066', 'height': '20px'})),
                            justify='center'),
                    dbc.Row(dbc.Col(dbc.NavLink("https://github.com/sachin6061", href='https://github.com/sachin6061',
                                                style={'text-align': 'center', 'color': '#000066', 'height': '20px'})),
                            justify='center'),
                    html.Hr(style={'color': 'white', 'margin': '10px'}),
                    dbc.Row(dbc.Col(html.H1('Python Developer', style={'text-align': 'center', 'color': '#800000'})))],
                   style={'height': '88vh'})


if __name__ == "__main__":
    app.run_server()
