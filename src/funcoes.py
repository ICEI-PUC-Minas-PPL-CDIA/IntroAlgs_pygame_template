import pygame
import random

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


def verificar_vida_baixa(vidas):
    return vidas <= 35.0


def tela_reparo(tela, relogio, perguntas_disponiveis, print_jogo, LARGURA_TELA, ALTURA_TELA, FPS, FONTE, BRANCO):
    """Abre uma janela de quiz com uma pergunta aleatória por cima do jogo pausado."""
    if not perguntas_disponiveis:
        return False, None
    
    fonte_pergunta = pygame.font.SysFont("Arial", 18, bold=True)
    fonte_opcao = pygame.font.SysFont("Courier New", 16)
    fonte_aviso = pygame.font.SysFont("Arial", 22, bold=True)
    
    questao = random.choice(perguntas_disponiveis)
    
    largura_janela, altura_janela = 600, 440
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
        rect_opcao = pygame.Rect(x_janela + 40, y_janela + 160 + (i * 60), largura_janela - 80, 42)
        retangulos_opcoes.append(rect_opcao)

    respondendo = True
    acertou = False

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
                        pygame.draw.rect(tela, (25, 25, 40), rect_janela)
                        pygame.draw.rect(tela, BRANCO, rect_janela, 3)

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
            pygame.draw.rect(tela, (25, 25, 40), rect_janela)
            pygame.draw.rect(tela, BRANCO, rect_janela, 3)
            
            desenhar_texto_multi_linha(tela, questao["pergunta"], fonte_pergunta, BRANCO, x_janela + 30, y_janela + 30, largura_janela - 60)
            
            letras_prefixo = ["A) ", "B) ", "C) ", "D) "]
            for i, opcao in enumerate(questao["opcoes"]):
                rect_opcao = retangulos_opcoes[i]
                cor_caixa = (60, 60, 90) if rect_opcao.collidepoint(pos_mouse) else (40, 40, 60)
                
                pygame.draw.rect(tela, cor_caixa, rect_opcao)
                pygame.draw.rect(tela, BRANCO, rect_opcao, 1)
                
                texto_formatado = f"{letras_prefixo[i]}{opcao}"
                texto_opcao = fonte_opcao.render(texto_formatado, True, BRANCO)
                tela.blit(texto_opcao, (rect_opcao.x + 15, rect_opcao.y + 10))
                
            pygame.display.flip()
        
    return acertou, questao
