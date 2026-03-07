import streamlit as st
import pandas as pd
import yfinance as yf
import FinanceDataReader as fdr
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("NS AI TERMINAL WEB")

# 종목 리스트
stocks = {
"삼성전자":"005930",
"SK하이닉스":"000660",
"NAVER":"035420",
"카카오":"035720",
"NVDA":"NVDA",
"AMD":"AMD",
"AAPL":"AAPL",
"MSFT":"MSFT",
"TSLA":"TSLA"
}

# 검색
ticker_input = st.text_input("종목 검색")

col1,col2 = st.columns([1,2])

# 패널
with col1:

    st.subheader("종목 패널")

    for name,ticker in stocks.items():

        df = yf.download(ticker,period="6mo")

        if len(df)==0:
            continue

        ma20 = df["Close"].rolling(20).mean().iloc[-1]
        ma60 = df["Close"].rolling(60).mean().iloc[-1]

        if ma20>ma60:
            trend="상승"
        else:
            trend="중립"

        st.write(name,trend)

# 차트
with col2:

    if ticker_input:

        ticker=ticker_input.upper()

        df = yf.download(ticker,period="1y")

        if len(df)==0:
            st.write("데이터 없음")

        else:

            df["MA20"]=df["Close"].rolling(20).mean()
            df["MA60"]=df["Close"].rolling(60).mean()

            fig,ax=plt.subplots()

            ax.plot(df["Close"],label="Price")
            ax.plot(df["MA20"],label="MA20")
            ax.plot(df["MA60"],label="MA60")

            ax.legend()

            st.pyplot(fig)

            if df["MA20"].iloc[-1]>df["MA60"].iloc[-1]:
                st.write("추세 : 상승")
            else:
                st.write("추세 : 중립")
