import pygame
from src.config import (
    LARGURA_TELA, ALTURA_TELA, FPS, TITULO_JOGO,
    AZUL_ESCURO, BRANCO, VERMELHO, AMARELO,
    VELOCIDADE_JOGADOR, VIDAS_INICIAIS,
    INTERVALO_METEORO_INICIAL, INTERVALO_METEORO_MINIMO, REDUCAO_INTERVALO,
<<<<<<< Updated upstream
    CAMINHO_NAVE, CAMINHO_METEORO, CAMINHO_FUNDO, DIFICULDADES,
)
from src.funcoes import limitar_valor, verificar_colisao, tomar_dano, jogador_perdeu
from src.meteoro import criar_meteoro, mover_meteoros, desenhar_meteoros
from src.dados import obter_recorde_jogador, atualizar_ranking, top10, melhor_pontuacao_global
=======
    CAMINHO_NAVE, CAMINHO_NAVE2, CAMINHO_METEOROS, CAMINHO_FUNDO,
    CAMINHO_SOM_COLISAO, CAMINHO_SOM_LEVEL_UP, CAMINHO_SOM_GAME_OVER, CAMINHO_MUSICA,
    CAMINHO_POWERUP_TIRO_ATIVO,
    DIFICULDADES,
    VELOCIDADE_JOGADOR_2, DISTANCIA_REVIVE, TEMPO_REVIVE, TEMPO_CORPO,
)
from src.funcoes import limitar_valor, verificar_colisao, tomar_dano, jogador_perdeu
from src.meteoro import criar_meteoro, mover_meteoros, desenhar_meteoros
from src.dados import obter_recorde_jogador, atualizar_ranking, top10, melhor_pontuacao_global, atualizar_ranking_coop, top10_coop
from src.power_ups import criar_powerup, aplicar_powerup, desenhar_powerup, atualizar_powerup, desenhar_tiro
>>>>>>> Stashed changes

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


def _tela_dificuldade(tela, fonte_grande, fonte):
    opcoes = list(DIFICULDADES.keys())
    selecionado = 1  # Medio por padrao

    while True:
        tela.fill((0, 0, 0))
        titulo = fonte_grande.render("Dificuldade", True, AMARELO)
        tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, 160))

        for i, nome in enumerate(opcoes):
            cor = AMARELO if i == selecionado else BRANCO
            txt = fonte.render(nome, True, cor)
            tela.blit(txt, (LARGURA_TELA // 2 - txt.get_width() // 2, 280 + i * 50))

        dica = fonte.render("Setas para escolher   ENTER para confirmar", True, (180, 180, 180))
        tela.blit(dica, (LARGURA_TELA // 2 - dica.get_width() // 2, ALTURA_TELA - 60))
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
                    return opcoes[selecionado]
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()


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


<<<<<<< Updated upstream
def _desenhar_hud(tela, fonte, pontos, vidas, recorde, global_score, level, dificuldade):
=======
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


def _desenhar_hud(tela, fonte, pontos, vidas, escudo, recorde, global_score, level, dificuldade):
>>>>>>> Stashed changes
    tela.blit(fonte.render(f"Pontos: {pontos}", True, BRANCO), (10, 10))
    tela.blit(fonte.render(f"Vidas: {vidas}", True, AMARELO), (10, 40))
    tela.blit(fonte.render(f"Escudo: {escudo}", True, (180, 220, 255)), (10, 70))
    tela.blit(fonte.render(f"Level: {level}", True, BRANCO), (10, 100))
    tela.blit(fonte.render(f"Dif: {dificuldade}", True, (180, 180, 255)), (10, 130))
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
<<<<<<< Updated upstream
    rect = pygame.Rect(LARGURA_TELA // 2 - w // 2, ALTURA_TELA - h - 20, w, h)
    return {"rect": rect, "vidas": VIDAS_INICIAIS, "pontos": 0, "invencivel_ate": 0}


=======
    if lado == "esquerda":
        x = LARGURA_TELA // 4 - w // 2
    elif lado == "direita":
        x = 3 * LARGURA_TELA // 4 - w // 2
    else:
        x = LARGURA_TELA // 2 - w // 2
    rect = pygame.Rect(x, ALTURA_TELA - h - 20, w, h)
    return {"rect": rect, "vidas": VIDAS_INICIAIS, "pontos": 0, "invencivel_ate": 0, "escudo": 0}


def _desenhar_hud_vs(tela, fonte, j1, nome1, j2, nome2, level, dificuldade):
    """HUD lado a lado para modo competição."""
    tela.blit(fonte.render(f"{nome1}", True, (100, 200, 255)), (10, 10))
    tela.blit(fonte.render(f"Pts: {j1['pontos']}", True, BRANCO), (10, 35))
    tela.blit(fonte.render(f"Vidas: {j1['vidas']}", True, AMARELO), (10, 60))
    tela.blit(fonte.render(f"Escudo: {j1.get('escudo', 0)}", True, (180, 220, 255)), (10, 85))

    txt2 = fonte.render(f"{nome2}", True, (255, 100, 100))
    tela.blit(txt2, (LARGURA_TELA - txt2.get_width() - 10, 10))
    txt2p = fonte.render(f"Pts: {j2['pontos']}", True, BRANCO)
    tela.blit(txt2p, (LARGURA_TELA - txt2p.get_width() - 10, 35))
    txt2v = fonte.render(f"Vidas: {j2['vidas']}", True, AMARELO)
    tela.blit(txt2v, (LARGURA_TELA - txt2v.get_width() - 10, 60))
    txt2s = fonte.render(f"Escudo: {j2.get('escudo', 0)}", True, (180, 220, 255))
    tela.blit(txt2s, (LARGURA_TELA - txt2s.get_width() - 10, 85))

    tela.blit(fonte.render(f"Level: {level}  Dif: {dificuldade}", True, (180, 180, 255)),
              (LARGURA_TELA // 2 - 70, 10))


def _tela_resultado_vs(tela, fonte_grande, fonte, nome1, pts1, nome2, pts2):
    tela.fill((0, 0, 0))
    if pts1 > pts2:
        vencedor = f"{nome1} venceu!"
    elif pts2 > pts1:
        vencedor = f"{nome2} venceu!"
    else:
        vencedor = "Empate!"
    tela.blit(fonte_grande.render(vencedor, True, AMARELO),
              (LARGURA_TELA // 2 - fonte_grande.size(vencedor)[0] // 2, ALTURA_TELA // 2 - 100))
    tela.blit(fonte.render(f"{nome1}: {pts1} pts", True, (100, 200, 255)),
              (LARGURA_TELA // 2 - 100, ALTURA_TELA // 2))
    tela.blit(fonte.render(f"{nome2}: {pts2} pts", True, (255, 100, 100)),
              (LARGURA_TELA // 2 - 100, ALTURA_TELA // 2 + 35))
    dica = fonte.render("R = jogar novamente   ESC = sair", True, (180, 180, 180))
    tela.blit(dica, (LARGURA_TELA // 2 - dica.get_width() // 2, ALTURA_TELA // 2 + 100))
    pygame.display.flip()


def _processar_colisoes(jogador, meteoros, particulas, sons, agora):
    """Verifica colisões para um jogador, retorna lista de meteoros atualizada."""
    if agora > jogador["invencivel_ate"]:
        for m in meteoros:
            if verificar_colisao(jogador["rect"], m["rect"]):
                # se tiver escudo, consome o escudo e remove o meteoro sem dano
                if jogador.get("escudo", 0) > 0:
                    # consume one shield instead of losing a life
                    jogador["escudo"] = max(0, jogador.get("escudo", 0) - 1)
                    try:
                        meteoros.remove(m)
                    except ValueError:
                        pass
                    _criar_explosao(particulas, m["rect"].center)
                    _tocar(sons, "colisao")
                    break
                # senao toma dano normalmente
                jogador["vidas"] = tomar_dano(jogador["vidas"], 1)
                jogador["invencivel_ate"] = agora + 2000
                try:
                    meteoros.remove(m)
                except ValueError:
                    pass
                _criar_explosao(particulas, m["rect"].center)
                _tocar(sons, "colisao")
                break
    return meteoros


def _loop_competicao(tela, relogio, fonte, fonte_grande, imagem_nave, imagem_nave2, imagens_meteoro,
                     imagem_fundo, sons, nome1, nome2, dificuldade,
                     vel_min, vel_max, interv_inicial, interv_min, reducao, pts_por_segundo):
    jogador1 = _novo_jogo(imagem_nave, "esquerda")
    jogador2 = _novo_jogo(imagem_nave2, "direita")

    powerups = []
    tiro_ativos = []
    ultimo_powerup = pygame.time.get_ticks()
    intervalo_powerup = random.randint(10000, 20000)
    
    meteoros, particulas = [], []
    intervalo_meteoro = interv_inicial
    ultimo_meteoro = ultimo_ponto = ultima_reducao = pygame.time.get_ticks()
    level, nivel_msg_ate = 1, 0
    _iniciar_musica(sons)

    while True:
        relogio.tick(FPS)
        agora = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                if sons.get("musica_ok"):
                    pygame.mixer.music.pause()
                resultado = _menu_pausa(tela, fonte_grande, fonte)
                if sons.get("musica_ok"):
                    if resultado == 2:
                        _parar_musica()
                    else:
                        pygame.mixer.music.unpause()
                if resultado == 2:
                    pygame.quit()
                    exit()

        teclas = pygame.key.get_pressed()
        # Jogador 1 — WASD
        if not jogador_perdeu(jogador1["vidas"]):
            vel1 = VELOCIDADE_JOGADOR * jogador1.get("velocidade_multiplier", 1.0)
            if teclas[pygame.K_a]:
                jogador1["rect"].x -= vel1
            if teclas[pygame.K_d]:
                jogador1["rect"].x += vel1
            if teclas[pygame.K_w]:
                jogador1["rect"].y -= vel1
            if teclas[pygame.K_s]:
                jogador1["rect"].y += vel1
            jogador1["rect"].x = limitar_valor(jogador1["rect"].x, 0, LARGURA_TELA - jogador1["rect"].width)
            jogador1["rect"].y = limitar_valor(jogador1["rect"].y, 0, ALTURA_TELA - jogador1["rect"].height)

        # Jogador 2 — setas
        if not jogador_perdeu(jogador2["vidas"]):
            vel2 = VELOCIDADE_JOGADOR_2 * jogador2.get("velocidade_multiplier", 1.0)
            if teclas[pygame.K_LEFT]:
                jogador2["rect"].x -= vel2
            if teclas[pygame.K_RIGHT]:
                jogador2["rect"].x += vel2
            if teclas[pygame.K_UP]:
                jogador2["rect"].y -= vel2
            if teclas[pygame.K_DOWN]:
                jogador2["rect"].y += vel2
            jogador2["rect"].x = limitar_valor(jogador2["rect"].x, 0, LARGURA_TELA - jogador2["rect"].width)
            jogador2["rect"].y = limitar_valor(jogador2["rect"].y, 0, ALTURA_TELA - jogador2["rect"].height)

        if agora - ultimo_meteoro >= intervalo_meteoro and agora >= nivel_msg_ate:
            meteoros.append(criar_meteoro(level, vel_min, vel_max))
            ultimo_meteoro = agora

        if agora - ultima_reducao >= 15000:
            intervalo_meteoro = max(interv_min, intervalo_meteoro - reducao)
            ultima_reducao = agora
            level += 1
            nivel_msg_ate = agora + 2000
            _tocar(sons, "level_up")

        if agora >= nivel_msg_ate:
            meteoros = mover_meteoros(meteoros)

        # --- Atualizar / coletar power-ups (antes das colisões) ---
        for p in powerups[:]:
            p["rect"].y += p.get("vel_y", 2)
            if p["rect"].top > ALTURA_TELA:
                powerups.remove(p)
                continue
            if not jogador_perdeu(jogador1["vidas"]) and atualizar_powerup(jogador1, p):
                powerups.remove(p)
                if p["tipo"] == "tiro" and meteoros:
                    alvo = min(meteoros, key=lambda m: _distancia(jogador1["rect"], m["rect"]))
                    try:
                        meteoros.remove(alvo)
                    except ValueError:
                        pass
                    _criar_explosao(particulas, alvo["rect"].center)
                    _tocar(sons, "colisao")
                _tocar(sons, "level_up")
                continue
            if not jogador_perdeu(jogador2["vidas"]) and atualizar_powerup(jogador2, p):
                powerups.remove(p)
                if p["tipo"] == "tiro" and meteoros:
                    alvo = min(meteoros, key=lambda m: _distancia(jogador2["rect"], m["rect"]))
                    try:
                        meteoros.remove(alvo)
                    except ValueError:
                        pass
                    _criar_explosao(particulas, alvo["rect"].center)
                    _tocar(sons, "colisao")
                _tocar(sons, "level_up")
                continue

        # --- Atualizar / coletar power-ups (antes das colisões para que escudo proteja imediatamente) ---
        for p in powerups[:]:
            p["rect"].y += p.get("vel_y", 2)
            if p["rect"].top > ALTURA_TELA:
                powerups.remove(p)
                continue
            # checar coleta para jogador1
            if not jogador_perdeu(jogador1["vidas"]) and atualizar_powerup(jogador1, p):
                powerups.remove(p)
                if p["tipo"] == "tiro" and meteoros:
                    alvo = min(meteoros, key=lambda m: _distancia(jogador1["rect"], m["rect"]))
                    try:
                        meteoros.remove(alvo)
                    except ValueError:
                        pass
                    _criar_explosao(particulas, alvo["rect"].center)
                    _tocar(sons, "colisao")
                _tocar(sons, "level_up")
                continue
            # checar coleta para jogador2
            if not jogador_perdeu(jogador2["vidas"]) and atualizar_powerup(jogador2, p):
                powerups.remove(p)
                if p["tipo"] == "tiro" and meteoros:
                    alvo = min(meteoros, key=lambda m: _distancia(jogador2["rect"], m["rect"]))
                    try:
                        meteoros.remove(alvo)
                    except ValueError:
                        pass
                    _criar_explosao(particulas, alvo["rect"].center)
                    _tocar(sons, "colisao")
                _tocar(sons, "level_up")
                continue

        # --- Gerar power-ups ---
        if agora - ultimo_powerup >= intervalo_powerup and agora >= nivel_msg_ate:
            powerups.append(criar_powerup(TAMANHO_METEORO_BASE))
            ultimo_powerup = agora
            intervalo_powerup = random.randint(10000, 20000)

        if agora - ultimo_ponto >= 1000:
            if not jogador_perdeu(jogador1["vidas"]):
                jogador1["pontos"] += pts_por_segundo * level
            if not jogador_perdeu(jogador2["vidas"]):
                jogador2["pontos"] += pts_por_segundo * level
            ultimo_ponto = agora

        if not jogador_perdeu(jogador1["vidas"]):
            meteoros = _processar_colisoes(jogador1, meteoros, particulas, sons, agora)
        if not jogador_perdeu(jogador2["vidas"]):
            meteoros = _processar_colisoes(jogador2, meteoros, particulas, sons, agora)

        # (power-up update handled earlier; drawing happens after background)

        # --- Expirar efeitos ---
        for j in (jogador1, jogador2):
            if j.get("velocidade_ate", 0) <= agora:
                j["velocidade_multiplier"] = 1.0
            if j.get("tiro_ate", 0) <= agora:
                j["pode_atirar"] = False

        if jogador_perdeu(jogador1["vidas"]) and jogador_perdeu(jogador2["vidas"]):
            break

        if imagem_fundo:
            tela.blit(imagem_fundo, (0, 0))
        else:
            tela.fill(AZUL_ESCURO)

        desenhar_meteoros(tela, meteoros, imagens_meteoro)
        _atualizar_e_desenhar_particulas(tela, particulas)
        for p in powerups:
            desenhar_powerup(tela, p)

        # atualizar / desenhar tiros ativos
        for ta in tiro_ativos[:]:
            ta["x"] += ta["vel_x"]
            ta["y"] += ta["vel_y"]
            rect = ta["image"].get_rect(center=(int(ta["x"]), int(ta["y"])))
            tela.blit(ta["image"], rect)
            alvo = ta.get("target")
            if alvo not in meteoros:
                tiro_ativos.remove(ta)
                continue
            if _distancia(rect, alvo["rect"]) < 20:
                # destruir meteoro
                try:
                    meteoros.remove(alvo)
                except ValueError:
                    pass
                _criar_explosao(particulas, alvo["rect"].center)
                _tocar(sons, "colisao")
                tiro_ativos.remove(ta)

        if not jogador_perdeu(jogador1["vidas"]):
            tr1 = jogador1["invencivel_ate"] - agora
            if tr1 <= 0 or tr1 <= 1000 or (agora // 50) % 2 == 0:
                _desenhar_jogador(tela, jogador1, imagem_nave)
        desenhar_tiro(tela, jogador1)
        if not jogador_perdeu(jogador2["vidas"]):
            tr2 = jogador2["invencivel_ate"] - agora
            if tr2 <= 0 or tr2 <= 1000 or (agora // 50) % 2 == 0:
                _desenhar_jogador(tela, jogador2, imagem_nave2)
        desenhar_tiro(tela, jogador2)

        _desenhar_hud_vs(tela, fonte, jogador1, nome1, jogador2, nome2, level, dificuldade)

        if agora < nivel_msg_ate:
            msg = fonte_grande.render(f"Level {level}!", True, AMARELO)
            tela.blit(msg, (LARGURA_TELA // 2 - msg.get_width() // 2, ALTURA_TELA // 2 - 40))
        pygame.display.flip()

    _parar_musica()
    _tocar(sons, "game_over")
    atualizar_ranking(nome1, jogador1["pontos"])
    atualizar_ranking(nome2, jogador2["pontos"])
    _tela_resultado_vs(tela, fonte_grande, fonte, nome1, jogador1["pontos"], nome2, jogador2["pontos"])
    return jogador1["pontos"], jogador2["pontos"]


def _distancia(r1, r2):
    dx = r1.centerx - r2.centerx
    dy = r1.centery - r2.centery
    return math.sqrt(dx * dx + dy * dy)


def _desenhar_hud_coop(tela, fonte, pontos, vidas1, nome1, vidas2, nome2, escudo1=0, escudo2=0, level=None, dificuldade=None):
    tela.blit(fonte.render(f"{nome1} Vidas: {vidas1}", True, (100, 200, 255)), (10, 10))
    tela.blit(fonte.render(f"Escudo: {escudo1}", True, (180, 220, 255)), (10, 35))
    tela.blit(fonte.render(f"{nome2} Vidas: {vidas2}", True, (255, 100, 100)),
              (LARGURA_TELA - fonte.size(f"{nome2} Vidas: {vidas2}")[0] - 10, 10))
    txt_esc2 = fonte.render(f"Escudo: {escudo2}", True, (180, 220, 255))
    tela.blit(txt_esc2, (LARGURA_TELA - txt_esc2.get_width() - 10, 35))
    tela.blit(fonte.render(f"Pts: {pontos}  Level: {level}  Dif: {dificuldade}", True, BRANCO),
              (LARGURA_TELA // 2 - 110, 10))


def _loop_cooperativo(tela, relogio, fonte, fonte_grande, imagem_nave, imagem_nave2, imagens_meteoro,
                      imagem_fundo, sons, nome1, nome2, dificuldade,
                      vel_min, vel_max, interv_inicial, interv_min, reducao, pts_por_segundo):
    jogador1 = _novo_jogo(imagem_nave, "esquerda")
    jogador2 = _novo_jogo(imagem_nave2, "direita")

    meteoros, particulas = [], []
    intervalo_meteoro = interv_inicial
    ultimo_meteoro = ultimo_ponto = ultima_reducao = pygame.time.get_ticks()
    level, nivel_msg_ate = 1, 0
    pontos_coop = 0

    # power-up state for coop
    powerups = []
    tiro_ativos = []
    ultimo_powerup = pygame.time.get_ticks()
    intervalo_powerup = random.randint(10000, 20000)

    # corpo = {"pos": (x,y), "morte_em": timestamp, "dono": jogador_dict, "progresso_revive": 0, "revivendo_desde": None}
    corpo1 = None  # corpo do jogador1 quando morto
    corpo2 = None  # corpo do jogador2 quando morto

    _iniciar_musica(sons)

    while True:
        relogio.tick(FPS)
        agora = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                if sons.get("musica_ok"):
                    pygame.mixer.music.pause()
                resultado = _menu_pausa(tela, fonte_grande, fonte)
                if sons.get("musica_ok"):
                    if resultado == 2:
                        _parar_musica()
                    else:
                        pygame.mixer.music.unpause()
                if resultado == 2:
                    pygame.quit()
                    exit()

        teclas = pygame.key.get_pressed()
        if not jogador_perdeu(jogador1["vidas"]):
            vel1 = VELOCIDADE_JOGADOR * jogador1.get("velocidade_multiplier", 1.0)
            if teclas[pygame.K_a]: jogador1["rect"].x -= vel1
            if teclas[pygame.K_d]: jogador1["rect"].x += vel1
            if teclas[pygame.K_w]: jogador1["rect"].y -= vel1
            if teclas[pygame.K_s]: jogador1["rect"].y += vel1
            jogador1["rect"].x = limitar_valor(jogador1["rect"].x, 0, LARGURA_TELA - jogador1["rect"].width)
            jogador1["rect"].y = limitar_valor(jogador1["rect"].y, 0, ALTURA_TELA - jogador1["rect"].height)

        if not jogador_perdeu(jogador2["vidas"]):
            vel2 = VELOCIDADE_JOGADOR_2 * jogador2.get("velocidade_multiplier", 1.0)
            if teclas[pygame.K_LEFT]:  jogador2["rect"].x -= vel2
            if teclas[pygame.K_RIGHT]: jogador2["rect"].x += vel2
            if teclas[pygame.K_UP]:    jogador2["rect"].y -= vel2
            if teclas[pygame.K_DOWN]:  jogador2["rect"].y += vel2
            jogador2["rect"].x = limitar_valor(jogador2["rect"].x, 0, LARGURA_TELA - jogador2["rect"].width)
            jogador2["rect"].y = limitar_valor(jogador2["rect"].y, 0, ALTURA_TELA - jogador2["rect"].height)

        # --- Gerar/mover meteoros ---
        if agora - ultimo_meteoro >= intervalo_meteoro and agora >= nivel_msg_ate:
            meteoros.append(criar_meteoro(level, vel_min, vel_max))
            ultimo_meteoro = agora
        if agora - ultima_reducao >= 15000:
            intervalo_meteoro = max(interv_min, intervalo_meteoro - reducao)
            ultima_reducao = agora
            level += 1
            nivel_msg_ate = agora + 2000
            _tocar(sons, "level_up")
        if agora >= nivel_msg_ate:
            meteoros = mover_meteoros(meteoros)

        # --- Pontuação conjunta ---
        if agora - ultimo_ponto >= 1000:
            vivos = (not jogador_perdeu(jogador1["vidas"])) + (not jogador_perdeu(jogador2["vidas"]))
            if vivos > 0:
                pontos_coop += pts_por_segundo * level
            ultimo_ponto = agora

        # --- Colisões ---
        if not jogador_perdeu(jogador1["vidas"]):
            meteoros = _processar_colisoes(jogador1, meteoros, particulas, sons, agora)
            if jogador_perdeu(jogador1["vidas"]):
                corpo1 = {"pos": jogador1["rect"].center, "morte_em": agora, "revivendo_desde": None}
        if not jogador_perdeu(jogador2["vidas"]):
            meteoros = _processar_colisoes(jogador2, meteoros, particulas, sons, agora)
            if jogador_perdeu(jogador2["vidas"]):
                corpo2 = {"pos": jogador2["rect"].center, "morte_em": agora, "revivendo_desde": None}

        # --- Expirar corpos ---
        if corpo1 and agora - corpo1["morte_em"] >= TEMPO_CORPO:
            corpo1 = None
        if corpo2 and agora - corpo2["morte_em"] >= TEMPO_CORPO:
            corpo2 = None

        # --- Lógica de revive ---
        # J1 vivo pode reviver J2
        if corpo2 and not jogador_perdeu(jogador1["vidas"]):
            pos_c2 = pygame.Rect(corpo2["pos"][0] - 20, corpo2["pos"][1] - 20, 40, 40)
            if _distancia(jogador1["rect"], pos_c2) <= DISTANCIA_REVIVE:
                if corpo2["revivendo_desde"] is None:
                    corpo2["revivendo_desde"] = agora
                elif agora - corpo2["revivendo_desde"] >= TEMPO_REVIVE:
                    jogador2["vidas"] = 1
                    jogador2["rect"].center = corpo2["pos"]
                    jogador2["invencivel_ate"] = agora + 2000
                    corpo2 = None
            else:
                corpo2["revivendo_desde"] = None

        # J2 vivo pode reviver J1
        if corpo1 and not jogador_perdeu(jogador2["vidas"]):
            pos_c1 = pygame.Rect(corpo1["pos"][0] - 20, corpo1["pos"][1] - 20, 40, 40)
            if _distancia(jogador2["rect"], pos_c1) <= DISTANCIA_REVIVE:
                if corpo1["revivendo_desde"] is None:
                    corpo1["revivendo_desde"] = agora
                elif agora - corpo1["revivendo_desde"] >= TEMPO_REVIVE:
                    jogador1["vidas"] = 1
                    jogador1["rect"].center = corpo1["pos"]
                    jogador1["invencivel_ate"] = agora + 2000
                    corpo1 = None
            else:
                corpo1["revivendo_desde"] = None

        # --- Condição de fim ---
        ambos_mortos = jogador_perdeu(jogador1["vidas"]) and jogador_perdeu(jogador2["vidas"])
        sem_revive = corpo1 is None and corpo2 is None
        if ambos_mortos and sem_revive:
            break

        # --- Desenho ---
        if imagem_fundo:
            tela.blit(imagem_fundo, (0, 0))
        else:
            tela.fill(AZUL_ESCURO)
        desenhar_meteoros(tela, meteoros, imagens_meteoro)
        _atualizar_e_desenhar_particulas(tela, particulas)
        for p in powerups:
            desenhar_powerup(tela, p)

        # --- Atualizar / desenhar power-ups ---
        for p in powerups[:]:
            p["rect"].y += p.get("vel_y", 2)
            if p["rect"].top > ALTURA_TELA:
                powerups.remove(p)
                continue
            if not jogador_perdeu(jogador1["vidas"]) and atualizar_powerup(jogador1, p):
                powerups.remove(p)
                if p["tipo"] == "tiro" and meteoros:
                    alvo = min(meteoros, key=lambda m: _distancia(jogador1["rect"], m["rect"]))
                    try:
                        meteoros.remove(alvo)
                    except ValueError:
                        pass
                    _criar_explosao(particulas, alvo["rect"].center)
                    _tocar(sons, "colisao")
                _tocar(sons, "level_up")
                continue
            if not jogador_perdeu(jogador2["vidas"]) and atualizar_powerup(jogador2, p):
                powerups.remove(p)
                if p["tipo"] == "tiro" and meteoros:
                    alvo = min(meteoros, key=lambda m: _distancia(jogador2["rect"], m["rect"]))
                    try:
                        meteoros.remove(alvo)
                    except ValueError:
                        pass
                    _criar_explosao(particulas, alvo["rect"].center)
                    _tocar(sons, "colisao")
                _tocar(sons, "level_up")
                continue

        # atualizar/draw tiros ativos
        for ta in tiro_ativos[:]:
            ta["x"] += ta["vel_x"]
            ta["y"] += ta["vel_y"]
            rect = ta["image"].get_rect(center=(int(ta["x"]), int(ta["y"])))
            tela.blit(ta["image"], rect)
            alvo = ta.get("target")
            if alvo not in meteoros:
                tiro_ativos.remove(ta)
                continue
            if _distancia(rect, alvo["rect"]) < 20:
                try:
                    meteoros.remove(alvo)
                except ValueError:
                    pass
                _criar_explosao(particulas, alvo["rect"].center)
                _tocar(sons, "colisao")
                tiro_ativos.remove(ta)

        # (power-ups already updated/drawn above)

        # --- Expirar efeitos ---
        for j in (jogador1, jogador2):
            if j.get("velocidade_ate", 0) <= agora:
                j["velocidade_multiplier"] = 1.0
            if j.get("tiro_ate", 0) <= agora:
                j["pode_atirar"] = False

        # Desenha corpos
        for corpo, cor_corpo in ((corpo1, (100, 200, 255)), (corpo2, (255, 100, 100))):
            if corpo:
                cx, cy = corpo["pos"]
                tempo_restante_corpo = TEMPO_CORPO - (agora - corpo["morte_em"])
                pygame.draw.circle(tela, cor_corpo, (cx, cy), 18, 2)
                # barra de tempo restante do corpo
                proporcao = tempo_restante_corpo / TEMPO_CORPO
                pygame.draw.rect(tela, (80, 80, 80), (cx - 20, cy - 28, 40, 5))
                pygame.draw.rect(tela, cor_corpo, (cx - 20, cy - 28, int(40 * proporcao), 5))
                # barra de progresso do revive
                rev = corpo["revivendo_desde"]
                if rev is not None:
                    prog = min(1.0, (agora - rev) / TEMPO_REVIVE)
                    pygame.draw.rect(tela, (80, 80, 80), (cx - 20, cy - 38, 40, 5))
                    pygame.draw.rect(tela, (0, 255, 100), (cx - 20, cy - 38, int(40 * prog), 5))
                    txt_rev = fonte.render("Revivendo...", True, (0, 255, 100))
                    tela.blit(txt_rev, (cx - txt_rev.get_width() // 2, cy - 55))

        if not jogador_perdeu(jogador1["vidas"]):
            tr1 = jogador1["invencivel_ate"] - agora
            if tr1 <= 0 or tr1 <= 1000 or (agora // 50) % 2 == 0:
                _desenhar_jogador(tela, jogador1, imagem_nave)
        desenhar_tiro(tela, jogador1)
        if not jogador_perdeu(jogador2["vidas"]):
            tr2 = jogador2["invencivel_ate"] - agora
            if tr2 <= 0 or tr2 <= 1000 or (agora // 50) % 2 == 0:
                _desenhar_jogador(tela, jogador2, imagem_nave2)
        desenhar_tiro(tela, jogador2)

        _desenhar_hud_coop(tela, fonte, pontos_coop, jogador1["vidas"], nome1, jogador2["vidas"], nome2, jogador1.get("escudo", 0), jogador2.get("escudo", 0), level, dificuldade)

        if agora < nivel_msg_ate:
            msg = fonte_grande.render(f"Level {level}!", True, AMARELO)
            tela.blit(msg, (LARGURA_TELA // 2 - msg.get_width() // 2, ALTURA_TELA // 2 - 40))
        pygame.display.flip()

    _parar_musica()
    _tocar(sons, "game_over")
    nome_dupla = f"{nome1} & {nome2}"
    atualizar_ranking_coop(nome_dupla, pontos_coop)

    tela.fill((0, 0, 0))
    tela.blit(fonte_grande.render("GAME OVER", True, VERMELHO),
              (LARGURA_TELA // 2 - fonte_grande.size("GAME OVER")[0] // 2, ALTURA_TELA // 2 - 100))
    tela.blit(fonte.render(f"Pontuacao da dupla: {pontos_coop}", True, BRANCO),
              (LARGURA_TELA // 2 - 130, ALTURA_TELA // 2))
    dica = fonte.render("R = jogar novamente   ESC = sair", True, (180, 180, 180))
    tela.blit(dica, (LARGURA_TELA // 2 - dica.get_width() // 2, ALTURA_TELA // 2 + 60))
    pygame.display.flip()
    return pontos_coop


>>>>>>> Stashed changes
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
    dificuldade = _tela_dificuldade(tela, fonte_grande, fonte)
    vel_min, vel_max, interv_inicial, interv_min, reducao, pts_por_segundo = DIFICULDADES[dificuldade]
    recorde = obter_recorde_jogador(nome_jogador)

    jogando = True
    while jogando:
        jogador = _novo_jogo(imagem_nave)
        meteoros = []
        intervalo_meteoro = interv_inicial
        ultimo_meteoro = pygame.time.get_ticks()
        ultimo_ponto = pygame.time.get_ticks()
        ultima_reducao = pygame.time.get_ticks()
        level = 1
        nivel_msg_ate = 0
        rodando = True
<<<<<<< Updated upstream
=======
        _iniciar_musica(sons)
        powerups = []
        tiro_ativos = []
        ultimo_powerup = pygame.time.get_ticks()
        intervalo_powerup = random.randint(10000, 20000)
>>>>>>> Stashed changes

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
            vel = VELOCIDADE_JOGADOR * jogador.get("velocidade_multiplier", 1.0)
            if teclas[pygame.K_LEFT]:
                jogador["rect"].x -= vel
            if teclas[pygame.K_RIGHT]:
                jogador["rect"].x += vel
            if teclas[pygame.K_UP]:
                jogador["rect"].y -= vel
            if teclas[pygame.K_DOWN]:
                jogador["rect"].y += vel

            jogador["rect"].x = limitar_valor(jogador["rect"].x, 0, LARGURA_TELA - jogador["rect"].width)
            jogador["rect"].y = limitar_valor(jogador["rect"].y, 0, ALTURA_TELA - jogador["rect"].height)

            if agora - ultimo_meteoro >= intervalo_meteoro and agora >= nivel_msg_ate:
                meteoros.append(criar_meteoro(level, vel_min, vel_max))
                ultimo_meteoro = agora

            if agora - ultima_reducao >= 15000:
                intervalo_meteoro = max(interv_min, intervalo_meteoro - reducao)
                ultima_reducao = agora
                level += 1
                nivel_msg_ate = agora + 2000

            if agora >= nivel_msg_ate:
                meteoros = mover_meteoros(meteoros)
            # --- Gerar power-ups ---
            if agora - ultimo_powerup >= intervalo_powerup and agora >= nivel_msg_ate:
                powerups.append(criar_powerup(TAMANHO_METEORO_BASE))
                ultimo_powerup = agora
                intervalo_powerup = random.randint(10000, 20000)

            # --- Atualizar power-ups (aplicar antes das colisões) ---
            for p in powerups[:]:
                p["rect"].y += p.get("vel_y", 2)
                if p["rect"].top > ALTURA_TELA:
                    powerups.remove(p)
                    continue
                if atualizar_powerup(jogador, p):
                    powerups.remove(p)
                    if p["tipo"] == "tiro" and meteoros:
                        alvo = min(meteoros, key=lambda m: _distancia(jogador["rect"], m["rect"]))
                        try:
                            meteoros.remove(alvo)
                        except ValueError:
                            pass
                        _criar_explosao(particulas, alvo["rect"].center)
                        _tocar(sons, "colisao")
                    _tocar(sons, "level_up")

            if agora - ultimo_ponto >= 1000:
                jogador["pontos"] += pts_por_segundo * level
                ultimo_ponto = agora

            if agora > jogador["invencivel_ate"]:
                for m in meteoros:
                    if verificar_colisao(jogador["rect"], m["rect"]):
                        # if player has a shield, consume it instead of losing a life
                        if jogador.get("escudo", 0) > 0:
                            jogador["escudo"] = max(0, jogador.get("escudo", 0) - 1)
                            try:
                                meteoros.remove(m)
                            except ValueError:
                                pass
                            _criar_explosao(particulas, m["rect"].center)
                            _tocar(sons, "colisao")
                            break
                        # otherwise take damage normally
                        jogador["vidas"] = tomar_dano(jogador["vidas"], 1)
<<<<<<< Updated upstream
                        jogador["invencivel_ate"] = agora + 1000
=======
                        jogador["invencivel_ate"] = agora + 2000
                        try:
                            meteoros.remove(m)
                        except ValueError:
                            pass
                        _criar_explosao(particulas, m["rect"].center)
                        _tocar(sons, "colisao")
>>>>>>> Stashed changes
                        break

            # --- Atualizar power-ups ---
            # (already handled earlier before collision)

            # --- Expirar efeitos ---
            if jogador.get("velocidade_ate", 0) <= agora:
                jogador["velocidade_multiplier"] = 1.0
            if jogador.get("tiro_ate", 0) <= agora:
                jogador["pode_atirar"] = False

            # atualizar/draw tiros ativos
            for ta in tiro_ativos[:]:
                ta["x"] += ta["vel_x"]
                ta["y"] += ta["vel_y"]
                rect = ta["image"].get_rect(center=(int(ta["x"]), int(ta["y"])))
                tela.blit(ta["image"], rect)
                alvo = ta.get("target")
                if alvo not in meteoros:
                    tiro_ativos.remove(ta)
                    continue
                if _distancia(rect, alvo["rect"]) < 20:
                    try:
                        meteoros.remove(alvo)
                    except ValueError:
                        pass
                    _criar_explosao(particulas, alvo["rect"].center)
                    _tocar(sons, "colisao")
                    tiro_ativos.remove(ta)

            if jogador_perdeu(jogador["vidas"]):
                rodando = False

            if jogador["pontos"] > recorde:
                recorde = jogador["pontos"]
                atualizar_ranking(nome_jogador, recorde)

            if imagem_fundo:
                tela.blit(imagem_fundo, (0, 0))
            else:
                tela.fill(AZUL_ESCURO)

<<<<<<< Updated upstream
            desenhar_meteoros(tela, meteoros, imagem_meteoro)
            _desenhar_jogador(tela, jogador, imagem_nave)
            _desenhar_hud(tela, fonte, jogador["pontos"], jogador["vidas"], recorde, melhor_pontuacao_global(), level, dificuldade)
=======
            desenhar_meteoros(tela, meteoros, imagens_meteoro)
            _atualizar_e_desenhar_particulas(tela, particulas)
            for p in powerups:
                desenhar_powerup(tela, p)
            tempo_restante = jogador["invencivel_ate"] - agora
            if tempo_restante <= 0 or tempo_restante <= 1000 or (agora // 50) % 2 == 0:
                _desenhar_jogador(tela, jogador, imagem_nave)
            desenhar_tiro(tela, jogador)
            _desenhar_hud(tela, fonte, jogador["pontos"], jogador["vidas"], jogador.get("escudo", 0), recorde, melhor_pontuacao_global(), level, dificuldade)
>>>>>>> Stashed changes
            if agora < nivel_msg_ate:
                msg = fonte_grande.render(f"Level {level}!", True, AMARELO)
                tela.blit(msg, (LARGURA_TELA // 2 - msg.get_width() // 2, ALTURA_TELA // 2 - 40))
            pygame.display.flip()

        _tela_game_over(tela, fonte_grande, fonte, jogador["pontos"], recorde)
        dificuldade = _tela_dificuldade(tela, fonte_grande, fonte)
        vel_min, vel_max, interv_inicial, interv_min, reducao, pts_por_segundo = DIFICULDADES[dificuldade]
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
