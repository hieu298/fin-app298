import requests
import pandas as pd
import streamlit as st
from vnstock.chart import *
def market_breadth(exchange ='HOSE',period='1D',industry='ALL'):
    url = f'https://apipubaws.tcbs.com.vn/stock-insight/v1/intraday/market-breadth?exchange={exchange}&industry={industry}&type={period}'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data)
    data['time'] = data['b'].apply(lambda x: x.get('t'))
    data['Mã Tăng'] =data['b'].apply(lambda x: x.get('a'))
    data['Mã Giảm'] =data['b'].apply(lambda x: x.get('d'))
    data['Mã Đứng'] =data['b'].apply(lambda x: x.get('s'))
    data['time']=pd.to_datetime(data['time']).dt.strftime('%d-%m-%Y (%H:%M:%S)')
    return data

def list_ind():
    url=f'https://apipubaws.tcbs.com.vn/tcanalysis/v1/news/industries'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data)
    data['id'] = data['listIndustry'].apply(lambda x: x.get('code'))
    data['name'] = data['listIndustry'].apply(lambda x: x.get('name'))
    return data

def index(exchange ='HOSE',period='1d',industry='ALL'):

    url =f'https://apipubaws.tcbs.com.vn/stock-insight/v1/intraday/industry-index?exchange={exchange}&industry={industry}&type={period}'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data)
    data['time'] = data['data'].apply(lambda x: x.get('s'))
    data['time']=pd.to_datetime(data['time']).dt.strftime('%d-%m-%Y (%H:%M)')
    data['index']= data['data'].apply(lambda x: x.get('i'))
    data['volume'] = data['data'].apply(lambda x: x.get('v'))

    return data

def topanhhuong(exchange ='HOSE',industry ='ALL',period='1d'):
    url =f'https://apipubaws.tcbs.com.vn/stock-insight/v1/intraday/market-leader?roomCode={exchange}&industryCode={industry}&timeframe={period}'

    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data)
    data['Mã Tăng'] = data['listInc'].apply(lambda x: x.get('ticker'))
    data['Điểm Tăng'] = data['listInc'].apply(lambda x: x.get('s'))
    data['Mã Giảm'] = data['listDesc'].apply(lambda x: x.get('ticker'))
    data['Điểm Giảm'] = data['listDesc'].apply(lambda x: x.get('s'))

    return data


def KhoingoaiGD(exchange='HOSE',industry ='ALL',period='1w'):
    url = f'https://apipubaws.tcbs.com.vn/stock-insight/v1/intraday/market-foreign-vol?exchange={exchange}&industry={industry}&type={period}'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data)
    data['time'] = data['data'].apply(lambda x: x.get('t'))
    data['time'] = pd.to_datetime(data['time']).dt.strftime('%d-%m-%Y (%H:%M)')
    data['vol'] = data['data'].apply(lambda x: x.get('v'))
    data['tích luỹ'] = data['data'].apply(lambda x: x.get('av'))
    return data

def GTGD(exchange = 'HOSE',industry ='ALL'):
    url = f'https://apipubaws.tcbs.com.vn/stock-insight/v1/intraday/val?exchange={exchange}&idt2={industry}'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data)
    data['time'] = data['lstVal'].apply(lambda x: x.get('t'))
    data['time'] = pd.to_datetime(data['time']).dt.strftime('%d-%m-%Y (%H:%M)')
    data['GTGD Hôm nay'] = data['lstVal'].apply(lambda x: x.get('av'))
    data['GTGD TB5D'] = data['lstVal'].apply(lambda x: x.get('aav'))

    return data

def muaban(exchange= 'HOSE',industry ='ALL'):
    url = f'https://apipubaws.tcbs.com.vn/stock-insight/v1/intraday/market-bidask?exchange={exchange}&industry={industry}'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data)
    data['time'] = data['data'].apply(lambda x: x.get('s'))
    data['time'] = pd.to_datetime(data['time']).dt.strftime('%d-%m-%Y (%H:%M)')
    data['dư mua'] = data['data'].apply(lambda x: x.get('br'))
    data['dư mua TB5'] = data['data'].apply(lambda x: x.get('br5'))
    data['dư bán'] = 100 -data['dư mua']
    return data

def cungcau(exchange = 'HOSE',industry ='ALL'):
    url = f'https://apipubaws.tcbs.com.vn/stock-insight/v1/intraday/market-supply-demand?exchange={exchange}&idl2={industry}'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data)
    data['time'] = data['data'].apply(lambda x: x.get('t'))
    data['time'] = pd.to_datetime(data['time']).dt.strftime('%d-%m-%Y (%H:%M)')
    data['Mua Chủ Động'] = data['data'].apply(lambda x: x.get('bup'))
    data['Bán Chủ Động'] = data['data'].apply(lambda x: x.get('sdp'))
    return data

def indicator(exchange = 'HOSE',industry ='ALL'):
    url = f'https://apipubaws.tcbs.com.vn/stock-insight/v1/intraday/tcprice/{exchange}_{industry}/indicator'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data)
    return data

def phanloaindt(exchange='HOSE',industry ='ALL',period='1w'):
    url = f'https://apipubaws.tcbs.com.vn/stock-insight/v1/intraday/investor-classify?exchange={exchange}&industry={industry}&type={period}'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data)
    return data

def nganhindex():
    url = f'https://api-finfo.vndirect.com.vn/v4/industry_classification?q=industryLevel:2'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data['data'])
    data1 = data[['industryCode', 'vietnameseName']]
    data1 = data1.rename(columns={'industryCode': 'indexCode', 'vietnameseName': 'Ngành'})
    url1 = f'https://mkw-socket-v2.vndirect.com.vn/mkwsocketv2/industrychange'
    response1 = requests.get(url1)
    data2 = response1.json()
    data2 = pd.DataFrame(data2['data'])
    data3 = pd.merge(data1, data2, how='inner', on='indexCode')
    data3 = data3.rename(columns=
                         {'indexCode': 'Mã Ngành',
                          'indIndex': 'Điểm Số Ngành',
                          'Giá Hiện Tại': 'Chỉ số',
                          'indChgCr1D': 'Điểm Thay đổi 1D',
                          'indChgCr3D': 'Điểm Thay đổi 3D',
                          'indChgCr5D': 'Điểm Thay đổi 5D',
                          'indChgCrMd': 'Điểm Thay đổi từ đầu tháng ',
                          'indChgCrQd': 'Điểm Thay đổi từ đầu quý ',
                          'indChgCrYd': 'Điểm Thay đổi từ đầu năm',
                          'indChgCr1M': 'Điểm Thay đổi 1M',
                          'indChgPctCr1D': 'Thay đổi 1D',
                          'indChgPctCr3D': 'Thay đổi 3D',
                          'indChgPctCr5D': 'Thay đổi 5D',
                          'indChgPctCrMd': 'Giá Hiện Tại',
                          'indChgPctCrQd': 'Giá Hiện Tại',
                          'indChgPctCrYd': 'Giá Hiện Tại',
                          'indChgPctCr1M': 'Thay đổi 1M',
                          'indChgPctCr3M': 'Thay đổi 3M',
                          'indChgPctCr6M': 'Thay đổi 6M',
                          'indChgPctCr1Y': 'Thay đổi 1Y',
                          'indChgPctCr3Y': 'Giá Hiện Tại',
                          'indChgPctCr5Y': 'Giá Hiện Tại', }
                         )
    new_data = data3[['Mã Ngành', 'Ngành', 'Điểm Số Ngành', 'Thay đổi 1D', 'Thay đổi 3D', 'Thay đổi 5D', 'Thay đổi 1M',
                      'Thay đổi 3M', 'Thay đổi 6M', 'Thay đổi 1Y']]
    return new_data

def worldindex():
    url = f'https://athenaaws.tcbs.com.vn/athena/v1/worldIndexes'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data['data'])
    return data

def fdindex():
    url = f'https://athenaaws.tcbs.com.vn/athena/v1/futureIndexes'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data['data'])
    return data

def topNN():
    url = f'https://athenaaws.tcbs.com.vn/athena/v1/topFE'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data['data'])
    return data


def topchangeHSX():
    url = f'https://athenaaws.tcbs.com.vn/athena/v1/topChange'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data)
    data1 = data['indexes'].iloc[0]
    data2 =pd.DataFrame(data1['data'])
    return data2
def topchangeHNX():
    url = f'https://athenaaws.tcbs.com.vn/athena/v1/topChange'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data)
    data1 = data['indexes'].iloc[1]
    data2 =pd.DataFrame(data1['data'])
    return data2

def topvol():
    url = f'https://athenaaws.tcbs.com.vn/athena/v1/topTradingVol'
    response = requests.get(url)
    data = response.json()
    data = pd.DataFrame(data)
    data1 = data['indexes'].iloc[0]
    data2 = pd.DataFrame(data1['data'])
    return data2