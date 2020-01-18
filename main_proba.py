import sys


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import math
import time

from helper import mathematics as _m
from helper import spline as _s
from helper import readobj as _r
from helper.global_states import *

from classes.sustav     import cestica
from classes.tex        import texture
from classes.tex        import bump


#start = _g.start
#print(start == _g.start)
    
def implementGLSL():
    global program, vertices,numAttributes, VBO,translationLocation,scaleLocation # todo dictanioary vidi pbo.py
    global uniformsLocations
    vertshader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertshader, vertexShaderSource)
    glCompileShader(vertshader)
    if(glGetShaderiv(vertshader, GL_COMPILE_STATUS) != GL_TRUE):
        raise RuntimeError(glGetShaderInfoLog(vertshader))
    
    
    fragshader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragshader, fragmentShaderSource)
    glCompileShader(fragshader)
    if(glGetShaderiv(fragshader, GL_COMPILE_STATUS) != GL_TRUE):
        raise RuntimeError(glGetShaderInfoLog(fragshader))
        
    program = glCreateProgram()
    glAttachShader(program, vertshader)
    glAttachShader(program, fragshader)
    
    #--ATTRIBS--
    glBindAttribLocation(program, numAttributes, "vertexPosition");
    numAttributes+=1
    #glBindAttribLocation(program, numAttributes, "vertexColor");
    #numAttributes+=1
    glBindAttribLocation(program, numAttributes, "Texcoord");
    numAttributes+=1
    
    glBindAttribLocation(program, numAttributes, "rm_Binormal");
    numAttributes+=1
    
    glBindAttribLocation(program, numAttributes, "rm_Tangent");
    numAttributes+=1
    #--ATTRIBS--
    
    
    glLinkProgram(program)
    if(glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE):
        raise RuntimeError(glGetProgramInfoLog(program))

    
    #--UNIFORMS--
    
    uniformsLocations["translate"] = glGetUniformLocation(program, "translateVector")
    #translationLocation = glGetUniformLocation(program, "translateVector")
    if (uniformsLocations["translate"] == GL_INVALID_INDEX):
        raise RuntimeError("Uniform " + "translateVector" + "not found in shader")
    if (uniformsLocations["translate"] == -1):
        raise RuntimeError("Uniform " + "translateVector" + "not found in shader")
    
    
    uniformsLocations["scale"] = glGetUniformLocation(program, "scale")
    #scaleLocation = glGetUniformLocation(program, "scale")
    if (uniformsLocations["scale"] == GL_INVALID_INDEX):
        raise RuntimeError("Uniform " + "scale" + "not found in shader")
    if (uniformsLocations["scale"] == -1):
        raise RuntimeError("Uniform " + "scale" + "not found in shader")
    
    
    uniformsLocations["rotate"] = glGetUniformLocation(program, "rotate")
    #scaleLocation = glGetUniformLocation(program, "scale")
    if (uniformsLocations["rotate"] == GL_INVALID_INDEX):
        raise RuntimeError("Uniform " + "rotate" + "not found in shader")
    if (uniformsLocations["rotate"] == -1):
        raise RuntimeError("Uniform " + "rotate" + "not found in shader")
    
    uniformsLocations["texture"] = glGetUniformLocation(program, "baseMap")
    if (uniformsLocations["texture"] == GL_INVALID_INDEX):
        raise RuntimeError("Uniform " + "baseMap" + "not found in shader")
    if (uniformsLocations["texture"] == -1):
        raise RuntimeError("Uniform " + "baseMap" + "not found in shader")
        
    uniformsLocations["light"] = glGetUniformLocation(program, "fvLightPosition")
    if (uniformsLocations["light"] == GL_INVALID_INDEX):
        raise RuntimeError("Uniform " + "fvLightPosition" + "not found in shader")
    if (uniformsLocations["light"] == -1):
        raise RuntimeError("Uniform " + "fvLightPosition" + "not found in shader")    
    
    uniformsLocations["eye"] = glGetUniformLocation(program, "fvEyePosition")
    if (uniformsLocations["eye"] == GL_INVALID_INDEX):
        raise RuntimeError("Uniform " + "fvEyePosition" + "not found in shader")
    if (uniformsLocations["eye"] == -1):
        raise RuntimeError("Uniform " + "fvEyePosition" + "not found in shader") 
        
    uniformsLocations["ambient"] = glGetUniformLocation(program, "fvAmbient")
    if (uniformsLocations["ambient"] == GL_INVALID_INDEX):
        raise RuntimeError("Uniform " + "fvAmbient" + "not found in shader")
    if (uniformsLocations["ambient"] == -1):
        raise RuntimeError("Uniform " + "fvAmbient" + "not found in shader") 
        
    uniformsLocations["specular"] = glGetUniformLocation(program, "fvSpecular")
    if (uniformsLocations["specular"] == GL_INVALID_INDEX):
        raise RuntimeError("Uniform " + "fvSpecular" + "not found in shader")
    if (uniformsLocations["specular"] == -1):
        raise RuntimeError("Uniform " + "fvSpecular" + "not found in shader") 
        
    uniformsLocations["diffuse"] = glGetUniformLocation(program, "fvDiffuse")
    if (uniformsLocations["specular"] == GL_INVALID_INDEX):
        raise RuntimeError("diffuse " + "fvDiffuse" + "not found in shader")
    if (uniformsLocations["specular"] == -1):
        raise RuntimeError("diffuse " + "fvDiffuse" + "not found in shader") 
        
    uniformsLocations["bump"] = glGetUniformLocation(program, "bumpMap")
    if (uniformsLocations["bump"] == GL_INVALID_INDEX):
        raise RuntimeError("Uniform " + "bumpMap" + "not found in shader")
    if (uniformsLocations["bump"] == -1):
        raise RuntimeError("Uniform " + "bumpMap" + "not found in shader")


    #--UNIFORMS--
    glUseProgram(program)
    #init program
    
    print(1)
    
    c=texture()
    r=c;
    b=bump()
    r2=b
    i=0
    glBindTexture(GL_TEXTURE_2D,r.ids[i])#texture
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
    glUniform1i(uniformsLocations["texture"], 0)
    
    glUniform3fv(uniformsLocations["eye"], 1 , list(ociste))
    
    glUniform4fv(uniformsLocations["ambient"], 1, ambientData)
    
    glUniform4fv(uniformsLocations["diffuse"], 1, diffuseData)
    
    glUniform4fv(uniformsLocations["specular"], 1, specularData)
    
    
    glBindTexture(GL_TEXTURE_2D, r2.ids[i])
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
    glUniform1i(uniformsLocations["bump"], 0)
    
    rotateData = [oss[0],oss[1],oss[2],alfaa]
    glUniform4fv(uniformsLocations["rotate"],1,rotateData)
    
    
    glUseProgram(0)
    
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    

    
    array_type = (GLfloat * len(vertices))
    glBufferData(GL_ARRAY_BUFFER, len(vertices) * offsets["GLfloat_size"], array_type(*vertices), GL_STATIC_DRAW)
    
    
    glBindBuffer(GL_ARRAY_BUFFER,VBO)
    
    float_size = offsets["c_float_size"]
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, False,  11*float_size, offsets["vertex"]) #stride: 0 -> slijedni vrhovi
    
    #glEnableVertexAttribArray(1) #     c_void_p(48)
    #glVertexAttribPointer(1, 4, GL_FLOAT, False,  10*float_size, color_offset)#(sizeof(float)* 3)
    
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, False,  11*float_size, offsets["tex"])
    
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 3, GL_FLOAT, False,  11*float_size, offsets["binormal"])
    
    glEnableVertexAttribArray(3)
    glVertexAttribPointer(3, 3, GL_FLOAT, False,  11*float_size, offsets["tangent"])


def renderSceneWithGLSL(i):
    global sustav

    #MOZDA I OFFSETE STAVIT U DICTIONARY,###################color_offset
    global uniformsLocations
    global billboard
    glPushMatrix()
    if(sustav[i] is None):
        sustav[i] = cestica(pot_tra)
    sustav[i].vrijeme_zivota-=1
    if(sustav[i].checkIFCloseToDead()):
        sub = 0.01
        if sustav[i].skaliraj > 0.2:
            sustav[i].skaliraj -= sub
        else:
            sustav[i].skaliraj=0.2
        #sustav[i].skaliraj-=(sustav[i].minSkal)

    if(sustav[i].checkIFDead() and time.time()- start > 2):
        del sustav[i]
        sustav[i] = cestica(pot_tra)

    #glUseProgram(program)
    # VELIKI PROBLEM BIO STO JE OVAJ IZRACUN BIO POSLIJE GLUNIFORM4V (translate data) pa 
    # je bio flickering
    if(sustav[i].umjetni_snijeg == True):
        sustav[i].trenY -= sustav[i].deltaY
        sustav[i].trenX = sustav[i].amplituda*math.sin(sustav[i].trenY) + sustav[i].pomakX
        #sustav[i].trenZ = sustav[i].amplituda*math.cos(sustav[i].trenY) + sustav[i].pomakZ
        
        translateData = [sustav[i].trenX, sustav[i].trenY, sustav[i].trenZ, 1]
        glUniform4fv(uniformsLocations["translate"], 1, translateData)
    else:
        sustav[i].index += 1
        sustav[i].trenY -= sustav[i].deltaY
        sustav[i].trenZ = sustav[i].amplituda*math.cos(sustav[i].trenY) + sustav[i].pomakZ

        translateData = [sustav[i].trajectory[sustav[i].index], sustav[i].trenY, sustav[i].trenZ, 1] #sustav[i].trajectory[sustav[i].index]
        glUniform4fv(uniformsLocations["translate"], 1, translateData)
        
        #print(sustav[i].index)

    if(billboard == 1):
        v1_t = [v1[0]+sustav[i].trenX, v1[1]+sustav[i].trenY, v1[2]+sustav[i].trenZ]
        v2_t = [v2[0]+sustav[i].trenX, v2[1]+sustav[i].trenY, v2[2]+sustav[i].trenZ]
        v3_t = [v3[0]+sustav[i].trenX, v3[1]+sustav[i].trenY, v3[2]+sustav[i].trenZ]
        v4_t = [v4[0]+sustav[i].trenX, v4[1]+sustav[i].trenY, v4[2]+sustav[i].trenZ]
        normal = _m.normalize(_m.calcNormala(v1_t,v2_t,v3_t))
        arsr = np.array([np.mean([v1_t[0],v2_t[0],v3_t[0],v4_t[0]]), np.mean([v1_t[1],v2_t[1],v3_t[1],v4_t[1]]), np.mean([v1_t[2],v2_t[2],v3_t[2],v4_t[2]])]) #

        os, alfa = _m.racunajOSR(normal, ociste-arsr)
        
        rotateData = [0.0,0.0,0.0,0.0]
        glUniform4fv(uniformsLocations["rotate"],1,rotateData)
        glRotatef(alfa,os[0],os[1],os[2])
        
    elif (billboard == -1):
        rotateData = [oss[0],oss[1],oss[2],alfaa]
        glUniform4fv(uniformsLocations["rotate"],1,rotateData)
        #glRotatef(alfa,os[0],os[1],os[2])
    
    
    scaleData = sustav[i].skaliraj
    glUniform1f(uniformsLocations["scale"], scaleData)
    
    glUniform3fv(uniformsLocations["light"], 1, lightPos)

    glDrawArrays(GL_QUADS, 0, 4)

    glPopMatrix()
    


def nacrtajKrivulju():
    global lista_ciljeva
    glPushMatrix()
    glColor3f(98/255, 107/255, 221/255)
    for segment in range(len(lista_ciljeva)):
        glBegin(GL_LINE_STRIP)
        for i in np.arange(0, 1+0.01, 0.1):
            i=round(i,2)
            glVertex3f(lista_ciljeva[segment][i][0], lista_ciljeva[segment][i][1], lista_ciljeva[segment][i][2])
        glEnd()
    glPopMatrix()



def crtajBor():
    global st,nd,rd,scale
    glPushMatrix()
    glTranslatef(0,0,3)
    #glEnable(GL_BLEND)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(96/255,185/255,62/255,0.3)
    glScalef(0.5,0.5,0.5)
    #glScalef(0.5*scale,0.5*scale,0.5*scale)

    for i in range(len(st)):
        glBegin(GL_TRIANGLES)
        glVertex3f(st[i][0],st[i][1],st[i][2])
        glVertex3f(nd[i][0],nd[i][1],nd[i][2])
        glVertex3f(rd[i][0],rd[i][1],rd[i][2])
        glEnd()
    #glDisable(GL_BLEND)
    glPopMatrix()


def crtajOsi():
    glPushMatrix()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #glScalef(scale,scale,scale)
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
def mijenjajSvitlo():
    global lightPos
    global dodaj1,dodaj2,dodaj3
    if(lightPos[0] >= 3.5 or lightPos[0] <= -7):
        dodaj1*=(-1)
    '''
    if(lightPos[1] >= 10 or lightPos[1] <= -3):
        dodaj2*=(-1)
    if(lightPos[2] >= 13 or lightPos[2] <= 0):
        dodaj3*=(-1)
    '''
    lightPos[0] -= 2*dodaj1
    #lightPos[1] += dodaj2   
    #lightPos[2] += dodaj3
def crtajSvitlo():
    global lightPos
    glPushMatrix()
    if moving_light == 1:
        mijenjajSvitlo()
    glPointSize(5.0)
    glColor3f(ambientData[0], ambientData[1], ambientData[2])
    glBegin(GL_POINTS)
    glVertex3f(lightPos[0],lightPos[1],lightPos[2])
    glEnd()
    
    glPopMatrix()
def nacrtajObjekt():
    #glScalef(0.15,0.15,0.15)
    global sta,nda,rda
    glColor(0.65,0.1569,0.384)
    for i in range(len(sta)):
        glBegin(GL_TRIANGLES)#GL_LINE_STRIP
        glVertex3f(sta[i][0],sta[i][1],sta[i][2])
        glVertex3f(nda[i][0],nda[i][1],nda[i][2])
        glVertex3f(rda[i][0],rda[i][1],rda[i][2])
        glEnd()
def crtajAvion():
    global poc
    global lista_ciljna_orijentacija
    global brojac,koja_tocka,pot_tra
    global spline

    os, alfa = _m.racunajOS(poc, lista_ciljna_orijentacija[koja_tocka], brojac)
    pot_tra = lista_ciljeva[koja_tocka][brojac]

    glPushMatrix()
    glTranslate(pot_tra[0],pot_tra[1],pot_tra[2])
    glRotate(alfa, os[0], os[1], os[2])
    glScale(0.5,0.5,0.5)
    nacrtajObjekt()
    glPopMatrix()
    if spline == 1:
        nacrtajKrivulju()
    
    if(brojac >=  1.00):
        koja_tocka+=1
        if koja_tocka == _s.vratiBrojTocaka()-3:
            koja_tocka=0
        brojac = 0.00
    else:
        #brojac+=0.01
        brojac+=0.04
        if(brojac>1.0):
            brojac=1.00
        brojac=round(brojac,3)

def crtajHelp():
    glPushMatrix()
    string1 = b"t - toggle"
    string2 = b"r - reset"
    string3 = b"q,w,e - eye + 1"
    string4 = b"a,s,d - eye - 1"
    string5 = b"RMB HOLD + move - scaling"
    string6 = b"k - draw spline"
    string7 = b"b - billboard"
    string8 = b"b - moving light"
    
    glRasterPos2f(-6.5,8.0)
    for i in range(0,len(string1)):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, string1[i])
    glRasterPos2f(-6.5,8.0-0.5)
    for i in range(0,len(string2)):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, string2[i])
    glRasterPos2f(-6.5,8.0-1.0)
    for i in range(0,len(string3)):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, string3[i])
    glRasterPos2f(-6.5,8.0-1.5)
    for i in range(0,len(string4)):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, string4[i])
    glRasterPos2f(-6.5,8.0-2.0)
    for i in range(0,len(string5)):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, string5[i])
    glRasterPos2f(-6.5,8.0-2.5)
    for i in range(0,len(string6)):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, string6[i])
    glRasterPos2f(-6.5,8.0-3.0)
    for i in range(0,len(string7)):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, string7[i])
    glRasterPos2f(-6.5,8.0-3.5)
    for i in range(0,len(string8)):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, string8[i])    
    glPopMatrix()
def renderSceneClassic():
    crtajBor()
    crtajOsi()
    crtajSvitlo()
    crtajAvion()
    crtajHelp()
    

def display():
    global r, r2, nikad_vise, scale, quadric,ociste,program,iz_aviona,look_at
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)#clear buffers to preset values, | GL_DEPTH_BUFFER_BIT
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    
    if iz_aviona == -1:
        look_at=[0,2.5,0]
        ociste = np.array([-10,3,15])
        gluLookAt(
                scale*ociste[0],scale*ociste[1],scale*ociste[2],
                look_at[0],look_at[1],look_at[2],#look_at.x, look_at.y, look_at.z,
                0, 1, 0) # up vector
    elif iz_aviona == 1:
        ociste = np.array([scale*pot_tra[0],scale*pot_tra[1]+5,scale*pot_tra[2]])
        gluLookAt(
                ociste[0],ociste[1],ociste[2],
                pot_tra[0],0.0,pot_tra[2],#look_at.x, look_at.y, look_at.z,
                pot_tra[0]+5, pot_tra[1]-5, pot_tra[2]+5) # up vector
        
    
    glPushMatrix()
    renderSceneClassic()

    glUseProgram(program)
    for i in range(0,len(sustav)):
        renderSceneWithGLSL(i)
    glUseProgram(0)
    
    glPopMatrix()
    glutSwapBuffers()
    

def reshape(width,height):
    glViewport(0, 0, GLsizei(width) , GLsizei(height))
    glClearDepth(1.0)
    glClearColor(0.0,0.0,0.0,0.0)
    glDepthMask(GL_TRUE)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glFrontFace(GL_CCW)
    glShadeModel(GL_SMOOTH)
    glDepthRange(0.0,1.0)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45,1.0,1.5,50.0)
    #glFrustum(-1.0, 1.0, -1.0, 1.0, 1.5, 50.0)
    


def moja_tipkovnica(tipka,misx,misy):
    global ociste,scale,iz_aviona,spline,moving_light,lightPos,billboard
    #print ("pritisnuto " ,str(tipka), type(tipka), "\n")
    tipka=tipka.decode("utf-8")
    if tipka == 'q':
        ociste[0]+=1
    elif tipka=='w':
        ociste[1]+=1
    elif tipka=='e':
        ociste[2]+=1
    
    if tipka == 'a':
        ociste[0]-=1
    elif tipka=='s':
        ociste[1]-=1
    elif tipka=='d':
        ociste[2]-=1
    
    if tipka=='t':
        iz_aviona=iz_aviona*(-1)
    
    if tipka=='k':
        spline=spline*(-1)
    
    if tipka=='m':
        moving_light*=-1
    if tipka== 'b':
        billboard=billboard*(-1)
    
    if tipka=='r':
        ociste = np.array([-10,3,15])
        scale = 1.0
        #lightPos=[0.0, 0.0, 2.0]
        #moving_light=-1


def mouse(button, state, x, y):
    global x0,y0,scaling,rotating
    if(button == GLUT_LEFT_BUTTON):
        rotating = (state==GLUT_DOWN)
    elif(button == GLUT_RIGHT_BUTTON):
        scaling = (state==GLUT_DOWN)
    x0=x
    y0=y
def motion(x1,y1):
    global x0,y0,rotation,scale,scaling
    if scaling:
        scale*= math.exp(((x1-x0)-(y1-y0))*.01)
    x0,y0=x1,y1
    
        
def animate(value):
    glutPostRedisplay()
    glutTimerFunc(20,animate,0)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE) # dva graficka spremnika- prikaz na zaslonu a u drugi se crta slijedeca scena
    glutInitWindowSize(800,450)
    glutInitWindowPosition(1000,5)
    glutCreateWindow("Treca samostalna vjezba!")
    glutDisplayFunc(display)# bez ovoga no display callbackregistered for window 1
    glutReshapeFunc(reshape)
    implementGLSL()
    glutMouseFunc(mouse)
    glutKeyboardFunc(moja_tipkovnica)
    glutMotionFunc(motion)
    glutTimerFunc(20, animate, 0)
    return glutMainLoop()

if __name__ == "__main__":
    sys.exit(main())