import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from vnstock import * #import all functions, including functions that provide OHLC data for charting
from vnstock.chart import *
from datetime import datetime, timedelta
from vnstock import * #import all functions
from tvDatafeed import TvDatafeed, Interval
st.set_page_config(layout="wide")
import module1
from module1 import market_breadth
from module1 import list_ind
from module1 import index
from module1 import topanhhuong
from module1 import KhoingoaiGD
from module1 import GTGD
from module1 import muaban
from module1 import cungcau
from module1 import indicator
from module1 import phanloaindt

exchange1 = list_ind()
option = exchange1['name'].to_list()
option.append('ALL')
id = st.sidebar.selectbox('Chọn Ngành',option)
exchange =st.sidebar.selectbox('Sàn Niêm Yết',['HOSE','HNX','UPCOM','VN30','ALL'])
period =st.sidebar.selectbox('Dữ liệu thời gian',['1d','1w','1M'])
industry= 5300
for i in range(0,18):
    if id == option[i]:
        industry= exchange1['id'].iloc[i]
        break;
    else:
        industry= 'ALL'

period1 = st.selectbox('Dữ liệu thời gian1',['1d','1w','1M'])
df1 = market_breadth(exchange =exchange,period=period1,industry=industry)
st.write(df1)
period2 = st.selectbox('Dữ liệu thời gian2',['1d','1w','1M'])
df2 = index(exchange =exchange,period=period2,industry=industry)
st.write(df2)
period3 = st.selectbox('Dữ liệu thời gian3',['1d','1w','1M'])
##df3 = topanhhuong(exchange =exchange,period=period3,industry=industry)
##st.write(df3)
period4 = st.selectbox('Dữ liệu thời gian4',['1d','1w','1M'])
df4 = KhoingoaiGD(exchange= exchange, period=period4,industry =industry)
st.write(df4)
df5 = GTGD()
st.write(df5)
df6 = muaban(exchange =exchange,industry =industry)
st.write(df6)
df7 = cungcau(exchange =exchange,industry =industry)
st.write(df7)
df8 = indicator(exchange =exchange,industry=industry)
st.write(df8)
df9 = phanloaindt(exchange =exchange,period=period,industry =industry)
st.write(df9)


##### Biểu đồ 1 #########

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df1['time'], y=df1['Mã Tăng'],name='Mã Tăng',
    mode='lines',
    line=dict(width=0.5, color='rgb(184, 247, 212)'),fillcolor='green',
    stackgroup='one',
    groupnorm='percent', # sets the normalization for the sum of the stackgroup
    hoverinfo = 'text+x+y',
))


fig.add_trace(go.Scatter(
    x=df1['time'], y=df1['Mã Đứng'], name='Mã Đứng',hoverinfo = 'text+x+y',
    mode='lines',
    line=dict(width=0.5, color='rgb(127, 166, 238)'),fillcolor='orange',
    stackgroup='one'))

fig.add_trace(go.Scatter(
    x=df1['time'], y=df1['Mã Giảm'],name='Mã Giảm',
    mode='lines',
    line=dict(width=0.5, color='rgb(111, 231, 219)'),fillcolor='red',hoverinfo = 'text+x+y',
    stackgroup='one'
))

fig.update_layout(
    title= 'Biến Động Thị Trường'+id,
    showlegend=True,
    xaxis_type='category',
    yaxis=dict(
        type='linear',
        range=[1, 100],
        ticksuffix='%'))

####### Biểuđồ2  ########
import plotly.subplots as sp
import plotly.graph_objects as go
fig1 = sp.make_subplots(specs=[[{"secondary_y": True}]])

# Thêm trace cho giá (line)
fig1.add_trace(go.Line(x=df2['time'], y=df2['index'], name='index'))

# Thêm trace cho khối lượng (cột)
fig1.add_trace(go.Bar(x=df2['time'], y=df2['volume'], name='Volume'), secondary_y=True)

# Cập nhật layout
fig1.update_layout(title='Chỉ số '+id, xaxis_title='Time')

# Cập nhật trục y thứ nhất
fig1.update_yaxes(title_text='Price', secondary_y=False,showgrid=False)


################Bieu do3#####################
##fig3 = go.Figure()
##df31= df3[['Mã Giảm','Điểm Giảm']]
##a = round(df3['Điểm Tăng'].sum(),2)
##a= str(a)
##b =str(round(df3['Điểm Giảm'].sum(),2) )
##df31 =df31.sort_values(by="Điểm Giảm", ascending=False)
##fig3.add_trace(go.Bar(x=df3['Mã Tăng'], y=df3['Điểm Tăng'],name='Tích cực '+a))
#fig3.add_trace(go.Bar(x=df3['Mã Giảm'], y=df31['Điểm Giảm'],name='Tiêu cực '+b))
#fig3.update_layout(title='Tác Động Điểm Số '+id, xaxis_title='Time')

################Bieu do4#####################
fig2 = go.Figure()

# Thêm trace Scatter
fig2.add_trace(go.Bar(x=df4['time'], y=df4['vol'], name='GTGD'))
fig2.add_trace(go.Line(x=df4['time'], y=df4['tích luỹ'], name='GTGD Tích Luỹ'))
fig2.update_layout(title='GTGD Khối Ngoại '+id, xaxis_title='Time')


################Bieu do5#####################
fig5= go.Figure()
fig5.add_trace(go.Scatter(x=df5['time'],y=df5['GTGD Hôm nay'],name='GTGD Hôm nay',fill='tonexty',hovertemplate='<b>%{x}</b><br>%{y}',mode ='lines+text',line=dict(color='white')))
fig5.add_trace(go.Scatter(x=df5['time'],y=df5['GTGD TB5D'],name='GTGD TB 5 Ngày',fill='tozeroy',hovertemplate='<b>%{x}</b><br>%{y} ',mode ='lines+text',fillcolor="orange",line=dict(color='white')))
fig5.update_layout( xaxis_title='Thời gian',yaxis_title='GTGD', )
fig5.update_layout(title='GTGD Khớp Lệnh Trong Ngày '+id, xaxis_title='Time')

################Bieu do6#####################

fig6 = go.Figure()

fig6.add_trace(go.Scatter(
    x=df6['time'], y=df6['dư mua'], name='Dư bán',hoverinfo = 'text+x+y',
    mode='lines',
    line=dict(width=0.5, color='rgb(127, 166, 238)'),fillcolor='green',
    stackgroup='one'))



fig6.add_trace(go.Scatter(
    x=df6['time'], y=df6['dư bán'], name='Dư bán',hoverinfo = 'text+x+y',
    mode='lines',
    line=dict(width=0.5, color='rgb(127, 166, 238)'),fillcolor='red',
    stackgroup='one'))
fig6.add_trace(go.Line(
    x=df6['time'], y=df6['dư mua TB5'],name='dư mua TB5 phiên',
    mode='lines',
    line=dict(width=1.5,color ='yellow'),fillcolor='white',hoverinfo = 'text+x+y',
))

fig6.update_layout(
    showlegend=True,
    xaxis_type='category',
    yaxis=dict(
        type='linear',
        range=[1, 100],
        ticksuffix='%'))
fig6.update_layout(title='Dư Mua Dư Bán '+id, xaxis_title='Time')

###############Bieu do 7##################

fig7 = go.Figure()

fig7.add_trace(go.Scatter(
    x=df7['time'], y=df7['Mua Chủ Động'], name='Mua Chủ Động',hoverinfo = 'text+x+y',
    mode='lines',
    line=dict(width=0.5, color='rgb(127, 166, 238)'),fillcolor='green',
    stackgroup='one'))



fig7.add_trace(go.Scatter(
    x=df7['time'], y=df7['Bán Chủ Động'], name='Bán Chủ Động',hoverinfo = 'text+x+y',
    mode='lines',
    line=dict(width=0.5, color='rgb(127, 166, 238)'),fillcolor='red',
    stackgroup='one'))

fig7.add_trace(go.Line(
    x=df7['time'], y=df7['Mua Chủ Động']/df7['Bán Chủ Động'],name='Tỷ lệ',
    mode='lines',
    line=dict(width=1.5,color ='yellow'),fillcolor='white',hoverinfo = 'text+x+y',
))


fig7.update_layout(title='Cung Cầu Chủ Động '+id, xaxis_title='Time')

###############Bieu do 7##################

fig8 = go.Figure(go.Indicator(
    mode = "gauge+number+delta",
    value = df8['summary'].loc['buy'],
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': df8['summary'].loc['signal'], 'font': {'size': 24}},
    delta = {'reference': 21, 'increasing': {'color': "white"}},
    gauge = {
        'axis': {'range': [None, 21], 'tickwidth': 1, 'tickcolor': "green"},
        'bar': {'color': "lime"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "white",
        'steps': [
            {'range': [0, 5], 'color': 'red'},
            {'range': [5, 10], 'color': 'yellow'},
            {'range': [10, 15], 'color': 'green'},
            {'range': [15, 21], 'color': 'purple'}],
        'threshold': {
            'line': {'color': "green", 'width': 4},
            'thickness': 0.75,
            'value': 21}}))

fig8.update_layout( font = {'color': "white", 'family': "Arial"})
fig8.update_layout(title='Động Thái '+id, xaxis_title='Time')



my_con = st.container(border=True)
chart1,chart2,chart3= my_con.columns(3)

with chart1:
    st.plotly_chart(fig, use_container_width=True)
with chart2:
    st.plotly_chart(fig1, use_container_width=True)
with chart3:
    st.plotly_chart(fig2, use_container_width=True)
my_con = st.container(border=True)
chart4,chart5,chart6= my_con.columns(3)
with chart4:
    st.plotly_chart(fig7, use_container_width=True)
with chart5:
    st.plotly_chart(fig6, use_container_width=True)
with chart6:
    st.plotly_chart(fig5, use_container_width=True)

my_con = st.container(border=True)
chart7,chart8= my_con.columns(2)
with chart4:
    st.plotly_chart(fig7, use_container_width=True)
with chart5:
    st.plotly_chart(fig8, use_container_width=True)