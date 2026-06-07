import random
import pygame
from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    VELOCIDADE_METEORO_MIN,
    VELOCIDADE_METEORO_MAX,
)


def criar_meteoro():
    """Cria um meteoro em posição aleatória no topo da tela."""
    tamanho = random.randint(20, 45)
    x = random.randint(0, LARGURA_TELA - tamanho)
    velocidade = random.randint(VELOCIDADE_METEORO_MIN, VELOCIDADE_METEORO_MAX)
    rect = pygame.Rect(x, -tamanho, tamanho, tamanho)
    return {"rect": rect, "velocidade": velocidade, "tamanho": tamanho}


def mover_meteoros(meteoros):
    """Move todos os meteoros para baixo e remove os que saíram da tela."""
    for m in meteoros:
        m["rect"].y += m["velocidade"]
    return [m for m in meteoros if m["rect"].top < ALTURA_TELA]


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
