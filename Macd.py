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
    plt.ylabel("Wartość jednej akcji ")


def macdAndSignalPlot(macdArray,signalArray):
    plt.figure(figsize=(17, 5))
    plt.plot(date[EMAL + SIGNAL:], macdArray[SIGNAL:], "r")
    plt.plot(date[EMAL + SIGNAL:], signalArray, "g")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xlim(date[EMAL], date[-1])
    # Ustawienie ticks na osi x, aby wyświetlać tylko styczniowe daty
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    plt.tight_layout()  # Dopasowanie layoutu
    plt.xticks(rotation=15)
    plt.subplots_adjust(bottom=0.1, top=0.9, left=0.05)
    plt.ylabel("Wartość średniej")
    plt.legend(["MACD","SIGNAL"],loc = "best")

    buy_points = buy(macdArray[SIGNAL:], signalArray, date[EMAL + SIGNAL:])
    sell_points = sell(macdArray[SIGNAL:], signalArray, date[EMAL + SIGNAL:])
    # Wyświetlanie punktów przecięcia na wykresie
    if buy_points:
        intersection_dates, intersection_values = zip(*buy_points)
        plt.scatter(intersection_dates, intersection_values, color='blue', marker='o')
    if sell_points:
        intersection_dates, intersection_values = zip(*sell_points)
        plt.scatter(intersection_dates, intersection_values, color='black', marker='x')

data = pd.read_csv('tsla_us_d.csv')
price = data['Otwarcie'].tolist()
date = pd.to_datetime(data['Data']).tolist()

# wykres ceny
pricePlot(date,price)
macdArray=macd(price)
signalArray=signal(macdArray)

# wykres macd i signal
macdAndSignalPlot(macdArray,signalArray)

plt.show()



