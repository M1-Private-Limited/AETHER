import openai 
from openai import AzureOpenAI
import streamlit as st
from streamlit_elements import dashboard
from streamlit_elements import elements, mui, html, nivo
import requests
import streamlit as st
from base64 import b64encode
import ploty 
from pandas.errors import ParserError
from streamlit_chat import message
import streamlit_toggle as tog
import pandas as pd
import json
import duckdb
import re
import os
import ast
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import json
import numpy as np
import re
import time
import warnings
import streamlit_shadcn_ui as ui
from local_components import card_container
from streamlit_shadcn_ui import slider, input, textarea, radio_group, switch
from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import plotly.express as px
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, PageBreak, Table, XPreformatted, KeepInFrame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import markdown
import io
import tableauserverclient as TSC
from st_on_hover_tabs import on_hover_tabs
import streamlit.components.v1 as components
from serpapi import GoogleSearch
from dotenv import load_dotenv
load_dotenv()



client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_KEY"),  
  api_version="YYYY-MM-DD"
)


#Page config
st.set_page_config(page_title="Data GPT",  layout="wide", page_icon="m1logo.png", initial_sidebar_state="expanded")
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


#Session states
if 'form_1' not in st.session_state:
    st.session_state['form_1'] = []  
if 'form_submissions' not in st.session_state:
    st.session_state['form_submissions'] = []
if 'final_df' not in st.session_state:
    st.session_state.final_df = pd.DataFrame()  
if 'chart_images' not in st.session_state:
    st.session_state['chart_images'] = []
if 'suggest_list' not in st.session_state:
    st.session_state['suggest_list'] = []
if 'qns_list' not in st.session_state:
    st.session_state['qns_list'] = []
if 'radio_value' not in st.session_state:
    st.session_state['radio_value'] = 'SAMPLE_CSV'
if 'video_played' not in st.session_state:
    st.session_state['video_played'] = False    
if 'first_qns' not in st.session_state:
    st.session_state['first_qns'] = True  
if 'response_content' not in st.session_state:
    st.session_state['response_content'] = ''  
if 'segments' not in st.session_state:
    st.session_state['segments'] = {}
if 'df_dictionary' not in st.session_state:
    st.session_state.df_dictionary = pd.DataFrame()  


 
with open('assets/loading.json', encoding='utf-8', errors='ignore') as f:
    loading = json.loads(f.read(),strict=False)   


#Define functions
def stream_data(query):
    for word in query.split(" "):
        yield word + " "
        time.sleep(0.02)

def extract_unique_values(df, column_list):
    result = []
    for col in column_list:
        if col in df.columns:
            unique_values = df[col].dropna().unique()[:10]
            unique_values_str = ",".join(map(str, unique_values))
            result.append(f"Column {col} has these unique values: {unique_values_str}")
    return "\n".join(result)
def excel_date_to_datetime(excel_date):
    return pd.to_datetime('1899-12-30') + pd.to_timedelta(excel_date, 'D')

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css("style.css")

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        df = pd.read_csv('assets/testingcsv.csv')
        st.session_state.final_df = df
        return df
    df = df.copy()
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]

            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min().date(),
                        df[column].max().date(),
                    ),
                    format="YYYY-MM-DD"
                )
                if len(user_date_input) == 2:
                    start_date, end_date = pd.to_datetime(user_date_input)
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input, na=False)]
    st.session_state.final_df = df
    return df

def safe_to_datetime(date_str):
    try:
        return pd.to_datetime(date_str, format='%d/%m/%Y')
    except ValueError as e1:
        try:
            return pd.to_datetime(date_str, origin='1899-12-30', unit='D')
        except ValueError as e2:
            print(f"Failed to parse date: {date_str}")
            return pd.NaT  
            
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    
    data['start_date'] = data['start_date'].apply(safe_to_datetime)
    
    return data

#load sample data
data = load_data('assets/testingcsv.csv')
data_sample = data.head(10).to_string()

#load particle effects
with open("assets/particles.html", "r") as f:
    html_code = f.read()
components.html(html_code)


@st.dialog("Intro Video")
def first(item):
    st.video('assets/second_draft.mp4')
if not st.session_state['video_played']:
    first("A")
    st.session_state['video_played'] = True


with st.container(border=True):
    st.markdown(

        """

        <style>

        .left-align {

            display: block;

            margin-left: 0;

            margin-right: auto;

            margin-bottom: 10px; /* Reduce bottom margin */

        }

        </style>

        <img src='https://github.com/ONGQ0019/filedumps/blob/main/aether5.png?raw=true' width='400' class='left-align'>

        """,

        unsafe_allow_html=True

    )

    with st.sidebar:

            st.image('assets/m1logo.png')
            tabs = on_hover_tabs(tabName=['Datasource', 'Dashboard', 'Chat'], 
                                iconName=['storage', 'dashboard', 'chat'],
                                styles = {'navtab': {'background-color':'#111',
                                                    'color': '#818181',
                                                    'font-size': '18px',
                                                    'transition': '.3s',
                                                    'white-space': 'nowrap',
                                                    'text-transform': 'uppercase'},
                                        'tabStyle': {':hover :hover': {'color': 'red',
                                                                        'cursor': 'pointer'}},
                                        'tabStyle' : {'list-style-type': 'none',
                                                        'margin-bottom': '30px',
                                                        'padding-left': '30px'},
                                        'iconStyle':{'position':'fixed',
                                                        'left':'7.5px',
                                                        'text-align': 'left'},
                                        },
                                key="1")


    if tabs == 'Datasource':
        with card_container(key="tab1"):
        #example connection to tableau
        # token_name = 'testing1'
        # personal_access_token = 'xxxxxx'
        # site_id = ''  # leave blank for default site
        # server_address = 'https://tabl0test'

        # # Create a tableau auth object
        # tableau_auth = TSC.PersonalAccessTokenAuth(token_name=token_name,
        #                                             personal_access_token=personal_access_token, 
        #                                             site_id=site_id)


        # server = TSC.Server(server_address)
        # server.version = '3.3'
        # server.add_http_options({'verify': False})
        # project_name = "Transformation - KPI Performance"
        # project_id = None

        # with server.auth.sign_in(tableau_auth):
        #     all_projects, pagination_item = server.projects.get()
        #     for project in all_projects:
        #         if project.name == project_name:
        #             project_id = project.id
        #             break

        # if project_id is None:
        #     raise ValueError(f"Project '{project_name}' not found.")

        # # Retrieve all datasources and manually filter by project ID
        # with server.auth.sign_in(tableau_auth):
        #     all_datasources, pagination_item = server.datasources.get()
        #     filtered_datasources = [ds for ds in all_datasources if ds.project_id == project_id]
        #     st.write(filtered_datasources)
        #     for datasource in filtered_datasources:
        #         st.write(f"Datasource name: {datasource.name}")
            st.subheader('Select Datasource')

        ### example datasource and dataset, you can connect to your own datasources
            datasources = [
                "REVENUE_AGGR",
                "SUBBASE_AGGR",
                "USAGE_AGGR",
                "VAS_ORDERS_AGGR",
                "VAS_SUBBASE_AGGR",
                "New vs Legacy"
            ]
            datasources1 = [
                "COMBI_SUBSCR",
                "COMBI_VAS",
                "COMBI_ORDER_DETAIL",
                "COMBI_CUST"
            ]      
            datasources2 = [
                "DS_PROFILE",
                "CHURN_MODELING",
                "SAMPLE_CSV"
            ]

            uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                st.write("Filename:", uploaded_file.name)
                st.dataframe(df)


            option = st.selectbox(
                "Which Datasource to connect?",
                ("Tableau", "Snowflake", "Databricks"),
            )


            with card_container(key="ta1"):
                st.write(f'{option} Datasources:')
                if option =='Tableau':
                    radio_options = [{"label": each, "value": each} for each in datasources]
                    radio_value = ui.radio_group(options=radio_options,  default_value="SUBBASE_AGGR" ,key="radio1")
                if option =='Snowflake':
                    radio_options = [{"label": each, "value": each} for each in datasources1]
                    radio_value = ui.radio_group(options=radio_options,  default_value="SUBBASE_AGGR" , key="radio2")
                if option =='Databricks':
                    radio_options = [{"label": each, "value": each} for each in datasources2]
                    radio_value = ui.radio_group(options=radio_options, default_value="SUBBASE_AGGR" , key="radio3")
                ui.badges(badge_list=[(f"Selected Datasource: {radio_value}", "default")], class_name="flex gap-2", key="main_badges3")
            st.session_state['radio_value'] = radio_value


    if tabs == 'Dashboard':
        tabby  = ui.tabs(options=['View Data', 'View Dictionary', 'View Analytics', 'Create Segments', 'Create Charts','Generate Report'], default_value='View Data', key="main_tabs")

        if tabby == 'View Data':
            rv = st.session_state['radio_value']
            with card_container(key="table1"):
                st.subheader(f'Editable Dataframe: {rv}')

                st.dataframe(filter_dataframe(data))


        if tabby == 'View Dictionary':
            with card_container(key="table2"):
                if len(st.session_state.final_df.head(5)) > 3:
                    df = st.session_state.final_df
                else:
                    df = data
                st.subheader('Dictionary Library')
                if len(st.session_state.df_dictionary) ==0 :
                    with st_lottie_spinner(loading,height =200, width = 200):  
                        prompt  =  f'''Study these columns {df.columns}. I am in a telco company, give your output in this python format:
                        df_dictionary = pd.DataFrame(
                        "ATTRIBUTE": ["BILL_SPENT", "DATA_USAGE", "CALL_DURATION", "SMS_SENT", "INTERNET_PACK"],
                        "VALUE": [
                            "Past 1 month Bill expenditure of the subscriber",
                            "Total data usage in the past month",
                            "Total call duration in the past month",
                            "Total SMS sent in the past month",
                            "Internet pack details subscribed by the user"
                        ]
                    )
                    I only want the output to be this python dataframe code and nothing else
                        '''
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {"role": "system", "content": "You are a data analyst assistant"},
                                {"role": "user", "content": prompt},
                            ]
                        )
                        dictionary  =response.choices[0].message.content

                        dictionary = re.sub(r"```(?:python)?\s*", "", dictionary).strip()

                        if dictionary.lower().startswith("python"):
                            dictionary = dictionary[6:].strip()


                        exec(dictionary)
                        st.session_state.df_dictionary = df_dictionary

                ui.table(data=st.session_state.df_dictionary, maxHeight=300)


        if tabby == 'View Analytics':
            if len(st.session_state.final_df.head(5)) > 3:
                df = st.session_state.final_df
            else:
                df = data
            total_customer = df['customer_id'].nunique()
            avg_bs = round(df['bill_spent'].mean(),2)
            avg_du = round(df['data_usage'].mean(),2)
            sunriser_percentage = round((df['sunriser'] == 'Yes').mean() * 100,1)
            vas_percentage = round((df['has_vas'] == 'Yes').mean() * 100,1)
            chinese_percentage = round((df['ethnicity'] == 'Chinese').mean() * 100,1)

            with card_container(key="table3"):
                st.subheader('Brief Analytics')
                st.caption('Last updated: 2024-09-30')
                cols = st.columns(3)
                with cols[0]:
                    ui.card(title="Number of Customers", content=f"{total_customer}", description="+20.1% from last month", key="card1").render()
                with cols[1]:
                    ui.card(title="Avg Bill Spent", content=f"${avg_bs}", description="+18.1% from last month", key="card2").render()
                with cols[2]:
                    ui.card(title="Avg Data Usage", content=f"{avg_du} GB", description="+19% from last month", key="card3").render()

                cols = st.columns(3)
                with cols[0]:
                    ui.card(title="Percentage of Sunriser Customer", content=f"{sunriser_percentage}%", description="+2.1% from last month", key="card4").render()
                with cols[1]:
                    ui.card(title="Percentage of Customer holding VAS", content=f"{vas_percentage}%", description="+5.1% from last month", key="card5").render()
                with cols[2]:
                    ui.card(title="Percentage of Chinese Customer", content=f"{chinese_percentage}%", description="-2% from last month", key="card6").render()

                init_streamlit_comm()

                st.subheader('Data Profiling')

                
                def get_pyg_renderer() -> "StreamlitRenderer":
                    return StreamlitRenderer(df, spec="./gw_config.json", debug=False)

                renderer = get_pyg_renderer()

                renderer.explorer(default_tab="data", key="pyg_explorer_1")



        if tabby == 'Create Segments':
            if len(st.session_state.final_df.head(5)) > 3:
                df = st.session_state.final_df
            else:
                df = data
            with card_container(key="table4"):
                st.subheader('Auto-segmentation with AI')

                generate_segment =st.button('Generate Segment Ideas')

                suggest_dict = None
                if generate_segment:
                    with st_lottie_spinner(loading,height =200, width = 200):  
                        prompt  =  f'''Generate 3 segment ideas for these columns {df.columns}. Be short and succinct. Make sure the segments utilize at least 2 attributes. Place those ideas into a python list like this 
                        ['Create segments for bill spent and data usage','idea2','idea3'] I want the output to only consist of the python list and nothing else'''
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {"role": "system", "content": "You are a data analyst assistant"},
                                {"role": "user", "content": prompt},
                            ]
                        )
                        suggest  =response.choices[0].message.content
                        suggest  = re.sub(r"```(?:python)?\s*", "", suggest).strip()
                        if suggest.lower().startswith("python"):
                                suggest = suggest[6:].strip()
                        st.session_state.suggest_list = ast.literal_eval(suggest)
                        #st.write(suggest_list)
                if len(st.session_state.suggest_list)> 1:
                    for each in st.session_state.suggest_list:
                        st.code(each)

                with st.form(key='my_form1'):

                    query1  = textarea(placeholder="Create your segments here...", key="textarea1")
                    submitted1 = st.form_submit_button("Submit")
                    if submitted1:
                        with st_lottie_spinner(loading,height =200, width = 200):  
                            prompt  =  f'''Here is the users segmenetation question:{query1} Here are all the columns: {df.columns}. Based on the user questions only, give me the relevant columns that will be used in python string only. For example, if the user ask for create 4 segments on bill spent and ethnicity then you
                            will return ONLY in python list ['bill_spent','ethnicity']. Your output must be a python list only.'''
                            response = client.chat.completions.create(
                                model="gpt-4o",
                                messages=[
                                    {"role": "system", "content": "You are a data analyst assistant"},
                                    {"role": "user", "content": prompt},
                                ]
                            )
                        ##  st.write(response.choices[0].message.content)
                            cl = response.choices[0].message.content
                            cl  = re.sub(r"```(?:python)?\s*", "", cl).strip()
                            if cl.lower().startswith("python"):
                                    cl = cl[6:].strip()
                            column_list = ast.literal_eval(cl)
                            result = extract_unique_values(df, column_list)


                            prompt  =  f'''Here is a sample of the data {result}, here is the users segmenetation question: {query1}. Help to user to come  up with segments give me a brief explanation of the segments and why you chose to do it this  way. Please give short and succinct sentences'''
                            response = client.chat.completions.create(
                                model="gpt-4o",
                                messages=[
                                    {"role": "system", "content": "You are a data analyst assistant"},
                                    {"role": "user", "content": prompt},
                                ]
                            )
                            st.session_state.response_content =response.choices[0].message.content

                            segments = {}

                            prompt = f"""
                            Here is a sample of the data {df.head(5)}.  here is the users segmenetation question: {query1}. Come up with the segments and provide the specific Python code to create those segments ONLY. I only want the output to be pure Python code without any descriptions, comments, or markdown formatting.
                            The segments should be structured as a dictionary. For example:

                            segments = {{
                                "Low Spend Low Usage": df[(df['bill_spent'] < 300) & (df['data_usage'] < 100)],
                                "High Spend Low Usage": df[(df['bill_spent'] >= 300) & (df['data_usage'] < 100)],
                                "High Spend High Usage": df[(df['bill_spent'] >= 300) & (df['data_usage'] >= 100)]
                            }} Again, i only want the code to create those segments ONLY.
                            """
                            response = client.chat.completions.create(
                                model="gpt-4o",
                                messages=[
                                    {"role": "system", "content": "You are a coding only assistant"},
                                    {"role": "user", "content": prompt},
                                ]
                            )
                            response_content2 =response.choices[0].message.content
                            response_content2 = re.sub(r"```(?:python)?\s*", "", response_content2).strip()

                            if response_content2.lower().startswith("python"):
                                response_content2 = response_content2[6:].strip()

                            ##st.write(response_content2)

                            exec(response_content2)
                            st.session_state.segments = segments

                            st.toast('Generating profiles... Will take awhile')
                    if len(st.session_state.response_content)> 1:
                        st.write_stream(stream_data(st.session_state.response_content))
                        for segment_name, segment_df in st.session_state.segments.items():
                            st.write(f"### Segment: {segment_name}")
                            try:
                                with st.popover(f"Data Profile for Segment {segment_name}"):

                                    # # Generate the profile report
                                    # pr = generate_profile(segment_df)

                                    
                                    # # Display the profile report with a specified height
                                    # st_profile_report(pr, height=800, navbar=True)  # Increased height if needed
                                    
                                    st.markdown(
                                        """
                                        <style>
                                        /* Target the iframe inside the st_profile_report */
                                        .reportview-container .streamlit-ydata-profiling iframe {
                                            width: 100% !important;  /* Make iframe take full width */
                                            max-width: 100% !important;  /* Ensure it doesn't exceed container */
                                        }

                                        /* Adjust the popover width */
                                        [data-baseweb="popover"] {
                                            width: 1000px !important;  /* Set your desired width */
                                        }

                                        /* Optional: Adjust the expander content width */
                                        .streamlit-expanderHeader {
                                            font-size: 18px;
                                        }
                                        </style>
                                        """,
                                        unsafe_allow_html=True
                                    )
                                    def get_pyg_renderer() -> "StreamlitRenderer":
                                        return StreamlitRenderer(segment_df, spec="./gw_config.json", debug=False)

                                    renderer = get_pyg_renderer()

                                    renderer.explorer(default_tab="data", key="pyg_explorer_1")
                            except:
                                st.error('Insufficient data')




        if tabby == 'Create Charts':
            if len(st.session_state.final_df.head(5)) > 3:
                df = st.session_state.final_df
            else:
                df = data
            with card_container(key="table5"):
                st.subheader('Charts Generation with AI')

                if st.button('Generate Chart Ideas'):
                    with st_lottie_spinner(loading,height =200, width = 200):  

                        try:
                            prompt  =  f"""
                            Here is a sample of the data {data.head(5)}, come up with 5 data analytic questions that can generate a pie chart/bar chart/calendar chart/race bar chart (e.g. 'data_usage' and 'has_vas', grouped by week)/map (a map on avg bill spent for each location over the months) . Try to use week for racebar chart. And please dont use location unless its a map.
                             You must state what chart to be used in the question. Give the questions in a python list ["qns1","qns2","qns3", "qns4", "qns5"]. Output must be a horizontal python list only, nothing else"""
                            response = client.chat.completions.create(
                                model="gpt-4o",
                                messages=[
                                    {"role": "system", "content": "You are a data analyst assistant"},
                                    {"role": "user", "content": prompt},
                                ]
                            )
                            #st.write(response.choices[0].message.content)
                            st.session_state.qns_list = ast.literal_eval(response.choices[0].message.content)

                        except:
                            st.error('Try again')
                if len(st.session_state.qns_list) >1:
                    for each in st.session_state.qns_list:
                        st.code(each)

                with st.form(key='my_form'):

                    mui_card_style= {"color": '#555', 'bgcolor': '#f5f5f5', "display": "flex", 'borderRadius': 1,  "flexDirection": "column"}
                    st.session_state['chart_images'] = []

                    txt = textarea(placeholder="Generate your charts here...", key="textarea2")

                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        with st_lottie_spinner(loading,height =200, width = 200):  

                            if 'pie chart' in txt.lower() or 'piechart' in txt.lower():
                                prompt  =  f'''Here is a sample of the data {data_sample}, here is the user's question: {txt}. The goal is to plot a pie chart. i need 
                                1) Column (small caps)
                                2) Title Recommendation. 
                                Give those answers in a python list like ['Column','Title Recommendation'], i only want the python list with these 2 elements as the output, nothing else. The column (first element) will be used in     
                                chart_data = df[column].value_counts().reset_index()
                                chart_data.columns = ['id', 'value']'''
                                response = client.chat.completions.create(
                                    model="gpt-4o",
                                    messages=[
                                        {"role": "system", "content": "You must obey the instruction given"},
                                        {"role": "user", "content": prompt},
                                    ]
                                )
                            
                                #st.write(response.choices[0].message.content)
                                input_string = response.choices[0].message.content
                                input_list = ast.literal_eval(input_string)

                                category = input_list[0]
                                title_recommendation = input_list[1]

                                chart_data = df[category].value_counts().reset_index()
                                chart_data.columns = ['id', 'value']

                                # Convert data to dictionary format suitable for Nivo
                                nivo_data = chart_data.to_dict(orient='records')

                                st.session_state['form_submissions'].append({
                                    'nivo_data': nivo_data,
                                    'title_recommendation': title_recommendation,
                                    'type' : 'piechart'
                                })

                            if ('bar chart' in txt.lower() or 'barchart' in txt.lower()) and 'race' not in txt.lower():
                                prompt  =  f'''Here is a sample of the data {data_sample}, here is the user's question: {txt}. The goal is to plot a bar chart. i need 
                                1) Column (small caps)
                                2) Title Recommendation. 
                                Give those answers in a python list like ['Column','Title Recommendation'], i only want the python list with these 2 elements as the output, nothing else. The column (first element) will be used in     
                                chart_data = df[column].value_counts().reset_index()
                                chart_data.columns = ['id', 'value']'''
                                response = client.chat.completions.create(
                                    model="gpt-4o",
                                    messages=[
                                        {"role": "system", "content": "You must obey the instruction given"},
                                        {"role": "user", "content": prompt},
                                    ]
                                )
                                #st.write(response.choices[0].message.content)
                                input_string = response.choices[0].message.content
                                input_list = ast.literal_eval(input_string)

                                category = input_list[0]
                                title_recommendation = input_list[1]

                                chart_data = df[category].value_counts().reset_index()
                                chart_data.columns = ['id', 'value']

                                # Convert data to dictionary format suitable for Nivo
                                nivo_data = chart_data.to_dict(orient='records')
                            # st.write(nivo_data)
                                st.session_state['form_submissions'].append({
                                    'nivo_data': nivo_data,
                                    'title_recommendation': title_recommendation,
                                    'type' : 'barchart'
                                })

                            if 'stacked' in txt.lower() or 'stacked bc' in txt.lower():
                            # st.write('stacking')
                                prompt = f'''Here is a sample of the data {data_sample}, here is the user's question: {txt}. The goal is to plot a stacked bar chart. I need 
                                1) Column for x-axis (small caps)
                                2) Stacking Column (small caps)
                                3) Title Recommendation. 
                                Give those answers in a python list like ['x_column', 'stacking_column', 'Title Recommendation'], I only want the python list with these 3 elements as the output, nothing else. The x_column (first element) will be used in     
                                chart_data = df.groupby(['x_column', 'stacking_column']).size().unstack(fill_value=0)'''
                            #  st.write(prompt)
                                response = client.chat.completions.create(
                                    model="gpt-4o",
                                    messages=[
                                        {"role": "system", "content": "You must obey the instruction given"},
                                        {"role": "user", "content": prompt},
                                    ]
                                )
                                #st.write(response.choices[0].message.content)
                                input_string = response.choices[0].message.content
                                input_list = ast.literal_eval(input_string)

                                category = input_list[0]
                                stacking_column = input_list[1]
                                title_recommendation = input_list[2]

                                chart_data = df.groupby([category, stacking_column]).size().unstack(fill_value=0).reset_index()

                                # Rename columns to match Nivo's expected format
                                chart_data.columns = ['id'] + list(chart_data.columns[1:])

                                # Convert data to dictionary format for Nivo
                                nivo_data = chart_data.to_dict(orient='records')
                                st.session_state['form_submissions'].append({
                                    'nivo_data': nivo_data,
                                    'title_recommendation': title_recommendation,
                                    'type' : 'stacked'
                                })


                            elif 'scatter plot' in txt.lower() or 'scatterplot' in txt.lower():
                                prompt = f'''Here is a sample of the data {data.to_csv(index=False)},
                                here is the user's question: {txt}.
                                The goal is to plot a scatter plot. I need:
                                1) Two Columns (small caps) for X and Y axes separated by a comma.
                                2) Title Recommendation.
                                Give the answers in a python list like [['x_column', 'y_column'], 'title recommendation'],
                                only the python list with these 2 elements as the output, nothing else.'''
                                
                                response = client.chat.completions.create(
                                    model="gpt-4o",
                                    messages=[
                                        {"role": "system", "content": "You must obey the instruction given"},
                                        {"role": "user", "content": prompt},
                                    ]
                                )
                                
                                #st.write(response.choices[0].message.content)
                                input_string = response.choices[0].message.content
                                input_list = ast.literal_eval(input_string)

                                columns = input_list[0]
                                title_recommendation = input_list[1]

                                if len(columns) != 2:
                                    st.error("Scatter plot requires exactly two columns for X and Y axes.")
                                else:
                                    x_column, y_column = columns

                                    # Prepare scatter plot data
                                    scatter_data = df[[x_column, y_column]].dropna()
                                    scatter_data.rename(columns={x_column: 'x', y_column: 'y'}, inplace=True)
                                    scatter_data = scatter_data.to_dict(orient='records')
                                    nivo_data = [
                                        {
                                            "id": "scatter-data",
                                            "data": scatter_data
                                        }
                                    ]
                                    st.session_state['form_submissions'].append({
                                        'nivo_data': nivo_data,
                                        'title_recommendation': title_recommendation,
                                        'type' : 'scatter'
                                    })

                            elif 'calendar chart' in txt.lower() or 'calendarchart' in txt.lower():
                                prompt  =  f'''Here is a sample of the data {data_sample}, here is the user's question: {txt}. The goal is to plot a calendar chart. i need 
                                1) Date Column (small caps)
                                2) Value Column (small caps)
                                3) Title Recommendation. 
                                Give those answers in a python list like ['Date Column','Value Column','Title Recommendation'], i only want the python list with these 3 elements as the output, nothing else. The columns will be used in     
                                chart_data = df[[date_column, value_column]].dropna()'''
                                response = client.chat.completions.create(
                                    model="gpt-4o",
                                    messages=[
                                        {"role": "system", "content": "You must obey the instruction given"},
                                        {"role": "user", "content": prompt},
                                    ]
                                )
                            
                                #st.write(response.choices[0].message.content)
                                input_string = response.choices[0].message.content
                                input_list = ast.literal_eval(input_string)

                                date_column = input_list[0]
                                value_column = input_list[1]
                                title_recommendation = input_list[2]

                                chart_data = df[[date_column, value_column]].dropna()


                                try:
                                    if chart_data[date_column].dtype == 'int64':
                                        chart_data[date_column] = chart_data[date_column].apply(excel_date_to_datetime)
                                    else:
                                        chart_data[date_column] = pd.to_datetime(chart_data[date_column], errors='coerce')
                                except Exception as e:
                                    st.error(f"Error converting date column: {e}")

                                chart_data = chart_data.dropna(subset=[date_column])

                                chart_data[value_column] = pd.to_numeric(chart_data[value_column], errors='coerce')

                                chart_data = chart_data.dropna(subset=[value_column])

                                chart_data[date_column] = chart_data[date_column].dt.strftime('%Y-%m-%d')

                                chart_data[date_column] = chart_data[date_column].astype(str)

                                chart_data[date_column] = chart_data[date_column].replace('', np.nan)
                                chart_data = chart_data.dropna(subset=[date_column])



                                nivo_data = chart_data.rename(columns={date_column: 'day', value_column: 'value'}).to_dict(orient='records')


                                # Store submission data
                                st.session_state['form_submissions'].append({
                                    'nivo_data': nivo_data,
                                    'title_recommendation': title_recommendation,
                                    'type': 'calendarchart'
                                })
                            elif 'race' in txt.lower():
                                                        prompt  =  f'''Here is a sample of the data {data_sample}, here is the user's question: {txt}. The goal is to create a race bar chart. i need 
                                                        1) Date Column (small caps)
                                                        2) Numerical Value Column (small caps)
                                                        3) Categorical Value Column (small caps)
                                                        4) Type of period (D,W,M) 
                                                        3) Title Recommendation. 
                                                        Give those answers in a python list like ['Date Column','Numerical Value Column','Categorical Value Column', 'Type of Period','Title Recommendation'], i only want the python list with these 3 elements as the output, nothing else.'''
                                                        response = client.chat.completions.create(
                                                            model="gpt-4o",
                                                            messages=[
                                                                {"role": "system", "content": "You must obey the instruction given"},
                                                                {"role": "user", "content": prompt},
                                                            ]
                                                        )
                                                    
                                                        input_string = response.choices[0].message.content
                                                        race_list = ast.literal_eval(input_string)
                                                        ##st.write(race_list)
                                                        date_column = race_list[0]
                                                        value_column = race_list[1]
                                                        cat_column =race_list[2]
                                                        period = race_list[3]
                                                        title_recommendation = race_list[4]

                                                        df[date_column] = pd.to_datetime(df[date_column], format='%d/%m/%Y')

                                                        df[period] = df[date_column].dt.to_period(period).astype(str)  # Grouping by week
                                                        # Group the data to compute average data usage for each week
                                                        df_weekly = df.groupby([period, cat_column], as_index=False).agg({value_column: 'mean'})

                                                        # Create a plotly bar chart race using 'data_usage' and 'phone_purchased', grouped by week
                                                        fig = px.bar(
                                                            df_weekly,
                                                            x=value_column, 
                                                            y= cat_column, 
                                                            color= cat_column,
                                                            animation_frame= period,  # Use the 'week' for weekly animation
                                                            range_x=[0, df_weekly[value_column].max() + 50], 
                                                            orientation='h', 
                                                            title= title_recommendation
                                                        )

                                                        # Streamlit app to display the plot
                                                        st.plotly_chart(fig)

                            elif 'map' in txt.lower():
                                @st.cache_data
                                def load_geojson(file_path):
                                    with open(file_path) as f:
                                        return json.load(f)

                                geojson = load_geojson('assets/singapore_districts.geojson')
                                pln_area_pattern = re.compile(r"<th>PLN_AREA_N<\/th>\s*<td>(.*?)<\/td>")
                                for feature in geojson['features']:
                                    description = feature['properties']['Description']
                                    match = pln_area_pattern.search(description)
                                    if match:
                                        feature['properties']['Name'] = match.group(1)
                                districts = [feature['properties']['Name'] for feature in geojson['features']]

                                prompt  =  f'''Here is a sample of the data {data_sample}, here is the user's question: {txt}. The goal is to create a animated map chart that moves with time frame. i need 
                                1) Date Column (small caps)
                                2) Numerical Value Column (small caps)
                                3) Type of period (D,W,M) 
                                4) Title Recommendation. 
                                Give those answers in a python list like ['Date Column','Numerical Value Column', 'Type of Period','Title Recommendation'], i only want the python list with these 3 elements as the output, nothing else.'''
                                response = client.chat.completions.create(
                                    model="gpt-4o",
                                    messages=[
                                        {"role": "system", "content": "You must obey the instruction given"},
                                        {"role": "user", "content": prompt},
                                    ]
                                )
                            
                                input_string = response.choices[0].message.content
                                race_list = ast.literal_eval(input_string)
                                date_column = race_list[0]
                                value_column = race_list[1]
                                period = race_list[2]
                                title_recommendation = race_list[3]

                                df[date_column] = pd.to_datetime(df[date_column], format='%d/%m/%Y')

                                # Extract year-month for the animation frame
                                df[period] = df[date_column].dt.to_period(period).astype(str)

                                # Aggregate data by district (location) and month
                                df_agg = df.groupby(['location', period])[value_column].sum().reset_index()

                                # Ensure all districts are represented in the aggregated data, including those with no values
                                all_months = df[period].unique()  # Get all unique months
                                all_locations = pd.DataFrame({'location': districts})  # Ensure all districts are included

                                # Create a DataFrame that contains all combinations of locations and months
                                all_combinations = pd.MultiIndex.from_product([all_locations['location'], all_months], names=['location', period]).to_frame(index=False)

                                # Merge the combinations with the aggregated data
                                df_agg = all_combinations.merge(df_agg, on=['location', period], how='left')
                                df_agg[value_column].fillna(0, inplace=True)  # Fill missing values with 0

                                # Create the animated choropleth map
                                fig = px.choropleth(
                                    df_agg,
                                    geojson=geojson,
                                    locations='location',
                                    featureidkey='properties.Name',  # Ensure this matches the property name in your GeoJSON
                                    color=value_column,
                                    hover_name='location',
                                    animation_frame= period,
                                    color_continuous_scale=px.colors.qualitative.Set3,  # Use a qualitative color scale
                                    projection='mercator'
                                )

                                # Update the layout to fit the map to the locations and show the outlines
                                fig.update_geos(
                                    fitbounds="locations",
                                    visible=False,
                                    showcountries=False,
                                    showcoastlines=False,
                                    showland=False,
                                    showframe=False
                                )

                                # Update the layout to increase the size of the map
                                fig.update_layout(
                                    width=800,  # Set the width of the figure
                                    height=600,  # Set the height of the figure
                                    margin={"r":0, "t":0, "l":0, "b":30}  # Adjust the bottom margin to reduce the distance

                                # Remove margins
                                )

                                # Display the plot in Streamlit
                                st.plotly_chart(fig)




                    with elements("dashboard"):
                        layout = [
                            dashboard.Item(f'item_{idx + 1}', 0, idx * 4, 4, 4)  # Adjust the position (x, y) dynamically
                            for idx in range(len(st.session_state['form_submissions']))
                        ]

                        def handle_layout_change(updated_layout):
                            print(updated_layout)

                        with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
                            for idx, submission in enumerate(st.session_state['form_submissions']):
                                nivo_data = submission['nivo_data']
                                title_recommendation = submission['title_recommendation']
                                plot_type = submission['type']
                                # Create a dynamic key for each Paper element
                                dynamic_key = f'item_{idx + 1}'

                                if 'calendar chart' in plot_type.lower() or 'calendarchart' in plot_type.lower():
                                        ploty.create_calendar_chart(nivo_data, title_recommendation)
                                        ploty.create_calendar_chart2(nivo_data, title_recommendation)
                                        img_bytes3 = ploty.create_calendar_chart2(nivo_data, title_recommendation)
                                        st.session_state['chart_images'].append((img_bytes3, "Calendar Chart: Category Distribution"))
                                elif 'calendar chart' not in plot_type.lower() or 'calendarchart' not in plot_type.lower():
                                    with mui.Paper(
                                        label=f'Plot {idx + 1}', 
                                        elevation=10, 
                                        variant="outlined", 
                                        square=True, 
                                        key=dynamic_key, 
                                        sx=mui_card_style
                                    ):

                                        if 'pie chart' in plot_type.lower() or 'piechart' in plot_type.lower():
                                            ploty.create_pie_chart(nivo_data, title_recommendation)
                                            img_bytes1 = ploty.create_pie_chart2(nivo_data, title_recommendation)
                                            st.session_state['chart_images'].append((img_bytes1, "Pie Chart: Category Distribution"))

                                        elif 'bar chart' in plot_type.lower() or 'barchart' in plot_type.lower():
                                            ploty.create_bar_chart(nivo_data, title_recommendation)
                                            img_bytes2 = ploty.create_bar_chart2(nivo_data, title_recommendation)
                                            st.session_state['chart_images'].append((img_bytes2, "Bar Chart: Category Distribution"))

                                        elif 'stacked' in plot_type.lower()  or 'stacked bc' in plot_type.lower():
                                            ploty.create_stacked_bar_chart(nivo_data, title_recommendation)

                                        elif 'scatter' in plot_type.lower()  or 'scatter' in plot_type.lower():
                                            ploty.create_scatter_plot(nivo_data,  title_recommendation)



        def create_pdf_report(chart_images, response_content, output_filename='report.pdf'):
            buffer = io.BytesIO()
            
            # Initialize the PDF document
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            
            # Define styles
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle(
                'Title',
                parent=styles['Title'],
                fontSize=24,
                leading=28,
                spaceAfter=24,
                alignment=TA_CENTER
            )
            
            header_style = ParagraphStyle(
                'Header',
                parent=styles['Heading1'],
                fontSize=18,
                leading=22,
                spaceAfter=18,
            )
            
            subheader_style = ParagraphStyle(
                'SubHeader',
                parent=styles['Heading2'],
                fontSize=14,
                leading=18,
                spaceAfter=14,
            )
            
            body_style = ParagraphStyle(
                'Body',
                parent=styles['Normal'],
                fontSize=10,
                leading=14,
                spaceAfter=12,
                alignment=TA_LEFT
            )
            
            # Add a cover page
            elements.append(Paragraph("Data GPT - Summary Report", title_style))
            elements.append(Spacer(1, 48))
            elements.append(Paragraph("Prepared by: M1 Aether", body_style))
            current_date = datetime.now().strftime("%Y-%m-%d")
            elements.append(Paragraph(f"Date: {current_date}", body_style))
            elements.append(PageBreak())
            

            # Add report content
            elements.append(Paragraph("Segmentation", header_style))
            elements.append(Spacer(1, 12))
            response_content_html = markdown.markdown(response_content)
            preformatted_content = XPreformatted(response_content_html, body_style)
            
            # Use KeepInFrame to ensure content stays within page margins
            frame_width = doc.width
            frame_height = doc.height
            keep_in_frame = KeepInFrame(frame_width, frame_height, content=[preformatted_content], mode = 'truncate')

            elements.append(keep_in_frame)            
            elements.append(PageBreak())
            
            # Add charts
            elements.append(Paragraph("Charts", header_style))
            elements.append(Spacer(1, 12))
            
            for img_bytes, chart_title in chart_images:
                elements.append(Paragraph(chart_title, subheader_style))
                elements.append(Spacer(1, 12))
                img = Image(io.BytesIO(img_bytes))
                img.drawHeight = 3 * inch  # Adjust as needed
                img.drawWidth = 6 * inch   # Adjust as needed
                elements.append(img)
                elements.append(Spacer(1, 24))
            
            # Build the PDF
            doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
            
            buffer.seek(0)
            return buffer

        def add_page_number(canvas, doc):
            page_num = canvas.getPageNumber()
            text = f"Page {page_num}"
            canvas.setFont('Helvetica', 10)
            canvas.drawRightString(200 * mm, 20 * mm, text)



        if tabby == 'Generate Report':
            with card_container(key="table6"):

                st.subheader("PDF Report")
                if st.button("Generate Report"):
                    if not st.session_state['chart_images']:
                        st.warning("Please generate at least one chart before downloading the report.")
                    else:
                        pdf_buffer = create_pdf_report(st.session_state['chart_images'], response_content = st.session_state.response_content )
                        st.download_button(
                            label="Download PDF Report",
                            data=pdf_buffer,
                            file_name="data_gpt_report.pdf",
                            mime="application/pdf"
                        )

if tabs == 'Chat':

    if len(st.session_state.final_df.head(5)) > 3:
        df = st.session_state.final_df
    else:
        df = data
    column_list = df.columns.to_list()
    rv = st.session_state['radio_value']
    ui.badges(badge_list=[(f'Selected Datasource: {rv}', "default")],
            class_name="flex gap-2", 
            key="main_badges1")
    st.subheader('Ask me anything, I am here to help!')
    cols = st.columns(3)
    with cols[0]:
        ui.card( content=f"Search for the latest singtel iphone 16 pro max promotions?", description="Search the internet", key="card1").render()
    with cols[1]:
        ui.card(content=f"Retrieve M1's iphone 16 pro max pricing", description="Document Retrieval", key="card2").render()
    with cols[2]:
        ui.card( content=f"Analyse my data and come up with some numerical segments", description="Data Analysis", key="card3").render()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    x_count = 0

 




    if prompt1 := st.chat_input(f"Hi, I am Aether. Ask me anything :)", key = {x_count}):
        x_count += 1
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt1)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt1})

        prompt2  =  f'''My question is: {prompt1}. Based on my question, what kind of word bes describe my question? ONLY reply with one word from a selection of ['Search', 'Retrieval', 'Analysis']. 
        If the word retrieve is mentioned, you are to reply with 'Retrieval'. If the word search the internet is mentioned, you are to reply with 'Search'. 
        IF the user ask for anything related to data or segmentation, you are to replly with the word 'Analysis'''
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are bot that can only reply with 1 word"},
                {"role": "user", "content": prompt2},
            ]
        )
        rs =response.choices[0].message.content
        if rs == 'Search':
            rs_line = 'User has requested me to search the internet...'
            with st.chat_message("assistant"):
                st.markdown(rs_line)
            st.session_state.messages.append({"role": "assistant", "content": rs_line}) 
            search = GoogleSearch({
                "q": f"{prompt1}", 
                "location": "Singapore",
                "api_key": os.getenv("SERAPI_KEY")
            })
            results = search.get_dict()
           # st.write(results)
            snippets = [result["snippet"] for result in results.get("organic_results", [])]
            combined_snippets = " ".join(snippets)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are to sumamrise complicated sentences extracted from many sites, focus on the user question {prompt1}. Also, Replace all $  with SGD."},
                    {"role": "user", "content": f"Here is the info that are messy {combined_snippets}, remember to focus on my question: {prompt1}"},
                ]
            ) 
            rs2 =response.choices[0].message.content
                
            with st.chat_message("assistant"):
                st.write_stream(stream_data(rs2))

            st.session_state.messages.append({"role": "assistant", "content": rs2})        
                    
        if rs == 'Retrieval':
            rs_line = 'User has requested me to retrieve documents from our database...'
            with st.chat_message("assistant"):
                st.markdown(rs_line)
            with open('assets/m1plan.txt', 'r') as file:
                info = file.read()            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"Here is the text: {info}, here is my question: {prompt1}."},
                    {"role": "user", "content": f"You are in a telco company working as a summariser"},
                ]
            ) 
            rs2 =response.choices[0].message.content
            with st.chat_message("assistant"):
                st.write_stream(stream_data(rs2))


            st.session_state.messages.append({"role": "assistant", "content": rs_line})     
        if rs == 'Analysis':
            result = extract_unique_values(df, column_list)
            rs_line = 'User has requested for a data analysis on our data...'
            with st.chat_message("assistant"):
                st.markdown(rs_line)
            st.session_state.messages.append({"role": "assistant", "content": rs_line}) 
            prompt  =  f'''My question is: {prompt1} and here's sample data: {result}. Please be concise, short and succinct with your answers and provide the best possible segmentations'''
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a segmentation expert for a telco company"},
                    {"role": "user", "content": prompt},
                ]
            )
            rs2 =response.choices[0].message.content
            with st.chat_message("assistant"):
                st.write_stream(stream_data(rs2))




if tabs != 'Chat':

    with open("assets/particles.html", "r") as f:

        html_code = f.read()
        
    components.html(html_code)