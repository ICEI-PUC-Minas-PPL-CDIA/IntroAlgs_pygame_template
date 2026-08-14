import pygame
import random

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CAMINHO_RECORDE,
    FONTE,
    RED_ANTARES,
    BRANCO,
    PRETO,
    CAMINHO_SPRITES,
    CONFIG_FASES
)

from src.funcoes import (
    jogador_perdeu,
    limitar_valor,
    verificar_colisao,
    tomar_dano,
    verificar_vida_baixa,
    calcular_pontos,
    tela_reparo,
    iniciar_entrada,
    iniciar_legenda,
    desenhar_legenda_digitada,
    sons_jogo,
)

from src.sprites import pegar_sprite, Obstacle, Enemies, Bullet, DeathStar
from src.dados import (
    salvar_recorde,
    carregar_recorde,
)

from src.conteudo import (
    FALAS_INICIO_FASE,
    FALAS_DANO,
    FALAS_DANO_CRITICO,
    FALAS_DEATH_STAR,
    perguntas
)

def tela_fim_partida(tela, fundo, relogio, subtitulo_texto, subtitulo_cor):
    """Tela de fim de partida (game over / vitoria).

    Todo o conteudo sobe gradualmente a partir da base da tela ate a posicao
    final, e so depois os botoes ficam clicaveis. Retorna True para reiniciar,
    False para sair.
    """
    # Fontes e textos fixos sao criados uma vez, fora do loop.
    fonte_titulo = pygame.font.Font(FONTE, 100)
    fonte_subtitulo = pygame.font.Font(FONTE, 50)
    fonte_botao = pygame.font.Font(FONTE, 30)

    # Tudo e posicionado a partir do centro da tela, para se adaptar a qualquer resolucao em vez de ficar preso no topo.
    centro_x = LARGURA_TELA // 2
    centro_y = ALTURA_TELA // 2

    titulo = fonte_titulo.render("Antares", True, RED_ANTARES)
    subtitulo = fonte_subtitulo.render(subtitulo_texto, True, subtitulo_cor)
    rotulo_jogar = fonte_botao.render("Jogar", True, BRANCO)
    rotulo_sair = fonte_botao.render("Sair", True, BRANCO)

    # Posicoes finais (centros) de cada elemento, relativas ao centro da tela.
    centro_titulo = (centro_x, centro_y - 180)
    centro_subtitulo = (centro_x, centro_y - 100)
    centro_botao_jogar = (centro_x, centro_y + 30)
    centro_botao_sair = (centro_x, centro_y + 120)
    deslocamento_y = ALTURA_TELA
    velocidade_subida = 30

    while True:
        relogio.tick(FPS)

        animando = deslocamento_y > 0
        if animando:
            deslocamento_y = max(0, deslocamento_y - velocidade_subida)

        pos_mouse = pygame.mouse.get_pos()

        # Areas dos botoes (servem para desenhar e para detectar o clique)
        botao_jogar = pygame.Rect(0, 0, 240, 60)
        botao_jogar.center = (centro_botao_jogar[0], centro_botao_jogar[1] + deslocamento_y)
        botao_sair = pygame.Rect(0, 0, 240, 60)
        botao_sair.center = (centro_botao_sair[0], centro_botao_sair[1] + deslocamento_y)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            # So aceita cliques depois que a animacao termina.
            if not animando and evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):
                    return True
                if botao_sair.collidepoint(evento.pos):
                    return False

        # Cor mais clara quando o mouse esta sobre o botao (efeito hover).
        cor_jogar = (90, 90, 90) if botao_jogar.collidepoint(pos_mouse) else (50, 50, 50)
        cor_sair = (90, 90, 90) if botao_sair.collidepoint(pos_mouse) else (50, 50, 50)

        tela.blit(fundo, (0, 0))
        tela.blit(titulo, titulo.get_rect(center=(centro_titulo[0], centro_titulo[1] + deslocamento_y)))
        tela.blit(subtitulo, subtitulo.get_rect(center=(centro_subtitulo[0], centro_subtitulo[1] + deslocamento_y)))

        pygame.draw.rect(tela, cor_jogar, botao_jogar)
        pygame.draw.rect(tela, cor_sair, botao_sair)

        # Centraliza o rotulo dentro do retangulo de cada botao.
        tela.blit(rotulo_jogar, rotulo_jogar.get_rect(center=botao_jogar.center))
        tela.blit(rotulo_sair, rotulo_sair.get_rect(center=botao_sair.center))

        pygame.display.flip()


def tela_fim_jogo(tela, fundo, relogio):
    """Tela de game over. Retorna True para reiniciar, False para sair."""
    return tela_fim_partida(tela, fundo, relogio, "Game over", RED_ANTARES)


def tela_vitoria(tela, fundo, relogio):
    """Tela de vitoria. Retorna True para reiniciar, False para sair."""
    return tela_fim_partida(tela, fundo, relogio, "You won", RED_ANTARES)




def desenhar_barra_vida(superficie, x, y, vidas_atuais, vidas_maximas=3, comprimento_barra = 150, cor_vida = (0, 255, 0), cor_fundo = (255, 0, 0), cor_outline = (255, 255, 255)):
    altura_barra = 15
    proporcao = max(0, vidas_atuais) / vidas_maximas
    largura_vida = int(comprimento_barra * proporcao)
    
    rect_fundo = pygame.Rect(x, y, comprimento_barra, altura_barra)
    rect_vida = pygame.Rect(x, y, largura_vida, altura_barra)
    
    pygame.draw.rect(superficie, cor_fundo, rect_fundo)
    pygame.draw.rect(superficie, cor_vida, rect_vida)
    pygame.draw.rect(superficie, cor_outline, rect_fundo, 2)

def tela_loading(tela, fase_atual, relogio):
    """Tela de loading/reparo entre as fases."""
    fonte = pygame.font.Font(FONTE, 50)
    texto = fonte.render(f"FASE {fase_atual} CONCLUIDA! Iniciando Sistemas...", True, BRANCO)
    rect_texto = texto.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
    
    tela.fill(PRETO)
    tela.blit(texto, rect_texto)
    pygame.display.flip()
    
    pygame.time.wait(2000)

def tela_fase_cinema(tela, fase_atual):
    fonte_grande = pygame.font.Font(FONTE, 80)
    
    tela.fill(PRETO)
    
    txt_fase = fonte_grande.render(f"FASE {fase_atual}", True, RED_ANTARES)
    rect_fase = txt_fase.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
    
    tela.blit(txt_fase, rect_fase)
    pygame.display.flip()
    
    pygame.time.wait(1500)

def executar_jogo():
    """Executa o loop principal do jogo e controla estado, colisões e pontuação."""
    pygame.init()

    tela = pygame.display.set_mode(
        (LARGURA_TELA, ALTURA_TELA),
        pygame.FULLSCREEN
    )
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()

    # --- Recursos que vivem o programa inteiro (carregados uma unica vez) ---

    # Jogador: usando tamanho 110x110 para capturar o quadrado perfeitamente
    player_image = pegar_sprite("assets/imagens/millenium_falcon_fr.bmp", x=0, y=0, width=118, height=32, scale=1)

    # Ferramenta de Reparo
    ferramenta_image = pygame.image.load("assets/imagens/item-de-reparo.png").convert_alpha()
    ferramenta_image = pygame.transform.scale(ferramenta_image, (90, 90))
    fonte_legenda = pygame.font.SysFont("Georgia", 22, italic=True)

    # 2. Criando a estrutura de Sprites usando Dicionários
    jogador = {
        "imagem": player_image,
        "rect": player_image.get_rect()
    }

    FREQUENCIA_ASTEROIDE = 40

    velocidade = 10
    fundo_x = 0
    velocidade_fundo = 5

    recorde = carregar_recorde(CAMINHO_RECORDE)

    imagem_original = pygame.image.load("assets/imagens/starsky.jpg").convert()
    imagem_original = pygame.transform.scale(imagem_original, (LARGURA_TELA, ALTURA_TELA))

    # Loop externo: cada volta e uma nova partida.
    jogando = True
    fase_atual = 1
    while jogando:
        # --- Reset: variaveis que vivem apenas uma partida nascem do zero ---
        lista_obstaculos = []
        lista_enemies = []
        lista_lasers_enemies = []
        lista_lasers_jogador = []

        cooldown_tiro_jogador = 0
        contador_tempo = 0
        pontos = 0
        vidas = 100.0
        vidas_death_star = 200
        death_star = None
        venceu = False
        destino_x = 20
        velocidade_entrada = 3
        entrando = iniciar_entrada(jogador, ALTURA_TELA)
        if fase_atual == 4:
            sons_jogo["fase_deathstar"].play(-1)
        ferramenta_coletada_na_fase = False
        ferramenta_na_tela = False
        ferramenta_rect = pygame.Rect(0, 0, 0, 0)
        ferramenta_velocidade = 5
        chances_perdidas = 0
        ticks_pra_spawnar_ds = 5000
        estado_legenda = {"ativa": False}
        dano_falado_na_fase = False
        critico_falado_na_partida = False
        laser_ds_tocando = False

        regras_fase = CONFIG_FASES[fase_atual]
        enemies_restantes_para_nascer = regras_fase["total_enemies"]
        total_enemies_da_fase = regras_fase["total_enemies"]
        
        intervalo_spawn = regras_fase["intervalo_spawn"] * 1000
        velocidade_enemy = regras_fase["vel_enemy"]

        enemies_mortos = 0

        ultimo_spawn_enemy = pygame.time.get_ticks()
        inicio_fase = pygame.time.get_ticks()
        perguntas_da_partida = list(perguntas)

        # Loop interno (partida): processa entrada, atualiza estado e renderiza.
        rodando = True
        while rodando:
            relogio.tick(FPS)

            vidas_antes_do_frame = vidas

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    jogando = False
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    rodando = False


            fundo_x -= velocidade_fundo
            if fundo_x <= -LARGURA_TELA:
                fundo_x = 0

            if entrando:
                # Fase de entrada: desliza para a direita, sem teclado nem clamp
                jogador["rect"].x += velocidade_entrada
                if jogador["rect"].x >= destino_x:
                    jogador["rect"].x = destino_x
                    entrando = False
            else:
                teclas = pygame.key.get_pressed()

                # Movimentação alterando direto os eixos X e Y do retângulo do jogador
                if teclas[pygame.K_LEFT]:
                    jogador["rect"].x -= velocidade
                if teclas[pygame.K_RIGHT]:
                    jogador["rect"].x += velocidade
                if teclas[pygame.K_UP]:
                    jogador["rect"].y -= velocidade
                if teclas[pygame.K_DOWN]:
                    jogador["rect"].y += velocidade

                # Limitando o jogador dentro das bordas da tela usando as propriedades do Rect
                jogador["rect"].x = limitar_valor(jogador["rect"].x, 0, LARGURA_TELA - jogador["rect"].width)
                jogador["rect"].y = limitar_valor(jogador["rect"].y, 0, ALTURA_TELA - jogador["rect"].height)
            
            teclas = pygame.key.get_pressed()

            if cooldown_tiro_jogador > 0:
                cooldown_tiro_jogador -= 1

            if teclas[pygame.K_SPACE] and cooldown_tiro_jogador == 0:
               
                novo_tiro = Bullet(jogador["rect"].right, jogador["rect"].centery)
                lista_lasers_jogador.append(novo_tiro)
                cooldown_tiro_jogador = 10

            tempo_atual = pygame.time.get_ticks()

            if enemies_restantes_para_nascer > 0:
                if tempo_atual - ultimo_spawn_enemy >= intervalo_spawn:
                    
                    lista_enemies.append(Enemies(LARGURA_TELA, ALTURA_TELA, velocidade_enemy + velocidade_fundo))
                    enemies_restantes_para_nascer -= 1
                    ultimo_spawn_enemy = tempo_atual 

            for enemy in lista_enemies[:]:
                enemy.atualizar(lista_lasers_enemies)

                if verificar_colisao(jogador["rect"], enemy.hitbox):
                    sons_jogo["colisao_nave"].play()
                    vidas = tomar_dano(vidas, 15.0) 
                    lista_enemies.remove(enemy)
                    enemies_restantes_para_nascer += 1 
                    continue

                if enemy.rect.x < -enemy.rect.width:
                    lista_enemies.remove(enemy)
                    enemies_restantes_para_nascer += 1

            for laser_en in lista_lasers_enemies[:]:
                laser_en.atualizar()

                if verificar_colisao(jogador["rect"], laser_en.rect):
                    vidas = tomar_dano(vidas, 5.0) # Cada tiro tira 5% de vida
                    lista_lasers_enemies.remove(laser_en)
                    continue
                
                if laser_en.rect.x < -laser_en.rect.width:
                    lista_lasers_enemies.remove(laser_en)

            for tiro in lista_lasers_jogador[:]:
                tiro.atualizar()
            
                if tiro.rect.x > LARGURA_TELA:
                    lista_lasers_jogador.remove(tiro)
                    continue
            
                for enemy in lista_enemies[:]:
                    if verificar_colisao(tiro.rect, enemy.hitbox):
                        pontos = calcular_pontos(pontos, 100)
                        enemies_mortos += 1 
                        lista_enemies.remove(enemy)
                        if tiro in lista_lasers_jogador:
                            lista_lasers_jogador.remove(tiro)
                        break
            
                if tiro in lista_lasers_jogador and death_star is not None and verificar_colisao(death_star.hitbox, tiro.rect):
                    vidas_death_star = tomar_dano(vidas_death_star, tiro.dano)
                    lista_lasers_jogador.remove(tiro)


            if enemies_mortos >= total_enemies_da_fase:
                if fase_atual == 4:
                    sons_jogo["fase_deathstar"].stop()
                tela_loading(tela, fase_atual, relogio)
                fase_atual += 1 
            
                if fase_atual > 4:
                    rodando = False
                    fase_atual = 1 
                else:
                    tela_fase_cinema(tela, fase_atual)

                    iniciar_legenda(estado_legenda, FALAS_INICIO_FASE[fase_atual], sons_jogo["antares"])

                    regras_fase = CONFIG_FASES[fase_atual]
                    enemies_restantes_para_nascer = regras_fase["total_enemies"]
                    total_enemies_da_fase = regras_fase["total_enemies"]
                    intervalo_spawn = regras_fase["intervalo_spawn"] * 1000
                    velocidade_enemy = regras_fase["vel_enemy"]
                    if fase_atual == 4:
                        sons_jogo["fase_deathstar"].play(-1)

                regras_fase = CONFIG_FASES[fase_atual]
                enemies_restantes_para_nascer = regras_fase["total_enemies"]
                total_enemies_da_fase = regras_fase["total_enemies"]
                intervalo_spawn = regras_fase["intervalo_spawn"] * 1000
                velocidade_enemy = regras_fase["vel_enemy"]

                lista_enemies.clear()
                lista_lasers_enemies.clear()
                lista_obstaculos.clear()

                enemies_mortos = 0
                ultimo_spawn_enemy = pygame.time.get_ticks()
                ferramenta_coletada_na_fase = False
                dano_falado_na_fase = False


                # Refaz a animação de entrada a cada nova fase
                entrando = iniciar_entrada(jogador, ALTURA_TELA)
                lista_lasers_jogador = []
                inicio_fase = pygame.time.get_ticks()


            contador_tempo += 1
            if contador_tempo >= FREQUENCIA_ASTEROIDE:
                lista_obstaculos.append(Obstacle(LARGURA_TELA, ALTURA_TELA))
                contador_tempo = 0

            if fase_atual == 4 and tempo_atual - inicio_fase >= ticks_pra_spawnar_ds and death_star is None:
                death_star = DeathStar(LARGURA_TELA, ALTURA_TELA)
        
                iniciar_legenda(estado_legenda, random.choice(FALAS_DEATH_STAR), sons_jogo["antares"])
                

            if death_star is not None:
                death_star.atualizar()
                if death_star.laser_rect is not None and not laser_ds_tocando:
                    sons_jogo["laser_deathstar"].play()
                    laser_ds_tocando = True
                elif death_star.laser_rect is None:
                    laser_ds_tocando = False

                # Feixe do superlaser: encostou no jogador, morreu.
                if death_star.laser_rect is not None and verificar_colisao(jogador["rect"], death_star.laser_rect):
                    vidas = 0

                # Estrela da morte destruida: o jogador venceu.
                if vidas_death_star <= 0:
                    sons_jogo["fase_deathstar"].stop()
                    venceu = True
                    rodando = False

            if verificar_vida_baixa(vidas) and not critico_falado_na_partida:
                critico_falado_na_partida = True
                iniciar_legenda(estado_legenda, FALAS_DANO_CRITICO[fase_atual], sons_jogo["antares"])

            if verificar_vida_baixa(vidas) and not ferramenta_na_tela and not ferramenta_coletada_na_fase:
                if random.random() < 0.005:
                    ferramenta_rect = ferramenta_image.get_rect()
                    ferramenta_rect.x = LARGURA_TELA 
                    ferramenta_rect.y = random.randint(0, ALTURA_TELA - ferramenta_rect.height)
                    ferramenta_na_tela = True

            if ferramenta_na_tela:
                ferramenta_rect.x -= ferramenta_velocidade
                
                # Se o jogador pegar a ferramenta de reparo
                if verificar_colisao(jogador["rect"], ferramenta_rect):
                    ferramenta_coletada_na_fase = True
                    ferramenta_na_tela = False
                    
                    # 1. Desenha tudo na tela rapidamente para capturar a imagem de fundo
                    tela.blit(imagem_original, (0, 0))
                    tela.blit(jogador["imagem"], jogador["rect"])
                    for obs in lista_obstaculos:
                        obs.desenhar(tela)
                    desenhar_barra_vida(tela, 20, 20, vidas, vidas_maximas=100)
                    
                    # Tira um print da tela do jogo para congelar no fundo do quiz
                    print_jogo = tela.copy()
                    
                    # 2. Abre a janela do quiz passando todas as configurações necessárias
                    acertou, questao_respondida = tela_reparo(
                        tela, relogio, perguntas_da_partida, print_jogo,
                        LARGURA_TELA, ALTURA_TELA, FPS, FONTE, BRANCO
                    )
                    
                    # 3. Aplica as regras do resultado do quiz
                    if acertou:
                        sons_jogo["tela_reparo"].play()
                        vidas = limitar_valor(vidas + 20.0, 0, 100.0) # Ganha 20% de vida
                        if questao_respondida in perguntas_da_partida:
                            perguntas_da_partida.remove(questao_respondida) # Remove para não repetir
                    else:
                        # Se errou, não ganha vida e a pergunta continua na lista (pode repetir)
                        pass
                
                # Se a ferramenta passar direto sem ser coletada, causa dano de 3%
                elif ferramenta_rect.x < -ferramenta_rect.width:
                    ferramenta_na_tela = False
                    chances_perdidas += 1
                    if chances_perdidas >= 3:
                        vidas = tomar_dano(vidas, 3.0)
                        chances_perdidas = 0

            for obstaculo in lista_obstaculos[:]:
                obstaculo.atualizar()

                if verificar_colisao(jogador["rect"], obstaculo.rect):
                    sons_jogo["colisao_nave"].play()
                    vidas = tomar_dano(vidas, obstaculo.dano)
                    lista_obstaculos.remove(obstaculo)

                elif obstaculo.rect.y > ALTURA_TELA:
                    lista_obstaculos.remove(obstaculo)
                    pontos += 1

            if vidas < vidas_antes_do_frame and not dano_falado_na_fase:
                dano_falado_na_fase = True
                iniciar_legenda(estado_legenda, FALAS_DANO[fase_atual], sons_jogo["antares"])

            if jogador_perdeu(vidas):
                if fase_atual == 4:
                    sons_jogo["fase_deathstar"].stop()
                rodando = False

            if pontos > recorde:
                recorde = pontos
                salvar_recorde(CAMINHO_RECORDE, recorde)

            tela.blit(imagem_original, (fundo_x, 0))
            tela.blit(imagem_original, (fundo_x + LARGURA_TELA, 0))

            for laser_en in lista_lasers_enemies:
                laser_en.desenhar(tela)

            for enemy in lista_enemies:
                enemy.desenhar(tela)

            for tiro in lista_lasers_jogador:
                tiro.desenhar(tela)

            tela.blit(jogador["imagem"], jogador["rect"])

            if ferramenta_na_tela:
                tela.blit(ferramenta_image, ferramenta_rect)
                          
            for obstaculo in lista_obstaculos:
                obstaculo.desenhar(tela)

            if death_star is not None and vidas_death_star > 0:
                death_star.desenhar(tela)
                death_star.desenhar_laser(tela)
                desenhar_barra_vida(tela, 10, ALTURA_TELA - 35, vidas_death_star, 200, LARGURA_TELA - 20, (255, 0, 0), (0, 0, 0), (118, 50, 1))

            desenhar_barra_vida(tela, 20, 20, vidas, vidas_maximas=100)

            fonte_hud = pygame.font.Font(FONTE, 24)

            texto_fase = fonte_hud.render(f"FASE {fase_atual}", True, BRANCO)
            rect_fase = texto_fase.get_rect()
           
            rect_fase.topright = (LARGURA_TELA - 20, 20)
            tela.blit(texto_fase, rect_fase)
            
            texto_alvo = fonte_hud.render(f"ALVOS: {enemies_mortos}/{total_enemies_da_fase}", True, BRANCO)
            rect_alvo = texto_alvo.get_rect()
            
            rect_alvo.topright = (LARGURA_TELA - 20, rect_fase.bottom + 5)
            tela.blit(texto_alvo, rect_alvo)

            desenhar_legenda_digitada(tela, estado_legenda, fonte_legenda, LARGURA_TELA, ALTURA_TELA, fase_atual)

            pygame.display.flip()

        # A partida acabou. Se o jogador nao fechou a janela, mostra a tela de fim.
        if jogando:
            if venceu:
                sons_jogo["conclusao_jogo"].play()
                jogando = tela_vitoria(tela, imagem_original, relogio)
                # Apos vencer, "Jogar" recomeca a campanha pela fase 1.
                if jogando:
                    fase_atual = 1
            else:
                jogando = tela_fim_jogo(tela, imagem_original, relogio)

    pygame.quit()

if __name__ == "__main__":
    executar_jogo()