# Configurações centrais do jogo (tela, cores e caminhos de arquivos).
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

TITULO_JOGO = "SpaceNinja"

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (212, 212, 212)
AZUL_ESCURO = (5, 5, 30)
VERMELHO = (220, 50, 50)
AMARELO = (255, 220, 50)

# Jogador
VELOCIDADE_JOGADOR = 5
VIDAS_INICIAIS = 3

# Meteoros (padrão Médio)
VELOCIDADE_METEORO_MIN = 3
VELOCIDADE_METEORO_MAX = 6
INTERVALO_METEORO_INICIAL = 1500  # milissegundos
INTERVALO_METEORO_MINIMO = 400
REDUCAO_INTERVALO = 150           # reduz a cada 15 s de jogo

# Pontuação: 1 ponto por segundo sobrevivido
PONTOS_POR_SEGUNDO = 1

# Dificuldades: (vel_min, vel_max, intervalo_inicial, intervalo_minimo, reducao, pontos_por_segundo)
DIFICULDADES = {
    "Facil":      (2, 4, 2200, 700, 100, 1),
    "Medio":      (3, 6, 1500, 400, 150, 2),
    "Dificil":    (4, 8, 1000, 300, 200, 4),
    "Impossivel": (6, 12, 600, 200, 250, 7),
}

CAMINHO_RECORDE = "data/recorde.txt"
CAMINHO_NAVE = "assets/imagens/nave.png"
CAMINHO_METEORO = "assets/imagens/meteoro.png"
CAMINHO_FUNDO = "assets/imagens/fundo.png"
