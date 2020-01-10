import random as rnd
import time
import numpy as np

from helper import global_states as _g

class cestica():
    
    def __init__(self,pot_tra):
        self.min_lt = 100#1300
        self.max_lt = 500
        self.vrijeme_zivota = rnd.randint(self.min_lt, self.max_lt)
        
        self.minSkal = 0.1
        self.maxSkal = 0.5
        self.skaliraj=((self.vrijeme_zivota-self.min_lt)/(self.max_lt-self.min_lt))*(self.maxSkal-self.minSkal)+self.minSkal

        self.amplituda = rnd.uniform(-1,1)
        
        self.vjerojatnost_umjetnog = 0.2 if time.time()-_g.start < 3 else 0.8
        self.umjetni_snijeg = np.random.choice([True,False], p=[self.vjerojatnost_umjetnog,1-self.vjerojatnost_umjetnog])
        #self.umjetni_snijeg = False
        self.trenY = rnd.randint(5,10) if not self.umjetni_snijeg else pot_tra[1] #
        self.trenX = rnd.uniform(-7,15) if not self.umjetni_snijeg else pot_tra[0] #

        self.minZ = -5
        self.maxZ = 0
        self.trenZ = rnd.randint(self.minZ,self.maxZ) if not self.umjetni_snijeg else pot_tra[2] #
        if self.umjetni_snijeg == True:
            #print(pot_tra) 
            pass
        
        self.deltaY = rnd.uniform(0.001,0.03)
        self.pomakX = rnd.uniform(-2,6) if not self.umjetni_snijeg else pot_tra[0]
        self.pomakZ = rnd.uniform(-2.0,2.0) if not self.umjetni_snijeg else pot_tra[2]
    def checkIFDead(self):
        return True if self.vrijeme_zivota <= 0 else False

    def checkIFCloseToDead(self):
        return True if self.vrijeme_zivota <= 50 and self.vrijeme_zivota >= 0 else False

