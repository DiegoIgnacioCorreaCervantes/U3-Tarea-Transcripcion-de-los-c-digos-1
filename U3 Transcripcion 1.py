import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import sys

def init_pygame():
    """Initializa Pygame y crea una ventana con soporte para OpenGL"""
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Cubo 3D - OpenGL con Python")

def init_opengl():
    """Configura el entorno OpenGL"""
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    # Configurar la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (800 / 600), 0.1, 50.0)

    # Configurar la posición inicial de la cámara
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(3, 3, 3, 0, 0, 0, 0, 1, 0)

def draw_cube():
    """Dibuja un cubo usando OpenGL"""

    # Definir los vértices del cubo (x, y, z)
    vertices = [
    # Cara frontal (z = 1)
    (-1, -1, 1),  # Vértice 0
    (1, -1, 1),  # Vértice 1
    (1, 1, 1),  # Vértice 2
    (-1, 1, 1),  # Vértice 3

    # Cara trasera (z = -1)
    (-1, -1, -1),  # Vértice 4
    (1, -1, -1),  # Vértice 5
    (1, 1, -1),  # Vértice 6
    (-1, 1, -1),  # Vértice 7
    ]

    # Definir las caras del cubo como índices a los vértices
    caras = [
    (0, 1, 2, 3),  # Cara frontal
    (4, 5, 6, 7),  # Cara trasera
    (0, 4, 7, 3),  # Cara izquierda
    (1, 5, 6, 2),  # Cara derecha
    (3, 2, 6, 7),  # Cara superior
    (0, 1, 5, 4),  # Cara inferior
    ]

    # Colores para cada cara (RGBA)
    colores = [
    (1.0, 0.0, 0.0, 1.0),  # Rojo
    (0.0, 1.0, 0.0, 1.0),  # Verde
    (0.0, 0.0, 1.0, 1.0),  # Azul
    (1.0, 1.0, 0.0, 1.0),  # Amarillo
    (1.0, 0.0, 1.0, 1.0),  # Magenta
    (0.0, 1.0, 1.0, 1.0),  # Cian
    ]

    glBegin(GL_QUADS)
    for i, cara in enumerate(caras):
        glColor4fv(colores[i])
        for vertice_idx in cara:
            glVertex3fv(vertices[vertice_idx])
    glEnd()

    # Dibujar los bordes del cubo
    glColor4f(1.0, 1.0, 1.0, 1.0)  # Color blanco para los bordes
    aristas = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # Aristas de la cara frontal
    (4, 5), (5, 6), (6, 7), (7, 4),  # Aristas de la cara trasera
    (0, 4), (1, 5), (2, 6), (3, 7),  # Aristas que conectan las caras
    ]
    glBegin(GL_LINES)
    for arista in aristas:
        for vertice_idx in arista:
            glVertex3fv(vertices[vertice_idx])
    glEnd()

def main():
    """Función principal del programa"""
    init_pygame()
    init_opengl()

    # Ángulos de rotación
    rotation_x = 0
    rotation_y = 0

    # Control de velocidad de rotación
    rotation_speed = 1

    # Bucle principal
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Controles de teclado
            if event.type == pygame.KEYDOWN:
                # Salir con la tecla ESC
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # Aumentar velocidad de rotación
                elif event.key == pygame.K_UP:
                    rotation_speed += 0.2
                # Disminuir velocidad de rotación
                elif event.key == pygame.K_DOWN:
                    rotation_speed = max(0.2, rotation_speed - 0.2)
                # Pausar/reanudar rotación
                elif event.key == pygame.K_SPACE:
                    rotation_speed = 0 if rotation_speed > 0 else 1

        # Actualizar ángulos de rotación
        rotation_x += 0.5 * rotation_speed
        rotation_y += 0.5 * rotation_speed

        # Limpiar la pantalla y el buffer de profundidad
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Resetear la matriz de modelado
        glLoadIdentity()

        # Posicionar la cámara
        gluLookAt(3, 3, 3, 0, 0, 0, 0, 1, 0)

        # Aplicar rotaciones
        glRotatef(rotation_x, 1, 0, 0)  # Rotación alrededor del eje X
        glRotatef(rotation_y, 0, 1, 0)  # Rotación alrededor del eje Y

        # Dibujar el cubo
        draw_cube()

        # Actualizar la pantalla
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()