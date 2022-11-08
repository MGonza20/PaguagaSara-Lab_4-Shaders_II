from math import radians, sin, cos
import pygame
from pygame.locals import *

from shaders import *
from gl import Renderer, Model

width = 960
height = 540

deltaTime = 0.0

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.setShaders(vertex_shader, fragment_shader)

rend.target.z = -5

face = Model("MandarinFish.obj", "MandarinFish.bmp")

face.position.z -= 5
face.scale.x = 0.5
face.scale.y = 0.5
face.scale.z = 0.5

rend.scene.append( face )


isRunning = True

while isRunning:

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_z:
                rend.filledMode()
            elif event.key == pygame.K_x:
                rend.wireframeMode()

            elif event.key == pygame.K_1:
                rend.setShaders(vertex_shader, fragment_shader)
            elif event.key == pygame.K_2:
                rend.setShaders(vertex_shader, toon_fragment_shader)
            elif event.key == pygame.K_3:
                rend.setShaders(wave_vertex_shader, fragment_shader)

    if True:
        if keys[K_q]:
            if rend.camDistance > 2:
                rend.camDistance -= 2 * deltaTime
        elif keys[K_e]:
            if rend.camDistance < 7:
                rend.camDistance += 2 * deltaTime
    
        if keys[K_a]:
            rend.angle -= 30 * deltaTime
        elif keys[K_d]:
            rend.angle += 30 * deltaTime

        if keys[K_w]:
            if rend.camPosition.y < 1.5:
                rend.camPosition.y += 5 * deltaTime
        elif keys[K_s]:
            if rend.camPosition.y > -1.5:
                rend.camPosition.y -= 5 * deltaTime

        rend.target.y = rend.camPosition.y 
        xDistance = sin(radians(rend.angle))
        zDistance = cos(radians(rend.angle))
        rend.camPosition.x = xDistance * rend.camDistance + rend.target.x 
        rend.camPosition.z = zDistance * rend.camDistance + rend.target.z 

    
    # Point light position
    if keys[K_LEFT]:
        rend.pointLight.x -= 10 * deltaTime
    elif keys[K_RIGHT]:
        rend.pointLight.x += 10 * deltaTime
    elif keys[K_UP]:
        rend.pointLight.y += 10 * deltaTime
    elif keys[K_DOWN]:
        rend.pointLight.y -= 10 * deltaTime

    deltaTime = clock.tick(60) / 1000
    rend.time += deltaTime


    rend.update()
    rend.render()
    pygame.display.flip()

pygame.quit()
