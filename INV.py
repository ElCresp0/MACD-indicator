import numpy as np
import pandas as pd
from funkcje import isNotLegit, EMA, makeLegit

    
def symuluj(close, MACD, EMA9):
    def suma(p, ceny, index, w):
        ret = 0
        for i in range(len(p)):
            ret += p[i]*ceny[i][index]
        return ret + w

    def buy(srodki, p, cena):
        x = int(srodki / cena)
        p += x
        srodki -= round(x * cena, 6)
        return (srodki, p)

    portfel = []
    for _ in range(len(close)):
        portfel.append(1000)
    wolne_srodki = 0
    suma0 = suma(portfel, close, 0, 0)

    for i in range(len(close[0])):
        worthIt = []
        for j in range(len(MACD)):
            worthIt.append((EMA9[j][i] - MACD[j][i], j)) #ponizej 0 - buy
        
        worthIt.sort()
        buyIt = []

        # sprzedaz
        for w in worthIt:
            # wariant 1)
            wolne_srodki += round(portfel[w[1]] * close[w[1]][i], 6)
            portfel[w[1]] = 0
            # wariant 2)
            # if w[0] > 0:
            #     wolne_srodki += round(portfel[w[1]] * close[w[1]][i], 6)
            #     portfel[w[1]] = 0
            if w[0] <= 0:
                buyIt.append(w)

        for b in buyIt:
            srodki = wolne_srodki / 2
            wolne_srodki -= srodki
            (srodki, portfel[b[1]]) = buy(srodki, portfel[b[1]], close[b[1]][i])
            wolne_srodki += srodki
        if len(buyIt) > 0:
            buy(wolne_srodki, portfel[buyIt[0][1]], close[buyIt[0][1]][i])
    
    sumaN = suma(portfel, close, -1, wolne_srodki)
    
    print("    przed: " + str(round(suma0, 2)))
    print("    po: " + str(round(sumaN, 2)))
    print("    zysk = " + str(round( ((sumaN - suma0) / suma0) * 100, 2)) + "%")
    
#     wyniki.append((alfa, round( ((sumaN - suma0) / suma0) * 100, 2)))
    
      
INPUT = ["MBK", "ALR", "MLS", "PKN", "EAT"]
MACD = []
EMA9 = []
CLOSE = []
for inp in INPUT:
    close = list(pd.read_csv('INPUT/INPUT_' + inp + '.csv').values)
    for i in range(len(close)):
        close[i] = float(close[i][0])
    ile = 950
    if len(close) >= ile:
        close = close[(len(close) - ile) : len(close)]
    else:
        print()
        print(inp + ": " + str(len(close)) + " < " + str(ile))
        
    makeLegit(close)
        
#     closeT = copy.deepcopy(close)
    EMA26 = np.array(EMA(26, 26, close))
    EMA12 = np.array(EMA(12, 26, close))

    TMACD = EMA12 - EMA26
    TEMA9 = EMA(9, 9, TMACD)
    while len(TEMA9) < len(EMA12):
        TEMA9 = [TEMA9[0]] + TEMA9

    while len(close) > len(TMACD):
        close.pop(0)
    MACD.append(TMACD)
    EMA9.append(TEMA9)
    CLOSE.append(close)
    
symuluj(CLOSE, MACD, EMA9)