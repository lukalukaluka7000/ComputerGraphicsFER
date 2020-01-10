from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
from PIL import Image

from helper import global_states as _g
#--TEXTURE PART--
#imageName="./.obj/mur_Ambiant.bmp"
imageName="./.obj/snow3.tga"
#imageName="./.obj/snow.bmp"
im = Image.open(imageName)
dur=list(im.getdata())
imgData=np.array(dur,dtype=np.uint32)
#--TEXTURE PART--
#--BUMP PART--
#bumpName="./.obj/Bricks (NM and Height).tga"
bumpName="./.obj/NormalMap.tga"
im2 = Image.open(bumpName)
dur2=list(im2.getdata())
imgData2=np.array(dur2,dtype=np.uint32)
#--BUMP PART--


class texture():
    def __init__(self):
        self.ids = self.genTexture()
    
    def genTexture(self):
        i=0
        ids=[]
        for i in range(0, _g.broj_cestica):
            glActiveTexture(GL_TEXTURE0)
            ID = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, ID)
            
            #glUniform1i(uniformsLocations["texture"], 0)
           
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, im.size[0], im.size[1],0,GL_RGBA, GL_UNSIGNED_BYTE, imgData)

            #glBindTexture(GL_TEXTURE_2D, 0)
            ids.append(ID)
        return ids
        
class bump():
    def __init__(self):
        self.ids = self.genBump()
    
    def genBump(self):
        i=0
        ids=[]
        for i in range(0, _g.broj_cestica):
            glActiveTexture(GL_TEXTURE1)
            ID = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, ID)
            
            #glUniform1i(uniformsLocations["texture"], 0)
           
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, im.size[0], im.size[1],0,GL_RGBA, GL_UNSIGNED_BYTE, imgData2)
            
            #glBindTexture(GL_TEXTURE_2D, 0)
            ids.append(ID)
        return ids
