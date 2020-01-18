import random as rnd
import time
import numpy as np
from scipy import signal

from helper import global_states as _g
from helper import brownian as _b
class cestica():
    
    def __init__(self,pot_tra):
        self.min_lt = 200 #100 1300
        self.max_lt = 500 # 500
        self.vrijeme_zivota = rnd.randint(self.min_lt, self.max_lt)
        
        self.minSkal = 0.1
        self.maxSkal = 0.5
        self.skaliraj=((self.vrijeme_zivota-self.min_lt)/(self.max_lt-self.min_lt))*(self.maxSkal-self.minSkal)+self.minSkal

        self.amplituda = rnd.uniform(-1,1)
        
        self.vjerojatnost_umjetnog = 0.10 if time.time()-_g.start < 4 else 0.5
        self.umjetni_snijeg = np.random.choice([True,False], p=[self.vjerojatnost_umjetnog,1-self.vjerojatnost_umjetnog])
        #self.umjetni_snijeg = False
        self.trenY = rnd.randint(9,10) if not self.umjetni_snijeg else pot_tra[1] #
        self.trenX = 0#rnd.uniform(-7,15) if not self.umjetni_snijeg else pot_tra[0] #
        # -7 15
        self.minZ = 0 # -5 0
        self.maxZ = 8
        self.trenZ = rnd.randint(self.minZ,self.maxZ) if not self.umjetni_snijeg else pot_tra[2] #
        
        self.deltaY = rnd.uniform(0.001,0.03)
        self.pomakX = rnd.uniform(-2,6) if not self.umjetni_snijeg else pot_tra[0]
        self.pomakZ = rnd.uniform(-1.0,4.0) if not self.umjetni_snijeg else pot_tra[2]
        
        if(self.umjetni_snijeg == False):
            # The Wiener process parameter.
            delta = 0.08
            # Total time.
            T = 100.0
            # Number of steps. # max_lt da nebude bound error
            N = self.vrijeme_zivota
            # Time step size
            dt = T/N
            # Number of realizations to generate.
            m = 1
            x = np.empty((m,N+1))
            #randX=rnd.uniform(-5, 5)
            x[:, 0] = self.trenX

            _b.brownian(x[:,0], N, dt, delta, out=x[:,1:])
           
            #self.trajectory = _b.smooth(x[0], 40)
            self.trajectory = list(signal.savgol_filter(x[0], 201, 7))
            self.index = 0

    def checkIFDead(self):
        return True if self.vrijeme_zivota <= 0  else False

    def checkIFCloseToDead(self):
        return True if self.vrijeme_zivota <= 100 and self.vrijeme_zivota >= 0 else False

