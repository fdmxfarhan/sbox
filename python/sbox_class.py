import pygame
import os.path
import pygame
import pygame.locals as pl
import socket
import time
HOST = '0.0.0.0'
PORT = 3000

pygame.font.init()

class Server:
    """docstring for Server."""
    def __init__(self):
        socket.setdefaulttimeout(0.1)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
        try:
            self.s.listen(12)
            self.WiFi = True
        except:
            print('[ Error ] You are not connected to any network.!!')
            self.WiFi = False
        self.box = {}
    def connect(self):
        for i in range(10):
            try:
                conn, addr = self.s.accept()
                conn.send(b'N')
                time.sleep(0.5)
                name = str(conn.recv(100))
                self.box[name] = conn
            except Exception as e:
                pass
        print(self.box)
    def close(self):
        self.s.close()
    def lightOn(self):
        try:
            self.box['alarm'].send(b'L')
        except:
            print("[ Error ] alarm box is not connected.")
    def lightOff(self):
        try:
            self.box['alarm'].send(b'l')
        except:
            print("[ Error ] alarm box is not connected.")
    def buzzerOn(self):
        try:
            self.box['alarm'].send(b'B')
        except:
            print("[ Error ] alarm box is not connected.")
    def buzzerOff(self):
        try:
            self.box['alarm'].send(b'b')
        except:
            print("[ Error ] alarm box is not connected.")
    def vibrateOn(self):
        try:
            self.box['alarm'].send(b'V')
        except:
            print("[ Error ] alarm box is not connected.")
    def vibrateOff(self):
        try:
            self.box['alarm'].send(b'v')
        except:
            print("[ Error ] alarm box is not connected.")

class Button:
    def __init__(self, x, y, image, scale, name, display):
        self.x = x
        self.y = y
        self.image = pygame.transform.rotozoom(image, 0, scale)
        self.image2 = pygame.transform.rotozoom(image, 0, scale)
        self.rect = self.image.get_rect()
        self.imageWidth = self.rect[2]
        self.imageHeight = self.rect[3]
        self.name = name
        self.display = display
    def show(self):
        self.display.blit(self.image,(self.x, self.y))
    def checkClick(self, commandArray, mouse_x, mouse_y, mouse_click, mouse_release):
        if(mouse_click and mouse_x > self.x and mouse_x < self.x + self.imageWidth and mouse_y > self.y and mouse_y < self.y + self.imageHeight):
            self.image = pygame.transform.rotozoom(self.image, 0, 1.05)
            if(self.name == "clear"):
                for comm in commandArray[1:]:
                    commandArray.remove(comm)
        elif(mouse_release):
            self.image = self.image2
        return commandArray
    def click(self, mouse_x, mouse_y, mouse_click, mouse_release):
        if(mouse_click and mouse_x > self.x and mouse_x < self.x + self.imageWidth and mouse_y > self.y and mouse_y < self.y + self.imageHeight):
            return True
        else:
            return False

###################################################### Titles
class Title:
    """docstring for Title."""
    def __init__(self, index, color, name, diplay):
        self.index = index
        self.name = name
        self.display = diplay
        self.color = color
        font = pygame.font.SysFont("tahoma", 14)
        self.text = font.render(name, True, (color[0] - 50, color[1] - 50, color[2] - 50))
        self.active = False
        self.kind = "Title"
    def show(self):
        pygame.draw.circle(self.display,self.color,(590,60 + self.index * 90), 15)
        self.display.blit(self.text,(590 - self.text.get_width()/2,80 + self.index * 90))
        if(self.active):
            pygame.draw.rect(self.display,self.color,(560,100 + self.index * 90, 60, 5))
        else:
            pygame.draw.rect(self.display,(220,255,255),(560,100 + self.index * 90, 60, 5))
    def checkClick(self, mouse_x, mouse_y, mouse_click, array):
        if(mouse_click and mouse_x > 550 and mouse_x < 630 and mouse_y > 30 + self.index * 90 and mouse_y < 100 + self.index * 90):
            for i in range(len(array)):
                array[i].active = False
            self.active = True

###############################################################################
class Statement:
    """docstring for State."""
    def __init__(self, x, y, image, name, display):
        self.display = display
        self.x = x
        self.y = y
        self.image = pygame.transform.rotozoom(image, 0, 0.45)
        self.name = name
        self.inputImage = image
        self.rect = self.image.get_rect()
        self.imageWidth = self.rect[2]
        self.imageHeight = self.rect[3]
        self.state = False
        self.drag = False
        self.kind = "Statement"
        self.scroll = 0
    def show(self):
        self.display.blit(self.image, (self.x, self.y - self.scroll))
    def checkCondition(self, commandArray, mouse_x, mouse_y, mouse_click, mouse_release, comm):
        flag = True
        for in_comm in comm.commands:
            if(in_comm.kind == "Condition"):
                if(mouse_y > in_comm.y and mouse_y < in_comm.y + in_comm.imageHeight):
                    comm.commmands = self.checkCondition(comm.commands, mouse_x, mouse_y, mouse_click, mouse_release, in_comm)
                    flag = False
                    return commandArray
        if(mouse_x > comm.x and mouse_y > comm.y and mouse_x < comm.x + 300 and mouse_y < comm.y + comm.imageHeight):
            comm.state = Statement(comm.x + 40, comm.y + 3, self.inputImage, self.name, self.display)
        return commandArray
    def checkClick(self, commandArray, mouse_x, mouse_y, mouse_click, mouse_release, scr):
        if mouse_release and self.drag:
            mouse_y += scr
            for comm in commandArray:
                if(comm.kind == "Condition" and comm.name != "for"):
                    commandArray = self.checkCondition(commandArray, mouse_x, mouse_y, mouse_click, mouse_release, comm)
            self.drag = False
        elif(self.drag):
            self.display.blit(self.image, (mouse_x - self.imageWidth/2, mouse_y - self.imageHeight/2))
        elif(mouse_click and mouse_x > self.x and mouse_x < self.x + self.imageWidth and mouse_y > self.y and mouse_y < self.y + self.imageHeight):
            self.drag = True
        return commandArray
    def checkDelete(self, commandArray, mouse_x, mouse_y, mouse_click, index):
        if len(self.commands) == 0 and mouse_click and mouse_x > self.x and mouse_y > self.y and mouse_x < self.x + self.imageWidth and mouse_y < self.y + self.imageHeight:
            for i in range(len(commandArray)-1,index, -1):
                commandArray[i].y = commandArray[i-1].y
                commandArray[i].x = commandArray[i-1].x
            commandArray.remove(commandArray[index])
        return commandArray

###############################################################################
class Condition:
    """docstring for Condition."""
    def __init__(self, x, y, image, name, display):
        self.display = display
        self.x = x
        self.y = y
        self.image = pygame.transform.rotozoom(image[0], 0, 0.45)
        self.firstImage = pygame.transform.rotozoom(image[1], 0, 0.45)
        self.middleImage = pygame.transform.rotozoom(image[2], 0, 0.45)
        self.endImage = pygame.transform.rotozoom(image[3], 0, 0.45)
        self.firstImageWidth = self.firstImage.get_rect()[2]
        self.middleImageWidth = self.middleImage.get_rect()[2]
        self.endImageWidth = self.endImage.get_rect()[2]
        self.firstImageHeight = self.firstImage.get_rect()[3]
        self.middleImageHeight = self.middleImage.get_rect()[3]
        self.endImageHeight = self.endImage.get_rect()[3]
        self.name = name
        self.inputImage = image
        self.rect = self.image.get_rect()
        self.imageWidth = self.rect[2]
        self.imageHeight = self.rect[3]
        self.state = False
        self.drag = False
        self.kind = "Condition"
        self.commands = []
        self.scroll = 0
    def show(self):
        self.display.blit(self.image, (self.x, self.y))
    def checkCondition(self, commandArray, mouse_x, mouse_y, mouse_click, mouse_release, comm):
        for in_comm in comm.commands:
            if(in_comm.kind == "Condition"):
                if(mouse_y > in_comm.y and mouse_y < in_comm.y + in_comm.imageHeight):
                    comm.commands = self.checkCondition(comm.commands, mouse_x, mouse_y, mouse_click, mouse_release, in_comm)
                    return commandArray
        if(len(comm.commands) == 0):
            comm.commands.append(Condition(comm.x + 15, comm.y + comm.firstImageHeight - 5, self.inputImage, self.name, self.display))
            for i in range(commandArray.index(comm) + 1, len(commandArray)):
                commandArray[i].y += comm.commands[-1].imageHeight - 20
        else:
            comm.commands.append(Condition( comm.commands[-1].x, comm.commands[-1].y + comm.commands[-1].imageHeight - 5, self.inputImage, self.name, self.display))
            for i in range(commandArray.index(comm) + 1, len(commandArray)):
                commandArray[i].y += comm.commands[-1].imageHeight - 5
        return commandArray
    def checkClick(self, commandArray, mouse_x, mouse_y, mouse_click, mouse_release, scr):
        if mouse_release and self.drag:
            mouse_y += scr
            if(mouse_x > 50 and mouse_x < 300):
                for comm in commandArray:
                    if (comm.kind == "Condition" and len(comm.commands) == 0):
                        if(mouse_y > comm.y and mouse_y < comm.y + comm.imageHeight):
                            comm.commands.append(Condition(comm.x + 15, comm.y + comm.firstImageHeight - 5, self.inputImage, self.name, self.display))
                            for i in range(commandArray.index(comm) + 1, len(commandArray)):
                                commandArray[i].y += comm.commands[-1].imageHeight - 20
                    elif(comm.kind == "Condition" and mouse_y > comm.y and mouse_y < comm.commands[-1].y + comm.commands[-1].imageHeight):
                        commandArray = self.checkCondition(commandArray, mouse_x, mouse_y, mouse_click, mouse_release, comm)
                if(mouse_y > commandArray[-1].y + commandArray[-1].imageHeight and mouse_y < commandArray[-1].y + commandArray[-1].imageHeight + self.imageHeight):
                    commandArray.append(Condition(commandArray[-1].x, commandArray[-1].y + commandArray[-1].imageHeight - 5, self.inputImage, self.name, self.display))
            self.drag = False
        elif(self.drag):
            self.display.blit(self.image, (mouse_x - self.imageWidth/2, mouse_y - self.imageHeight/2))
        elif(mouse_click and mouse_x > self.x and mouse_x < self.x + self.imageWidth and mouse_y > self.y and mouse_y < self.y + self.imageHeight):
            self.drag = True
        for comm in self.commands:
            if(comm.kind == "Condition"):
                comm.commands = comm.checkClick(comm.commands, mouse_x, mouse_y, mouse_click, self.commands.index(comm))
        return commandArray
    def checkDelete(self, commandArray, mouse_x, mouse_y, mouse_click, index, mouse_left_click):
        if len(self.commands) == 0 and mouse_click and mouse_x > self.x and mouse_y > self.y and mouse_x < self.x + self.imageWidth and mouse_y < self.y + self.imageHeight:
            for i in range(len(commandArray)-1,index, -1):
                commandArray[i].y = commandArray[i-1].y
                commandArray[i].x = commandArray[i-1].x
            commandArray.remove(commandArray[index])
        for comm in self.commands:
            self.commands = comm.checkDelete(self.commands, mouse_x, mouse_y, mouse_click, self.commands.index(comm), mouse_left_click)
        return commandArray
    def showCommand(self,commandArray, index):
        if(len(self.commands) == 0):
            self.display.blit(self.image, (self.x, self.y - self.scroll))
            self.imageHeight = self.rect[3]
            cnt = 0
            for i in range(index + 1, len(commandArray)):
                commandArray[i].y =  self.y + self.imageHeight + cnt - 5
                cnt += commandArray[i].imageHeight -5
        else:
            self.imageHeight = self.firstImageHeight + self.endImageHeight - 5
            self.display.blit(self.firstImage, (self.x, self.y - self.scroll))
            cnt = 0
            for comm in self.commands:
                for i in range(comm.y - self.scroll, comm.y - self.scroll + comm.imageHeight, 5):
                    self.display.blit(self.middleImage, (comm.x - 15, i))
                comm.y = self.y + self.firstImageHeight + cnt - 5
                cnt += comm.imageHeight - 5
                if(comm.kind == "Box"):
                    comm.scroll = self.scroll
                    comm.show()
                elif(comm.kind == "Condition"):
                    comm.scroll = self.scroll
                    self.commands = comm.showCommand(self.commands, self.commands.index(comm))
                self.imageHeight += comm.imageHeight - 5
            self.display.blit(self.endImage, (self.x, self.commands[-1].y - self.scroll + self.commands[-1].imageHeight - 5))
            cnt = 0
            for i in range(index + 1, len(commandArray)):
                commandArray[i].y = self.commands[-1].y + self.commands[-1].imageHeight + self.endImageHeight + cnt - 10
                cnt += commandArray[i].imageHeight -5
        if(self.state):
            self.state.x = self.x + 40
            self.state.y = self.y + 3
            self.state.scroll = self.scroll
            self.state.show()
        return commandArray
###############################################################################
class Box:
    clickDown = False
    clickUp = False
    drag = False
    def __init__(self, x, y, image, name, display):
        self.display = display
        self.x = x
        self.y = y
        self.inputImage = image
        self.image = pygame.transform.rotozoom(image, 0, 0.45)
        self.rect = self.image.get_rect()
        self.imageWidth = self.rect[2]
        self.imageHeight = self.rect[3]
        self.name = name
        self.kind = "Box"
        self.scroll = 0
        if(name == "delay"):
            self.textinput = inputText(self.x + 60, self.y + 15, display)
            self.value = 0
            self.textinput.text = '1'
        self.selected  = False
    def show(self):
        self.display.blit(self.image, (self.x, self.y - self.scroll))
        if(self.name == "delay"):
            self.textinput.x = self.x + 60
            self.textinput.y = self.y + 15
            self.textinput.show(self.scroll)
            if(self.selected):
                self.textinput.get()
            if(self.textinput.text != ''):
                self.value = int(self.textinput.text)
    def updateDelay(self, mouse_x, mouse_y, mouse_click):
        mouse_y += self.scroll
        if mouse_click and mouse_x > self.x and mouse_y > self.y and mouse_x < self.x + self.imageWidth and mouse_y < self.y + self.imageHeight:
            self.selected = True
            self.textinput.text = ''
        elif mouse_click:
            self.selected = False
    def checkCondition(self, display, commandArray, mouse_x, mouse_y, mouse_click, mouse_release, comm):
        flag = True
        for comm2 in comm.commands:
            if(comm2.kind == "Condition"):
                comm.commands, flag = self.checkCondition(display, comm.commands, mouse_x, mouse_y, mouse_click, mouse_release, comm2)
        if flag:
            if(len(comm.commands) == 0):
                if(mouse_y > comm.y and mouse_y < comm.y + comm.imageHeight):
                    comm.commands.append(Box( comm.x + 15, comm.y + comm.firstImageHeight - 5, self.inputImage, self.name, self.display))
                    flag = False
                    for i in range(commandArray.index(comm) + 1, len(commandArray)):
                        commandArray[i].y += comm.commands[-1].imageHeight - 20
            elif(comm.kind == "Condition" and mouse_y > comm.y and mouse_y < comm.commands[-1].y + comm.commands[-1].imageHeight + 30):
                comm.commands.append(Box( comm.commands[-1].x, comm.commands[-1].y + comm.commands[-1].imageHeight - 5, self.inputImage, self.name, self.display))
                flag = False
                for i in range(commandArray.index(comm) + 1, len(commandArray)):
                    commandArray[i].y += comm.commands[-1].imageHeight - 5
        return commandArray, flag
    def checkClick(self, display, commandArray, mouse_x, mouse_y, mouse_click, mouse_release, scr):
        if mouse_release and self.drag:
            mouse_y += scr
            if(mouse_x > 50 and mouse_x < 300):
                for comm in commandArray:
                    if (comm.kind == "Condition"):
                        commandArray, flag = self.checkCondition(display, commandArray, mouse_x, mouse_y, mouse_click, mouse_release, comm)
                if(mouse_y > commandArray[-1].y + commandArray[-1].imageHeight and mouse_y < commandArray[-1].y + commandArray[-1].imageHeight + self.imageHeight):
                    commandArray.append(Box(commandArray[-1].x, commandArray[-1].y + commandArray[-1].imageHeight - 5, self.inputImage, self.name, self.display))
            self.drag = False
        elif(self.drag):
            display.blit(self.image, (mouse_x - self.imageWidth/2, mouse_y - self.imageHeight/2))
        elif(mouse_click and mouse_x > self.x and mouse_x < self.x + self.imageWidth and mouse_y > self.y and mouse_y < self.y + self.imageHeight):
            self.drag = True
        return commandArray
    def checkDelete(self, commandArray, mouse_x, mouse_y, mouse_click, index, mouse_left_click):
        if(self.name == "delay"):
            self.updateDelay(mouse_x, mouse_y, mouse_left_click)
        if mouse_click and mouse_x > self.x and mouse_y > self.y and mouse_x < self.x + self.imageWidth and mouse_y < self.y + self.imageHeight:
            for i in range(len(commandArray)-1,index, -1):
                commandArray[i].y = commandArray[i-1].y
                commandArray[i].x = commandArray[i-1].x
            commandArray.remove(commandArray[index])
        return commandArray

class inputText:
    def __init__(self, x, y, display):
        self.x = x
        self.y = y
        self.display = display
        self.font = pygame.font.SysFont("tahoma", 14)
        self.text = ''
    def show(self, scroll):
        self.font_text = self.font.render(self.text, True, (100,100,100,100))
        self.display.blit(self.font_text, (self.x, self.y - scroll))
    def get(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if(event.key >= 48 and event.key <= 57):
                    self.text += event.unicode

class TextInput:
    """
    This class lets the user input a piece of text, e.g. a name or a message.
    This class let's the user input a short, one-lines piece of text at a blinking cursor
    that can be moved using the arrow-keys. Delete, home and end work as well.
    """
    def __init__(
            self,
            initial_string="",
            font_family="",
            font_size=20,
            antialias=True,
            text_color=(0, 0, 0),
            cursor_color=(0, 0, 1),
            repeat_keys_initial_ms=400,
            repeat_keys_interval_ms=35,
            max_string_length=-1):
        """
        :param initial_string: Initial text to be displayed
        :param font_family: name or list of names for font (see pygame.font.match_font for precise format)
        :param font_size:  Size of font in pixels
        :param antialias: Determines if antialias is applied to font (uses more processing power)
        :param text_color: Color of text (duh)
        :param cursor_color: Color of cursor
        :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
        :param repeat_keys_interval_ms: Interval between key press repetition when held
        :param max_string_length: Allowed length of text
        """

        # Text related vars:
        self.antialias = antialias
        self.text_color = text_color
        self.font_size = font_size
        self.max_string_length = max_string_length
        self.input_string = initial_string  # Inputted text

        if not os.path.isfile(font_family):
            font_family = pygame.font.match_font(font_family)

        self.font_object = pygame.font.Font(font_family, font_size)

        # Text-surface will be created during the first update call:
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)


        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size / 20 + 1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(initial_string)  # Inside text
        self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  # /|\
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
                if event.key not in self.keyrepeat_counters:
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pl.K_BACKSPACE:
                    self.input_string = (
                        self.input_string[:max(self.cursor_position - 1, 0)]
                        + self.input_string[self.cursor_position:]
                    )

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == pl.K_DELETE:
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + self.input_string[self.cursor_position + 1:]
                    )

                elif event.key == pl.K_RETURN:
                    return True

                elif event.key == pl.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                elif event.key == pl.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pl.K_END:
                    self.cursor_position = len(self.input_string)

                elif event.key == pl.K_HOME:
                    self.cursor_position = 0

                elif len(self.input_string) < self.max_string_length or self.max_string_length == -1:
                    # If no special key is pressed, add unicode of key to input_string
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + event.unicode
                        + self.input_string[self.cursor_position:]
                    )
                    self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

            elif event.type == pl.KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

        # Update key counters:
        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = (
                    self.keyrepeat_intial_interval_ms
                    - self.keyrepeat_interval_ms
                )

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pygame.event.post(pygame.event.Event(pl.KEYDOWN, key=event_key, unicode=event_unicode))

        # Re-render text surface:
        self.surface = self.font_object.render(self.input_string, self.antialias, self.text_color)

        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            cursor_y_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if self.cursor_position > 0:
                cursor_y_pos -= self.cursor_surface.get_width()
            self.surface.blit(self.cursor_surface, (cursor_y_pos, 0))

        self.clock.tick()
        return False

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self.input_string = ""
        self.cursor_position = 0
