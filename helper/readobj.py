
def readOBJ(filename):
    with open(filename, "r") as f:
        txt=f.readlines()
    v,f=[],[]
    for line in txt:
        if(line[0] == 'v'):
            v.append(list(map(lambda x: float(x),line[1:].split())))
        elif(line[0] == 'f'):
            f.append(list(map(lambda x: int(x)-1,  line[1:].split())))

    sta,nda,rda=[],[],[]
    for poligon in f:
        sta.append(v[poligon[0]])
        nda.append(v[poligon[1]])
        rda.append(v[poligon[2]])
    
    return sta,nda,rda