import matplotlib.pyplot as plt
from influxdb_client import InfluxDBClient
import queries as q
import streamlit as st
import pandas as pd
import altair as alt
st.set_page_config(
    page_title="RG_04",
    # page_icon="favicon.ico",
    # layout="wide"
)
# import numpy as np

# Specify the InfluxDB connection details
bucket = "testing"
org = "University of Colombo"
token = "bw2bP-TBWai6Acgp_nLMVIblVEmAUDAHCu_TIKvnPQIMSTq1Ll_5aWAIaALPT-ab1o-p1kqX-HSYRrp9wSVcWw=="
url = "http://localhost:8086"

sensor_id_1 = 'TLM0100'
sensor_id_2 = 'TLM0101'

# Attempt to establish a connection
try:
    client = InfluxDBClient(url=url, token=token)
    # Connection successful
    print("Connection to InfluxDB successful!")

    # Now you can perform operations on the database using the 'client' object
    query_api = client.query_api()

    # Temperature plot
    queryTemp = q.tempWithtime(bucket, 1)
    result = query_api.query(org=org, query=queryTemp)
    # temperatureData = pd.DataFrame(columns=["_time", "_value", "sensor_id"])
    # for table in result:
    #     for record in table.records:
    #         matplotlib_datetime = pd.to_datetime(record.get_time())
    #         temperatureData.loc[len(temperatureData)] = [matplotlib_datetime, record.get_value()]
    TempData = []
    for table in result:
        for record in table.records:
            time = pd.to_datetime(record.get_time())
            temperature = record.get_value()
            sensor_id = record.values.get('sensor_id')
            TempData.append({"Time": time, "Temperature": temperature, "Sensor_ID": sensor_id})
    # Convert the list of dictionaries to a DataFrame
    temperatureData = pd.DataFrame(TempData)
    # Plot the line chart
    chart_data_temp = temperatureData.pivot(index='Time', columns='Sensor_ID', values='Temperature')
    st.line_chart(chart_data_temp, use_container_width=True)

    # Humidity plot
    queryHumidity = q.humidityWithtime(bucket, 1)
    result = query_api.query(org=org, query=queryHumidity)
    HumidityData = []
    for table in result:
        for record in table.records:
            time = pd.to_datetime(record.get_time())
            humidity = record.get_value()
            sensor_id = record.values.get('sensor_id')
            HumidityData.append({"Time": time, "Humidity": humidity, "Sensor_ID": sensor_id})
    # Convert the list of dictionaries to a DataFrame
    humidityData = pd.DataFrame(HumidityData)
    # Plot the line chart
    chart_data_humidity = humidityData.pivot(index='Time', columns='Sensor_ID', values='Humidity')
    print(chart_data_humidity.head())
    st.line_chart(chart_data_humidity, use_container_width=True)

    # Humidity plot using Altair
    chart = alt.Chart(humidityData).mark_line().encode(
        x='Time',y='Humidity'
    )
    # Create the chart
    # chart = alt.Chart(humidityData).mark_line().encode(
    #     x='Time',
    #     y='Humidity'.__getitem__(sensor_id_1.__len__()),
    #     color=alt.value('blue')  # Customize the color for sensor1
    # ).properties(
    #     title='Humidity Sensor Readings',
    #     width=600,
    #     height=400
    # )
    #
    # # Add another line for sensor2
    # chart += alt.Chart(humidityData).mark_line().encode(
    #     x='Time',
    #     y='Humidity'.__getitem__(sensor_id_2.__len__()),
    #     color=alt.value('red')  # Customize the color for sensor2
    # )

    st.altair_chart(chart, use_container_width=True)

    # co values plot
    queryCO = q.coWithtime(bucket, 1)
    result = query_api.query(org=org, query=queryCO)
    COData = []
    for table in result:
        for record in table.records:
            time = pd.to_datetime(record.get_time())
            co = record.get_value()
            sensor_id = record.values.get('sensor_id')
            COData.append({"Time": time, "CO": co, "Sensor_ID": sensor_id})
    # Convert the list of dictionaries to a DataFrame
    coData = pd.DataFrame(COData)
    # Plot the area chart
    chart_data_co = coData.pivot(index='Time', columns='Sensor_ID', values='CO')
    st.area_chart(chart_data_co, use_container_width=True)

    # Plot using pyplot
    # Plot the line chart
    fig, ax = plt.subplots()
    ax.plot(coData["Time"], coData["CO"])
    # Set the y-axis limits
    # ax.set_ylim([COData['CO'].min(), COData['CO'].max()])
    # Add labels and title
    ax.set_xlabel("Time")
    ax.set_ylabel("Values")
    ax.set_title("CO with Time")

    # Display the chart in Streamlit
    st.pyplot(fig)
    # Remember to close the connection when you're done
    client.close()

except Exception as e:
    # Connection failed
    print("Connection to InfluxDB failed:", str(e))
