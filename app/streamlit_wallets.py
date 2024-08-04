import streamlit as st
import requests
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime, timedelta

FASTAPI_URL = 'http://127.0.0.1:8000'
wallet_endpoints = {

    "ViennaLife": "/vienna/get_all_vienna",
    "Nokia": "/nokia/get_all_nokia",
    "Generali": "/generali/get_all_generali",
    "Revolut": "/revolut/get_all_revolut",
    "Etoro": "/transactions/get_all_etoro",
    "Obligacje": "/obligacje/get_all_obligacje",
    "XTB" : "/xtb/get_all_xtb"

}

date_wallet_endpoints = {

    "ViennaLife": "/vienna/get_all_dates"

}

add_transaction_endpoints = {
    "ViennaLife": "/vienna/add_vienna_transaction",
    "Nokia": "/nokia/add_nokia_transaction",
    "Generali": "/generali/add_generali_transaction",
    "Revolut": "/revolut/add_revolut_transaction",
    "Etoro": "/transactions/add_etoro_transaction",
    "Obligacje": "/obligacje/add_obligacje_transaction",
    "XTB" : "/xtb/add_xtb_transaction"
}

def get_wallet_dates(tab):

    endpoint = date_wallet_endpoints[tab]
    response = requests.get(f"{FASTAPI_URL}{endpoint}")

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return []
    

def fetch_wallet_totals(tab):

    endpoint = wallet_endpoints[tab]

    response = requests.get(f"{FASTAPI_URL}{endpoint}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return []
    
def add_transcation(tab, data):

    print(f'DEBUG: add_transaction endpoint function called')
    endpoint = add_transaction_endpoints[tab]
    url = f"{FASTAPI_URL}{endpoint}"

    payload = {
        "date": data.get('date'),
        "initial_amount": data.get('initial_amount'),
        "deposit_amount": data.get('deposit_amount'),
        "total_amount": data.get('total_amount')
    }

    print(f'ADD_TRANSACTION: Following data will be send: {payload}')

    response = requests.post(url=url, json=payload)

    if response.status_code == 201:
        return response.json()
    else:
        st.error(f"Failed to process POST request: {response.status_code}")
        return []


def generate_wallet_chart_2nd_with_legend(wallet_data):

    df = pd.DataFrame(wallet_data)

     # Debug: Print DataFrame columns and first few rows
    print("Columns in DataFrame:", df.columns)
    print("First few rows of the DataFrame:\n", df.head())

    # Check if the necessary columns exist
    if 'total_amount' not in df.columns or 'deposit_amount' not in df.columns:
        st.error("DataFrame must contain 'total_amount' and 'deposit_amount' columns.")
        return

    # Calculate profit as a separate column
    df['profit'] = df['total_amount'] - df['deposit_amount']

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['date'], 
        y=df['deposit_amount'], 
        name='Deposit Amount',
        marker=dict(color='lightblue')
    ))

    fig.add_trace(go.Bar(
        x=df['date'], 
        y=df['profit'], 
        name='Profit',
        marker=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=df['date'], 
        y=df['total_amount'], 
        mode='lines+markers', 
        name='Total Amount Trend',
        line=dict(color='red', width=2),
        marker=dict(size=6)
    ))

    fig.update_layout(
        barmode='stack',
        xaxis_title='Date',
        yaxis_title='Value',
        title='ViennaLife',
        xaxis=dict(
            tickformat="%Y-%m-%d",
            tickmode="array",
            tickvals=df['date'].tolist(),
        )
    )

    # Show the figure
    st.plotly_chart(fig)

    
def generate_wallet_chart(df, time_delta):

    
    fig = px.bar(df, x='date', y='total_amount',
                 labels={'total_amount': 'Value'}
                 )
    # Adjust bar width and other properties if necessary
    fig.update_traces(marker_line_width=0.3)



    # Ensure tickvals receives a list of values, not being mistakenly indexed
    fig.update_xaxes(
        tickformat="%Y-%m-%d",  
        tickmode="array",
        # tickvals=time_delta,
        # rangebreaks=[
        #     dict(values=time_delta)
        # ]
    )

    
    st.plotly_chart(fig)


def get_time_delta(tab):

    dates = get_wallet_dates(tab)
    dates_list = []
    
    for date in dates:
        for k,v in date.items():
            dates_list.append(v)
    dates_list.sort()
    
    date_objects = [datetime.strptime(date, '%Y-%m-%d') for date in dates_list]

    all_dates = []

    for i in range(len(date_objects) -1):
        start_date = date_objects[i]
        end_date = date_objects[i+1]

        current_date = start_date + timedelta(days=1)

        while current_date < end_date:
            all_dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)

    
    return all_dates

 
    


