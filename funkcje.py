import numpy as np
import pandas as pd


def isNotLegit(f):
    if type(f) != type(float()) or str(f) == "nan":
        return True
    else:
        return False
    
def EMA(n, uni, data):
    alfa = 2 / (n + 1)
    EMAN = []
    ciach = n - 1
    mianownik = 0
    for i in range(n):
        mianownik += pow(1 - alfa, i)
    for i in range(uni,len(data)):
        licznik = 0
        for j in range(i-ciach, i+1):
            licznik += (data[j] * pow(1 - alfa, i - j))
        EMAN.append(licznik/mianownik)
    return EMAN

def rachciach(vec1, vec2):
    if len(vec1) != len(vec2):
        print("nierowne wektory")
        return []
    def roznica(x, y):
        if x > y:
            return 1
        elif x == y:
            return 0
        else:
            return -1
    ciachy = []
    for i in range(len(vec1)):
        if vec1[i] == vec2[i]:
            ciachy.append(i)
        elif i < len(vec1) - 1 and roznica(vec1[i], vec2[i]) == -roznica(vec1[i+1], vec2[i+1]):
            ciachy.append(i + 1)
    return ciachy

def makeLegit(close):
    for i in range(len(close)):
        if isNotLegit(float(close[i])):
            if i == 0:
                close[i] = close[i + 1]
            elif i == len(close) - 1 or isNotLegit(close[i + 1]):
                close[i] = close[i - 1]
            else:
                close[i] = (close[i-1] + close[i+1]) / 2