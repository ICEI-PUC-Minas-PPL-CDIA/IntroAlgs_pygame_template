import pygame
from src.config import (
    LARGURA_TELA, ALTURA_TELA, FPS, TITULO_JOGO,
    AZUL_ESCURO, BRANCO, VERMELHO, AMARELO,
    VELOCIDADE_JOGADOR, VIDAS_INICIAIS,
    INTERVALO_METEORO_INICIAL, INTERVALO_METEORO_MINIMO, REDUCAO_INTERVALO,
    CAMINHO_NAVE, CAMINHO_METEORO, CAMINHO_FUNDO,
)
from src.funcoes import limitar_valor, verificar_colisao, tomar_dano, jogador_perdeu
from src.meteoro import criar_meteoro, mover_meteoros, desenhar_meteoros
from src.dados import obter_recorde_jogador, atualizar_ranking

TAMANHO_NAVE = (60, 52)
TAMANHO_METEORO_BASE = 45


def _carregar_imagens():
    """Tenta carregar imagens separadas; retorna None se falhar."""
    try:
        nave = pygame.image.load(CAMINHO_NAVE).convert_alpha()
        nave = pygame.transform.scale(nave, TAMANHO_NAVE)
        meteoro = pygame.image.load(CAMINHO_METEORO).convert_alpha()
        meteoro = pygame.transform.scale(meteoro, (TAMANHO_METEORO_BASE, TAMANHO_METEORO_BASE))
        fundo = pygame.image.load(CAMINHO_FUNDO).convert()
        fundo = pygame.transform.scale(fundo, (LARGURA_TELA, ALTURA_TELA))
        return nave, meteoro, fundo
    except Exception:
        return None, None, None


def _tela_inicial(tela, fonte_grande, fonte):
    tela.fill((0, 0, 0))
    titulo = fonte_grande.render("SpaceNinja", True, AMARELO)
    dica = fonte.render("Pressione ENTER para começar   ESC para sair", True, (180, 180, 180))
    tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, ALTURA_TELA // 2 - 60))
    tela.blit(dica, (LARGURA_TELA // 2 - dica.get_width() // 2, ALTURA_TELA // 2 + 20))
    pygame.display.flip()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()


def _tela_login(tela, fonte_grande, fonte):
    nome = ""
    while True:
        tela.fill((0, 0, 0))
        titulo = fonte_grande.render("SpaceNinja", True, AMARELO)
        instrucao = fonte.render("Digite seu nome e pressione ENTER:", True, BRANCO)
        campo = fonte.render(nome + "|", True, BRANCO)
        tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, ALTURA_TELA // 2 - 120))
        tela.blit(instrucao, (LARGURA_TELA // 2 - instrucao.get_width() // 2, ALTURA_TELA // 2 - 20))
        tela.blit(campo, (LARGURA_TELA // 2 - campo.get_width() // 2, ALTURA_TELA // 2 + 20))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif evento.key == pygame.K_RETURN and nome.strip():
                    return nome.strip()
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                elif len(nome) < 20:
                    nome += evento.unicode


def _desenhar_hud(tela, fonte, pontos, vidas, recorde):
    tela.blit(fonte.render(f"Pontos: {pontos}", True, BRANCO), (10, 10))
    tela.blit(fonte.render(f"Vidas: {vidas}", True, AMARELO), (10, 40))
    txt = fonte.render(f"Recorde: {recorde}", True, AMARELO)
    tela.blit(txt, (LARGURA_TELA - txt.get_width() - 10, 10))


def _tela_game_over(tela, fonte_grande, fonte, pontos, recorde):
    tela.fill((0, 0, 0))
    msg = fonte_grande.render("GAME OVER", True, VERMELHO)
    sub = fonte.render(f"Pontuação: {pontos}   Recorde: {recorde}", True, BRANCO)
    dica = fonte.render("R = jogar novamente   ESC = sair", True, (180, 180, 180))
    tela.blit(msg, (LARGURA_TELA // 2 - msg.get_width() // 2, ALTURA_TELA // 2 - 80))
    tela.blit(sub, (LARGURA_TELA // 2 - sub.get_width() // 2, ALTURA_TELA // 2))
    tela.blit(dica, (LARGURA_TELA // 2 - dica.get_width() // 2, ALTURA_TELA // 2 + 60))
    pygame.display.flip()


def _desenhar_jogador(tela, jogador, imagem_nave):
    if imagem_nave:
        tela.blit(imagem_nave, jogador["rect"])
    else:
        r = jogador["rect"]
        pygame.draw.polygon(tela, BRANCO, [
            (r.centerx, r.top),
            (r.left, r.bottom),
            (r.right, r.bottom),
        ])


def _novo_jogo(imagem_nave):
    w, h = TAMANHO_NAVE if imagem_nave else (40, 40)
    rect = pygame.Rect(LARGURA_TELA // 2 - w // 2, ALTURA_TELA - h - 20, w, h)
    return {"rect": rect, "vidas": VIDAS_INICIAIS, "pontos": 0, "invencivel_ate": 0}


def executar_jogo():
    """Executa o loop principal do jogo."""
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 30)
    fonte_grande = pygame.font.SysFont(None, 72)

    imagem_nave, imagem_meteoro, imagem_fundo = _carregar_imagens()

    _tela_inicial(tela, fonte_grande, fonte)
    nome_jogador = _tela_login(tela, fonte_grande, fonte)
    recorde = obter_recorde_jogador(nome_jogador)

    jogando = True
    while jogando:
        jogador = _novo_jogo(imagem_nave)
        meteoros = []
        intervalo_meteoro = INTERVALO_METEORO_INICIAL
        ultimo_meteoro = pygame.time.get_ticks()
        ultimo_ponto = pygame.time.get_ticks()
        ultima_reducao = pygame.time.get_ticks()
        rodando = True

        while rodando:
            relogio.tick(FPS)
            agora = pygame.time.get_ticks()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT]:
                jogador["rect"].x -= VELOCIDADE_JOGADOR
            if teclas[pygame.K_RIGHT]:
                jogador["rect"].x += VELOCIDADE_JOGADOR
            if teclas[pygame.K_UP]:
                jogador["rect"].y -= VELOCIDADE_JOGADOR
            if teclas[pygame.K_DOWN]:
                jogador["rect"].y += VELOCIDADE_JOGADOR

            jogador["rect"].x = limitar_valor(jogador["rect"].x, 0, LARGURA_TELA - jogador["rect"].width)
            jogador["rect"].y = limitar_valor(jogador["rect"].y, 0, ALTURA_TELA - jogador["rect"].height)

            if agora - ultimo_meteoro >= intervalo_meteoro:
                meteoros.append(criar_meteoro())
                ultimo_meteoro = agora

            if agora - ultima_reducao >= 5000:
                intervalo_meteoro = max(INTERVALO_METEORO_MINIMO, intervalo_meteoro - REDUCAO_INTERVALO)
                ultima_reducao = agora

            meteoros = mover_meteoros(meteoros)

            if agora - ultimo_ponto >= 1000:
                jogador["pontos"] += 1
                ultimo_ponto = agora

            if agora > jogador["invencivel_ate"]:
                for m in meteoros:
                    if verificar_colisao(jogador["rect"], m["rect"]):
                        jogador["vidas"] = tomar_dano(jogador["vidas"], 1)
                        jogador["invencivel_ate"] = agora + 1000
                        break

            if jogador_perdeu(jogador["vidas"]):
                rodando = False

            if jogador["pontos"] > recorde:
                recorde = jogador["pontos"]
                atualizar_ranking(nome_jogador, recorde)

            if imagem_fundo:
                tela.blit(imagem_fundo, (0, 0))
            else:
                tela.fill(AZUL_ESCURO)

            desenhar_meteoros(tela, meteoros, imagem_meteoro)
            _desenhar_jogador(tela, jogador, imagem_nave)
            _desenhar_hud(tela, fonte, jogador["pontos"], jogador["vidas"], recorde)
            pygame.display.flip()

        _tela_game_over(tela, fonte_grande, fonte, jogador["pontos"], recorde)
        aguardando = True
        while aguardando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        aguardando = False
                    if evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

    pygame.quit()
