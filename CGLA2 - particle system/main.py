# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 18:43:40 2019

@author: lukab
"""
import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import factorial
from PIL import Image
import random as rnd
import math
import time

class cestica():
    def __init__(self):
        self.min_lt = 500#1300
        self.max_lt = 1000
        self.vrijeme_zivota = rnd.randint(self.min_lt, self.max_lt)
        #vrijeme zivota proporcionalno sa skaliraj
        
        self.minSkal = 0.1
        self.maxSkal = 0.5
        #self.skaliraj = rnd.uniform(0.1,0.4)
        self.skaliraj=((self.vrijeme_zivota-self.min_lt)/(self.max_lt-self.min_lt))*(self.maxSkal-self.minSkal)+self.minSkal
            
        #new_value = ( (old_value - old_min) / (old_max - old_min) ) * (0.4 - 0.1) + 0.1
        self.mnozi = -1 #NOT YET IMPLEMENTED
        
        #alfa prop sa vrijeme zivota TODO
        self.amplituda = rnd.uniform(-1,1)
        self.trenY = rnd.randint(4,5)
        self.trenX = rnd.uniform(-50,50)
        #self.trenZ = rnd.choice([0,-3,4])
        #MAKE Z PROPORTIONAL TO SKALIRAJ
        self.minZ = 0#-3
        self.maxZ = 8
        self.trenZ = rnd.randint(self.minZ,self.maxZ)
        #self.trenZ = closest([0,7],(((self.skaliraj-self.minSkal)/(self.maxSkal-self.minSkal))*(self.maxZ-self.minZ)+self.minZ))
        self.deltaY = rnd.uniform(0.001,0.03)#0.01
        self.pomakX=rnd.uniform(-2,6)
        self.pomakZ=rnd.uniform(-1.0,4.0)

    def checkIFDead(self):
        return True if self.vrijeme_zivota <= 0 else False
    
    def checkIFCloseToDead(self):
        return True if self.vrijeme_zivota <= 50 and self.vrijeme_zivota >= 0 else False

class texture():
    def __init__(self):
        self.ids = self.genTexture()
    
    def genTexture(self):
        i=0
        ids=[]
        #ID=np.array([0,1,2,3,4])
        #ID = glGenTextures(5)
        
        for i in range(0,len(sustav)):
            #print(i)
            #print(ID[i])
            ID = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, ID)
            
           
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, im.size[0], im.size[1],0,GL_RGBA, GL_UNSIGNED_BYTE, imgData)
            
            #glBindTexture(GL_TEXTURE_2D, 0)
            ids.append(ID)
        return ids
'''
v1=[-1.0, 0.0, 0.0]
v2=[ 1.0, 0.0, 0.0]
v3=[ 1.0, 2.0, 0.0]
v4=[-1.0, 2.0, 0.0]
'''
v1=[-0.25, -0.25, 0.0]
v2=[ 0.25, -0.25, 0.0]
v3=[ 0.25,  0.25, 0.0]
v4=[-0.25,  0.25, 0.0]
tC = [[0.0,0.0,0.0],[1.0,0.0,0.0],[1.0,1.0,0.0],[0.0,1.0,0.0]]
nikad_vise=False
r=None
ociste = np.array([-10,3,15])
ar_sred_ravn = np.array([np.mean([v1[0],v2[0],v3[0],v4[0]]), np.mean([v1[1],v2[1],v3[1],v4[1]]), np.mean([v1[2],v2[2],v3[2],v4[2]])]) #

sustav=dict()
sustav = { new_list: None for new_list in range(0,150)}
for i in range(0,len(sustav)):
    sustav[i] = cestica()

#--TEXTURE PART--
#imageName="./.obj/snow.bmp"
imageName="./.obj/snow3.tga"
#imageName="./.obj/iskrica.tga"
#imageName="./.obj/flake_big.tga"
#imageName="./.obj/flake_big.png"
im = Image.open(imageName)
dur=list(im.getdata())
imgData=np.array(dur,dtype=np.uint32)
#--TEXTURE PART--

#--STABLO PART--
with open("./.obj/stablo.obj", "r") as f:
    txt=f.readlines()
v=[]
f=[]
for line in txt:
    if(line[0] == 'v'):
        v.append(line[1:].split())
    elif(line[0] == 'f'):
        f.append(line[1:].split())

for i in range(len(f)):
    for j in range(3):
        f[i][j] = int(f[i][j])
        f[i][j]-=1
for i in range(len(v)):
    for j in range(3):
        v[i][j] = float(v[i][j])
v=np.array(v)

Ap_crtaj4 = []
for i,tocka in enumerate(v):
    tockaV = np.insert(tocka, len(tocka), 1)
    Ap_crtaj4.append(tockaV)
x1l=[]
y1l=[]
x2l=[]
y2l=[]
x3l=[]
y3l=[]
z1l=[]
z2l=[]
z3l=[]

for i,poligon in enumerate(f):
    for j,svaki in enumerate(poligon):
        if j==0:
            x1=Ap_crtaj4[svaki][0]
            y1=Ap_crtaj4[svaki][1]
            z1=Ap_crtaj4[svaki][2]
            x1l.append(x1)
            y1l.append(y1)
            z1l.append(z1)
        elif j==1:
            x2=Ap_crtaj4[svaki][0]
            y2=Ap_crtaj4[svaki][1]
            z2=Ap_crtaj4[svaki][2]
            x2l.append(x2)
            y2l.append(y2)
            z2l.append(z2)
        elif j==2:
            x3=Ap_crtaj4[svaki][0]
            y3=Ap_crtaj4[svaki][1]
            z3=Ap_crtaj4[svaki][2]
            x3l.append(x3)
            y3l.append(y3)
            z3l.append(z3)
#--STABLO PART--
def crtajOsi():
    glPushMatrix()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.8,0.3,0.3,0.3)#red x
    glLineWidth(3)
    glBegin(GL_LINES)
    glVertex3f(-4.0, 0.0, 0.0)
    glVertex3f(10.0, 0.0, 0.0)
    glEnd()
    glFlush()
    
    glColor4f(0.3,0.8,0.3,0.3)#green y
    glLineWidth(3)
    glBegin(GL_LINES)
    glVertex3f(0.0, -4.0, 0.0)
    glVertex3f(0.0, 10.0, 0.0)
    glEnd()
    glFlush()

    glColor4f(0.2,0.3,0.8,0.3)#blue z
    glLineWidth(3)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0 , -4.0 )
    glVertex3f(0.0, 0.0 , 10.0)
    glEnd()

    glFlush()
    glDisable(GL_BLEND)
    glPopMatrix()
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
def racunajOS(poc, cilj):
    os = np.cross(poc, cilj)
    kut = angle(poc, cilj)
    kutUStupnjevima = convertToDeg(kut)
    return os, kutUStupnjevima
normala = normalize(calcNormala(v1,v2,v3))
os, alfa = racunajOS(normala, ociste-ar_sred_ravn)
def mijenjajOciste():
    global ociste
    global dodaj
    if(ociste[2] >= 20 or ociste[2] <= -5):
        dodaj*=(-1)
    ociste[2] += dodaj
def crtajCesticu(i,ID):
    global ar_sred_ravn,normala,os,alfa
    global v1,v2,v3,v4
    global ociste
    global sustav

    sustav[i].vrijeme_zivota-=1
    
    if(sustav[i].checkIFCloseToDead()):
        sustav[i].skaliraj-=(sustav[i].minSkal/50)
    if(sustav[i].checkIFDead()):
        del sustav[i]
        sustav[i] = cestica()

    glPushMatrix()
    sustav[i].trenY -= sustav[i].deltaY
    sustav[i].trenX = sustav[i].amplituda*math.sin(sustav[i].trenY) + sustav[i].pomakX
    sustav[i].trenZ = sustav[i].amplituda*math.sin(sustav[i].trenY) + sustav[i].pomakZ
    glTranslatef(sustav[i].trenX, sustav[i].trenY , sustav[i].trenZ)
    glRotate(alfa,os[0],os[1],os[2])
    glScalef(sustav[i].skaliraj, sustav[i].skaliraj, sustav[i].skaliraj)
    glBindTexture(GL_TEXTURE_2D,ID[i])#texture
    glEnable(GL_TEXTURE_2D)

    glEnable(GL_BLEND)#ajsjdjsd
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0,1.0,1.0,0.40)
    glBegin(GL_QUADS)
    glTexCoord3f(tC[0][0], tC[0][1], tC[0][2]); 
    glVertex3f(v1[0],v1[1],v1[2]);
    glTexCoord3f(tC[1][0], tC[1][1], tC[1][2]); 
    glVertex3f(v2[0],v2[1],v2[2]);
    glTexCoord3f(tC[2][0], tC[2][1], tC[2][2]); 
    glVertex3f(v3[0],v3[1],v3[2]);
    glTexCoord3f(tC[3][0], tC[3][1], tC[3][2]); 
    glVertex3f(v4[0],v4[1],v4[2]);
    glEnd()
    glPopMatrix()
    
    glDisable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)
    glFlush()
    glDisable(GL_BLEND)


def crtajPlane():
    global r
    global nikad_vise
    if(not nikad_vise):
        c=texture()
        r=c;  
        nikad_vise=True
    
    for i in range(0,len(sustav)):
        crtajCesticu(i,r.ids)

def crtajBor():
    global x1l,y1l,z1l,x2l,y2l,z2l,x3l,y3l,z3l
    glPushMatrix()
    glTranslatef(0,0,3.0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(96/255,185/255,62/255,0.3)
    glScalef(0.5,0.5,0.5)
    for i in range(len(x1l)):
        glBegin(GL_TRIANGLES)
        glVertex3f(x1l[i],y1l[i],z1l[i])
        glVertex3f(x2l[i],y2l[i],z2l[i])
        glVertex3f(x3l[i],y3l[i],z3l[i])
        glEnd()
    glDisable(GL_BLEND)
    glPopMatrix()

def nacrtajRavan():
    glPushMatrix()
    glScalef(2,2,2)
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0,0.0,0.0,0.2)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBegin(GL_QUADS)
    glVertex3f(v1[0],v1[1],v1[2]);
    glVertex3f(v2[0],v2[1],v2[2]);
    glVertex3f(v3[0],v3[1],v3[2]);
    glVertex3f(v4[0],v4[1],v4[2]);
    glEnd()
    glDisable(GL_BLEND)
    glPopMatrix()
    
    
def renderScene():
    crtajPlane()
    crtajBor()
    crtajOsi()
    
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)#| GL_DEPTH_BUFFER_BITclear buffers to preset values, | GL_DEPTH_BUFFER_BIT
    glLoadIdentity()
    glPushMatrix()
    glTranslatef(-3, -1, -11.0); # translatiraj z kameru uzrak ili ju priblizi
    glRotate(10, 1, 0, 0)
    glRotate(30, 0, 1, 0)  #2 reda prije pomaknes kameru ulijevo, ali onda treba rotirati sve oko y osi LOGICNO
    renderScene()
    glPopMatrix()
    glutSwapBuffers()


def reshape(width,height):
    #glEnable(GL_DEPTH_TEST) # pitat prof kako se to rjesi
    glViewport(0, 0, GLsizei(width) , GLsizei(height))
    glClearDepth(1.0)
    glClearColor(0.0,0.0,0.0,0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


#INIT
glutInit()
glutInitDisplayMode(GLUT_DOUBLE) # dva graficka spremnika- prikaz na zaslonu a u drugi se crta slijedeca scena
glutInitWindowSize(1900,900)
glutInitWindowPosition(5,5)
glutCreateWindow("2. domaca zadaca u Pythonu iz RA")
glutDisplayFunc(display)# bez ovoga no display callbackregistered for window 1
glutReshapeFunc(reshape)
glutIdleFunc(display)
glutMainLoop()