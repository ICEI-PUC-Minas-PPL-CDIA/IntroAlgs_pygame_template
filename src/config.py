# Configurações centrais do jogo (tela, cores e caminhos de arquivos).
import pygame

# Resolução dinâmica: usa o tamanho real do monitor (sem barras pretas em
# nenhuma proporção). Precisamos inicializar só o subsistema de vídeo para
# conseguir consultar a resolução do desktop antes de criar a janela.
pygame.display.init()
_info = pygame.display.Info()
LARGURA_TELA = _info.current_w
ALTURA_TELA = _info.current_h

FPS = 60

TITULO_JOGO = "Antares"

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
RED_ANTARES = (178, 38, 0)
WALLPAPER = "assets/imagens/starsky.jpg"

CAMINHO_RECORDE = "data/recorde.txt"
CAMINHO_SPRITES = "assets/imagens/spritesheet.bmp"
FONTE = "assets/fontes/Starjout.ttf"