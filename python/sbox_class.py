import pygame

class Box:
    clickDown = False
    clickUp = False
    drag = False
    def __init__(self, x, y, image, name):
        self.x = x
        self.y = y
        self.image = pygame.transform.rotozoom(image, 0, 0.45)
        self.rect = self.image.get_rect()
        self.imageWidth = self.rect[2]
        self.imageHeight = self.rect[3]
        self.name = name
    def show(self, display):
        display.blit(self.image, (self.x, self.y))
    def checkClick(self, display, commandArray, mouse_x, mouse_y, mouse_click, mouse_release):
        if mouse_release and self.drag:
            if(mouse_x > 50 and mouse_x < 50 + self.imageWidth):
                if(mouse_y > 65 + 52*len(commandArray) and mouse_y < 65 + 52*len(commandArray) + 52):
                    commandArray.append(self)
            self.drag = False
        elif(self.drag):
            display.blit(self.image, (mouse_x - self.imageWidth/2, mouse_y - self.imageHeight/2))
        elif(mouse_click and mouse_x > self.x and mouse_x < self.x + self.imageWidth and mouse_y > self.y and mouse_y < self.y + self.imageHeight):
            self.drag = True
        return commandArray
