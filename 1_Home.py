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
from vnstock_data.trading_insights import *
from vnstock_data.ohlc import *
from plotly.subplots import make_subplots
st.title("  :green[TRANG CHỦ]📊")
st.markdown('<span style="color:red"> 💻Phiên bản v1.1 </span>', unsafe_allow_html=True)
input = st.sidebar.selectbox("Dữ Liệu Đầu Vao:",['Giá Trị','Khối Lượng'])
symbol = st.sidebar.text_input("Chọn Mã ","Vnindex")
date= st.sidebar.radio('Option',['10 Ngày','1 Tháng','3 Tháng','6 Tháng','1 Năm'])
date1 = datetime.today().strftime('%Y-%m-%d')
st.markdown('Giao dịch khối ngoại')
def load_NN():
    df_NN = foreign_trade_data(symbol= symbol, start_date='2021-01-01', end_date=date1, limit=5000, page=1, lang='vi')
    df_NN = df_NN.sort_index(ascending=False)
    return df_NN
def load_tudoanh():
    df_TD = proprietary_trade_data(symbol=symbol, start_date='2022-01-01', end_date=date1,limit=1000, page=1, lang='vi')
    df_TD = df_TD.sort_index(ascending=False)
    return df_TD
def load_vnindex():
    df_VN= stock_historical_data (symbol=symbol, start_date='2021-01-01', end_date=date1, resolution='1D', type='stock', beautify=True, decor=True, source='ssi')
    return df_VN
df_VN=load_vnindex()
df_TD=load_tudoanh()
df_NN=load_NN()

fig1 = go.Figure()
if date == "10 Ngày":
    df_NN = df_NN.tail(10)
    df_VN = df_VN.tail(10)
    df_TD = df_TD.tail(10)
    df_NN["Giá tri tích luỹ"] = df_NN['GtMua'].cumsum() - df_NN['GtBan'].cumsum()
    df_TD["Giá tri tích luỹ"] = df_TD['GtMua'].cumsum() - df_TD['GtBan'].cumsum()

elif date == "1 Tháng":
    df_NN = df_NN.tail(21)
    df_VN = df_VN.tail(21)
    df_TD = df_TD.tail(21)
    df_NN["Giá tri tích luỹ"] = df_NN['GtMua'].cumsum() - df_NN['GtBan'].cumsum()
    df_TD["Giá tri tích luỹ"] = df_TD['GtMua'].cumsum() - df_TD['GtBan'].cumsum()

elif date == "3 Tháng":
    df_NN = df_NN.tail(65)
    df_VN = df_VN.tail(65)
    df_TD = df_TD.tail(65)
    df_NN["Giá tri tích luỹ"] = df_NN['GtMua'].cumsum() - df_NN['GtBan'].cumsum()
    df_TD["Giá tri tích luỹ"] = df_TD['GtMua'].cumsum() - df_TD['GtBan'].cumsum()

elif date == "6 Tháng":
    df_NN = df_NN.tail(120)
    df_VN = df_VN.tail(120)
    df_TD = df_TD.tail(120)
    df_NN["Giá tri tích luỹ"] = df_NN['GtMua'].cumsum() - df_NN['GtBan'].cumsum()
    df_TD["Giá tri tích luỹ"] = df_TD['GtMua'].cumsum() - df_TD['GtBan'].cumsum()

elif date == "1 Năm":
    df_NN = df_NN.tail(240)
    df_VN = df_VN.tail(240)
    df_TD = df_TD.tail(240)
    df_NN["Giá tri tích luỹ"] = df_NN['GtMua'].cumsum() - df_NN['GtBan'].cumsum()
    df_TD["Giá tri tích luỹ"] = df_TD['GtMua'].cumsum() - df_TD['GtBan'].cumsum()

if input =="Giá Trị":
    y1 = df_NN['GtMua']
    y2= df_NN['GtBan']
    z1 = y1-y2
    y11 = df_TD['GtMua']
    y22 = df_TD['GtBan']
    z11 = y11 - y22
elif input == "Khối Lượng":
    y1 = df_NN['KLMua']
    y2 = df_NN['KLBan']
    z1 = y1-y2
    y11 = df_TD['KLcpMua']
    y22 = df_TD['KlcpBan']
    z11 = y11 - y22
fig1.add_trace(go.Bar(x=df_NN['Ngay'], y=y1,name=input +' Mua', marker=dict(color='Green')))
fig1.add_trace(go.Bar(x=df_NN['Ngay'], y=y2*-1,name=input+' Bán', marker=dict(color='Red')))
fig1.add_trace(go.Line(x=df_NN['Ngay'], y=z1,name=input+' Ròng',marker=dict(color='yellow')))
fig1.update_layout(barmode ='relative')
fig1.update_layout(
    title=input +' Giao Dịch Khối Ngoại'+" Của "+ symbol,
    xaxis_title='Thời gian',
    yaxis_title='Giá trị',
    xaxis=dict(tickangle=40,tickmode='auto'),
    showlegend=True)
fig1.update_layout(
    yaxis=dict(title=input, side='left',  showgrid = False),
    yaxis2=dict(title='Chỉ số giá', side='right', overlaying='y',showgrid = False),
)

fig2 = go.Figure()
fig2 = make_subplots(specs=[[{"secondary_y": True}]])
fig2.add_trace(go.Line(x=df_NN['Ngay'], y=df_NN['Giá tri tích luỹ'],name='Luỹ kế NN',marker=dict(color='blue')))
fig2.add_trace(go.Line(x=df_NN['Ngay'], y=df_TD['Giá tri tích luỹ'],name='Luỹ kế TD',marker=dict(color='green')))
fig2.add_trace(go.Line(x=df_NN['Ngay'], y=df_VN['Close'],name='Giá',marker=dict(color='red')),secondary_y=True,)

fig2.update_layout(
    yaxis=dict(title=input, side='left',  showgrid = False),
    yaxis2=dict(title='Chỉ số giá', side='right', overlaying='y',showgrid = False),
    title="Tương quan giá và Giá Trị Ròng"+" Của "+ symbol,
    xaxis_title='Thời gian',
    yaxis_title='Giá trị',
    xaxis=dict(tickangle=40,tickmode='auto'),
    showlegend=True)
fig3 = go.Figure()
fig3.add_trace(go.Bar(x=df_TD['Ngay'], y=y11,name=input +' Mua', marker=dict(color='Green')))
fig3.add_trace(go.Bar(x=df_TD['Ngay'], y=y22*-1,name=input+' Bán', marker=dict(color='Red')))
fig3.add_trace(go.Line(x=df_TD['Ngay'], y=z11,name=input+' Ròng',marker=dict(color='yellow')))
fig3.update_layout(barmode ='relative')
fig3.update_layout(
    title=input +' Giao Dịch Tự Doanh'+" Của "+ symbol,
    xaxis_title='Thời gian',
    yaxis_title='Giá trị',
    xaxis=dict(tickangle=40,tickmode='auto'),
    showlegend=True)
fig3.update_layout(
    yaxis=dict(title=input, side='left',  showgrid = False),
    yaxis2=dict(title='Chỉ số giá', side='right', overlaying='y',showgrid = False),
)
Period = st.sidebar.selectbox("Chọn Khoảng Dữ Liêu",['1D','1W','1M','1Y'])
today = datetime.today().strftime('%Y-%m-%d')
yesterday = datetime.today()-timedelta(days=1)
yesterday = yesterday.strftime('%Y-%m-%d')
params = {
            "exchangeName": "HOSE,HNX",}
df = stock_screening_insights (params, size=1700, drop_lang='vi')

df = df[['ticker','marketCap','prev1DayGrowthPercent','priceGrowth1Week','prev1MonthGrowthPercent','prev1YearGrowthPercent']]
df =df.rename(columns={ 'ticker':'ticker',
                        'marketCap':'Vốn hoá',
                        'prev1DayGrowthPercent':'1D',
                        'priceGrowth1Week':'1W',
                        'prev1MonthGrowthPercent':'1M',
                        'prev1YearGrowthPercent':'1Y'})
df= df.dropna()
TongMcap = df['Vốn hoá'].sum()
df['Tỷ trọng'] = df['Vốn hoá']/TongMcap
vnindex = stock_historical_data("VNINDEX", yesterday, today, "1D", 'index')
vnindexC = vnindex['close']

if Period == '1D':
    df['Ảnh Hưởng D'] = df['Tỷ trọng']*df['1D']
    df['Điểm']= df['Ảnh Hưởng D']*vnindexC[0]/100
if Period == '1W':
    df['Ảnh Hưởng D'] = df['Tỷ trọng']*df['1W']
    df['Điểm']= df['Ảnh Hưởng D']*vnindexC[0]/100
if Period == '1M':
    df['Ảnh Hưởng D'] = df['Tỷ trọng']*df['1M']
    df['Điểm']= df['Ảnh Hưởng D']*vnindexC[0]/100
if Period == '1Y':
    df['Ảnh Hưởng D'] = df['Tỷ trọng']*df['1Y']
    df['Điểm']= df['Ảnh Hưởng D']*vnindexC[0]/100

df1= df.sort_values(by= "Điểm",ascending=False)
df1=df1.tail(9)
df2= df.sort_values(by= "Điểm",ascending=False)
df2=df2.head(9)
df3 = pd.concat([df1,df2],axis=0)
df3= df3.sort_values(by= "Điểm",ascending=False)
fig4 = go.Figure()
for index, row in df3.iterrows():
    color = 'green' if row['Điểm'] > 0 else 'red'
    fig4.add_trace(go.Bar(x=[row['ticker']], y=[row['Điểm']], marker=dict(color=color)))
    fig4.update_layout(showlegend=False,title=" ĐIỂM TÁC ĐỘNG ")

my_con = st.container(border=False)
chart1,chart2= my_con.columns(2)
with chart1:
    st.plotly_chart(fig1)
with chart2:
    st.plotly_chart(fig3)

chart3,chart4= my_con.columns(2)
with chart3:
    st.plotly_chart(fig2)
with chart4:
    st.plotly_chart(fig4)


st.markdown('HEATMAP')
@st.cache_data
def load_data_heatmap():
    df = fr_trade_heatmap(symbol='VNINDEX', report_type='Value')
    selected_col = ['stockSymbol','priceChangePercent','nmTotalTradedQty']
    new_df = df[selected_col]
    new_df.columns=['ticker','delta','volume']

    df1 = listing_companies()
    selected = ['ticker', 'sector']
    new_df1 = df1[selected]
    result1 = pd.merge(new_df, new_df1, on='ticker', how='inner')

    params = {
        "exchangeName": "HOSE,HNX,UPCOM",
    }
    df2 =stock_screening_insights (params, size=1700, drop_lang='vi')
    select_column = ['ticker', 'marketCap']
    new_df2 = df2[select_column]
    result = pd.merge(result1, new_df2, on='ticker', how='inner')
    df_final = result.dropna(subset=['delta','volume'],inplace=False)
    df_final['detla'] = round(df_final['delta'],4)
    df_final['delta'] = pd.to_numeric(df_final['delta'], errors='coerce')
    df_final = df_final.dropna(subset=['delta'])
    color_bin = [-100, -2, -1, 0, 1, 2, 100]
    df_final['colors'] = pd.cut(df_final['delta'], bins=color_bin, labels=['#750c1c', '#ba0f29', '#ed2644', '#40634c', '#378c35', '#2f5c2e'])
    return df_final
df_final = load_data_heatmap()
st.sidebar.markdown("### HEATMAP ###")

pick = ['volume','marketCap']
tieu_chi = st.sidebar.selectbox("Tiêu Chí", pick)
if tieu_chi:
    fig3 = px.treemap(df_final, path=[px.Constant("Biều đổ nhiệt Vnindex"), 'sector','ticker','delta'], values = tieu_chi, color='colors',
                        color_discrete_map ={'(?)':'#0c0f24', '#750c1c':'#750c1c', '#ba0f29':'#ba0f29','#ed2644':'#ed2644','#40634c':'#40634c','#378c35':'#378c35','#2f5c2e':'#2f5c2e'},
                        custom_data=['ticker', 'delta', 'volume'],
                        hover_data = {'delta':':.2f'},
                            )
    fig3.update_traces(hovertemplate='<b>%{label}</b><br>Volume: %{customdata[2]:.2f}<br>Delta: %{customdata[1]:.2f}%')
    fig3.update_traces(textposition='middle center')
    fig3.update_layout(title='----', margin=dict(t=0, l=0, r=0, b=0))
    fig3.update_layout(
            plot_bgcolor='#817f87',  # Màu nền của khu vực biểu đồ
            paper_bgcolor='#817f87',
        font=dict(color='#dce0dc'),  # Đặt màu chữ
        )
    font=dict(color='#dce0dc')
st.plotly_chart(fig3, use_container_width=True)


from module1 import worldindex
af1 = worldindex()
af1=af1.sort_values(by='changePercent',ascending=False)
fig4 = go.Figure(data=[go.Table(
    header=dict(values=['Chỉ số', 'Điểm','Thay Đổi'],
                line_color='darkgrey',
                fill_color='darkred',
                align='left'),
    cells=dict(values=[
                    af1.viName, # 1st column
                    af1.value,
                    round(af1.changePercent,2)

                                        ], # 2nd column
               line_color="darkgrey",
               fill_color='black',
               align='left',
            font_color=['red','white',['lime' if x >0  else
           "red" for x in list(af1.changePercent)]],
           height=23
           ))
])


from module1 import fdindex
af2 = fdindex()
af2=af2.sort_values(by='changePercent',ascending=False)
fig5 = go.Figure(data=[go.Table(
    header=dict(values=['Chỉ số', 'Điểm','Thay Đổi'],
                line_color='darkgrey',
                fill_color='darkred',
                align='left'),
    cells=dict(values=[
                    af2['viName'], # 1st column
                    af2['value'],
                    round(af2['changePercent'],2)

                                        ], # 2nd column
        line_color='darkgrey',
        # Màu sắc của ô dựa trên điều kiện
        align='left',
        font_color=['red','white',['lime' if x >0  else
           "red" for x in list(af2.changePercent)]],
           height=23
           ))
])

my_con = st.container(border=False)
chart4,chart5= my_con.columns(2)
with chart4:
    st.markdown('Chỉ Số Chứng Khoán')
    st.plotly_chart(fig4)
with chart5:
    st.markdown('Chỉ Số Hàng Hoá')
    st.plotly_chart(fig5)

###################################
from module1 import topNN
af3 = topNN()
af3=af3.sort_values(by='net',ascending=False)
fig6 = go.Figure(data=[go.Table(
    header=dict(values=['Mã', 'GT NN MUA','KL NN Bán','GT RÒNG'],
                line_color='darkgrey',
                fill_color='darkred',
                align='left'),
    cells=dict(values=[
                    af3.symbol, # 1st column
                    af3['buy']*af3['matchPrice']/1000000000,
                    af3['sell']*af3['matchPrice']/1000000000,
                    af3.net*af3['matchPrice']/1000000000

                                        ], # 2nd column
        line_color='darkgrey',
        # Màu sắc của ô dựa trên điều kiện
        align='left',
        font_color=['white','lime','red',['lime' if x >0  else
           "red" for x in list(af3.net)]],
           height=23
           ))
])
fig6.update_layout(title='Top GT NN MUA/BÁN')


from module1 import topchangeHSX
from module1 import topchangeHNX
af4 = topchangeHSX()
af5 = topchangeHNX()

fig7 = go.Figure(data=[go.Table(
    header=dict(values=['HSX', 'Thay đổi giá','HNX','Thay đổi giá'],
                line_color='darkgrey',
                fill_color='darkred',
                align='left'),
cells=dict(values=[
                    af4.symbol, # 1st column
                    af4.change,
                    af5.symbol,
                    af5.change

                                        ], # 2nd column
        line_color='darkgrey',
        # Màu sắc của ô dựa trên điều kiện
        align='left',
        font_color=['white',['#dc00ff' if x >0  else
           "aqua" for x in list(af4.change)],'white',['#dc00ff' if x >0  else
           "aqua" for x in list(af5.change)]],
           height=20
           ))
])
fig7.update_layout(title='Top Thay Đổi Giá')

from module1 import topvol

af6= topvol()

fig8 = go.Figure(data=[go.Table(
    header=dict(values=['Mã', 'Volume','%Thay dổi','TB 5D Vol'],
                line_color='darkgrey',
                fill_color='darkred',
                align='left'),
cells=dict(values=[
                    af6.symbol, # 1st column
                    af6.vol,
                    round(af6.changePercent,2),
                    round(af6.volPer5D,2)

                                        ], # 2nd column
        line_color='darkgrey',
        # Màu sắc của ô dựa trên điều kiện
        align='left',
        font_color=['white','lime',['lime' if x >0  else
           "red" for x in list(af6.changePercent)],'yellow'],
           height=20
           ))
])
fig8.update_layout(title='Top VOL')


my_con = st.container(border=True)
chart6,chart7= my_con.columns(2)
with chart6:
    st.plotly_chart(fig6)
with chart7:
    st.plotly_chart(fig7)


st.plotly_chart(fig8)
