import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Window dimensions
windowWidth = 900
windowHeight = 700

# Mosquito variables
numMosquitoes = 40
mosquitoX = [0] * numMosquitoes
mosquitoY = [0] * numMosquitoes
mosquitoSpeedX = [0] * numMosquitoes
mosquitoSpeedY = [0] * numMosquitoes
mosquitoMoving = True  # State to control mosquito movement

# Dengue message
dengueMessage = None

# Initialize OpenGL settings
def initGL():
    glClearColor(1.0, 1.0, 1.0, 1.0)  # Background color temporarily white
    random.seed()  # Seed for randomization

    # Initialize mosquito positions and speeds
    for i in range(numMosquitoes):
        mosquitoX[i] = -0.5 + random.random()
        mosquitoY[i] = -0.5 + random.random()
        mosquitoSpeedX[i] = 0.01 * (random.random() - 0.5)
        mosquitoSpeedY[i] = 0.01 * (random.random() - 0.5)

# Draw a rectangle
def drawRectangle(x, y, width, height, r, g, b):
    glColor3f(r, g, b)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

# Draw the background with two colors
def drawBackground():
    drawRectangle(-1.0, 0.0, 2.0, 1.0, 0.5, 0.8, 1.0)  # Upper half (sky blue)
    drawRectangle(-1.0, -1.0, 2.0, 1.0, 0.6, 0.6, 0.6)  # Lower half (gray)

# Draw a mosquito
def drawMosquito(x, y):
    glColor3f(0.0, 0.0, 0.0)  # Black body
    glBegin(GL_POLYGON)
    glVertex2f(x - 0.01, y)
    glVertex2f(x, y + 0.01)
    glVertex2f(x + 0.01, y)
    glVertex2f(x, y - 0.01)
    glEnd()

    glBegin(GL_LINES)  # Wings
    glVertex2f(x, y)
    glVertex2f(x + 0.02, y + 0.02)
    glVertex2f(x, y)
    glVertex2f(x - 0.02, y + 0.02)
    glEnd()

# Draw a human
def drawHuman(x, y):
    glColor3f(1.0, 0.8, 0.6)  # Skin color
    glBegin(GL_POLYGON)
    for i in range(360):
        angle = i * math.pi / 180.0
        glVertex2f(x + 0.05 * math.cos(angle), (y - 0.05) + 0.05 * math.sin(angle))  # Adjusted closer to the body
    glEnd()

    # Hair
    glColor3f(0.0, 0.0, 0.0)  # Black hair
    glBegin(GL_POLYGON)
    for i in range(180):  # Top half of the head
        angle = i * math.pi / 180.0
        glVertex2f(x + 0.05 * math.cos(angle), (y - 0.02) + 0.05 * math.sin(angle))  # Adjusted position
    glEnd()

    # Eyes
    glColor3f(0.0, 0.0, 0.0)  # Black eyes
    drawRectangle(x - 0.02, (y - 0.05) + 0.01, 0.01, 0.01, 0.0, 0.0, 0.0)  # Left eye
    drawRectangle(x + 0.01, (y - 0.05) + 0.01, 0.01, 0.01, 0.0, 0.0, 0.0)  # Right eye

    # Nose
    glColor3f(1.0, 0.8, 0.6)  # Skin color for nose
    drawRectangle(x - 0.005, (y - 0.05) - 0.005, 0.01, 0.02, 1.0, 0.8, 0.6)

    # Mouth
    glColor3f(1.0, 0.0, 0.0)  # Red for mouth
    drawRectangle(x - 0.015, (y - 0.05) - 0.025, 0.03, 0.005, 1.0, 0.0, 0.0)

    # Arms
    glColor3f(1.0, 0.8, 0.6)  # Skin color
    drawRectangle(x - 0.1, y - 0.15, 0.05, 0.02, 1.0, 0.8, 0.6)  # Left arm
    drawRectangle(x + 0.05, y - 0.15, 0.05, 0.02, 1.0, 0.8, 0.6)  # Right arm

    # Body
    glColor3f(0.0, 0.0, 1.0)  # Blue shirt
    drawRectangle(x - 0.05, y - 0.25, 0.1, 0.15, 0.0, 0.0, 1.0)

    # Legs
    glColor3f(0.0, 0.0, 0.0)  # Black pants
    drawRectangle(x - 0.05, y - 0.4, 0.03, 0.15, 0.0, 0.0, 0.0)
    drawRectangle(x + 0.02, y - 0.4, 0.03, 0.15, 0.0, 0.0, 0.0)

# Render text
def renderText(x, y, text):
    glColor3f(0.0, 0.0, 0.0)  # Text color (black)
    glRasterPos2f(x, y)  # Position of the text

    for c in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))  # Render each character

# Update mosquito positions
def updateMosquitoes():
    global mosquitoMoving
    if not mosquitoMoving:
        return

    for i in range(numMosquitoes):
        mosquitoX[i] += mosquitoSpeedX[i]
        mosquitoY[i] += mosquitoSpeedY[i]

        # Bounce off walls
        if mosquitoX[i] > 1.0 or mosquitoX[i] < -1.0:
            mosquitoSpeedX[i] = -mosquitoSpeedX[i]
        if mosquitoY[i] > 1.0 or mosquitoY[i] < -1.0:
            mosquitoSpeedY[i] = -mosquitoSpeedY[i]

# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    drawBackground()  # Draw the background

    # Draw mosquitoes
    for i in range(numMosquitoes):
        drawMosquito(mosquitoX[i], mosquitoY[i])

    # Draw humans
    drawHuman(0.6, -0.2)
    drawHuman(0.8, -0.2)

    # Render dengue message if set
    if dengueMessage:
        renderText(-0.9, 0.9, dengueMessage)  # Top-left corner

    pygame.display.flip()

# Handle keyboard input
def handleKeypress(key):
    global mosquitoMoving, dengueMessage

    if key == K_s:
        mosquitoMoving = False  # Stop mosquitoes
    elif key == K_d:
        mosquitoMoving = True  # Start mosquitoes
    elif key == K_a:
        dengueMessage = "Dengue Awareness: Prevent stagnant water to stop mosquito breeding."

# Timer function for animation
def timer(value):
    updateMosquitoes()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)  # 60 FPS

# Main function
def main():
    pygame.init()

    displayMode = DOUBLEBUF | RGB
    pygame.display.set_mode((windowWidth, windowHeight), displayMode)

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(windowWidth, windowHeight)
    glutCreateWindow("Scene with Dengue Awareness")

    initGL()

    # Start the timer
    glutTimerFunc(16, timer, 0)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                handleKeypress(event.key)

        # Call the display function
        display()

    pygame.quit()

if __name__ == "__main__":
    main()
