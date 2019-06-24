import sys

import OpenGL
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import *

import pywavefront
from pywavefront import visualization

import numpy as np

home = pywavefront.Wavefront ( 'Trabalho2CG.obj ' )
wid,hei = 480,480

posX,posY,posZ = 0,2,10
focusX,focusY,focusZ = 0,2,0

mouseX,mouseY = int(wid/2),int(hei/2)

theta,phi = np.pi,0
distaceOfFocus = 10

WdirectX,WdirectZ = 0,0.1
DdirectZ,DdirectX = 0,0.1

Keyspressed = []

def main():
  glutInit(sys.argv)
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
  glutInitWindowSize(wid,hei)
  glutCreateWindow('Tabalho 2 Computacao Grafica')

  glClearColor(.8,.8,1.,1.)
  
  glShadeModel(GL_SMOOTH)
  glEnable(GL_CULL_FACE)
  glEnable(GL_DEPTH_TEST)
  
  '''
  glEnable(GL_LIGHTING)
  lightZeroPosition = [2.,10.,2.,1.]
  lightZeroColor = [4.0,4.0,4.0,4.0] #green tinged
  glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
  glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
  glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
  glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.02)
  glEnable(GL_LIGHT0)
  '''
  glutSetCursor(GLUT_CURSOR_NONE) #Cursor do mouse Invisivel

  glutDisplayFunc(display)
  glutKeyboardFunc(keydown)
  glutKeyboardUpFunc(keyup)
  glutPassiveMotionFunc(mouseMove)

  glMatrixMode(GL_PROJECTION)
  
  gluPerspective(40.,1.,1.,40.)
  glMatrixMode(GL_MODELVIEW)
  gluLookAt(posX,posY,posZ,focusX,focusY,focusZ,0,1,0)
  glutWarpPointer(mouseX,mouseY)
  glPushMatrix()
  
  glutMainLoop()

def display():
  movimentOfCamera()
  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
  glPushMatrix()
  color = [1.0,0.,0.,1.]
  visualization.draw(home)
  glPopMatrix()
  glutSwapBuffers()

def mouseMove(x,y):
  global wid,hei
  global posX,posY,posZ
  global focusX,focusY,focusZ
  global mouseX,mouseY
  global phi,theta,distaceOfFocus
  global WdirectX,WdirectZ,DdirectX,DdirectZ

  dx = mouseX-x
  dy = mouseY-y
  rotX = map(dx,0,wid,0,np.pi)
  rotY = map(dy,0,hei,0,np.pi)

  theta += rotX
  phi += rotY
  if phi > np.pi/2:
    phi = np.pi/2;
  elif phi < -np.pi/2:
    phi = -np.pi/2

  focusX = np.cos(phi)*np.sin(theta)*distaceOfFocus
  focusY = np.sin(phi)*distaceOfFocus
  focusZ = np.cos(phi)*np.cos(theta)*distaceOfFocus

  WdirectX = (focusX - posX)/100 #para forcar tamanho do vetor direção para 0.1
  WdirectZ = (focusZ - posZ)/100

  DdirectX = np.sin(theta - np.pi/2)*np.cos(phi)*0.1 
  DdirectZ = np.cos(theta - np.pi/2)*np.cos(phi)*0.1

  glutWarpPointer(mouseX,mouseY)
  glLoadIdentity()
  gluLookAt(posX,posY,posZ,focusX,focusY,focusZ,0,1,0)
  glutPostRedisplay()


def keyup(key,x,y):
  global Keyspressed
  index = 0
  for k in Keyspressed:
    if ord(key) == k:
      Keyspressed.pop(index)
      break
    index += 1

def keydown(key,x,y):
  global Keyspressed

  keyPress = ord(key)
  if(keyPress == 119 or keyPress == 115 or keyPress == 100 or keyPress == 97 or keyPress == 122 or keyPress == 32):
    #W,S,D,A,Z,SpaceBar
    ok = True   
    for k in Keyspressed:
      if k == keyPress:
        ok = False
        break
    if ok:
      Keyspressed.append(keyPress)
  elif(keyPress == 27):
    #ESC
    glutLeaveMainLoop() #Sair do Programa   

def map(Value,Min,Max,Newmin,Newmax):
  #Retorna um valor equivalente do intevalo [Min,Max] para o intervalo [Nexmin,Newmax]
  x = (Newmax-Newmin)/(Max-Min)
  y = Value-Min
  return y*x + Newmin

def movimentOfCamera():
  global Keyspressed
  global posX,posY,posZ,focusX,focusY,focusZ
  global WdirectX,WdirectZ,DdirectX,DdirectZ

  for keyPress in Keyspressed:
    if(keyPress == 119): #W
      posZ += WdirectZ
      posX += WdirectX
      focusZ += WdirectZ
      focusX += WdirectX
    elif(keyPress == 115): #S
      posZ -= WdirectZ
      posX -= WdirectX
      focusZ -= WdirectZ
      focusX -= WdirectX
    elif(keyPress ==  100): #D
      posZ += DdirectZ
      posX += DdirectX
      focusZ += DdirectZ
      focusX += DdirectX
    elif(keyPress == 97): #A
      posZ -= DdirectZ
      posX -= DdirectX
      focusZ -= DdirectZ
      focusX -= DdirectX
    elif(keyPress == 122): #Z -> abaixar
      posY -= 0.1
      focusY -= 0.1
    elif(keyPress == 32): #Space bar -> levantar
      posY += 0.1
      focusY += 0.1

  glLoadIdentity()
  gluLookAt(posX,posY,posZ,focusX,focusY,focusZ,0,1,0)
  glutPostRedisplay()

if __name__ == '__main__': main()
