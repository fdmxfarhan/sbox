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
run_button = pygame_gui.elements.UIButton(relative_rect=button_layout_rect, text='Run', manager=manager)

start_img = pygame.image.load('start.png')
lighton_img = pygame.image.load('lightOn.png')
lightoff_img = pygame.image.load('lightOff.png')
alarmon_img = pygame.image.load('alarmOn.png')
alarmoff_img = pygame.image.load('alarmOff.png')
delay_img = pygame.image.load('delay.png')
if_img = pygame.image.load('if.png')
while_img = pygame.image.load('while.png')
for_img = pygame.image.load('for.png')

start = Box(50, 50, start_img, "start", manager)
lighton = Box(600, 10, lighton_img, "lighton", manager)
lightoff = Box(600, 70, lightoff_img, "lightoff", manager)
alarmon = Box(600, 130, alarmon_img, "alarmon", manager)
alarmoff = Box(600, 190, alarmoff_img, "alarmoff", manager)
delay = Box(600, 250, delay_img, "delay", manager)
bif = Box(800, 10, if_img, "if", manager)
bwhile = Box(800, 120, while_img, "while", manager)
bfor = Box(800, 230, for_img, "for", manager)

commands = [start]
mouse_x = 0
mouse_y = 0
mouse_click = False
mouse_release = False

def runCommands():
    for i in range(len(commands)):
        if(commands[i].name == "delay"):
            print(commands[i].name + ' ' + str(commands[i].value))
        else:
            print(commands[i].name)

def showAll():
    start.show(gameDisplay)
    lighton.show(gameDisplay)
    lightoff.show(gameDisplay)
    alarmon.show(gameDisplay)
    alarmoff.show(gameDisplay)
    delay.show(gameDisplay)
    bif.show(gameDisplay)
    bwhile.show(gameDisplay)
    bfor.show(gameDisplay)

def checkAll():
    global commands
    commands = lighton.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)
    commands = alarmon.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)
    commands = lightoff.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)
    commands = alarmoff.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)
    commands = delay.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)
    commands = bif.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)
    commands = bwhile.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)
    commands = bfor.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)

def showCommands():
    global commands
    for i in range(1,len(commands)):
        gameDisplay.blit(commands[i].image, (50, 65 + i*45))
        if(commands[i].name == "delay"):
            commands[i].showDelayTex(gameDisplay, 110, 80 + i*45)
    if(commands[-1].name == "delay"):
        commands[-1].updateDelay()

while not crashed:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == run_button:
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
