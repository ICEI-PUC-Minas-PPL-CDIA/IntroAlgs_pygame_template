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
    CAMINHO_SPRITES
)

from src.funcoes import (
    jogador_perdeu,
    limitar_valor,
    verificar_colisao,
    tomar_dano,
    verificar_vida_baixa,
    tela_reparo
)

from src.dados import (
    salvar_recorde,
    carregar_recorde,
)

from src.sprites import pegar_sprite, Obstacle, Bullet

# Banco de dados das perguntas

perguntas = [
    {
        "pergunta": "O que armazena uma Matriz de tamanho 3x3?",
        "opcoes": ["3 elementos", "6 elementos", "9 elementos", "0 elementos"],
        "correta": 2
    },
    {
        "pergunta": "O que acontece se tentarmos ler a posição 5 de um vetor de tamanho 3?",
        "opcoes": ["Ele aumenta de tamanho sozinho", "Dá erro de índice fora do limite", "O programa adivinha o valor", "Ele apaga o vetor"],
        "correta": 1
    },
    {
        "pergunta": "Qual comando usamos para repetir um bloco de código enquanto uma condição for verdadeira?",
        "opcoes": ["if", "while", "else", "print"],
        "correta": 1
    },
    {
        "pergunta": "Para que serve o comando 'if' no Python?",
        "opcoes": ["Para repetir o código", "Para criar uma lista", "Para fazer uma pergunta/teste condicional", "Para fechar o jogo"],
        "correta": 2
    },
    {
        "pergunta": "Se o comando 'if' não for atendido, qual comando opcional roda logo em seguida?",
        "opcoes": ["else", "while", "for", "import"],
        "correta": 0
    },
    {
        "pergunta": "Qual das opções abaixo é usada para criar uma lista vazia?",
        "opcoes": ["lista = 0", "lista = []", "lista = 'vazia'", "lista = True"],
        "correta": 1
    },
    {
        "pergunta": "O que acontece se você criar um loop 'while True' sem nenhum comando para pará-lo?",
        "opcoes": ["O computador desliga", "O loop roda apenas uma vez", "Gera um loop infinito e trava o programa", "O Python corrige sozinho"],
        "correta": 2
    },
    {
        "pergunta": "Qual estrutura é ideal para percorrer todos os elementos de uma lista um por um?",
        "opcoes": ["import", "if", "else", "for"],
        "correta": 3
    },
    {
        "pergunta": "O que o comando 'print()' faz no Python?",
        "opcoes": ["Exibe uma mensagem na tela/terminal", "Soma dois números", "Salva o jogo", "Deleta um arquivo"],
        "correta": 0
    },
    {
        "pergunta": "Qual o valor da variável 'x' após rodar: x = 5 + 3?",
        "opcoes": ["5", "3", "53", "8"],
        "correta": 3
    }

]

def tela_fim_jogo(tela, fundo, relogio):
    """Mostra a tela de fim de jogo. Retorna True para reiniciar, False para sair."""
    # Fontes e textos fixos sao criados uma vez, fora do loop.
    fonte_titulo = pygame.font.Font(FONTE, 100)
    fonte_subtitulo = pygame.font.Font(FONTE, 50)
    fonte_botao = pygame.font.Font(FONTE, 30)

    # Tudo e posicionado a partir do centro da tela, para se adaptar a qualquer
    # resolucao em vez de ficar preso no topo.
    centro_x = LARGURA_TELA // 2
    centro_y = ALTURA_TELA // 2

    titulo = fonte_titulo.render("Antares", True, RED_ANTARES)
    rect_titulo = titulo.get_rect(center=(centro_x, centro_y - 180))

    subtitulo = fonte_subtitulo.render("Game over", True, RED_ANTARES)
    rect_subtitulo = subtitulo.get_rect(center=(centro_x, centro_y - 100))

    rotulo_jogar = fonte_botao.render("Jogar", True, BRANCO)
    rotulo_sair = fonte_botao.render("Sair", True, BRANCO)

    # Areas dos botoes (servem para desenhar e para detectar o clique).
    botao_jogar = pygame.Rect(0, 0, 240, 60)
    botao_jogar.center = (centro_x, centro_y + 30)
    botao_sair = pygame.Rect(0, 0, 240, 60)
    botao_sair.center = (centro_x, centro_y + 120)

    while True:
        relogio.tick(FPS)

        pos_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):
                    return True
                if botao_sair.collidepoint(evento.pos):
                    return False

        # Cor mais clara quando o mouse esta sobre o botao (efeito hover).
        cor_jogar = (90, 90, 90) if botao_jogar.collidepoint(pos_mouse) else (50, 50, 50)
        cor_sair = (90, 90, 90) if botao_sair.collidepoint(pos_mouse) else (50, 50, 50)

        tela.blit(fundo, (0, 0))
        tela.blit(titulo, rect_titulo)
        tela.blit(subtitulo, rect_subtitulo)

        pygame.draw.rect(tela, cor_jogar, botao_jogar)
        pygame.draw.rect(tela, cor_sair, botao_sair)

        # Centraliza o rotulo dentro do retangulo de cada botao.
        tela.blit(rotulo_jogar, rotulo_jogar.get_rect(center=botao_jogar.center))
        tela.blit(rotulo_sair, rotulo_sair.get_rect(center=botao_sair.center))

        pygame.display.flip()


def desenhar_barra_vida(superficie, x, y, vidas_atuais, vidas_maximas=3):
    comprimento_barra = 150
    altura_barra = 15
    proporcao = max(0, vidas_atuais) / vidas_maximas
    largura_vida = int(comprimento_barra * proporcao)
    
    rect_fundo = pygame.Rect(x, y, comprimento_barra, altura_barra)
    rect_vida = pygame.Rect(x, y, largura_vida, altura_barra)
    
    pygame.draw.rect(superficie, (255, 0, 0), rect_fundo)
    pygame.draw.rect(superficie, (0, 255, 0), rect_vida)
    pygame.draw.rect(superficie, (255, 255, 255), rect_fundo, 2)


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
    ferramenta_image = pegar_sprite(CAMINHO_SPRITES, x=900, y=690, width=200, height=200, scale=0.15)

    # 2. Criando a estrutura de Sprites usando Dicionários
    jogador = {
        "imagem": player_image,
        "rect": player_image.get_rect(topleft=(100, 100))
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
    while jogando:
        # --- Reset: variaveis que vivem apenas uma partida nascem do zero ---
        lista_obstaculos = []
        contador_tempo = 0
        pontos = 0
        vidas = 100.0
        ferramenta_coletada_na_fase = False
        jogador["rect"].topleft = (100, 100)


        ferramenta_na_tela = False
        ferramenta_rect = pygame.Rect(0, 0, 0, 0)
        ferramenta_velocidade = 5
        chances_perdidas = 0
        lista_balas = []
        cooldown_tiro = 0
        perguntas_da_partida = list(perguntas)

        # Loop interno (partida): processa entrada, atualiza estado e renderiza.
        rodando = True
        while rodando:
            relogio.tick(FPS)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    jogando = False
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    rodando = False

            
            fundo_x -= velocidade_fundo
            if fundo_x <= -LARGURA_TELA:
                fundo_x = 0

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

            # Tiro
            cooldown_tiro = max(0, cooldown_tiro - 1)
            if teclas[pygame.K_SPACE] and cooldown_tiro == 0:
                lista_balas.append(Bullet(jogador["rect"].right, jogador["rect"].centery))
                cooldown_tiro = 10

            # Atualizar balas e colisão com asteroides
            for bala in lista_balas[:]:
                bala.atualizar()

                if bala.rect.x > LARGURA_TELA:
                    lista_balas.remove(bala)
                    continue

                for obstaculo in lista_obstaculos[:]:
                    if verificar_colisao(bala.rect, obstaculo.rect):
                        lista_balas.remove(bala)
                        lista_obstaculos.remove(obstaculo)
                        break

            contador_tempo += 1
            if contador_tempo >= FREQUENCIA_ASTEROIDE:
                lista_obstaculos.append(Obstacle(LARGURA_TELA, ALTURA_TELA))
                contador_tempo = 0

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
                    vidas = limitar_valor(vidas + 20.0, 0, 100.0)
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
                    vidas = tomar_dano(vidas, obstaculo.dano)
                    lista_obstaculos.remove(obstaculo)

                elif obstaculo.rect.y > ALTURA_TELA:
                    lista_obstaculos.remove(obstaculo)
                    pontos += 1

            if jogador_perdeu(vidas):
                 
                 rodando = False

            if pontos > recorde:
                recorde = pontos
                salvar_recorde(CAMINHO_RECORDE, recorde)

            tela.blit(imagem_original, (fundo_x, 0))
            tela.blit(imagem_original, (fundo_x + LARGURA_TELA, 0))

            tela.blit(jogador["imagem"], jogador["rect"])
            for bala in lista_balas:
                bala.desenhar(tela)

            if ferramenta_na_tela:
                tela.blit(ferramenta_image, ferramenta_rect)
                          
            for obstaculo in lista_obstaculos:
                obstaculo.desenhar(tela)

            desenhar_barra_vida(tela, 20, 20, vidas, vidas_maximas=100)

            pygame.display.flip()

        # A partida acabou. Se o jogador nao fechou a janela, mostra a tela de fim.
        if jogando:
            jogando = tela_fim_jogo(tela, imagem_original, relogio)

    
    
    
    
    
    
    
    pygame.quit()

if __name__ == "__main__":
    executar_jogo()