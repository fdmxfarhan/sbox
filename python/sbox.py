import pygame
from sbox_class import *

pygame.init()
gameDisplay = pygame.display.set_mode((1100,600))
pygame.display.set_caption('S-box')
font = pygame.font.SysFont("tahoma", 20)
text_Codes = font.render("Commands:", True, (0, 128, 0))

################################################ Loading Images
start_img = pygame.image.load('start.png')
lighton_img = pygame.image.load('lightOn.png')
lightoff_img = pygame.image.load('lightOff.png')
alarmon_img = pygame.image.load('alarmOn.png')
alarmoff_img = pygame.image.load('alarmOff.png')
vibrateon_img = pygame.image.load('vibrateon.png')
vibrateoff_img = pygame.image.load('vibrateoff.png')
delay_img = pygame.image.load('delay.png')
if_img = pygame.image.load('if.png')
while_img = pygame.image.load('while.png')
for_img = pygame.image.load('for.png')
forever_img = pygame.image.load('forever.png')
firstif_img = pygame.image.load('firstif.png')
firstwhile_img = pygame.image.load('firstwhile.png')
firstfor_img = pygame.image.load('firstfor.png')
firstforever_img = pygame.image.load('firstforever.png')
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
true_img = pygame.image.load('true.png')
false_img = pygame.image.load('false.png')
run_img = pygame.image.load('run.png')
stop_img = pygame.image.load('stop.png')
clear_img = pygame.image.load('clear.png')
temp_img = pygame.image.load('temperature.png')
light_img = pygame.image.load('light.png')
humidity_img = pygame.image.load('humidity.png')
distance_img = pygame.image.load('distance.png')

################################################# Buttons
run_btn = Button(900, 510, run_img, 0.15, "run", gameDisplay)
stop_btn = Button(1000, 510, stop_img, 0.37, "stop", gameDisplay)
clear_btn = Button(410, 530, clear_img, 0.13, "clear", gameDisplay)

################################################# Commandes
start = Command(50, 50, start_img, "start",gameDisplay)
lighton = Command(700, 40, lighton_img, "lighton",gameDisplay)
lightoff = Command(700, 100, lightoff_img, "lightoff", gameDisplay)
alarmon = Command(700, 160, alarmon_img, "alarmon", gameDisplay)
alarmoff = Command(700, 220, alarmoff_img, "alarmoff", gameDisplay)
vibrateon = Command(700, 280, vibrateon_img, "vibrateon", gameDisplay)
vibrateoff = Command(700, 340, vibrateoff_img, "vibrateoff", gameDisplay)
delay = Command(850, 40, delay_img, "delay", gameDisplay)

################################################# Conditions
cif = Condition(700, 40, [if_img, firstif_img, middle_img, end_img], "if", gameDisplay)
cwhile = Condition(700, 150, [while_img, firstwhile_img, middle_img, end_img], "while", gameDisplay)
cfor = Condition(700, 260, [for_img, firstfor_img, middle_img, end_img], "for", gameDisplay)
cforever = Condition(700, 370, [forever_img, firstforever_img, middle_img, end_img], "forever", gameDisplay)

################################################# Statements
temphigher = Statement(700, 40, temphigher_img, "temphigher", gameDisplay)
templess = Statement(700, 90, templess_img, "templess", gameDisplay)
lighthigher = Statement(700, 140, lighthigher_img, "lighthigher", gameDisplay)
lightless = Statement(700, 190, lightless_img, "lightless", gameDisplay)
humidityhigher = Statement(700, 240, humidityhigher_img, "humidityhigher", gameDisplay)
humidityless = Statement(700, 290, humidityless_img, "humidityless", gameDisplay)
distancehigher = Statement(700, 340, distancehigher_img, "distancehigher", gameDisplay)
distanceless = Statement(700, 390, distanceless_img, "distanceless", gameDisplay)
true = Statement(700, 440, true_img, "true", gameDisplay)
false = Statement(700, 490, false_img, "false", gameDisplay)

################################################# Titles
Events = Title(0, (50,255,50), "Commands", gameDisplay)
Conditions = Title(1, (250,50,250), "Conditions", gameDisplay)
Statements = Title(2, (50,50,255), "Statements", gameDisplay)
Values = Title(3, (255,255,50), "Values", gameDisplay)
Display = Title(4, (255,100,100), "Display", gameDisplay)

################################################# Values

Events.active = True
################################################ Variables
commands = [start]
mouse_x = 0
mouse_y = 0
mouse_click = False
mouse_release = False
mouse_right_click = False
background_color = (150,250,250)
button_color = (0,0,255)
clock = pygame.time.Clock()
crashed = False
doScroll = False
last_scr = 0
scr = 0
server = Server()

def runCommands():
    mouse_click = False
    mouse_release = False
    showAll()
    checkAll()
    server.connect()
    for i in range(len(commands)):
        if(commands[i].name == "delay"):
            print(commands[i].name + ' ' + str(commands[i].value))
        else:
            print(commands[i].name)
        commands[i].run(server, stop_btn)

def showAll():
    start.show()
    if(Events.active):
        lighton.show()
        lightoff.show()
        alarmon.show()
        alarmoff.show()
        vibrateon.show()
        vibrateoff.show()
        delay.show()
    elif(Conditions.active):
        cif.show()
        cwhile.show()
        cfor.show()
        cforever.show()
    elif(Statements.active):
        temphigher.show()
        templess.show()
        humidityhigher.show()
        humidityless.show()
        lighthigher.show()
        lightless.show()
        distancehigher.show()
        distanceless.show()
        true.show()
        false.show()
    run_btn.show()
    stop_btn.show()
    clear_btn.show()
def checkAll():
    global commands
    if(Events.active):
        commands = lighton.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = alarmon.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = lightoff.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = alarmoff.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = vibrateon.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = vibrateoff.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = delay.checkClick(gameDisplay, commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
    elif(Conditions.active):
        commands = cif.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = cfor.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = cwhile.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = cforever.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
    elif(Statements.active):
        commands = temphigher.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = templess.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = humidityhigher.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = humidityless.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = lighthigher.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = lightless.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = distancehigher.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = distanceless.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = true.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
        commands = false.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release, scr)
    Events.checkClick(mouse_x, mouse_y, mouse_click, [Conditions, Statements, Events, Values, Display])
    Conditions.checkClick(mouse_x, mouse_y, mouse_click, [Conditions, Statements, Events, Values, Display])
    Statements.checkClick(mouse_x, mouse_y, mouse_click, [Conditions, Statements, Events, Values, Display])
    Values.checkClick(mouse_x, mouse_y, mouse_click, [Conditions, Statements, Events, Values, Display])
    Display.checkClick(mouse_x, mouse_y, mouse_click, [Conditions, Statements, Events, Values, Display])

    commands = run_btn.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release)
    commands = stop_btn.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release)
    commands = clear_btn.checkClick(commands, mouse_x, mouse_y, mouse_click, mouse_release)

def showCommands():
    global commands
    for i in range(0,len(commands)):
        if(commands[i].kind == "Command"):
            commands[i].scroll = scr
            commands[i].show()
            if(commands[i].name == "delay"):
                commands[i].updateNumber(mouse_x, mouse_y, mouse_click)
        elif(commands[i].kind == "Condition"):
            commands[i].scroll = scr
            commands = commands[i].showCommand(commands, i)
            if(commands[i].name == "for"):
                commands[i].updateNumber(mouse_x, mouse_y, mouse_click)
    for i in range(1,len(commands)):
        if(i < len(commands)):
            commands = commands[i].checkDelete(commands, mouse_x, mouse_y + scr, mouse_right_click, i, mouse_click)

def showDisplay():
    pygame.draw.rect(gameDisplay,(200,255,255),(30,40,500,540))
    pygame.draw.rect(gameDisplay,(220,255,255),(550,30,80,560))
    Events.show()
    Conditions.show()
    Statements.show()
    Values.show()
    Display.show()

def scroll():
    global scr, doScroll, last_scr
    scr /= 2
    if(mouse_x > 510 and mouse_x < 530 and mouse_y < 580 and mouse_y > 40 or doScroll):
        pygame.draw.rect(gameDisplay,(235,235,235),(520,40,10,540))
        if(mouse_click):
            scr = mouse_y - 60
    else:
        pygame.draw.rect(gameDisplay,(245,245,245),(520,40,10,540))
    if(mouse_click and mouse_x > 515 and mouse_x < 535 and mouse_y < 49 + 32 + scr and mouse_y > 49 + scr):
        doScroll = True
    elif(mouse_release):
        doScroll = False
    if(doScroll):
        scr = mouse_y - 60
    if(scr < 0):
        scr = 0
    if(scr >490):
        scr = 490
    pygame.draw.rect(gameDisplay,(210,210,210),(520,50 + scr,10,30))
    scr *= 2
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
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 4 and event.pos[0] < 550:
            scr -= 5
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 5 and event.pos[0] < 550:
            scr += 5
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_right_click = True
    gameDisplay.fill(background_color)
    showDisplay()
    showAll()
    showCommands()
    pygame.draw.rect(gameDisplay, background_color, (30,0,500,40))
    pygame.draw.rect(gameDisplay, background_color, (30,580,500,600))
    gameDisplay.blit(text_Codes,(30,15))
    scroll()
    checkAll()
    if(run_btn.click(mouse_x, mouse_y, mouse_click, mouse_release)):
        runCommands()
    pygame.display.update()
    clock.tick(60)
    mouse_click = False
    mouse_release = False
    mouse_right_click = False
pygame.quit()
quit()
server.close()
