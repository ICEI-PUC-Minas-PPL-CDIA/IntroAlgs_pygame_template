import pygame
import random

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    CAMINHO_POWERUP_VELOCIDADE,
    CAMINHO_POWERUP_ESCUDO,
    CAMINHO_POWERUP_TIRO,
    CAMINHO_POWERUP_TIRO_ATIVO,
)

def criar_powerup(size=100):
    """Cria um power-up em uma posição aleatória; o power-up cai (vel_y).

    `size` define largura/altura do sprite; use o mesmo tamanho dos meteoros.
    """
    tipo = random.choice(["velocidade", "escudo", "tiro"])
    x = random.randint(0, LARGURA_TELA - size)
    y = random.randint(0, 20)  # aparece dentro da tela
    rect = pygame.Rect(x, y, size, size)

    if tipo == "velocidade":
        imagem = pygame.image.load(CAMINHO_POWERUP_VELOCIDADE).convert_alpha()
    elif tipo == "escudo":
        imagem = pygame.image.load(CAMINHO_POWERUP_ESCUDO).convert_alpha()
    else:  # tiro
        imagem = pygame.image.load(CAMINHO_POWERUP_TIRO).convert_alpha()

    imagem = pygame.transform.scale(imagem, (size, size))
    vel_y = random.randint(2, 4)
    return {"tipo": tipo, "rect": rect, "imagem": imagem, "vel_y": vel_y}

def aplicar_powerup(jogador, powerup):
    """Aplica o efeito do power-up ao jogador.

    - velocidade: dobra a velocidade por 5s
    - escudo: protege de uma colisão (consumível)
    - tiro: carrega o tiro ativo (efeito tratado no loop)
    """
    tipo = powerup["tipo"]
    agora = pygame.time.get_ticks()
    if tipo == "velocidade":
        jogador["velocidade_multiplier"] = 2.0
        jogador["velocidade_ate"] = agora + 5000
    elif tipo == "escudo":
        # acumula escudos até o máximo de 3
        jogador["escudo"] = min(jogador.get("escudo", 0) + 1, 3)
    elif tipo == "tiro":
        jogador["pode_atirar"] = True
        jogador["tiro_ate"] = agora + 5000

def desenhar_powerup(tela, powerup):
    """Desenha o power-up na tela."""
    tela.blit(powerup["imagem"], powerup["rect"].topleft)   

def atualizar_powerup(jogador, powerup):
    """Verifica se o jogador pegou o power-up e aplica o efeito."""
    if jogador["rect"].colliderect(powerup["rect"]):
        aplicar_powerup(jogador, powerup)
        return True  # Power-up coletado
    return False

def desenhar_tiro(tela, jogador):
    """Desenha o tiro do jogador se ele tiver o power-up de tiro ativo."""
    if jogador.get("pode_atirar", False):
        tiro_rect = pygame.Rect(jogador["rect"].centerx - 5, jogador["rect"].top - 10, 10, 20)
        imagem_tiro = pygame.image.load(CAMINHO_POWERUP_TIRO_ATIVO).convert_alpha()
        tela.blit(imagem_tiro, tiro_rect.topleft)
