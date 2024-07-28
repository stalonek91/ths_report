import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from csv_handler import CSVHandler
from io import StringIO

FASTAPI_URL = 'http://127.0.0.1:8000'

def fetch_portfolio_summary():
    response = requests.get(f"{FASTAPI_URL}/portfolio/get_all_portfolio")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return []
    
def get_portfolio_perc():
    response = requests.get(f"{FASTAPI_URL}/portfolio/calculate_perc/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch response data: {response.status_code}")
        return []
    
def add_csv_to_db(file):

    files = {"file": (file.name, file, "text/csv")}
    response = requests.post(f"{FASTAPI_URL}/transactions/add_csv", files=files)
    if response.status_code == 201:
        return response.json()
    else:
        st.error(f"Failed to process the POST request: {response.status_code}")
        return []

def main():

    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", ['Summary', "Transactions", "Pornosy",], index=0)


    if selection == 'Summary':
 

        st.title("Portfolio :blue[Summary] 🤫🤫🤫🤫🤫🤫")

        portfolio_summary = fetch_portfolio_summary()
        portfolio_percentage = get_portfolio_perc()

        if portfolio_summary:
            df = pd.DataFrame(portfolio_summary)
            st.dataframe(df)
        else:
            st.warning("No data to display")


        

        if portfolio_percentage:
            fig, ax = plt.subplots(figsize=(6,3), subplot_kw=dict(aspect="equal"))
            df_perc = pd.DataFrame(portfolio_percentage)
            st.write(df_perc)

            fig, ax = plt.subplots()
            ax.pie(df_perc['Percentage'], labels=df_perc['Wallet'], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)

            options = st.selectbox(
            "Show wallet details",
            df_perc,
            index=None,
            placeholder="Select Your wallet",
            )
            st.write("You selected:", options)


        dataframe = pd.DataFrame(
            np.random.randn(10, 20),
            columns=('col %d' % i for i in range(20)))
        st.dataframe(dataframe.style.highlight_max(axis=0))

        chart_data = pd.DataFrame(
            np.random.rand(20,3),
            columns=['a', 'b', 'c'])
        
        st.line_chart(chart_data)

        latitude = 50.63678
        longitude = 17.82635
        
        magia = pd.DataFrame(
            {
                'lat': [latitude],
                'lon': [longitude]
            }
        )
            
        
        st.map(latitude=50.63678, longitude=17.82635, data=magia)


        @st.cache_data
        def gen_random():
            return np.random.randn(10, 20)
        
        df_table = pd.DataFrame(
            
            gen_random(),
            columns = ('Column %d' % i for i in range (20))
        )
        st.table(df_table)

        x = st.slider('x')
        st.write(x, 'squared is', x * x)

        if st.checkbox('Show dataframe'):
            chart_data = pd.DataFrame(
                np.random.randn(5,4),
                columns= ('Col to: %d' % i for i in range (4))
            )

            chart_data

    elif selection == "Pornosy":

        tab1, tab2, tab3 = st.tabs(["Lorem Ipsum xd", "Wazne", "Sojka Sylwester Portfolio Project CV"])

        with tab1:
            st.title("Jan Router 3")
            st.image('/Users/sylwestersojka/Documents/HomeBudget/app/papaj3.png')

        with tab2:
            st.title('Powazna Strona.')

            if 'trigger_sleep' not in st.session_state:
                st.session_state['trigger_sleep'] = False

            if st.button("Don't click"):
                st.session_state['trigger_sleep'] = True

            if st.session_state['trigger_sleep']:
                with st.spinner('Warto czekac ...'):
                    time.sleep(5)
                
                st.success('Jednak nie warto 😅 Ale nastepna juz na powaznie serio.')
                st.image('/Users/sylwestersojka/Documents/HomeBudget/app/papaj2.png')

        with tab3:
            st.warning('You have been pranked!!!',icon="⚠️")
            st.image('/Users/sylwestersojka/Documents/HomeBudget/app/prenk.png')

    elif selection == "Transactions": 
        st.title('Load CSV to DB')
        print(f'1/2::: trying to upload a file')
        uploaded_file = st.file_uploader("Choose CSV file", type="csv")
        print(f'2/2::: Code after file uploading')
        

        if uploaded_file is not None:
            response = add_csv_to_db(uploaded_file)
            st.success(response)
        else:
            st.info("Please upload a CSV file")




        


if __name__ == "__main__":
    main()