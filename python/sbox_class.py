import pygame
import pygame_gui
import os.path
import pygame
import pygame.locals as pl

pygame.font.init()

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
            pygame.draw.rect(self.display,(240,255,255),(560,100 + self.index * 90, 60, 5))
    def checkClick(self, mouse_x, mouse_y, mouse_click, array):
        if(mouse_click and mouse_x > 550 and mouse_x < 630 and mouse_y > 30 + self.index * 90 and mouse_y < 100 + self.index * 90):
            for i in range(len(array)):
                array[i].active = False
            self.active = True

###############################################################################
class Statement:
    """docstring for State."""
    def __init__(self, arg):
        super(State, self).__init__()
        self.arg = arg
        self.kind = "Statement"

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
    def show(self):
        self.display.blit(self.image, (self.x, self.y))
    def checkClick(self, commandArray, mouse_x, mouse_y, mouse_click, mouse_release):
        if mouse_release and self.drag:
            if(mouse_x > 50 and mouse_x < 300):
                if(mouse_y > commandArray[-1].y + commandArray[-1].imageHeight and mouse_y < commandArray[-1].y + commandArray[-1].imageHeight + self.imageHeight):
                    commandArray.append(Condition(commandArray[-1].x, commandArray[-1].y + commandArray[-1].imageHeight - 5, self.inputImage, self.name, self.display))
            self.drag = False
        elif(self.drag):
            self.display.blit(self.image, (mouse_x - self.imageWidth/2, mouse_y - self.imageHeight/2))
        elif(mouse_click and mouse_x > self.x and mouse_x < self.x + self.imageWidth and mouse_y > self.y and mouse_y < self.y + self.imageHeight):
            self.drag = True
        return commandArray
    def checkDelete(self, commandArray, mouse_x, mouse_y, mouse_click, index):
        if mouse_click and mouse_x > self.x and mouse_y > self.y and mouse_x < self.x + self.imageWidth and mouse_y < self.y + self.imageHeight:
            for i in range(len(commandArray)-1,index, -1):
                commandArray[i].y = commandArray[i-1].y
                commandArray[i].x = commandArray[i-1].x
            commandArray.remove(commandArray[index])
        return commandArray
    def showCommand(self,commandArray, index):
        if(len(self.commands) == 0):
            self.display.blit(self.image, (self.x, self.y))
        else:
            self.display.blit(self.firstImage, (self.x, self.y))
            self.display.blit(self.endImage, (self.x, self.y))
        return commandArray
###############################################################################
class Box:
    clickDown = False
    clickUp = False
    drag = False
    def __init__(self, x, y, image, name, manager, display):
        self.display = display
        self.x = x
        self.y = y
        self.manager = manager
        self.inputImage = image
        self.image = pygame.transform.rotozoom(image, 0, 0.45)
        self.rect = self.image.get_rect()
        self.imageWidth = self.rect[2]
        self.imageHeight = self.rect[3]
        self.name = name
        self.kind = "Box"
        if(name == "delay"):
            self.textinput = TextInput()
            self.value = 0
            self.textinput.input_string = '0'
    def show(self):
        self.display.blit(self.image, (self.x, self.y))
    def updateDelay(self):
        events = pygame.event.get()
        self.textinput.update(events)
        if(self.textinput.input_string == ''):
            self.value = 0
        else:
            try:
                self.value = int(self.textinput.input_string)
            except Exception as e:
                self.textinput.input_string = 0
    def showDelayTex(self, display, x, y):
        display.blit(self.textinput.get_surface(), (x, y))
    def checkClick(self, display, commandArray, mouse_x, mouse_y, mouse_click, mouse_release):
        if mouse_release and self.drag:
            if(mouse_x > 50 and mouse_x < 300):
                if(mouse_y > commandArray[-1].y + commandArray[-1].imageHeight and mouse_y < commandArray[-1].y + commandArray[-1].imageHeight + self.imageHeight):
                    commandArray.append(Box(commandArray[-1].x, commandArray[-1].y + commandArray[-1].imageHeight - 5, self.inputImage, self.name, self.manager, self.display))
            self.drag = False
        elif(self.drag):
            display.blit(self.image, (mouse_x - self.imageWidth/2, mouse_y - self.imageHeight/2))
        elif(mouse_click and mouse_x > self.x and mouse_x < self.x + self.imageWidth and mouse_y > self.y and mouse_y < self.y + self.imageHeight):
            self.drag = True
        return commandArray
    def checkDelete(self, commandArray, mouse_x, mouse_y, mouse_click, index):
        if mouse_click and mouse_x > self.x and mouse_y > self.y and mouse_x < self.x + self.imageWidth and mouse_y < self.y + self.imageHeight:
            for i in range(len(commandArray)-1,index, -1):
                commandArray[i].y = commandArray[i-1].y
                commandArray[i].x = commandArray[i-1].x
            commandArray.remove(commandArray[index])
        return commandArray

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
