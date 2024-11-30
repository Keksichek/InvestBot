import dash
from dash import dcc, html, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px

# Создаем примерные данные
np.random.seed(42)
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="M")
strategies = ["Краткосрочная", "Среднесрочная", "Долгосрочная", "Высокодоходная долгосрочная"]

data = pd.DataFrame({
    "Дата": np.tile(dates, len(strategies)),
    "Стратегия": np.repeat(strategies, len(dates)),
    "Доходность (%)": np.random.uniform(-5, 15, len(dates) * len(strategies)),
    "Инвестиции (тыс. руб.)": np.random.uniform(100, 1000, len(dates) * len(strategies)),
    "Распределение (%)": np.random.uniform(10, 40, len(dates) * len(strategies))
})

# Группируем данные для отображения в таблице
summary = data.groupby("Стратегия").agg({
    "Доходность (%)": "mean",
    "Инвестиции (тыс. руб.)": "sum",
    "Распределение (%)": "mean"
}).reset_index()

# Инициализация приложения Dash
app = dash.Dash(__name__)

# Стили
app.layout = html.Div([
    html.Div([
        html.H1("Дашборд управления инвестициями", style={"textAlign": "center", "color": "#2C3E50", "marginBottom": "30px"}),

        # Поле для ввода текста
        html.Div([
            html.Label("Введите ваше имя:", style={"fontSize": "16px", "color": "#34495E"}),
            dcc.Input(id="user-name", type="text", placeholder="Ваше имя", style={"width": "50%", "marginBottom": "20px", "padding": "5px"})
        ]),

        # Dropdown для выбора стратегии
        html.Div([
            html.Label("Выберите стратегию:", style={"fontSize": "16px", "color": "#34495E"}),
            dcc.Dropdown(
                id="strategy-dropdown",
                options=[{"label": s, "value": s} for s in strategies],
                value="Краткосрочная",
                style={"width": "50%", "marginBottom": "20px", "padding": "5px"}
            )
        ]),

        # Чеклист для выбора нескольких стратегий
        html.Div([
            html.Label("Сравните стратегии:", style={"fontSize": "16px", "color": "#34495E"}),
            dcc.Checklist(
                id="strategy-checklist",
                options=[{"label": s, "value": s} for s in strategies],
                value=[strategies[0]],
                inline=True,
                style={"marginBottom": "20px"}
            )
        ]),

        # DatePickerRange для выбора диапазона дат
        html.Div([
            html.Label("Выберите период:", style={"fontSize": "16px", "color": "#34495E"}),
            dcc.DatePickerRange(
                id="date-picker",
                start_date=dates.min(),
                end_date=dates.max(),
                display_format="YYYY-MM-DD",
                style={"marginBottom": "20px"}
            )
        ]),

        # Слайдер для выбора диапазона инвестиций
        html.Div([
            html.Label("Диапазон инвестиций (тыс. руб.):", style={"fontSize": "16px", "color": "#34495E"}),
            dcc.RangeSlider(
                id="investment-slider",
                min=100, max=1000, step=50,
                marks={i: f"{i}" for i in range(100, 1001, 200)},
                value=[300, 700],
                tooltip={"placement": "bottom"}
            )
        ], style={"marginBottom": "20px"}),

        # График доходности
        html.Div([
            dcc.Graph(id="performance-graph", config={"displayModeBar": False}),
        ], style={"marginBottom": "30px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)", "borderRadius": "10px", "padding": "20px", "backgroundColor": "#F9F9F9"}),

        # Таблица данных
        html.Div([
            html.Label("Детальная информация:", style={"fontSize": "16px", "color": "#34495E"}),
            html.Div(id="data-table", style={"overflowX": "auto", "marginBottom": "20px", "padding": "10px", "backgroundColor": "#FDFDFD", "border": "1px solid #E0E0E0", "borderRadius": "10px"})
        ]),

        # Круговая диаграмма распределения портфеля
        html.Div([
            dcc.Graph(id="pie-chart", config={"displayModeBar": False})
        ], style={"boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)", "borderRadius": "10px", "padding": "20px", "backgroundColor": "#F9F9F9"})
    ], style={"width": "80%", "margin": "auto", "backgroundColor": "#FFFFFF", "padding": "30px", "borderRadius": "15px", "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)"})
], style={"backgroundColor": "#ECF0F1", "padding": "30px"})


# Callbacks для интерактивности

@app.callback(
    Output("performance-graph", "figure"),
    [Input("strategy-dropdown", "value"),
     Input("date-picker", "start_date"),
     Input("date-picker", "end_date"),
     Input("investment-slider", "value")]
)
def update_performance_graph(selected_strategy, start_date, end_date, investment_range):
    filtered_data = data[(data["Стратегия"] == selected_strategy) &
                         (data["Дата"] >= start_date) &
                         (data["Дата"] <= end_date) &
                         (data["Инвестиции (тыс. руб.)"] >= investment_range[0]) &
                         (data["Инвестиции (тыс. руб.)"] <= investment_range[1])]
    fig = px.line(
        filtered_data,
        x="Дата",
        y="Доходность (%)",
        title=f"Доходность стратегии: {selected_strategy}",
        labels={"Дата": "Дата", "Доходность (%)": "Доходность (%)"},
        template="plotly_white"
    )
    fig.update_layout(title_font_size=20, title_x=0.5)
    return fig


@app.callback(
    Output("data-table", "children"),
    [Input("strategy-checklist", "value")]
)
def update_table(selected_strategies):
    filtered_summary = summary[summary["Стратегия"].isin(selected_strategies)]
    table = html.Table([
        html.Thead(html.Tr([html.Th(col, style={"border": "1px solid #E0E0E0", "padding": "10px", "backgroundColor": "#EAF2F8"}) for col in filtered_summary.columns])),
        html.Tbody([
            html.Tr([html.Td(filtered_summary.iloc[i][col], style={"border": "1px solid #E0E0E0", "padding": "10px"}) for col in filtered_summary.columns])
            for i in range(len(filtered_summary))
        ])
    ], style={"width": "100%", "borderCollapse": "collapse"})
    return table


@app.callback(
    Output("pie-chart", "figure"),
    [Input("strategy-dropdown", "value")]
)
def update_pie_chart(selected_strategy):
    filtered_data = data[data["Стратегия"] == selected_strategy]
    fig = px.pie(
        filtered_data,
        values="Распределение (%)",
        names="Дата",
        title=f"Распределение портфеля: {selected_strategy}",
        template="plotly_white"
    )
    fig.update_layout(title_font_size=20, title_x=0.5)
    return fig


# Запуск приложения
if __name__ == "__main__":
    app.run_server(debug=True)
