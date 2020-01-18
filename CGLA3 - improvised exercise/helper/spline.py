import numpy as np

tocke=[]
#tocke.append([-25,15,-5,1])
tocke.append([-20,15,0,1])
tocke.append([-15,15,5,1])
tocke.append([-10,15,0,1])
tocke.append([-5,15,-5,1])
tocke.append([0,17,0,1])
tocke.append([5,17,5,1])
tocke.append([10,17,0,1])
tocke.append([15,17,-5,1])
tocke.append([20,17,0,1])
tocke.append([25,20,5,1])
tocke.append([30,20,0,1])
tocke.append([35,20,-5,1])
tocke.append([40,20,0,1])
tocke.append([45,22,5,1])
#tocke.append([50,22,0,1])
#tocke.append([55,22,-5,1])
tocke = np.array(tocke)
n=len(tocke)

#matrica = np.array([[-0.5,1.5,-1.5,0.5],[1,-2,1,0],[-0.5,0,0.5,0]])
#matrica2 = np.array([[-1/6,3/6,-3/6,1/6],[3/6,-1,3/6,0],[-3/6,0,3/6,0],[1/6,4/6,1/6,0]])

matrica2 = np.array([[-1/6,3/6,-3/6,1/6],[3/6,-1,3/6,0],[-3/6,0,3/6,0],[1/6,4/6,1/6,0]])
matrica  = np.array([[-0.5,1.5,-1.5,0.5],[1,-2,1,0],[-0.5,0,0.5,0]])

def vratiBrojTocaka():
    return n

def vrati4tockice(index):
    return np.array([tocke[index], tocke[index+1], tocke[index+2], tocke[index+3]])

def izrCilj():
    lista_ciljeva=[]
    koje_tocke=0
    for i in range(n-3):
        cilj=dict()
        cilj = {round(new_list,3): [] for new_list in np.arange(0,1,0.001)}
        chosen_tocke=None
        chosen_tocke = vrati4tockice(koje_tocke)
        for t in np.arange(0, 1+0.001, 0.001):
            t=round(t,3)
            uk = np.dot((3/8)*np.array([t*t*t, t*t, t, 1]), np.dot(matrica2, chosen_tocke))
            cilj[t] = uk
        lista_ciljeva.append(cilj)
        koje_tocke+=1
    return lista_ciljeva


def izrOrj():
    lista_orjentira=[]
    koje_tocke=0
    for i in range(n-3):
        orj =dict()
        orj = {round(new_list,3): [] for new_list in np.arange(0,1,0.001)}
        chosen_tocke=None
        chosen_tocke = vrati4tockice(koje_tocke)
        for t in np.arange(0, 1+0.001, 0.001):
            t=round(t,3)
            uk=np.dot(np.array([t*t, t, 1]), np.dot(matrica,chosen_tocke))
            orj[t] = uk
        lista_orjentira.append(orj)
        koje_tocke+=1
    return lista_orjentira