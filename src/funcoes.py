import pygame
import random
import math
from pygame import mixer


class _SomMudo:
    """Evita que a inicialização do aúdio em SO sem driver de aúdio disponível crashe a aplicação"""

    def play(self, *args, **kwargs):
        return None

    def stop(self, *args, **kwargs):
        return None

    def set_volume(self, *args, **kwargs):
        return None


_ARQUIVOS_SONS = {
    "antares": "assets/sons/sound_antares.mp3",
    "coleta_gema": "assets/sons/coleta_gema.mp3",
    "colisao_nave": "assets/sons/colisao_asteroide-nave.mp3",
    "conclusao_jogo": "assets/sons/conclusao_jogo.mp3",
    "fase_deathstar": "assets/sons/fase_deathstar.mp3",
    "laser_deathstar": "assets/sons/laser_deathstar.mp3",
    "tela_reparo": "assets/sons/tela_reparo.mp3",
}


def carregar_sons():
    """Carrega os sons gerais do jogo"""
    try:
        mixer.init()
    except pygame.error:
        return {nome: _SomMudo() for nome in _ARQUIVOS_SONS}

    sons = {nome: pygame.mixer.Sound(caminho) for nome, caminho in _ARQUIVOS_SONS.items()}
    for som in sons.values():
        som.set_volume(0.15)
    return sons


sons_jogo = carregar_sons()

def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual."""
    return pontos_atual + pontos_ganhos


def tomar_dano(vida_atual, dano):
    """Reduz a vida atual com base no dano recebido."""
    return vida_atual - dano


def jogador_perdeu(vidas):
    """Indica se o jogador ficou sem vidas."""
    return vidas <= 0


def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def verificar_colisao(retangulo_1, retangulo_2):
    """Verifica sobreposição entre dois retângulos do Pygame."""
    return retangulo_1.colliderect(retangulo_2)


def iniciar_entrada(jogador, ALTURA_TELA):
    """Posiciona a nave fora da tela (à esquerda, centralizada no Y) para a
    animação de entrada e retorna True para o estado 'entrando'."""
    jogador["rect"].y = (ALTURA_TELA - jogador["rect"].height) / 2
    jogador["rect"].x = -jogador["rect"].width - 5
    return True


def verificar_vida_baixa(vidas):
    return vidas <= 35.0


def tela_reparo(tela, relogio, perguntas_disponiveis, print_jogo, LARGURA_TELA, ALTURA_TELA, FPS, FONTE, BRANCO):
    """Abre uma janela de quiz com uma pergunta aleatória por cima do jogo pausado."""
    if not perguntas_disponiveis:
        return False, None
    
    fonte_pergunta = pygame.font.SysFont("Arial", 22, bold=True)
    fonte_opcao = pygame.font.SysFont("Courier New", 18)
    fonte_aviso = pygame.font.SysFont("Arial", 26, bold=True)
    
    questao = random.choice(perguntas_disponiveis)
    
    largura_janela, altura_janela = 920, 600
    x_janela = (LARGURA_TELA - largura_janela) // 2
    y_janela = (ALTURA_TELA - altura_janela) // 2
    rect_janela = pygame.Rect(x_janela, y_janela, largura_janela, altura_janela)
    
    def desenhar_texto_multi_linha(superficie, texto, fonte, cor, x, y, largura_maxima):
        palavras = texto.split(' ')
        linhas = []
        linha_atual = ""
        
        for palavra in palavras:
            testar_linha = linha_atual + palavra + " "
            if fonte.size(testar_linha)[0] < largura_maxima:
                linha_atual = testar_linha
            else:
                linhas.append(linha_atual)
                linha_atual = palavra + " "
        linhas.append(linha_atual)
        
        offset_y = 0
        for linha in linhas: 
            render_linha = fonte.render(linha.strip(), True, cor)
            superficie.blit(render_linha, (x, y + offset_y))
            offset_y += fonte.get_linesize()
        return offset_y

    retangulos_opcoes = []
    for i in range(len(questao["opcoes"])):
        rect_opcao = pygame.Rect(x_janela + 60, y_janela + 220 + (i * 75), largura_janela - 120, 55)
        retangulos_opcoes.append(rect_opcao)

    respondendo = True
    acertou = False

    imagem_fundo_reparo = pygame.image.load("assets/imagens/imagem-tela-de-reparo.png").convert_alpha()
    imagem_fundo_reparo = pygame.transform.scale(imagem_fundo_reparo, (largura_janela, altura_janela))

    def desenhar_botao_pixel_art(superficie, rect, cor_fundo, cor_borda_escura, cor_borda_clara, espessura=4):
        # Corpo principal do botão
        pygame.draw.rect(superficie, cor_fundo, rect)
        pygame.draw.line(superficie, cor_borda_escura, (rect.left, rect.bottom - 1), (rect.right, rect.bottom - 1), espessura)
        pygame.draw.line(superficie, cor_borda_escura, (rect.right - 1, rect.top), (rect.right - 1, rect.bottom), espessura)
        pygame.draw.line(superficie, cor_borda_clara, (rect.left, rect.top), (rect.right, rect.top), espessura)
        pygame.draw.line(superficie, cor_borda_clara, (rect.left, rect.top), (rect.left, rect.bottom), espessura)

    COR_FUNDO_BTN = (20, 20, 35)
    COR_BORDA_ESCURA = (5, 5, 15)
    COR_BORDA_CLARA = (0, 180, 255)
    COR_HOVER_CLARA = (0, 255, 200)

    largura_caixa_pergunta, altura_caixa_pergunta = largura_janela - 120, 130
    rect_pergunta = pygame.Rect(x_janela + 60, y_janela + 40, largura_caixa_pergunta, altura_caixa_pergunta)

    while respondendo:
        relogio.tick(FPS)
        pos_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for idx_clique, rect_opcao in enumerate(retangulos_opcoes):
                    if rect_opcao.collidepoint(evento.pos):
                        
                        # Preparação prévia do fundo do Pop-up para o aviso
                        tela.blit(print_jogo, (0, 0))
                        tela.blit(imagem_fundo_reparo, rect_janela.topleft)

                        if idx_clique == questao["correta"]:
                            acertou = True
                            texto_aviso = fonte_aviso.render("CORRETO! +20% DE SINAL RECUPERADO", True, (0, 255, 0))
                        else:
                            texto_aviso = fonte_aviso.render("SISTEMA FALHOU! REPARO INDISPONÍVEL", True, (255, 0, 0))
                        
                        # Desenha o aviso centralizado
                        rect_aviso = texto_aviso.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
                        tela.blit(texto_aviso, rect_aviso)
                        
                        # Força o display a atualizar antes do wait travar a execução
                        pygame.display.update()
                        
                        # Tela estática por 1.5 segundos após responder
                        pygame.time.wait(1500)
                        respondendo = False
        
        # Desenho padrão do loop enquanto o usuário escolhe a resposta
        if respondendo:
            tela.blit(print_jogo, (0, 0))
            tela.blit(imagem_fundo_reparo, rect_janela.topleft)
            
            desenhar_botao_pixel_art(tela, rect_pergunta, COR_FUNDO_BTN, COR_BORDA_ESCURA, COR_BORDA_CLARA)
            desenhar_texto_multi_linha(tela, questao["pergunta"], fonte_pergunta, BRANCO, rect_pergunta.x + 25, rect_pergunta.y + 25, largura_caixa_pergunta - 50)
            
            letras_prefixo = ["A) ", "B) ", "C) ", "D) "]
            for i, opcao in enumerate(questao["opcoes"]):
                rect_opcao = retangulos_opcoes[i]
                
                if rect_opcao.collidepoint(pos_mouse):
                    desenhar_botao_pixel_art(tela, rect_opcao, (30, 30, 55), COR_BORDA_ESCURA, COR_HOVER_CLARA)
                else:
                    desenhar_botao_pixel_art(tela, rect_opcao, COR_FUNDO_BTN, COR_BORDA_ESCURA, COR_BORDA_CLARA)
                
                texto_formatado = f"{letras_prefixo[i]}{opcao}"
                texto_opcao = fonte_opcao.render(texto_formatado, True, BRANCO)
                
                y_centro_texto = rect_opcao.y + (rect_opcao.height - texto_opcao.get_height()) // 2
                tela.blit(texto_opcao, (rect_opcao.x + 25, y_centro_texto))
                
            pygame.display.flip()
        
    return acertou, questao

def _gerar_matriz_estrela(tamanho_grade=14):
    """Gera a grade de pixels de uma estrela de 8 pontas estilizada.
    Códigos por célula: 0 = vazio, 1 = contorno, 2 = núcleo,
    3 = brilho interno, 4 = ponto de destaque (reflexo)."""
    centro = (tamanho_grade - 1) / 2
    raio_nucleo = tamanho_grade * 0.28
    raio_ponta = tamanho_grade * 0.5

    matriz = [[0] * tamanho_grade for _ in range(tamanho_grade)]

    for gy in range(tamanho_grade):
        for gx in range(tamanho_grade):
            dx = gx - centro
            dy = gy - centro
            distancia = math.hypot(dx, dy)
            angulo = math.atan2(dy, dx)

            # As 8 pontas "esticam" o alcance nos ângulos múltiplos de 45 graus
            fator_ponta = abs(math.cos(angulo * 4)) ** 3
            alcance = raio_nucleo + (raio_ponta - raio_nucleo) * fator_ponta

            if distancia <= alcance:
                if distancia <= raio_nucleo * 0.45:
                    matriz[gy][gx] = 3
                elif distancia <= alcance - 1:
                    matriz[gy][gx] = 2
                else:
                    matriz[gy][gx] = 1

    # Pontinho de reflexo, sempre no quadrante superior-esquerdo do núcleo
    px = int(centro - raio_nucleo * 0.35)
    py = int(centro - raio_nucleo * 0.35)
    if 0 <= py < tamanho_grade and 0 <= px < tamanho_grade:
        matriz[py][px] = 4

    return matriz


_MATRIZ_AVATAR_ANTARES = _gerar_matriz_estrela()


def _obter_paleta_antares(fase_atual):
    """Paleta de cores da Antares por fase: começa vermelho/laranja escuro e
    vai ficando mais clara e mais amarelada conforme ela fica mais forte."""
    paletas = {
        1: {"contorno": (90, 20, 0),   "nucleo": (178, 38, 0),   "brilho": (220, 90, 20),  "destaque": (255, 190, 90)},
        2: {"contorno": (110, 25, 0),  "nucleo": (205, 65, 5),   "brilho": (240, 125, 30), "destaque": (255, 205, 100)},
        3: {"contorno": (130, 35, 0),  "nucleo": (230, 100, 15), "brilho": (255, 165, 50), "destaque": (255, 220, 120)},
        4: {"contorno": (150, 45, 0),  "nucleo": (255, 140, 25), "brilho": (255, 200, 80), "destaque": (255, 245, 180)},
    }
    return paletas.get(fase_atual, paletas[1])


def _misturar_cor(cor_a, cor_b, fator):
    """Interpola linearmente entre duas cores RGB (fator de 0 a 1)."""
    return tuple(int(cor_a[i] + (cor_b[i] - cor_a[i]) * fator) for i in range(3))


def desenhar_avatar_antares(tela, x, y, fase_atual, tamanho_pixel=5, tempo=None):
    """Desenha o avatar pixel art da Antares (estrela de 8 pontas) na posição
    (x, y) = canto superior esquerdo. Pulsa suavemente e, quanto mais avançada
    a fase, mais rápido pulsa e mais brilhante/amarelada fica a cor — dando a
    sensação de que ela está ficando mais forte."""
    paleta = _obter_paleta_antares(fase_atual)

    if tempo is None:
        tempo = pygame.time.get_ticks()

    velocidade_pulso = 260 - fase_atual * 25  # fases avançadas pulsam mais rápido
    pulso = (math.sin(tempo / velocidade_pulso) + 1) / 2  # 0..1

    largura_avatar = len(_MATRIZ_AVATAR_ANTARES[0]) * tamanho_pixel
    altura_avatar = len(_MATRIZ_AVATAR_ANTARES) * tamanho_pixel
    centro_avatar = (x + largura_avatar // 2, y + altura_avatar // 2)
    # Halo suave atrás da estrela: mais forte e mais amarelo nas fases avançadas
    raio_halo = int(largura_avatar * (0.55 + fase_atual * 0.05) * (0.9 + pulso * 0.15))
    alpha_halo = 40 + fase_atual * 25
    camada_halo = pygame.Surface((raio_halo * 2, raio_halo * 2), pygame.SRCALPHA)
    pygame.draw.circle(camada_halo, (*paleta["destaque"], alpha_halo), (raio_halo, raio_halo), raio_halo)
    tela.blit(camada_halo, (centro_avatar[0] - raio_halo, centro_avatar[1] - raio_halo))

    cor_nucleo = _misturar_cor(paleta["nucleo"], paleta["brilho"], pulso * 0.3)
    cores_por_valor = {1: paleta["contorno"], 2: cor_nucleo, 3: paleta["brilho"], 4: paleta["destaque"]}

    for gy, linha in enumerate(_MATRIZ_AVATAR_ANTARES):
        for gx, valor in enumerate(linha):
            if valor == 0:
                continue
            rect_pixel = pygame.Rect(x + gx * tamanho_pixel, y + gy * tamanho_pixel, tamanho_pixel, tamanho_pixel)
            pygame.draw.rect(tela, cores_por_valor[valor], rect_pixel)

def iniciar_legenda(estado_legenda, texto, som=None):
    """Define uma nova fala a ser exibida e reinicia o efeito de digitação.
    Se um som for passado, ele é tocado no instante em que a fala começa."""
    estado_legenda["texto"] = texto
    estado_legenda["caracteres_visiveis"] = 0
    estado_legenda["temporizador"] = 0
    estado_legenda["tempo_parada"] = 0
    estado_legenda["ativa"] = True

    if som is not None:
        som.play()

    return estado_legenda


def desenhar_legenda_digitada(tela, estado_legenda, fonte_legenda, largura_tela, altura_tela, fase_atual=1, velocidade=2, tempo_exibicao=240):
    """Desenha a fala atual da Antares com efeito de digitação, junto com seu avatar."""
    if not estado_legenda.get("ativa"):
        return

    texto = estado_legenda["texto"]

    if estado_legenda["caracteres_visiveis"] < len(texto):
        estado_legenda["temporizador"] += 1
        if estado_legenda["temporizador"] >= velocidade:
            estado_legenda["temporizador"] = 0
            estado_legenda["caracteres_visiveis"] += 1

    texto_visivel = texto[:estado_legenda["caracteres_visiveis"]]

    altura_caixa = 110
    margem_lateral = 60
    margem_inferior = 30
    rect_caixa = pygame.Rect(
        margem_lateral,
        altura_tela - altura_caixa - margem_inferior,
        largura_tela - (margem_lateral * 2),
        altura_caixa
    )

    superficie_caixa = pygame.Surface((rect_caixa.width, rect_caixa.height), pygame.SRCALPHA)
    superficie_caixa.fill((0, 0, 0, 190))
    tela.blit(superficie_caixa, rect_caixa.topleft)
    pygame.draw.rect(tela, (0, 180, 255), rect_caixa, 2)

    # Avatar de Antares, encostado na esquerda da caixa
    tamanho_pixel_avatar = 5
    margem_avatar = 15
    largura_avatar = len(_MATRIZ_AVATAR_ANTARES[0]) * tamanho_pixel_avatar
    altura_avatar = len(_MATRIZ_AVATAR_ANTARES) * tamanho_pixel_avatar
    x_avatar = rect_caixa.x + margem_avatar
    y_avatar = rect_caixa.y + (rect_caixa.height - altura_avatar) // 2
    desenhar_avatar_antares(tela, x_avatar, y_avatar, fase_atual, tamanho_pixel_avatar)

    deslocamento_x_texto = largura_avatar + margem_avatar * 2

    nome_render = fonte_legenda.render("ANTARES", True, (0, 200, 255))
    tela.blit(nome_render, (rect_caixa.x + deslocamento_x_texto, rect_caixa.y + 10))

    largura_maxima_texto = rect_caixa.width - deslocamento_x_texto - 20
    palavras = texto_visivel.split(' ')
    linhas = []
    linha_atual = ""
    for palavra in palavras:
        linha_teste = linha_atual + palavra + " "
        if fonte_legenda.size(linha_teste)[0] < largura_maxima_texto:
            linha_atual = linha_teste
        else:
            linhas.append(linha_atual)
            linha_atual = palavra + " "
    linhas.append(linha_atual)

    y_texto = rect_caixa.y + 45
    for linha in linhas:
        render_linha = fonte_legenda.render(linha.strip(), True, (255, 255, 255))
        tela.blit(render_linha, (rect_caixa.x + deslocamento_x_texto, y_texto))
        y_texto += fonte_legenda.get_linesize()

    if estado_legenda["caracteres_visiveis"] >= len(texto):
        estado_legenda["tempo_parada"] += 1
        if estado_legenda["tempo_parada"] > tempo_exibicao:
            estado_legenda["ativa"] = False