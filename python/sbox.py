import pygame
import pygame_gui
from sbox_class import *
pygame.init()
gameDisplay = pygame.display.set_mode((1100,600))
pygame.display.set_caption('S-box')
manager = pygame_gui.UIManager((800, 600), 'theme.json')

background_color = (0,220,220)
button_color = (0,0,255)

button_layout_rect = pygame.Rect(600, 530, 150, 40)
clock = pygame.time.Clock()
crashed = False
hello_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect, text='Run', manager=manager)

start_img = pygame.image.load('start.png')
lighton_img = pygame.image.load('lightOn.png')
lightoff_img = pygame.image.load('lightOff.png')
alarmon_img = pygame.image.load('alarmOn.png')
alarmoff_img = pygame.image.load('alarmOff.png')

start = Box(50, 50, start_img, "start")
lighton = Box(600, 10, lighton_img, "lighton")
lightoff = Box(600, 70, lightoff_img, "lightoff")
alarmon = Box(600, 130, alarmon_img, "alarmon")
alarmoff = Box(600, 190, alarmoff_img, "alarmoff")

commands = [start]
mouse_x = 0
mouse_y = 0
mouse_click = False
mouse_release = False

def runCommands():
    for i in range(len(commands)):
        print(commands[i].name)

def showAll():
    start.show(gameDisplay)
    lighton.show(gameDisplay)
    lightoff.show(gameDisplay)
    alarmon.show(gameDisplay)
    alarmoff.show(gameDisplay)
def checkAll():
    global commands
    commands = lighton.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)
    commands = alarmon.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)
    commands = lightoff.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)
    commands = alarmoff.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)
def showCommands():
    global commands
    for i in range(1,len(commands)):
        gameDisplay.blit(commands[i].image, (50, 65 + i*45))
while not crashed:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    runCommands()
        elif event.type == pygame.MOUSEMOTION:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_click = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_click = False
            mouse_release = True
        manager.process_events(event)
    gameDisplay.fill(background_color)
    pygame.draw.rect(gameDisplay,(200,255,255),(30,30,500,540))
    manager.update(time_delta)
    manager.draw_ui(gameDisplay)
    showAll()
    showCommands()
    checkAll()
    pygame.display.update()
    clock.tick(60)
    mouse_click = False
    mouse_release = False
pygame.quit()
quit()
