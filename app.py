# creation: 20230323
# copyright (c) 2023 Sam C. Lin and Kenneth A. Lin
#
import streamlit as st
import datetime
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title='Freestyle Libre CSV Viewer',
#    layout='centered'
        layout='wide'
)

file = st.file_uploader(label="Upload CSV", type='csv')
if file is not None:
    # read uploaded file & format
    df = pd.read_csv(file)
    df.reset_index(inplace=True)
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    df['Device Timestamp'] = pd.to_datetime(df['Device Timestamp'])
    
    filldata = pd.DataFrame(df[['Device Timestamp', 'Notes']].value_counts()).reset_index()
    filldata.drop(columns=[0], inplace=True)
    filldata.sort_values(by='Device Timestamp', inplace=True)
    df = df.merge(filldata, on='Device Timestamp', how='left', suffixes=['_x', ''])
    df.drop(columns=['Notes_x'], inplace=True)

    overlay_notes = st.checkbox(
        label='**Show Notes on graph**', help='Check this to overlay note data on the graph!')

    fig = go.Figure()

    # plot historic glucose
    fig.add_trace(go.Scatter(x=df['Device Timestamp'], y=df['Historic Glucose mg/dL'],
                             mode='lines+markers',
                             name='Historic',
                             marker={
                                 'color': 'blue'
    }))

    # plot scan glucose
    fig.add_trace(go.Scatter(x=df['Device Timestamp'], y=df['Scan Glucose mg/dL'],
                             mode='markers',
                             name='Scan',
                             marker={
                                 'color': 'red'
    }))

    if overlay_notes:
        fig.add_trace(go.Scatter(x=df['Device Timestamp'], y=df['Scan Glucose mg/dL'],
                                 mode='text',
                                 name='Notes',
                                 text=df['Notes'],
                                 textposition='top center',
                                 textfont={
                                     'color':'black'
                                 },
                                 marker={
            'color': '#900C3F'
        }))
    # format hover text
    fig.update_traces(
        hovertemplate="Timestamp: %{x}<br>" + "Glucose: %{y} mg/dL"
    )

    # format plot
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Blood Glucose mg/dL",
        title="Time vs Glucose mg/dL"
    )

    st.plotly_chart(fig,use_container_width=True)

    with st.expander('Note data (Expand to show)'):
        st.write(filldata)

    with st.expander(label='Raw Data (Expand to show)'):
        st.dataframe(df)
