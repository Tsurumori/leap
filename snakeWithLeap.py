import sys
from pygame.locals import *
import os, inspect, thread, time

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2 ** 32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
import Leap
from Leap import CircleGesture, KeyTapGesture
import pygame
import random

Snakespeed = 10
Window_Width = 800
Window_Height = 500
Cell_Size = 20  # Width and height of the cells
# Ensuring that the cells fit perfectly in the window. eg if cell size was
# 10     and window width or windowheight were 15 only 1.5 cells would
# fit.
assert Window_Width % Cell_Size == 0, "Window width must be a multiple of cell size."
# Ensuring that only whole integer number of cells fit perfectly in the window.
assert Window_Height % Cell_Size == 0, "Window height must be a multiple of cell size."
Cell_W = int(Window_Width / Cell_Size)  # Cell Width
Cell_H = int(Window_Height / Cell_Size)  # Cellc Height

White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)  # Defining element colors for the program.
Green = (0, 255, 0)
DARKGreen = (0, 155, 0)
DARKGRAY = (40, 40, 40)
YELLOW = (255, 255, 0)
Red_DARK = (150, 0, 0)
BLUE = (0, 0, 255)
BLUE_DARK = (0, 0, 150)
BGCOLOR = Black  # Background color
x = 0
y = 0
z = 0
i = 0
list = [0, 0, 0]
UP = 'up'
DOWN = 'down'  # Defining keyboard keys.
LEFT = 'left'
RIGHT = 'right'

HEAD = 0  # Syntactic sugar: index of the snake's head


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()
        for hand in frame.hands:
            global list
            list[0] = hand.direction.pitch
            list[1] = hand.direction.yaw
            list[2] = hand.palm_normal.roll
            # print 'hands detected'
            print 'x %f    y %f    z %f' % (list[0], list[1], list[2])
        #     print list
        # print "frame"
        # print list
def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    print ('controller created.')
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."

    global SnakespeedCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    SnakespeedCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((Window_Width, Window_Height))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake')
    showStartScreen()
    # try:
    #     sys.stdin.readline()
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     # Remove the sample listener when done
    #     controller.remove_listener(listener)
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    startx = random.randint(5, Cell_W - 6)
    starty = random.randint(5, Cell_H - 6)
    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Start the apple in a random place.
    apple = getRandomLocation()

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            # if event.type == QUIT:
            #     terminate()
            # elif event.type == KEYDOWN:
            #     if (event.key == K_LEFT) and direction != RIGHT:
            #         direction = LEFT
            #     elif (event.key == K_RIGHT) and direction != LEFT:
            #         direction = RIGHT
            #     elif (event.key == K_UP) and direction != DOWN:
            #         direction = UP
            #     elif (event.key == K_DOWN) and direction != UP:
            #         direction = DOWN
            #     elif event.key == K_ESCAPE:
            #         terminate()

            if (list[2] > 2) and direction != RIGHT:
                direction = LEFT
                print 'success LEFT x %f    y %f    z %f' % (list[0], list[1], list[2])
            elif (list[2] < -1) and direction != LEFT:
                direction = RIGHT
                print 'success RIGHT x %f    y %f    z %f' % (list[0], list[1], list[2])
            elif (list[0] > 1) and direction != DOWN:
                direction = UP
                print 'success UP x %f    y %f    z %f' % (list[0], list[1], list[2])
            elif (list[0] < -1) and direction != UP:
                direction = DOWN
                print 'success DOWN x %f    y %f    z %f' % (list[0], list[1], list[2])
            elif event.key == K_ESCAPE:
                terminate()
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == Cell_W or wormCoords[HEAD]['y'] == -1 or \
                wormCoords[HEAD]['y'] == Cell_H:
            return  # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return  # game over

        # check if Snake has eaten an apply
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation()  # set a new apple somewhere
        else:
            del wormCoords[-1]  # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'],
                       'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'],
                       'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD][
                                'x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD][
                                'x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        SnakespeedCLOCK.tick(Snakespeed)


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press to play.And please keep typing during the game.', True, White)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (Window_Width - 500, Window_Height - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Snake!', True, White, DARKGreen)
    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (Window_Width / 2, Window_Height / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        SnakespeedCLOCK.tick(Snakespeed)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, Cell_W - 1), 'y': random.randint(0, Cell_H - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 100)
    gameSurf = gameOverFont.render('Game', True, White)
    overSurf = gameOverFont.render('Over', True, White)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (Window_Width / 2, 10)
    overRect.midtop = (Window_Width / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, White)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (Window_Width - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * Cell_Size
        y = coord['y'] * Cell_Size
        wormSegmentRect = pygame.Rect(x, y, Cell_Size, Cell_Size)
        pygame.draw.rect(DISPLAYSURF, DARKGreen, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(
            x + 4, y + 4, Cell_Size - 8, Cell_Size - 8)
        pygame.draw.rect(DISPLAYSURF, Green, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * Cell_Size
    y = coord['y'] * Cell_Size
    appleRect = pygame.Rect(x, y, Cell_Size, Cell_Size)
    pygame.draw.rect(DISPLAYSURF, Red, appleRect)


def drawGrid():
    for x in range(0, Window_Width, Cell_Size):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, Window_Height))
    for y in range(0, Window_Height, Cell_Size):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (Window_Width, y))


if __name__ == "__main__":
    main()
