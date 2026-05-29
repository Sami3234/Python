import pygame

pygame.init()

white = (255, 255, 255)

x = 400
y = 400

display_surface = pygame.display.set_mode((x, y))
pygame.display.set_caption("Image")

image = pygame.image.load("image.jpg")
image = pygame.transform.scale(image, (400, 400))

while True:
    display_surface.fill(white)
    display_surface.blit(image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()