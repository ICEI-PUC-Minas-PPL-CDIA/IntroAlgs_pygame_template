import pygame
import random

def pegar_sprite(local_arquivo, x, y, width, height, scale=1):
    """Corta um único elemento de uma spritesheet BMP e remove o fundo."""
    
    # 1. Carrega o BMP e usa .convert() (sem alpha) para otimizar a velocidade
    sheet = pygame.image.load(local_arquivo).convert_alpha()

    # 2. Cria uma superfície padrão para o recorte (não precisa de SRCALPHA aqui)
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # 3. Copia o pedaço da folha BMP para a nossa nova imagem
    image.blit(sheet, (0, 0), (x, y, width, height))
    
    # 4. CONFIGURAÇÃO DA TRANSPARÊNCIA (O segredo para o BMP)
    # Pegamos a cor do pixel no canto superior esquerdo (0,0) do recorte, 
    # assumindo que o fundo do seu sprite começa ali.
    cor_do_fundo = image.get_at((0, 0))
    
    # Dizemos ao Pygame para ignorar essa cor específica na hora de desenhar
    image.set_colorkey(cor_do_fundo)
    
    # 5. Aplica o redimensionamento, se houver
    if scale != 1:
        novo_largura = int(width * scale)
        novo_altura = int(height * scale)
        image = pygame.transform.scale(image, (novo_largura, novo_altura))
        
    return image


class Obstacle:
    def __init__(self, ancho_tela=800):
        # ----------------------------------------------------------------------
        # TESTE PROVISÓRIO: Criando um quadrado azul para testar o jogo
        # (Depois que funcionar, vamos trocar isso pela imagem do asteroide)
        # self.image = pygame.Surface((50, 50))
        # self.image.fill((0, 0, 255)) # Cor Azul bem visível
        # ----------------------------------------------------------------------
        
        # Se quiser testar a imagem direto depois, é só descomentar as duas linhas abaixo
        # e apagar as duas linhas do quadrado azul ali em cima:
        self.image = pegar_sprite("assets/imagens/asteroide_sheet.png", x=0, y=0, width=120, height=230, scale=0.3)
        
        self.rect = self.image.get_rect()
        
        # Sorteia a posição X de nascimento do asteroide
        self.rect.x = random.randint(0, max(1, ancho_tela - self.rect.width))
        
        # Nasce logo no topo da tela para vermos na hora
        self.rect.y = -10
        
        # Sorteia a velocidade de queda
        self.velocidad = random.randint(4, 7)
        
    def atualizar(self):
        # Faz o obstáculo cair no eixo Y
        self.rect.y += self.velocidad
        
    def desenhar(self, tela):
        # Desenha o obstáculo na tela
        tela.blit(self.image, self.rect)