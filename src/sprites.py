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
    TIPOS = [
        (0.6, 5),   # pequeno → -5%
        (1.0, 10),  # médio   → -10%
        (1.5, 15),  # grande  → -15%
    ]

    def __init__(self, ancho_tela=800, alto_tela=600):
        scale, self.dano = random.choice(self.TIPOS)
        
        # ----------------------------------------------------------------------
        # TESTE PROVISÓRIO: Criando um quadrado azul para testar o jogo
        # (Depois que funcionar, vamos trocar isso pela imagem do asteroide)
        # self.image = pygame.Surface((50, 50))
        # self.image.fill((0, 0, 255)) # Cor Azul bem visível
        # ----------------------------------------------------------------------
        
        # Se quiser testar a imagem direto depois, é só descomentar as duas linhas abaixo
        # e apagar as duas linhas do quadrado azul ali em cima:
        self.image = pegar_sprite(
            "assets/imagens/asteroide_sheet.png",
            x=0, y=0, width=48, height=48, scale=scale
        )
        
        self.rect = self.image.get_rect()
        
        # Sorteia a posição Y de nascimento do asteroide
        self.rect.y = random.randint(0, alto_tela - self.rect.height)

        # Surge o obstáculo da direita para a esquerda
        self.rect.x = ancho_tela
        
        # Sorteia a velocidade de queda
        self.velocidad = random.randint(4, 7)
        
    def atualizar(self):
        # Faz o obstáculo cair no eixo X
        self.rect.x -= self.velocidad
        
    def desenhar(self, tela):
        # Desenha o obstáculo na tela
        tela.blit(self.image, self.rect)

class Bullet:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/imagens/bullet.png").convert_alpha()
        # Reduz o tamanho da bala
        self.image = pygame.transform.scale(self.image, (100, 84))
        self.rect = self.image.get_rect(midleft=(x, y))
        self.velocidade = 15

    def atualizar(self):
        self.rect.x += self.velocidade

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)

    