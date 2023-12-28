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

from module1 import nganhindex
st.header(':green[NGÀNH]📈📈')
df0 = nganhindex()
a =st.selectbox('Khoảng thời gian',['1 Ngày','1 Tuần','1 Tháng','3 Tháng','6 Tháng','1 Năm'])
if a =='1 Ngày':
    df00 = df0[['Ngành','Thay đổi 1D']].sort_values(by="Thay đổi 1D")
    x = df00['Thay đổi 1D']
elif a =='1 Tuần':
    df00 = df0[['Ngành','Thay đổi 5D']].sort_values(by="Thay đổi 5D")
    x = df00['Thay đổi 5D']
elif a =='1 Tháng':
    df00 = df0.sort_values(by="Thay đổi 1M")
    x = df00['Thay đổi 1M']
elif a =='3 Tháng':
    df00 = df0.sort_values(by="Thay đổi 3M")
    x = df00['Thay đổi 3M']
elif a =='6 Tháng':
    df00 = df0.sort_values(by="Thay đổi 6M")
    x = df00['Thay đổi 6M']
elif a =='1 Năm':
    df00 = df0.sort_values(by="Thay đổi 1Y")
    x = df00['Thay đổi 1Y']
fig = go.Figure(go.Bar(
            x=x,
            y=df00['Ngành'],
            orientation='h',
            text=round(x,2).apply(lambda x:f'{x}%'),  # Thêm giá trị text
            textposition='outside',
            marker=dict(
                color=x.apply(lambda x: 'green' if x > 0 else 'red'),
        # Vị trí văn bản bên trong thanh
)))
fig.update_layout(
    title='Diễn Biến Ngành '+ a,
    xaxis_title='Thay đổi',
    yaxis_title='Ngành')

st.plotly_chart(fig,use_container_width=True)

#########################################



from module1 import topanhhuong
st.header(':green[TÁC ĐỘNG THỊ TRƯỜNG]')
exchange = st.selectbox('Sở GD',['HOSE','HNX','UPCOM',])
period =st.selectbox('Khoảng thời gian',['1d','1w','1M'])
df1= topanhhuong(exchange=exchange,industry='ALL',period=period)
fig1 = go.Figure()
df11= df1[['Mã Giảm','Điểm Giảm']]
a = round(df1['Điểm Tăng'].sum(),2)
a= str(a)
b =str(round(df1['Điểm Giảm'].sum(),2))
df11 =df11.sort_values(by="Điểm Giảm", ascending=False).reset_index(drop=True)
fig1.add_trace(go.Bar(x=df1['Mã Tăng'], y=df1['Điểm Tăng'],name='Tích cực '+a,text=df1['Điểm Tăng'],textposition='outside',marker_color='grey'))
fig1.add_trace(go.Bar(x=df11['Mã Giảm'], y=df11['Điểm Giảm'],name='Tiêu cực '+b,text=df11['Điểm Giảm'],textposition='outside',marker_color='red'))
fig1.update_layout(title='Tác Động Điểm Số '+exchange+"  "+ period, xaxis_title='Time')
##################################################
from module1 import  GTGD
df2 = GTGD(exchange=exchange)
fig2= go.Figure()
fig2.add_trace(go.Scatter(x=df2['time'],y=df2['GTGD Hôm nay'],name='GTGD Hôm nay',fill='tonexty',hovertemplate='<b>%{x}</b><br>%{y}',mode ='lines+text',fillcolor="red",line=dict(color='white')))
fig2.add_trace(go.Scatter(x=df2['time'],y=df2['GTGD TB5D'],name='GTGD TB 5 Ngày',fill='tozeroy',hovertemplate='<b>%{x}</b><br>%{y} ',mode ='lines+text',fillcolor="grey",line=dict(color='white')))
fig2.update_layout( xaxis_title='Thời gian',yaxis_title='GTGD', )
fig2.update_layout(title='GTGD Khớp Lệnh Trong Ngày '+exchange+"  "+ period, xaxis_title='Time')

##############################################
from module1 import market_breadth
df3 = market_breadth(exchange =exchange,period=period,industry='ALL')

fig3 = go.Figure()

fig3.add_trace(go.Scatter(
    x=df3['time'], y=df3['Mã Tăng'],name='Mã Tăng',
    mode='lines',
    line=dict(width=0.5, color='rgb(184, 247, 212)'),fillcolor='green',
    stackgroup='one',
    groupnorm='percent', # sets the normalization for the sum of the stackgroup
    hoverinfo = 'text+x+y',
))


fig3.add_trace(go.Scatter(
    x=df3['time'], y=df3['Mã Đứng'], name='Mã Đứng',hoverinfo = 'text+x+y',
    mode='lines',
    line=dict(width=0.5, color='rgb(127, 166, 238)'),fillcolor='orange',
    stackgroup='one'))

fig3.add_trace(go.Scatter(
    x=df3['time'], y=df3['Mã Giảm'],name='Mã Giảm',
    mode='lines',
    line=dict(width=0.5, color='rgb(111, 231, 219)'),fillcolor='red',hoverinfo = 'text+x+y',
    stackgroup='one'
))

fig3.update_layout(
    title= 'Biến Động Thị Trường '+exchange +"  "+ period ,
    showlegend=True,
    xaxis_type='category',
    yaxis=dict(
        type='linear',
        range=[1, 100],
        ticksuffix='%'))


###########################
from module1 import muaban
df4 = muaban(exchange=exchange,industry='ALL')

fig4 = go.Figure()

fig4.add_trace(go.Scatter(
    x=df4['time'], y=df4['dư mua'], name='Dư bán',hoverinfo = 'text+x+y',
    mode='lines',
    line=dict(width=0.5, color='rgb(127, 166, 238)'),fillcolor='green',
    stackgroup='one'))



fig4.add_trace(go.Scatter(
    x=df4['time'], y=df4['dư bán'], name='Dư bán',hoverinfo = 'text+x+y',
    mode='lines',
    line=dict(width=0.5, color='rgb(127, 166, 238)'),fillcolor='red',
    stackgroup='one'))

fig4.add_trace(go.Line(
    x=df4['time'], y=df4['dư mua TB5'],name='dư mua TB5 phiên',
    mode='lines',
    line=dict(width=2,color ='yellow'),fillcolor='white',hoverinfo = 'text+x+y',))
fig4.update_layout(
    title= 'Dư Mua/Bán Trong Ngày '+exchange,
    showlegend=True,
    xaxis_type='category',
    yaxis=dict(
        type='linear',
        range=[1, 100],
        ticksuffix='%'))


#######################################
from module1 import cungcau
df5 = cungcau(exchange=exchange,industry='ALL')
fig5= go.Figure()

fig5.add_trace(go.Scatter(
    x=df5['time'], y=df5['Mua Chủ Động'], name='Mua Chủ Động',hoverinfo = 'text+x+y',
    mode='lines',
    line=dict(width=0.5, color='rgb(127, 166, 238)'),fillcolor='green',
    stackgroup='one'))



fig5.add_trace(go.Scatter(
    x=df5['time'], y=df5['Bán Chủ Động'], name='Bán Chủ Động',hoverinfo = 'text+x+y',
    mode='lines',
    line=dict(width=0.5, color='rgb(127, 166, 238)'),fillcolor='red',
    stackgroup='one'))

fig5.add_trace(go.Line(
    x=df5['time'], y=df5['Mua Chủ Động']/df5['Bán Chủ Động'],name='Tỷ lệ',
    mode='lines',
    line=dict(width=1.5,color ='yellow'),fillcolor='white',hoverinfo = 'text+x+y',
))
fig5.update_layout(title='Cung Cầu Chủ Động Trong Ngày '+exchange, xaxis_title='Time')
##########################################
from module1 import index
df6= index(exchange=exchange,industry='ALL',period=period)
import plotly.subplots as sp
import plotly.graph_objects as go
fig6 =go.Figure()
fig6 = sp.make_subplots(specs=[[{"secondary_y": True}]])
# Thêm trace cho giá (line)
fig6.add_trace(go.Line(x=df6['time'], y=df6['index'], name='index',mode='lines',line=dict(color ='red',width=2)))
# Thêm trace cho khối lượng (cột)
fig6.add_trace(go.Bar(x=df6['time'], y=df6['volume'], name='Volume',marker=dict(color='grey')), secondary_y=True)
# Cập nhật layout
fig6.update_layout(title='Chỉ số '+exchange+"  "+period)
# Cập nhật trục y thứ nhất
fig6.update_yaxes(title_text='Index', secondary_y=False,showgrid=False)

my_con = st.container(border=True)
chart1,chart2= my_con.columns(2)
with chart1:
    st.plotly_chart(fig6, use_container_width=True)
with chart2:
    st.plotly_chart(fig1, use_container_width=True)

my_con = st.container(border=True)
chart3,chart4= my_con.columns(2)
with chart3:
    st.plotly_chart(fig2, use_container_width=True)
with chart4:
    st.plotly_chart(fig3, use_container_width=True)

my_con = st.container(border=True)
chart4,chart5= my_con.columns(2)
with chart4:
    st.plotly_chart(fig4, use_container_width=True)
with chart5:
    st.plotly_chart(fig5, use_container_width=True)

