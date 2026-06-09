import math
import pygame
import random
from src.config import (
    LARGURA_TELA, ALTURA_TELA, FPS, TITULO_JOGO,
    AZUL_ESCURO, BRANCO, VERMELHO, AMARELO,
    VELOCIDADE_JOGADOR, VIDAS_INICIAIS,
    INTERVALO_METEORO_INICIAL, INTERVALO_METEORO_MINIMO, REDUCAO_INTERVALO,
    CAMINHO_NAVE, CAMINHO_METEORO, CAMINHO_FUNDO,
)
from src.funcoes import limitar_valor, verificar_colisao, tomar_dano, jogador_perdeu
from src.meteoro import criar_meteoro, mover_meteoros, desenhar_meteoros
from src.dados import obter_recorde_jogador, atualizar_ranking, top10, melhor_pontuacao_global

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
    tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 80))

    linhas = [
        "Desvie dos meteoros e sobreviva o maior tempo possivel!",
        "",
        "Setas direcionais  :  mover a nave",
        "Cada segundo sobrevivido vale 1 ponto",
        "Voce comeca com 3 vidas - cada colisao remove 1",
        "ESC  :  pausar o jogo",
    ]
    for i, linha in enumerate(linhas):
        txt = fonte.render(linha, True, BRANCO)
        tela.blit(txt, (LARGURA_TELA // 2 - txt.get_width() // 2, 220 + i * 35))

    dica = fonte.render("Pressione ENTER para começar   ESC para sair", True, (180, 180, 180))
    tela.blit(dica, (LARGURA_TELA // 2 - dica.get_width() // 2, ALTURA_TELA - 60))
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


def _tela_ranking(tela, fonte_grande, fonte):
    while True:
        tela.fill((0, 0, 0))
        titulo = fonte_grande.render("TOP 10", True, AMARELO)
        tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 40))

        lista = top10()
        if lista:
            for i, (nome, pontos) in enumerate(lista):
                cor = AMARELO if i == 0 else BRANCO
                linha = fonte.render(f"{i + 1}. {nome} — {pontos} pts", True, cor)
                tela.blit(linha, (LARGURA_TELA // 2 - linha.get_width() // 2, 140 + i * 35))
        else:
            vazio = fonte.render("Nenhuma pontuação registrada ainda.", True, (180, 180, 180))
            tela.blit(vazio, (LARGURA_TELA // 2 - vazio.get_width() // 2, ALTURA_TELA // 2))

        dica = fonte.render("ENTER ou ESC para voltar", True, (180, 180, 180))
        tela.blit(dica, (LARGURA_TELA // 2 - dica.get_width() // 2, ALTURA_TELA - 40))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    return


def _menu_pausa(tela, fonte_grande, fonte):
    opcoes = ["Voltar ao Jogo", "Ver Ranking", "Fechar Jogo"]
    selecionado = 0

    while True:
        tela.fill((0, 0, 0))
        titulo = fonte_grande.render("PAUSADO", True, AMARELO)
        tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, ALTURA_TELA // 2 - 140))

        for i, opcao in enumerate(opcoes):
            cor = BRANCO if i == selecionado else (100, 100, 100)
            txt = fonte.render(opcao, True, cor)
            tela.blit(txt, (LARGURA_TELA // 2 - txt.get_width() // 2, ALTURA_TELA // 2 - 30 + i * 50))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                elif evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                elif evento.key == pygame.K_RETURN:
                    if selecionado == 1:
                        _tela_ranking(tela, fonte_grande, fonte)
                    else:
                        return selecionado  # 0 = voltar, 2 = fechar
                elif evento.key == pygame.K_ESCAPE:
                    return 0  # ESC na pausa volta ao jogo


def _criar_explosao(particulas, pos):
    """Adiciona partículas de explosão na posição dada."""
    for _ in range(12):
        angulo = random.uniform(0, 2 * math.pi)
        velocidade = random.uniform(2, 6)
        particulas.append({
            "x": pos[0], "y": pos[1],
            "vel_x": velocidade * math.cos(angulo),
            "vel_y": velocidade * math.sin(angulo),
            "raio": random.randint(3, 6),
            "vida": random.randint(15, 25),
        })


def _atualizar_e_desenhar_particulas(tela, particulas):
    """Move, encolhe e desenha partículas; remove as que expiraram."""
    for p in particulas:
        p["x"] += p["vel_x"]
        p["y"] += p["vel_y"]
        p["raio"] -= 0.3
        p["vida"] -= 1
        if p["raio"] > 0:
            pygame.draw.circle(tela, (255, 140, 0), (int(p["x"]), int(p["y"])), int(p["raio"]))
    particulas[:] = [p for p in particulas if p["vida"] > 0]


def _desenhar_hud(tela, fonte, pontos, vidas, recorde, global_score, level):
    tela.blit(fonte.render(f"Pontos: {pontos}", True, BRANCO), (10, 10))
    tela.blit(fonte.render(f"Vidas: {vidas}", True, AMARELO), (10, 40))
    tela.blit(fonte.render(f"Level: {level}", True, BRANCO), (10, 70))
    txt_recorde = fonte.render(f"Recorde: {recorde}", True, AMARELO)
    txt_global = fonte.render(f"Global: {global_score}", True, (180, 180, 255))
    tela.blit(txt_recorde, (LARGURA_TELA - txt_recorde.get_width() - 10, 10))
    tela.blit(txt_global, (LARGURA_TELA - txt_global.get_width() - 10, 40))


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
        particulas = []
        intervalo_meteoro = INTERVALO_METEORO_INICIAL
        ultimo_meteoro = pygame.time.get_ticks()
        ultimo_ponto = pygame.time.get_ticks()
        ultima_reducao = pygame.time.get_ticks()
        level = 1
        nivel_msg_ate = 0
        rodando = True

        while rodando:
            relogio.tick(FPS)
            agora = pygame.time.get_ticks()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    resultado = _menu_pausa(tela, fonte_grande, fonte)
                    if resultado == 2:
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

            if agora - ultimo_meteoro >= intervalo_meteoro and agora >= nivel_msg_ate:
                meteoros.append(criar_meteoro(level))
                ultimo_meteoro = agora

            if agora - ultima_reducao >= 15000:
                intervalo_meteoro = max(INTERVALO_METEORO_MINIMO, intervalo_meteoro - REDUCAO_INTERVALO)
                ultima_reducao = agora
                level += 1
                nivel_msg_ate = agora + 2000

            if agora >= nivel_msg_ate:
                meteoros = mover_meteoros(meteoros)

            if agora - ultimo_ponto >= 1000:
                jogador["pontos"] += level
                ultimo_ponto = agora

            if agora > jogador["invencivel_ate"]:
                for m in meteoros:
                    if verificar_colisao(jogador["rect"], m["rect"]):
                        jogador["vidas"] = tomar_dano(jogador["vidas"], 1)
                        jogador["invencivel_ate"] = agora + 2000
                        meteoros.remove(m)
                        _criar_explosao(particulas, m["rect"].center)
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
            _atualizar_e_desenhar_particulas(tela, particulas)
            tempo_restante = jogador["invencivel_ate"] - agora
            if tempo_restante <= 0 or tempo_restante <= 1000 or (agora // 50) % 2 == 0:
                _desenhar_jogador(tela, jogador, imagem_nave)
            _desenhar_hud(tela, fonte, jogador["pontos"], jogador["vidas"], recorde, melhor_pontuacao_global(), level)
            if agora < nivel_msg_ate:
                msg = fonte_grande.render(f"Level {level}!", True, AMARELO)
                tela.blit(msg, (LARGURA_TELA // 2 - msg.get_width() // 2, ALTURA_TELA // 2 - 40))
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
