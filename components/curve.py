from datetime import date
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_mantine_components as dmc

from dash import dcc, html 
import pandas as pd
import numpy as np
from datetime import timedelta



def get_missing_dates(dates, date, max_date): 
    i = 0
    dt_breaks = []
    while date < max_date:
        date+=timedelta(days=1)
        if date not in dates: 
            dt_breaks.append(date)
    return 


def historical_curve(df, x_label, y_label, title, ytitle, grouped='price_type', graph_type='Line', mode='lines+markers'):
    df.dropna(inplace=True) 
    df = df.sort_values(by=[x_label]).reset_index(drop=True)
    
    fig = make_subplots()
    hovertemplate = '%{y:,}'
    if 'Percentage' in graph_type: 
        hovertemplate = "%{y}% (%{customdata[0]:,})" 
    for cDate, color in zip(df[grouped].drop_duplicates(), ['#69C574', '#34829E']):
        serie_df = df[df[grouped] == cDate]
        serie_df = serie_df.sort_values(by=[x_label])
        serie_df[x_label] = serie_df[x_label].map(lambda x: x.strftime("%d-%b %H:%M"))
        # serie_df[x_label] = serie_df[x_label].map(lambda d: d.strftime('%d-%b-%y'))
        # serie_df.to_excel('serie_df.xlsx')
        if graph_type=='Line':
            fig.add_trace(go.Scatter(
                x=serie_df[x_label], 
                y=serie_df[y_label], 
                mode=mode,
                marker=dict(size=5),
                marker_color=color,
                name=cDate,
                line=dict(width=1.8), 
                line_shape='spline', 
                hovertemplate=hovertemplate
                ), row=1, col=1)

        else:
            fig.add_trace(go.Bar(
                x=serie_df[x_label], 
                y=serie_df[y_label], 
                marker_color=color,
                name=cDate, 
                customdata=serie_df.filter(['Total'], axis=1).values,
                hovertemplate=hovertemplate
                ), row=1, col=1)
     
    dt_breaks = get_missing_dates(
        df[x_label].drop_duplicates().tolist(), 
        df[x_label].min(),
        df[x_label].max()
    )

    # xtickformat='%d-%b-%y'
    fig.update_layout(
        # barmode='stack' if 'Stacked' in graph_type else None, 
        paper_bgcolor='#F7F9F9',
        plot_bgcolor='#F7F9F9',
        hovermode="x unified",
        margin=dict(t=10, b=50),
        hoverlabel=dict(bgcolor='white', font_size=14),
        # height=590,
        yaxis=dict(title=ytitle, gridcolor='#d6d4d4'),
        # rangebreaks=[dict(values=dt_breaks)],
        xaxis = dict(
            title=x_label,
            linecolor='#b3b3b3',
            type='category', 
            # tickformat=xtickformat, 
            # rangebreaks=[dict(values=dt_breaks)], 
            tickmode='linear'
        ),
        legend=dict(
            orientation="h",
            xanchor="center",
            yanchor="top",
            y=-0.2,
            x=0.5
        ), 
        font=dict(
            family="Helvetica",
            size=14,
            color="#555555"
        )
    )
    # tickmode='linear', 
    fig.update_xaxes(categoryorder='array', categoryarray= df[x_label].drop_duplicates().tolist())
    fig.update_traces(
        opacity=1
    )

    # title = dmc.Text(title, size='xl', weight=500, style={"color": '#7f7f7f', 'fontFamily': 'Open Sans'})
    title = html.H2(title, style={'fontFamily': 'Helvetica', 'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '1.5em'})
    graph = dcc.Graph(figure=fig, style={"height": 590})
    chart = dmc.Paper([
        dmc.Center([
            title
        ], style={"marginTop": '15px', "width": "100%"}), 
        graph
    ], pt='xl', pb='xl', shadow="xs", radius="xs", withBorder=True, class_name='card_custom_color')
    return chart