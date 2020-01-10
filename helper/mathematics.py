import numpy as np
import math
def calcNormala(v1,v2,v3):
    raz1 = [x1 - x2 for (x1, x2) in zip(v1, v2)]
    raz2 = [x1 - x2 for (x1, x2) in zip(v1, v3)]
    return np.cross(raz1, raz2)
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
       return v
    return v / norm
def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))
def length(v):
  return math.sqrt(dotproduct(v, v))
def angle(v1, v2):
  return math.acos(round(dotproduct(v1, v2) / (length(v1) * length(v2)),3))
def convertToDeg(kut):
    return kut *180/math.pi
def racunajOSR(poc, cilj):
    os = np.cross(poc, cilj)
    kut = angle(poc, cilj)
    kutUStupnjevima = convertToDeg(kut)
    return os, kutUStupnjevima
def racunajOS(poc, cilj, t):
    os = np.cross(poc[:3], cilj[t][:3])
    kut = angle(poc, cilj[round(t,2)])
    kutUStupnjevima = convertToDeg(kut)
    return os, kutUStupnjevima