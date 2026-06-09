import random
import pygame
from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    VELOCIDADE_METEORO_MIN,
    VELOCIDADE_METEORO_MAX,
)


def criar_meteoro(level=1):
    """Cria um meteoro; a partir do level 10 vem de qualquer direção."""
    tamanho = random.randint(20, 45)
    velocidade = random.randint(VELOCIDADE_METEORO_MIN, VELOCIDADE_METEORO_MAX)

    if level >= 10:
        direcao = random.choice(["cima", "baixo", "esquerda", "direita"])
    else:
        direcao = "cima"

    if direcao == "cima":
        x = random.randint(0, LARGURA_TELA - tamanho)
        rect = pygame.Rect(x, -tamanho, tamanho, tamanho)
        vel_x, vel_y = 0, velocidade
    elif direcao == "baixo":
        x = random.randint(0, LARGURA_TELA - tamanho)
        rect = pygame.Rect(x, ALTURA_TELA, tamanho, tamanho)
        vel_x, vel_y = 0, -velocidade
    elif direcao == "esquerda":
        y = random.randint(0, ALTURA_TELA - tamanho)
        rect = pygame.Rect(-tamanho, y, tamanho, tamanho)
        vel_x, vel_y = velocidade, 0
    else:
        y = random.randint(0, ALTURA_TELA - tamanho)
        rect = pygame.Rect(LARGURA_TELA, y, tamanho, tamanho)
        vel_x, vel_y = -velocidade, 0

    return {"rect": rect, "vel_x": vel_x, "vel_y": vel_y, "tamanho": tamanho}


def mover_meteoros(meteoros):
    """Move todos os meteoros e remove os que saíram da tela."""
    for m in meteoros:
        m["rect"].x += m["vel_x"]
        m["rect"].y += m["vel_y"]
    area_valida = pygame.Rect(-100, -100, LARGURA_TELA + 200, ALTURA_TELA + 200)
    return [m for m in meteoros if m["rect"].colliderect(area_valida)]


def desenhar_meteoros(tela, meteoros, imagem=None):
    """Desenha cada meteoro como imagem ou círculo cinza se não houver imagem."""
    for m in meteoros:
        if imagem:
            img = pygame.transform.scale(imagem, (m["tamanho"], m["tamanho"]))
            tela.blit(img, m["rect"])
        else:
            pygame.draw.circle(
                tela,
                (150, 100, 60),
                m["rect"].center,
                m["tamanho"] // 2,
            )
