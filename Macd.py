import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

EMAL =26 #exponential moving average long term average
EMAS =12 #exponential moving average long short average
SIGNAL = 9 #exponential moving average
def alpha(n):
    return 2/(n+1)
def up(value,index,days):
    ratio = 1-alpha(days)
    sum=0
    for i in range(days+1):
        sum+=value[index-i]*ratio**i
    return sum
def down(days):
    ratio = 1 - alpha(days)
    sum=0
    for i in range(days+1):
        sum+=ratio**i
    return sum

def exponentialMovingAverage(value,index,days):
    return up(value,index,days)/down(days)

def macd(value):
    macdArray = []
    for i in range(len(value)-EMAL):
        macdArray.append(exponentialMovingAverage(value,i+EMAL,12)-exponentialMovingAverage(value,i+EMAL,EMAL))

    return macdArray

def signal(value):
    signalArray = []
    for i in range(len(value)-SIGNAL):
        signalArray.append(exponentialMovingAverage(value,i+SIGNAL,SIGNAL))
    return signalArray
def buy(f1, f2, dates):
    intersect = []
    for i in range(len(f1)-1):
        a= f1[i] - f2[i]
        b=f1[i+1] - f2[i+1]
        if a*b <0 and f1[i]<f2[i]:
            intersect.append((dates[i], (f1[i]+f1[i+1])/2))  # Dodajemy parę (data, wartość)
    return intersect

def sell(f1, f2, dates):
    intersect = []
    for i in range(len(f1)-1):
        a= f1[i] - f2[i]
        b=f1[i+1] - f2[i+1]
        if a*b <0 and f1[i]>f2[i]:
            intersect.append((dates[i], (f1[i]+f1[i+1])/2))  # Dodajemy parę (data, wartość)
    return intersect

def simulation(price,macdArray,signalArray,date):
    limitedPrice =price[EMAL+SIGNAL:]
    wallet = 0
    stockAmount = 1000#ile akcji na poczatek
    limitedData = date[EMAL + SIGNAL:]
    buy_points = buy(macdArray[SIGNAL:], signalArray, limitedData)
    sell_points = sell(macdArray[SIGNAL:], signalArray, limitedData)
    [buyDay, _ ] = buy_points[0]
    [sellDay, _ ] = sell_points[0]
    buyIndex=0
    sellIndex=0
    for i in range(len(limitedData)-1):
        wallet = np.trunc(wallet * 100) / 100
        value = (limitedPrice[i] + limitedPrice[i + 1]) / 2# srednia z dnia zakupu i dnia poprzeniego aby lepiej oddać faktyczna sytuacje
        #value = limitedPrice[i]
        #kupno
        if(limitedData[i]==buyDay and wallet>value):

            stockBuy = int(wallet/value)
            wallet = wallet - stockBuy*value
            stockAmount = stockBuy
            if buyIndex<len(buy_points)-1:
                buyIndex+=1
                [buyDay, _ ] = buy_points[buyIndex]
            #sprzedaż
        elif (limitedData[i]==sellDay and stockAmount>0):
            wallet = wallet +value*stockAmount
            if sellIndex<len(sell_points)-1:
                sellIndex+=1
                [sellDay, _ ] = sell_points[sellIndex]

    #na koniec sprzedaz

    if stockAmount>0:
        wallet = wallet + price[-1] * stockAmount

    wallet = np.trunc(wallet * 100) / 100
    return wallet
def pricePlot(date ,price):
    plt.figure(figsize=(17, 5))
    plt.plot(date[EMAL:], price[EMAL:])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xlim(date[EMAL], date[-1])
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    plt.tight_layout()  # Dopasowanie layoutu
    plt.xticks(rotation=15)
    plt.subplots_adjust(bottom=0.1,top=0.9,left=0.05)
    plt.title("TESLA")
    plt.ylabel("Wartość jednej akcji w dolarach [$] ")

def macdAndSignalPlot(date,macdArray,signalArray,month=4):
    plt.figure(figsize=(17, 5))
    plt.plot(date[EMAL + SIGNAL:], macdArray[SIGNAL:], "r")
    plt.plot(date[EMAL + SIGNAL:], signalArray, "g")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xlim(date[EMAL], date[-1])
    # Ustawienie ticks na osi x, aby wyświetlać tylko styczniowe daty
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=month))
    plt.tight_layout()  # Dopasowanie layoutu
    plt.xticks(rotation=15)
    plt.subplots_adjust(bottom=0.1, top=0.9, left=0.05)
    plt.ylabel("Wartość średniej")

    buy_points = buy(macdArray[SIGNAL:], signalArray, date[EMAL + SIGNAL:])
    sell_points = sell(macdArray[SIGNAL:], signalArray, date[EMAL + SIGNAL:])
    # Wyświetlanie punktów przecięcia na wykresie
    if buy_points:
        intersection_dates, intersection_values = zip(*buy_points)
        plt.scatter(intersection_dates, intersection_values, color='blue', marker='o')

    if sell_points:
        intersection_dates, intersection_values = zip(*sell_points)
        plt.scatter(intersection_dates, intersection_values, color='black', marker='x')
        plt.legend(["MACD", "SIGNAL","Buy Points","Sell Points"], loc="best",fontsize=15)

    plt.axhline(y=0, color='k')

def currencyPlot(date ,price):
    plt.figure(figsize=(17, 5))
    plt.plot(date, price)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xlim(date[0], date[-1])
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=12))
    plt.tight_layout()  # Dopasowanie layoutu
    plt.xticks(rotation=15)
    plt.subplots_adjust(bottom=0.1,top=0.9,left=0.05)
    plt.title("EUR/PLN")
    plt.ylabel("Cena EUR w PLN ")

def profit(start,end):
    return ((end-start)/start)*100

data = pd.read_csv('tsla_us_d.csv')
price = data['Otwarcie'].tolist()
date = pd.to_datetime(data['Data']).tolist()

currencyData = pd.read_csv('eurpln_w.csv')
currencyPrice = currencyData['Otwarcie'].tolist()
currencyDate = pd.to_datetime(currencyData['Data']).tolist()

currencyPlot(currencyDate,currencyPrice)
currencyMacdArray=macd(currencyPrice)
currencySignalArray=signal(currencyMacdArray)

macdAndSignalPlot(currencyDate,currencyMacdArray,currencySignalArray,12)

# wykres ceny
pricePlot(date,price)
macdArray=macd(price)
signalArray=signal(macdArray)

# wykres macd i signal
macdAndSignalPlot(date,macdArray,signalArray)


wallet = simulation(price,macdArray,signalArray,date)
print("TESLA")
print("kapitał poczatkowy: ",1000*price[EMAL+SIGNAL],"$")
print("wartość portfela na koniec: ",wallet,"$")
print("zysk: ",round(profit(1000*price[EMAL+SIGNAL],wallet),2),"%")
wallet = simulation(currencyPrice,currencyMacdArray,currencySignalArray,currencyDate)
print("EUR/PLN")
print("kapitał poczatkowy: ",1000*currencyPrice[EMAL+SIGNAL],"PLN")
print("wartość portfela na koniec: ",wallet,"PLN")
print("zysk: ",round(profit(1000*currencyPrice[EMAL+SIGNAL],wallet),2),"%")


plt.show()



