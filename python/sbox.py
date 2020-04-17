import pygame
import pygame_gui
from sbox_class import *
pygame.init()
gameDisplay = pygame.display.set_mode((1100,600))
pygame.display.set_caption('S-box')
manager = pygame_gui.UIManager((1100, 600), 'theme.json')
font = pygame.font.SysFont("comicsansms", 30)
text_Codes = font.render("Commands:", True, (0, 128, 0))

background_color = (0,250,220)
button_color = (0,0,255)

button_layout_rect = pygame.Rect(900, 530, 150, 40)
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
firstif_img = pygame.image.load('firstif.png')
firstwhile_img = pygame.image.load('firstwhile.png')
firstfor_img = pygame.image.load('firstfor.png')
middle_img = pygame.image.load('middle.png')
end_img = pygame.image.load('end.png')
temphigher_img = pygame.image.load('temphigher.png')
templess_img = pygame.image.load('templess.png')
lighthigher_img = pygame.image.load('lighthigher.png')
lightless_img = pygame.image.load('lightless.png')
humidityhigher_img = pygame.image.load('humidityhigher.png')
humidityless_img = pygame.image.load('humidityless.png')
distancehigher_img = pygame.image.load('distancehigher.png')
distanceless_img = pygame.image.load('distanceless.png')

start = Box(50, 50, start_img, "start", manager,gameDisplay)
lighton = Box(700, 40, lighton_img, "lighton", manager,gameDisplay)
lightoff = Box(700, 100, lightoff_img, "lightoff", manager, gameDisplay)
alarmon = Box(700, 160, alarmon_img, "alarmon", manager, gameDisplay)
alarmoff = Box(700, 220, alarmoff_img, "alarmoff", manager, gameDisplay)
delay = Box(700, 280, delay_img, "delay", manager, gameDisplay)

cif = Condition(700, 40, [if_img, firstif_img, middle_img, end_img], "if", gameDisplay)
cwhile = Condition(700, 150, [while_img, firstwhile_img, middle_img, end_img], "while", gameDisplay)
cfor = Condition(700, 260, [for_img, firstfor_img, middle_img, end_img], "for", gameDisplay)

Events = Title(0, (50,255,50), "Events", gameDisplay)
Conditions = Title(1, (250,50,250), "Conditions", gameDisplay)
Statements = Title(2, (50,50,255), "Statements", gameDisplay)
Events.active = True

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
    start.show()
    if(Events.active):
        lighton.show()
        lightoff.show()
        alarmon.show()
        alarmoff.show()
        delay.show()
    elif(Conditions.active):
        cif.show()
        cwhile.show()
        cfor.show()

def checkAll():
    global commands
    if(Events.active):
        commands = lighton.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)
        commands = alarmon.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)
        commands = lightoff.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)
        commands = alarmoff.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)
        commands = delay.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release)
    if(Conditions.active):
        commands = cif.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release)
        commands = cfor.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release)
        commands = cwhile.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release)
    Events.checkClick(mouse_x, mouse_y, mouse_click, [Conditions, Statements, Events])
    Conditions.checkClick(mouse_x, mouse_y, mouse_click, [Conditions, Statements, Events])
    Statements.checkClick(mouse_x, mouse_y, mouse_click, [Conditions, Statements, Events])

def showCommands():
    global commands
    for i in range(1,len(commands)):
        if(commands[i].kind == "Box"):
            commands[i].show()
            if(commands[i].name == "delay"):
                commands[i].showDelayTex(gameDisplay, 110, commands[i].y + 15)
        elif(commands[i].kind == "Condition"):
            commands = commands[i].showCommand(commands, i)
    for i in range(1,len(commands)):
        if(i < len(commands) and commands[i].kind == "Box"):
            commands = commands[i].checkDelete(commands, mouse_x, mouse_y, mouse_click, i)
    if(commands[-1].name == "delay" and commands[-1].kind == "Box"):
        commands[-1].updateDelay()

def showDisplay():
    pygame.draw.rect(gameDisplay,(200,255,255),(30,40,500,540))
    pygame.draw.rect(gameDisplay,(240,255,255),(550,30,80,560))
    gameDisplay.blit(text_Codes,(30,15))
    Events.show()
    Conditions.show()
    Statements.show()


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
    manager.update(time_delta)
    manager.draw_ui(gameDisplay)
    showDisplay()
    showAll()
    showCommands()
    checkAll()
    pygame.display.update()
    clock.tick(60)
    mouse_click = False
    mouse_release = False
pygame.quit()
quit()
