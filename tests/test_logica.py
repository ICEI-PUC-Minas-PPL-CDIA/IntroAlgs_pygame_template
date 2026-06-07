from src.funcoes import calcular_pontos, jogador_perdeu, limitar_valor, tomar_dano, verificar_colisao
import pygame


def test_calcular_pontos():
    """Deve somar corretamente os pontos atuais com os pontos ganhos."""
    assert calcular_pontos(10, 5) == 15


def test_jogador_perdeu_com_zero_vidas():
    """Deve indicar derrota quando o total de vidas chega a zero."""
    assert jogador_perdeu(0) is True


def test_jogador_nao_perdeu_com_vidas():
    """Nao deve indicar derrota quando o jogador ainda tem vidas."""
    assert jogador_perdeu(3) is False


def test_limitar_valor_abaixo_do_minimo():
    """Deve retornar o limite minimo quando o valor informado for menor."""
    assert limitar_valor(-5, 0, 100) == 0


def test_limitar_valor_acima_do_maximo():
    """Deve retornar o limite maximo quando o valor informado for maior."""
    assert limitar_valor(150, 0, 100) == 100


def test_limitar_valor_dentro_do_intervalo():
    """Deve manter o valor original quando ele ja estiver no intervalo."""
    assert limitar_valor(50, 0, 100) == 50


def test_tomar_dano():
    """Deve subtrair o dano das vidas corretamente."""
    assert tomar_dano(3, 1) == 2


def test_verificar_colisao_sobrepostos():
    """Dois rects sobrepostos devem colidir."""
    pygame.init()
    r1 = pygame.Rect(0, 0, 50, 50)
    r2 = pygame.Rect(25, 25, 50, 50)
    assert verificar_colisao(r1, r2) is True


def test_verificar_colisao_separados():
    """Dois rects separados nao devem colidir."""
    pygame.init()
    r1 = pygame.Rect(0, 0, 50, 50)
    r2 = pygame.Rect(200, 200, 50, 50)
    assert verificar_colisao(r1, r2) is False
