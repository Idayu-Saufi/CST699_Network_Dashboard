import streamlit as st
import pandas as pd
import plotly.express as px
import base64 #Standard Python Module
from io import StringIO, BytesIO #Standard Python Module


def generate_excel_download_link(df):
    # Credit Excel: https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = BytesIO()
    df.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)

def generate_html_download_link(fig):
    # Credit Plotly: https://discuss.streamlit.io/t/download-plotly-plot-as-html/4426/2
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot Chart</a>'
    return st.markdown(href, unsafe_allow_html=True)

# emoji: https://www.webfx.com/tools/emoji-cheat-sheet/

st.set_page_config(page_title="Network Dashboard", layout="wide") 

st.title ("Network Dashboard")

uploaded_file = st.file_uploader("Choose XLSX  file", type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    #st.dataframe(df)

    #FILTER DATA AT ST
    st.sidebar.header("Filter:")
    name = st.sidebar.multiselect(
        "Select Department Name:",
        options=df["Name"].unique(),
        default=df["Name"].unique()
    )

    AP_type = st.sidebar.multiselect(
        "Select AP type:",
        options=df["AP_Type"].unique(),
        default=df["AP_Type"].unique()
    )

    IP_address = st.sidebar.multiselect(
        "Select IP Address:",
        options=df["IP_Address"].unique(),
        default=df["IP_Address"].unique()
    )
    status = st.sidebar.multiselect(
        "Select Status:",
        options=df["Status"].unique(),
        default=df["Status"].unique()
    )

    df_selection = df.query(
        "AP_Type == @AP_type | Name == @name | IP_Address == @IP_address | Status == @status" 
    )

    st.dataframe(df_selection)

    groupby_column = st.selectbox(
        'What would you like to analyse?',
        ('Name', 'IP_Address', 'Switch IP', 'Status', 'AP_Type')
    )

    #GROUP DATAFRAME
    ouput_columns = 'Total_AP',
    df_grouped = df.groupby(by=[groupby_column], as_index=False)[ouput_columns].sum()
    st.dataframe(df_grouped) #to show new table with columns selected
    
    st.title(":bar_chart: Network Chart")
    st.markdown("##")
    
    #PLOT DATAFRAME
    #BAR CHART
    fig_bar = px.bar(
        df_grouped,
        x=groupby_column,
        y='Total_AP',
        #color='Status',
        #color_continuous_scale=['red', 'yellow', 'green'],
        template='plotly_white',
        title=f'<b>Network Bar Chart by {groupby_column}</b>'
    )
    #st.plotly_chart(fig)

    #PIE CHART
    fig_pie = px.pie(data_frame=df,
                 names=groupby_column,
                 values='Total_AP',
                 title="<b>AP Pie Chart",
                 template="plotly_dark"
    )
    #st.plotly_chart(fig_pie)


    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_bar, use_container_width=True)
    right_column.plotly_chart(fig_pie, use_container_width=True)

    #LINE CHART
    fig_line = px.line(
        df_grouped,
        x=groupby_column,
        y='Total_AP',
        template='plotly_dark',
        title=f'<b>Network Line Chart by {groupby_column}</b>'
    )

    #DONUT-LIKE PIE CHART
    fig_donut = px.pie(
        df_grouped,
        names=groupby_column,
        values='Total_AP',
        template='plotly_dark',
        title=f'<b>Network Donut-Like Pie Chart by {groupby_column}</b>',
        hole=.3
    )

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_line, use_container_width=True)
    right_column.plotly_chart(fig_donut, use_container_width=True)

    #DOWNLOAD SECTION
    st.subheader('Download: ')
    st.markdown("Updated Excel File: ")
    generate_excel_download_link(df_grouped)
    st.markdown("Bar Chart: ")
    generate_html_download_link(fig_bar)
    st.markdown("Pie Chart: ")
    generate_html_download_link(fig_pie)
    st.markdown("Line Chart: ")
    generate_html_download_link(fig_line)
    st.markdown("Donut-Like Pie Chart: ")
    generate_html_download_link(fig_donut)
