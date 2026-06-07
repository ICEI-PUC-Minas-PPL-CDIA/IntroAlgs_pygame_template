import pygame

pygame.init()

largura = 800
altura = 600

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Lizard Adventure")

clock = pygame.time.Clock()

lagarto = pygame.Rect(100, 450, 50, 50)

velocidade_pulo = 0

rodando = True

while rodando:

    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
        lagarto.x -= 5

    if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
        lagarto.x += 5

    if (teclas[pygame.K_w] or teclas[pygame.K_SPACE]) and lagarto.bottom == 500:
        velocidade_pulo = -15

    velocidade_pulo += 0.8
    lagarto.y += velocidade_pulo

    if lagarto.bottom >= 500:
        lagarto.bottom = 500
        velocidade_pulo = 0

    tela.fill((120, 200, 255))

    pygame.draw.rect(tela, (120, 80, 40), (0, 500, 800, 100))
    pygame.draw.rect(tela, (0, 180, 0), lagarto)

    pygame.display.update()

pygame.quit()
