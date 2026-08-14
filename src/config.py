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
CAMINHO_DEATH_STAR = "assets/imagens/death_star.png"
FONTE = "assets/fontes/Starjout.ttf"

CONFIG_FASES = {
    1: {"total_enemies": 8, "intervalo_spawn": 2.0, "vel_enemy": 4},
    2: {"total_enemies": 15, "intervalo_spawn": 1.25, "vel_enemy": 5},
    3: {"total_enemies": 22, "intervalo_spawn": 0.90, "vel_enemy": 6},
    4: {"total_enemies": 25, "intervalo_spawn": 5.0, "vel_enemy": 2}#Estrela da morte
}