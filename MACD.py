import pandas as pd
import matplotlib.pyplot as plt

def isInDateRange(time, start,end):
    if (time >= start) & (time <= end):
        return True
    else:
        return False

def EMA(period,chart_data):
    alfa=2/(period+1)
    ema=[]

    for i in range(len(chart_data)):
        if i==0:
            ema.append(chart_data[i])
        else:
            ema.append(chart_data[i]*alfa+ema[i-1]*(1-alfa))
    return ema

def partial_chart(start,end):
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    pchart = chart[(chart['time'] >= start) & (chart['time'] <= end)]
    plt.figure(figsize=(14, 7))
    plt.plot(pchart['time'], pchart['close'], color='royalblue', label='EURUSD')
    plt.title(f'Wykres notowań od {start.strftime("%Y-%m-%d")} do {end.strftime("%Y-%m-%d")}')

    first_buy = True
    first_sell = True

    for i in range(len(buy_signals)):
        if isInDateRange(buy_signals[i], start, end):
            candle_stick = pchart.loc[pchart['time'] == buy_signals[i], 'close']
            index = candle_stick.index[0]
            price = candle_stick.values[0]
            plt.scatter(pchart['time'][index], price, color='darkgreen', marker='^', s=100, label='BUY Signal' if first_buy else "")
            first_buy = False
            #print(f'Buy at value: {price}')
            plt.annotate(f'{pchart["close"][index]}', (pchart['time'][index], price),
                         textcoords='offset points', xytext=(0, 30), ha='center', fontsize=10, color='darkgreen')

    for i in range(len(sell_signals)):
        if isInDateRange(sell_signals[i], start, end):
            candle_stick = pchart.loc[chart['time'] == sell_signals[i], 'close']
            index = candle_stick.index[0]
            price = candle_stick.values[0]
            plt.scatter(pchart['time'][index], price, color='red', marker='v', s=100,  label='Sell Signal' if first_sell else "")
            #print(f'Sell at value: {price}')
            plt.annotate(f'{pchart["close"][index]}', (pchart['time'][index], price),
                         textcoords='offset points', xytext=(0, -30), ha='center', fontsize=10, color='red')
            first_sell = False

    plt.xlabel('Data')
    plt.ylabel('Cena')
    plt.grid(True)
    plt.legend(loc=1)
    plt.show()

def partial_macd(start,end):
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    pchart = chart[(chart['time'] >= start) & (chart['time'] <= end)]
    #plt.figure(figsize=(30, 10))
    plt.figure(figsize=(14, 7))
    plt.plot(pchart['time'], pchart['MACD'], label='MACD', color='blue')
    plt.plot(pchart['time'], pchart['Signal'], label='Signal', color='tomato')

    first_buy = True
    first_sell = True

    for i in range(len(buy_signals)):
        if isInDateRange(buy_signals[i], start, end):
            candle_stick = pchart.loc[pchart['time'] == buy_signals[i], 'MACD']
            index = candle_stick.index[0]
            macd = candle_stick.values[0]
            plt.scatter(pchart['time'][index], macd, color='darkgreen', marker='^', s=100,  label='Buy Signal' if first_buy else "")
            plt.annotate(f'{pchart["close"][index]}', (pchart['time'][index], macd),
                         textcoords='offset points', xytext=(0, 30), ha='center', fontsize=10, color='darkgreen')
            first_buy = False

    for i in range(len(sell_signals)):
        if isInDateRange(sell_signals[i], start, end):
            candle_stick = pchart.loc[chart['time'] == sell_signals[i], 'MACD']
            index = candle_stick.index[0]
            macd = candle_stick.values[0]
            plt.scatter(pchart['time'][index], macd, color='red', marker='v', s=100,  label='Sell Signal' if first_sell else "")
            plt.annotate(f'{pchart["close"][index]}', (pchart['time'][index], macd),
                         textcoords='offset points', xytext=(0, -30), ha='center', fontsize=10, color='red')
            first_sell = False

    plt.title(f'Wykres MACD od {start.strftime("%Y-%m-%d")} do {end.strftime("%Y-%m-%d")}')
    plt.legend(loc=2)
    plt.grid(True)
    plt.show()

def wallet(start, end, stock_amount):
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    pchart = chart[(chart['time'] >= start) & (chart['time'] <= end)].reset_index(drop=True)

    starting_capital = stock_amount * pchart['close'][0]
    stocks = stock_amount
    available_funds = 0

    capital_over_time = []
    time_stamps = []

    buys=0
    sells =0
    wins = 0
    entry_price = pchart['close'][0]
    print('')
    print(f'Starting capital = {starting_capital}$')
    print(f'Available funds = {available_funds}$')
    print('')

    for i in range(len(pchart)):

        current_capital = available_funds + (stocks * pchart['close'][i])
        capital_over_time.append(current_capital)
        time_stamps.append(pchart['time'][i])

        if available_funds==0:
           if pchart['time'][i] in sell_signals:
               print(f"Selling {round(stocks, 2)} stocks at:{pchart['close'][i]}$ ")
               available_funds= stocks * pchart['close'][i]
               stocks = 0
               sells += 1
               if pchart['close'][i] > entry_price:
                   wins+=1
               print(f'Available funds = {round(available_funds, 2)}$')
               print("")

        else:
           if pchart['time'][i] in buy_signals:
                stocks = available_funds / pchart['close'][i]
                print(f"Buying {round(stocks, 2)} stocks at:{pchart['close'][i]}$")
                available_funds=0
                buys += 1
                entry_price = pchart['close'][i]
                print(f'Available funds = {round(available_funds, 2)}$')
                print("")

    if(stocks!=0):
        available_funds = stocks * pchart['close'].iloc[-1]

    print(f"At this moment wallet is worth {round(available_funds, 2)}$")
    print(f"Your profit is {round(available_funds-starting_capital, 2)}$")
    print(f"Buying positions: {buys}")
    print(f"Selling positions: {sells}")
    print(f"Winning positions: {wins}")

    plt.figure(figsize=(12, 5))
    plt.plot(time_stamps, capital_over_time, label="Kapitał", color="royalblue")
    plt.xlabel("Czas")
    plt.ylabel("Kapitał ($)")
    plt.title("Zmiana kapitału w czasie")
    plt.legend()
    plt.grid()
    plt.show()

chart=pd.read_csv('FX_EURUSD, 1D.csv')
chart['time'] = pd.to_datetime(chart['time'], unit='s')

chart['EMA12']=EMA(12, chart['high'])
chart['EMA26']=EMA(26, chart['high'])
chart['MACD']= chart['EMA12'] - chart['EMA26']
chart['Signal']=EMA(9, chart['MACD'])
#print(chart.head(50))

#wykres MACD
plt.figure(figsize=(30,10))
plt.plot(chart['time'],chart['MACD'], label='MACD', color='blue')
plt.plot(chart['time'],chart['Signal'], label='Signal', color='tomato')

buy_signals=[]
sell_signals=[]

first_buy = True
first_sell = True

for i in range(len(chart)):
    if chart['MACD'][i]>chart['Signal'][i] and chart['MACD'][i-1]<chart['Signal'][i-1]:
        buy_signals.append(chart['time'][i])
        plt.scatter(chart['time'][i],chart['MACD'][i],color='darkgreen', marker='^', s=100,  label='BUY Signal' if first_buy else "")
        first_buy = False
    elif chart['MACD'][i]<chart['Signal'][i] and chart['MACD'][i-1]>chart['Signal'][i-1]:
        plt.scatter(chart['time'][i], chart['MACD'][i], color='red',marker='v', s=100, label='SELL Signal' if first_sell else "")
        sell_signals.append(chart['time'][i])
        first_sell = False

plt.title('Wskaźnik MACD z miejscami kupna/sprzedaży', size=30)
plt.legend(loc=1, prop={'size': 20})
plt.grid(True)
plt.show()

#wykres notowań
plt.figure(figsize=(14,7))
plt.plot(chart['time'], chart['close'], color='royalblue', label='EURUSD')
plt.title('Notowania EURUSD')
plt.xlabel('Data')
plt.ylabel('Cena')
plt.grid(True)
plt.legend()
plt.show()

#wykres notowań z naniesionymi sygnałami
plt.figure(figsize=(14,7))
plt.plot(chart['time'], chart['close'], color='royalblue', label='EURUSD')
plt.title('Notowania EURUSD + sygnały')

first_buy = True
first_sell = True

for i in range(len(buy_signals)):
    candle_stick=chart.loc[chart['time'] == buy_signals[i], 'close']
    index=candle_stick.index[0]
    price=candle_stick.values[0]
    plt.scatter(chart['time'][index], price, color='darkgreen',marker='^', s=100, label='BUY Signal' if first_buy else "")
    first_buy = False

for i in range(len(sell_signals)):
    candle_stick=chart.loc[chart['time'] == sell_signals[i], 'close']
    index=candle_stick.index[0]
    price=candle_stick.values[0]
    plt.scatter(chart['time'][index], price, color='red',marker='v', s=100, label='Sell Signal' if first_sell else "")
    first_sell = False

plt.xlabel('Data')
plt.ylabel('Cena')
plt.grid(True)
plt.legend()
plt.show()

#Cały okres
partial_macd('2020-05-13','2025-03-01')
partial_chart('2020-05-13','2025-03-01')
wallet('2020-05-13','2025-03-01',1000)

#1. Okres wzrostów, 8 przecięć
#partial_chart('2020-05-03','2020-10-20')
#partial_macd('2020-05-03','2020-10-20')
#wallet('2020-05-03','2020-10-20',1000)

#2. Okres spadków, 8 przecięć
#partial_chart('2022-02-12','2022-05-20')
#partial_macd('2022-02-12','2022-05-20')
#wallet('2022-02-12','2022-05-20',1000)

#3. Okres dużych wahań i niestabilności, 8 przecięć
#partial_chart('2024-02-22','2024-06-02')
#partial_macd('2024-02-22','2024-06-02')
#wallet('2024-02-22','2024-06-02',1000)