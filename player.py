import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, width, height, ):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface([width, height])
        self.image = pygame.transform.scale(pygame.image.load("pixelsprite.png").convert_alpha(), (width, height))
        # self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.orientation = "right"

    def face(self, direction):
        # left
        if direction == "left":
            if self.orientation == "right":
                self.image = pygame.transform.flip(self.image, True, False)

            if self.orientation == "down":
                self.image = pygame.transform.rotate(self.image, -90)

            if self.orientation == "up":
                self.image = pygame.transform.rotate(self.image, 90)

            self.orientation = "left"
        # right
        elif direction == "right":
            if self.orientation == "left":
                self.image = pygame.transform.flip(self.image, True, False)

            if self.orientation == "down":
                self.image = pygame.transform.rotate(self.image, 90)

            if self.orientation == "up":
                self.image = pygame.transform.rotate(self.image, -90)

            self.orientation = "right"
        # up
        elif direction == "up":
            if self.orientation == "left":
                self.image = pygame.transform.rotate(self.image, -90)
            if self.orientation == "right":
                self.image = pygame.transform.rotate(self.image, 90)
            if self.orientation == "down":
                self.image = pygame.transform.rotate(self.image, 180)
            self.orientation = "up"
        # down
        elif direction == "down":
            if self.orientation == "right":
                self.image = pygame.transform.rotate(self.image, -90)
            if self.orientation == "left":
                self.image = pygame.transform.rotate(self.image, 90)
            if self.orientation == "up":
                self.image = pygame.transform.rotate(self.image, 180)
            self.orientation = "down"