import time
import numpy as np
from helper import mathematics as _m
from helper import spline as _s
from helper import readobj as _r


from ctypes import c_void_p, sizeof, c_float

from OpenGL.GL import GLfloat



def getStartTime():
    start = time.time()
    return start
    
    
start = getStartTime()

st,nd,rd    = _r.readOBJ("./.obj/stablo.obj")
sta,nda,rda = _r.readOBJ("./.obj/heli7.obj")

v1=[-0.25, -0.25, 1.0]
v2=[ 0.25, -0.25, 1.0]
v3=[ 0.25,  0.25, 1.0]
v4=[-0.25,  0.25, 1.0]
ar_sred_ravn = np.array([np.mean([v1[0],v2[0],v3[0],v4[0]]), np.mean([v1[1],v2[1],v3[1],v4[1]]), np.mean([v1[2],v2[2],v3[2],v4[2]])]) #

nikad_vise=False
r=None
r2=None

ociste = np.array([-10,3,15])
look_at=[0,2.5,0]
lightPos=[0.0, 0.0, 2.0]

broj_cestica = 100
sustav=dict()
sustav = { new_list: None for new_list in range(0, broj_cestica)}


program=None
VBO=None
numAttributes=0

uniformsLocations=dict()

vertices = [-0.25,-0.25,1.0,0.0,0.0,0.0,1.0,0.0,1.0,0.0,0.0,  0.25,-0.25,1.0,1.0,0.0,0.0,1.0,0.0,1.0,0.0,0.0,  0.25,0.25,1.0,1.0,1.0,0.0,1.0,0.0,1.0,0.0,0.0,   -0.25,0.25,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,0.0]

normala = _m.normalize(_m.calcNormala(v4,v1,v2))
oss, alfaa = _m.racunajOSR(normala, _m.normalize(ociste-ar_sred_ravn))


scale=1.0
iz_aviona = -1
spline = -1
moving_light=-1
billboard = -1

offsets = dict()
offsets["c_float_size"] = sizeof(c_float)
float_size = offsets["c_float_size"]
offsets["GLfloat_size"] = sizeof(GLfloat)
offsets["null"]         = c_void_p(0)
offsets["vertex"]       = c_void_p(0 * float_size)
offsets["tex"]          = c_void_p(3 * float_size)
offsets["binormal"]     = c_void_p(5 * float_size)
offsets["tangent"]      = c_void_p(8 * float_size)
#color_offset  = c_void_p(3 * float_size)



with open("./shaders/shader.vert", 'r') as f:
    vertexShaderSource = f.read()
with open("./shaders/shader.frag", 'r') as f:
    fragmentShaderSource = f.read()
    
    
dodaj1=0.01
dodaj2=0.01
dodaj3=0.01



poc= np.array([0,0,1, 1])
lista_ciljeva = _s.izrCilj()
lista_ciljna_orijentacija = _s.izrOrj()
koja_tocka=0
brojac=0.1



rotating = False
scaling = False

pot_tra=[-7.3125,5.625,0.186875,0.375]
