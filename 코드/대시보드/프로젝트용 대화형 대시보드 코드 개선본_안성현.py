from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import seaborn as sns # 시각화
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots

#쇼핑 데이터
df_online = pd.read_csv("online_store_customer_data.csv", index_col=0)
df_online = df_online.dropna(axis=0)

# 주식 데이터
df_stock = pd.read_csv("faang_stocks_pandemic_data.csv", index_col=0)
df_stock = df_stock.dropna(axis=0)

# 스타일
app = Dash(external_stylesheets=[dbc.themes.MORPH])

# HTML 레이아웃 구성
app.layout = html.Div(
    [
        html.H1(children="Interactive DashBoard Analytics", className="header_title", style = {'padding-left' : '10px'}),
        html.Nav([], className = "navbar"),
        dcc.Tabs([
            # 첫번째 탭
            dcc.Tab(label = "Online Shopping", children = [
                # 조건 선택지
                html.Br(),
                html.H4("Group Category", style = {'padding-left' : '10px'}),
                dcc.Dropdown(id='Category_online',
                    options=['Gender', 'Segment', 'Marital_status', 'Employees_status'],
                    value='Gender', clearable=False, style = {'width' : '400px', 'padding-left' : '10px'}
                ),
                html.Div([
                    html.Div([
                        # 파이 그래프
                        html.Br(),
                        html.H5("Pie Graph of Online Shopping", style = {'padding-left' : '10px'}),
                        dcc.Graph(id='pie_graph')
                        ], className = 'first-tap-one'),
                    html.Div([
                        # 바 그래프
                        html.Br(),
                        html.H5("Bar Graph of Online Shopping", style = {'padding-left' : '10px'}),
                        dcc.Graph(id='bar_graph_sum')
                        ], className = 'first-tap-two'),
                    html.Div([
                        # 바 그래프
                        html.Br(),
                        html.H5("Bar Graph of Online Shopping", style = {'padding-left' : '10px'}),
                        dcc.Graph(id='bar_graph_mean')
                        ], className = 'first-tap-three')
                    ], className = 'wrapper2')
            ]),
            # 두번째 탭
            dcc.Tab(label = "Stock Data", children = [
                html.Div([
                    html.Div([
                        # 조건 선택지1 = 회사
                        html.Br(),
                        html.H4("Company Category", style = {'padding-left' : '10px'}),
                        dcc.Dropdown(id='Category_stock_company',
                            options=['Facebook', 'Apple', 'Netflix', 'Google', 'Amazon'],
                            value='Facebook', clearable=False, style = {'width' : '400px', 'padding-left' : '10px'}
                        )
                        ], className = 'first-tap-one'),
                    html.Div([
                        # 조건 선택지2 = 시작가, 종가, 최고가, 최저가, 거래량
                        html.Br(),
                        html.H4("Stock Type", style = {'padding-left' : '10px'}),
                        dcc.Dropdown(id='Category_stock_price',
                            options=['Open', 'Close', 'High', 'Low', 'Volume'],
                            value='Close', clearable=False, style = {'width' : '400px', 'padding-left' : '10px'}
                        )
                        ], className = 'first-tap-two')
                    ], className = 'wrapper'),
                html.Div([
                    html.Div([
                        # 꺾은 선 그래프
                        html.Br(),
                        html.H5("Line Graph of Stock", style = {'padding-left' : '10px'}),
                        dcc.Graph(id='line_graph')
                        ], className = 'first-tap-one'),
                    html.Div([
                        # 캔들 차트
                        html.Br(),
                        html.H5("Candle Chart of Stock", style = {'padding-left' : '10px'}),
                        dcc.Graph(id='candle_chart')
                        ], className = 'first-tap-two')
                    ], className = 'wrapper')
            ])
        ])
    ])
# 온라인 쇼핑 파이 차트 콜백
@app.callback(
    Output("pie_graph", "figure"),
    Input("Category_online", "value"))
# 파이 차트 생성
def generate_pie_chart(Category_online):
    # 조건으로 그룹핑
    df_online_processed = df_online.groupby(Category_online).sum().reset_index()
    fig = px.pie(df_online_processed, values='Amount_spent', names=Category_online, hole=.3, color_discrete_sequence=px.colors.sequential.Magenta)
    fig.update_layout(autosize=True, paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)')
    return fig

# 온라인 쇼핑 그룹별 총액 막대 그래프 콜백
@app.callback(
    Output("bar_graph_sum", "figure"),
    Input("Category_online", "value"))
# 막대 그래프 생성
def generate_bar_plot(Category_online):
    layout = go.Layout(title={'text':'Total Amount_Spent',
                                'font':{'size':16}}, # Title 설정
                        font = {'color':'#22194D'} # 전체 글자(폰트) 색상
                        ,paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                        )
    
    # 조건으로 그룹핑 후 총 소비액
    df_online_processed = df_online.groupby(Category_online).sum().reset_index()
    colors = sns.color_palette('Pastel2', len(df_online_processed[Category_online])).as_hex()
    # x축 연도, y축 인구수, Bar 클래스 생성
    data = go.Bar(x=df_online_processed[Category_online], y=df_online_processed['Amount_spent'], 
                marker = {'color':colors,# 막대 색상 또는 리스트를 이용하여 각 막대 색상 변경가능
                            'line':{'color':'black', 'width':2}, # 막대 테두리 설정
                            'pattern':{'shape':'/'}, # 사선 패턴
                        },
                width=0.5, # 막대 폭
                )
    # 막대 그래프(Bar Chart, 바 차트)를 포함하는
    # Figure 생성
    fig = go.Figure(data=data, layout=layout) 
    fig.update_layout(autosize=True)
    return fig

# 온라인 쇼핑 1인당 평균 소비액 막대 그래프 콜백
@app.callback(
    Output("bar_graph_mean", "figure"),
    Input("Category_online", "value"))
# 막대 그래프 생성
def generate_bar_plot(Category_online):
    layout = go.Layout(title={'text':'Mean Amount_Spent',
                                'font':{'size':16}}, # Title 설정
                        font = {'color':'#22194D'} # 전체 글자(폰트) 색상
                        ,paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                        )
    
    # 성별로 그룹핑 후 평균 소비액 시각화
    df_online_processed = df_online.groupby(Category_online).mean().reset_index()
    colors = sns.color_palette('Pastel2', len(df_online_processed[Category_online])).as_hex()
    # x축 연도, y축 인구수, Bar 클래스 생성
    data = go.Bar(x=df_online_processed[Category_online], y=df_online_processed['Amount_spent'], 
            marker = {'color':colors,# 막대 색상 또는 리스트를 이용하여 각 막대 색상 변경가능
                        'line':{'color':'black', 'width':2}, # 막대 테두리 설정
                        'pattern':{'shape':'/'}, # 사선 패턴
                    },
            width=0.5, # 막대 폭
            ) 
    fig = go.Figure(data=data, layout=layout) 
    fig.update_layout(autosize=True)
    return fig

# 주식 데이터 라인 그래프
@app.callback(
    Output("line_graph", "figure"),
    Input("Category_stock_company", "value"),
    Input("Category_stock_price", "value"))
# 라인 그래프 생성
def generate_pie_chart(Category_stock_company, Category_stock_price):
    fig = px.line(df_stock[df_stock['Name']==Category_stock_company], x=df_stock[df_stock['Name']==Category_stock_company].Date, y=Category_stock_price, title=Category_stock_price+' Price of Stock')
    fig.update_layout(autosize=True, paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)')
    return fig

# 주식 데이터 캔들 차트
@app.callback(
    Output("candle_chart", "figure"),
    Input("Category_stock_company", "value"),
    Input("Category_stock_price", "value"))
# 캔들 차트 생성
def generate_pie_chart(Category_stock_company, Category_stock_price):
    candle = go.Candlestick(
        x=df_stock[df_stock['Name']==Category_stock_company].Date,
        open=df_stock[df_stock['Name']==Category_stock_company]['Open'],
        high=df_stock[df_stock['Name']==Category_stock_company]['High'],
        low=df_stock[df_stock['Name']==Category_stock_company]['Low'],
        close=df_stock[df_stock['Name']==Category_stock_company]['Close'],
        increasing_line_color='red', # 상승봉
        decreasing_line_color='blue' # 하락봉
    )
    fig = go.Figure(data=candle)
    fig.update_layout(autosize=True, paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)')
    return fig

# 서버 실행
app.run_server(debug=True)