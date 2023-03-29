# CTRL + Enter uruchamia

# import copy
import numpy as np
import pandas as pd
from funkcje import isNotLegit, EMA, makeLegit

    
def symuluj(close, MACD, EMA9, wyniki, inp):
    def suma(p, cena, w):
        return p * cena + w
    portfel = 1000
    wolne_srodki = 0
    suma0 = suma(portfel, close[0], 0)

    for i in range(len(close)):
        if MACD[i] < EMA9[i]:
            #sprzedaje wszystko
            wolne_srodki += round(portfel * close[i], 6)
            portfel = 0
        elif MACD[i] > EMA9[i]:
            #kupuje ile sie da
            x = int(wolne_srodki / close[i])
            portfel += x
            wolne_srodki -= round(x * close[i], 6)
    
    sumaN = suma(portfel, close[-1], wolne_srodki)
    
    MACD = pd.DataFrame(MACD)
    EMA9 = pd.DataFrame(EMA9)
    MACD.to_csv("OUTPUT/"+inp+"_MACD.csv", index = False)
    EMA9.to_csv("OUTPUT/"+inp+"_SIGNAL.csv", index = False)
    
    print(inp)
    print("    przed: " + str(round(suma0, 2)))
    print("    po: " + str(round(sumaN, 2)))
    print("    zysk = " + str(round( ((sumaN - suma0) / suma0) * 100, 2)) + "%")
    
#     wyniki.append((alfa, round( ((sumaN - suma0) / suma0) * 100, 2)))
    
      
INPUT = ["MBK", "ALR", "MLS", "PKN", "EAT"]
wyniki = []
for inp in INPUT:
    close = list(pd.read_csv('INPUT/INPUT_' + inp + '.csv').values)
    for i in range(len(close)):
        close[i] = float(close[i][0])
    ile = 1000
    if len(close) >= ile:
        close = close[(len(close) - ile) : len(close)]
    else:
        print()
        print(inp + ": " + str(len(close)) + " < " + str(ile))
        
    makeLegit(close)
        
#     closeT = copy.deepcopy(close)
    EMA26 = np.array(EMA(26, 26, close))
    EMA12 = np.array(EMA(12, 26, close))

    MACD = EMA12 - EMA26
    EMA9 = EMA(9, 9, MACD)
    while len(EMA9) < len(EMA12):
        EMA9 = [EMA9[0]] + EMA9

    while len(close) > len(MACD):
        close.pop(0)
    symuluj(close, MACD, EMA9, wyniki, inp)

