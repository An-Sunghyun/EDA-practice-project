from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# 
app = Dash(__name__)
# HTML 레이아웃 구성
app.layout = html.Div([
    html.Div(),html.Div(),
    html.H4('Analysis of the restaurant sales'),
    dcc.Graph(id="graph"),
    html.P("Names"),
    dcc.Dropdown(id='names',
        options=['smoker', 'day', 'time', 'sex'],
        value='day', clearable=False
    ),
    html.P("Values"),
    dcc.Dropdown(id='values',
        options=['total_bill', 'tip', 'size'],
        value='total_bill', clearable=False
    ),
])

# 콜백 조건부 설정
@app.callback(
    Output("graph", "figure"), 
    Input("names", "value"), 
    Input("values", "value"))
# 그래프 생성
def generate_chart(names, values):
    df = px.data.tips() # replace with your own data source
    fig = px.pie(df, values=values, names=names, hole=.3)
    return fig

# 서버 실행
app.run_server(debug=True)