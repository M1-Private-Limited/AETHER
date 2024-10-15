import streamlit as st
import random
from streamlit_elements import nivo
from streamlit_elements import mui, html
from streamlit_elements import elements, mui, html, nivo
import numpy as np
import pandas as pd
import nivo_chart as nc
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go


def create_pie_chart(data, title):
    with mui.Typography:
        html.div(
            title,
            css={
                "display": "block",
                "margin-top": "1em",
                "margin-bottom": "1em",
                "margin-left": "1em",
                "margin-right": "0em",
                "font-weight": "bold"
            }
        )
    with mui.Box(sx={"height": 500}):
        nivo.Pie(
            data= data,
            margin={"top": 40, "right": 80, "bottom": 80, "left": 80},
            innerRadius=0.5,
            padAngle=0.7,
            cornerRadius=3,
            colors={"scheme": "nivo"},
            borderWidth=1,
            borderColor={"from": "color", "modifiers": [["darker", 0.2]]},
            radialLabelsSkipAngle=10,
            radialLabelsTextColor="#333333",
            radialLabelsLinkColor={"from": "color"},
            sliceLabelsSkipAngle=10,
            sliceLabelsTextColor="#333333",
            legends=[
                {
                    "anchor": "bottom",
                    "direction": "row",
                    "justify": False,
                    "translateX": 0,
                    "translateY": 56,
                    "itemsSpacing": 0,
                    "itemWidth": 100,
                    "itemHeight": 18,
                    "itemTextColor": "#999",
                    "itemDirection": "left-to-right",
                    "itemOpacity": 1,
                    "symbolSize": 18,
                    "symbolShape": "circle",
                    "effects": [
                        {
                            "on": "hover",
                            "style": {
                                "itemTextColor": "#000"
                            }
                        }
                    ]
                }
            ],
            motionConfig="wobbly",  # Adding motion configuration for smooth animations
            activeOuterRadiusOffset=8  # Slightly expand the pie slice on hover
        )


def create_pie_chart2(data, title):
    # Assuming data is a list of dictionaries with 'id' and 'value' keys
    df_pie = pd.DataFrame(data)
    
    # Create the pie chart
    fig = px.pie(
        df_pie,
        names='id',
        values='value',
        title=title,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hole=0.5  # Inner radius for the donut chart
    )
    
    # Customize the layout
    fig.update_layout(
        title={
            'text': title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24, 'color': 'black'}
        },
        legend={
            'orientation': 'h',
            'xanchor': 'center',
            'x': 0.5,
            'y': -0.1,
            'font': {'size': 12, 'color': '#999'}
        },
        margin=dict(t=40, b=80, l=80, r=80)
    )
    
    # Customize the pie chart
    fig.update_traces(
        textinfo='percent+label',
        textfont_size=14,
        marker=dict(
            line=dict(color='#000000', width=1)
        ),
        pull=[0.1 if i == 0 else 0 for i in range(len(df_pie))]  # Slightly expand the first slice
    )
    
    # # Display the figure in Streamlit
    #st.plotly_chart(fig)
    img_bytes = pio.to_image(fig, format='png', engine='kaleido')
    return img_bytes


def create_bar_chart(data, title):
    with mui.Typography:
        html.div(
            title,
            css={
                "display": "block",
                "margin-top": "1em",
                "margin-bottom": "1em",
                "margin-left": "1em",
                "margin-right": "0em",
                "font-weight": "bold"
            }
        )
    with mui.Box(sx={"height": 500}):
        nivo.Bar(
            data=data,
            keys=["value"],  # Adjust based on the structure of your data
            indexBy="id",  # Adjust based on your data labels
            margin={"top": 50, "right": 130, "bottom": 50, "left": 60},
            padding=0.3,
            valueScale={"type": "linear"},
            indexScale={"type": "band", "round": True},
            colors={"scheme": "nivo"},
            borderColor={"from": "color", "modifiers": [["darker", 1.6]]},
            axisTop=None,
            axisRight=None,
            axisBottom={
                "tickSize": 5,
                "tickPadding": 5,
                "tickRotation": 0,
                "legend": "Category",
                "legendPosition": "middle",
                "legendOffset": 32
            },
            axisLeft={
                "tickSize": 5,
                "tickPadding": 5,
                "tickRotation": 0,
                "legend": "Value",
                "legendPosition": "middle",
                "legendOffset": -40
            },
            labelSkipWidth=12,
            labelSkipHeight=12,
            labelTextColor={"from": "color", "modifiers": [["darker", 1.6]]},
            legends=[
                {
                    "dataFrom": "keys",
                    "anchor": "bottom-right",
                    "direction": "column",
                    "justify": False,
                    "translateX": 120,
                    "translateY": 0,
                    "itemsSpacing": 2,
                    "itemWidth": 100,
                    "itemHeight": 20,
                    "itemDirection": "left-to-right",
                    "itemOpacity": 0.85,
                    "symbolSize": 20,
                    "effects": [
                        {
                            "on": "hover",
                            "style": {
                                "itemOpacity": 1
                            }
                        }
                    ]
                }
            ],
            motionConfig="wobbly",  # Smooth animations
            role="application",  # Accessibility improvement
            ariaLabel="Bar chart representation"
        )

def create_bar_chart2(data, title):
    # Convert data to DataFrame
    df_bar = pd.DataFrame(data)

    # Create bar chart using Plotly Express
    fig = px.bar(
        df_bar, 
        x="id", 
        y="value", 
        title=title, 
        labels={"id": "Category", "value": "Value"},
        color="id",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Customize the chart
    fig.update_layout(
        margin=dict(l=60, r=130, t=50, b=50),
        xaxis_title="Category",
        yaxis_title="Value",
        legend_title="Category",
        height=500
    )

    # Display the chart in Streamlit
    #st.plotly_chart(fig)
    img_bytes = pio.to_image(fig, format='png', engine='kaleido')
    return img_bytes












def create_stacked_bar_chart(data, title):
    if len(data) == 0:
        st.write("NO Keys: ", keys)

        return  # If no data, don't attempt to plot

    # Extract keys dynamically, but ensure 'id' is excluded
    keys = list(data[0].keys())
    keys.remove("id")  # Assuming 'id' is for the x-axis


    with mui.Typography:
        html.div(
            title,
            css={
                "display": "block",
                "margin-top": "1em",
                "margin-bottom": "1em",
                "margin-left": "1em",
                "margin-right": "0em",
                "font-weight": "bold"
            }
        )

    with mui.Box(sx={"height": 500}):
        # Bar chart renderin
        nivo.Bar(
            data=data,
            keys=keys,  # Dynamically use the extracted keys for stacking
            indexBy="id",  # The primary index for the x-axis (e.g., categories)
            margin={"top": 50, "right": 130, "bottom": 50, "left": 60},
            padding=0.3,
            valueScale={"type": "linear"},
            indexScale={"type": "band", "round": True},
            colors={"scheme": "nivo"},
            borderColor={"from": "color", "modifiers": [["darker", 1.6]]},
            axisBottom={
                "tickSize": 5,
                "tickPadding": 5,
                "tickRotation": 0,
                "legend": "Category",
                "legendPosition": "middle",
                "legendOffset": 32
            },
            axisLeft={
                "tickSize": 5,
                "tickPadding": 5,
                "tickRotation": 0,
                "legend": "Value",
                "legendPosition": "middle",
                "legendOffset": -40
            },
            legends=[
                {
                    "dataFrom": "keys",
                    "anchor": "bottom-right",
                    "direction": "column",
                    "justify": False,
                    "translateX": 120,
                    "translateY": 0,
                    "itemsSpacing": 2,
                    "itemWidth": 100,
                    "itemHeight": 20,
                    "itemDirection": "left-to-right",
                    "itemOpacity": 0.85,
                    "symbolSize": 20,
                    "effects": [
                        {
                            "on": "hover",
                            "style": {
                                "itemOpacity": 1
                            }
                        }
                    ]
                }
            ],
            motionConfig="wobbly",  # Smooth animations
            role="application",
            ariaLabel="Stacked bar chart representation"
        )



def create_scatter_plot(data, title):
    with mui.Typography:
        html.div(
            title,
            css={
                "display": "block",
                "margin-top": "1em",
                "margin-bottom": "1em",
                "margin-left": "1em",
                "margin-right": "0em",
                "font-weight": "bold"
            }
        )

    with mui.Box(sx={"height": 500}):
        nivo.ScatterPlot(
            data=data,
            margin={"top": 40, "right": 80, "bottom": 80, "left": 80},
            xScale={"type": "linear"},
            yScale={"type": "linear"},
            colors={"scheme": "category10"},
            axisBottom={
                "orient": "bottom",
                "tickSize": 5,
                "tickPadding": 5,
                "tickRotation": 0,
                "legend": "x",
                "legendPosition": "middle",
                "legendOffset": 46
            },
            axisLeft={
                "orient": "left",
                "tickSize": 5,
                "tickPadding": 5,
                "tickRotation": 0,
                "legend": "y",
                "legendPosition": "middle",
                "legendOffset": -60
            },
            legends=[
                {
                    "anchor": "bottom-right",
                    "direction": "column",
                    "justify": False,
                    "translateX": 100,
                    "translateY": 0,
                    "itemWidth": 80,
                    "itemHeight": 20,
                    "itemTextColor": "#999",
                    "symbolSize": 12,
                    "symbolShape": "circle",
                    "effects": [
                        {
                            "on": "hover",
                            "style": {
                                "itemTextColor": "#000"
                            }
                        }
                    ]
                }
            ],
            motionConfig="gentle",
            activePointOpacity=1,
            inactivePointOpacity=0.7,
        )




def create_calendar_chart(data, title):
    # Convert 'day' column back to datetime to determine the range
    df = pd.DataFrame(data)
    df['day'] = pd.to_datetime(df['day'], format='%Y-%m-%d')

    # Find the earliest and latest date
    earliest_date = df['day'].min()
    latest_date = df['day'].max()

    # Calculate the first day of the month for the earliest date
    from_date = earliest_date.replace(day=1)

    # Calculate the last day of the month for the latest date
    to_date = latest_date + pd.offsets.MonthEnd(0)

    # Convert back to strings for the Nivo chart
    from_date_str = from_date.strftime('%Y-%m-%d')
    to_date_str = to_date.strftime('%Y-%m-%d')

    calendar_chart = {
        "layout": {
            "title": title,
            "type": "calendar",
            "height": 500,  # Increased height
            "width": 1000,  # Increased width
            "from": from_date_str,
            "to": to_date_str,
            "emptyColor": "#eeeeee",
            "colors": ["#61cdbb", "#97e3d5", "#e8c1a0", "#f47560"],
            # Adjusted margin to reduce space between title and calendar
            "margin": {"top": 1, "right": 10, "bottom": 10, "left": 10},
            "yearSpacing": 40,
            "monthBorderWidth": 1,  # Thin black border between months
            "monthBorderColor": "#000000",  # Black color for month border
            "dayBorderWidth": 2,
            "dayBorderColor": "#ffffff",
            "monthLegendOffset": 10,  # Offset for month labels
            "daySpacing": 5,  # Space between days
            "legends": [
                {
                    "anchor": "bottom",  # Changed position to the bottom
                    "direction": "row",
                    "translateY": 0,  # Move the legend down
                    "itemCount": 4,
                    "itemWidth": 100,  # Adjust width for better visibility
                    "itemHeight": 60,
                    "itemsSpacing": 14,
                    "itemDirection": "left-to-right",
                    "symbolSize": 20,  # Adjust symbol size for better visibility
                    "symbolShape": "circle",  # Circle shape for legend symbols
                }
            ],
        },
    }

    # Render the Nivo chart
    nc.nivo_chart(data=data, layout=calendar_chart["layout"])








def create_calendar_chart2(data, title):
    df_cal = pd.DataFrame(data, columns=['day', 'value'])
    df_cal['day'] = pd.to_datetime(df_cal['day'], format='%Y-%m-%d')
    
    df_cal['year'] = df_cal['day'].dt.year
    df_cal['month'] = df_cal['day'].dt.month
    df_cal['day_of_week'] = df_cal['day'].dt.dayofweek
    df_cal['week_of_year'] = df_cal['day'].dt.isocalendar().week
    
    # Create a complete range of dates for the heatmap
    min_date = df_cal['day'].min()
    max_date = df_cal['day'].max()
    all_dates = pd.date_range(start=min_date, end=max_date, freq='D')
    all_dates_df = pd.DataFrame(all_dates, columns=['day'])
    all_dates_df['year'] = all_dates_df['day'].dt.year
    all_dates_df['month'] = all_dates_df['day'].dt.month
    all_dates_df['day_of_week'] = all_dates_df['day'].dt.dayofweek
    all_dates_df['week_of_year'] = all_dates_df['day'].dt.isocalendar().week

    # Merge the data with the complete date range
    merged_df = pd.merge(all_dates_df, df_cal, on='day', how='left')
    merged_df['value'] = merged_df['value'].fillna(0)  # Fill NaN values with 0

    # Drop duplicate columns
    merged_df = merged_df.drop(columns=['year_y', 'month_y', 'day_of_week_y', 'week_of_year_y'])
    merged_df = merged_df.rename(columns={'year_x': 'year', 'month_x': 'month', 'day_of_week_x': 'day_of_week', 'week_of_year_x': 'week_of_year'})
    
    # Create a pivot table for the heatmap
    pivot_df = merged_df.pivot_table(index='day_of_week', columns='week_of_year', values='value', fill_value=0)
    
    # Define the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        colorscale='Viridis'
    ))

    # Update the layout for better aesthetics
    fig.update_layout(
        title=title,
        xaxis_nticks=52,
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 2, 3, 4, 5, 6],
            ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        ),
        height=600,
        width=1000,
        margin=dict(t=50, r=50, b=50, l=50),
        plot_bgcolor='white'
    )

    fig.update_xaxes(title_text='Week of Year')
    fig.update_yaxes(title_text='Day of Week')

    #st.plotly_chart(fig)    
    img_bytes = pio.to_image(fig, format='png', engine='kaleido')
    return img_bytes