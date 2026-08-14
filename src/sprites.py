import pygame
import random
import math
from src.config import CAMINHO_DEATH_STAR

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

class DeathStar:
    # Ciclo do superlaser, em frames: espera -> carrega o triangulo -> dispara o feixe.
    TEMPO_RECARGA = 200   # pausa entre um tiro e outro
    TEMPO_CARGA = 80      # triangulo convergindo, ainda sem feixe (nao machuca)
    TEMPO_DISPARO = 100   # feixe reto ativo: encostou, morreu
    ESPESSURA_FEIXE = 4
    LASER_COR = (87, 25, 255)   # roxo do glow (o nucleo e sempre branco)

    def __init__(self, ancora_x, ancora_y):
        self.image = pegar_sprite(CAMINHO_DEATH_STAR, x=0, y=0, width=424, height=412, scale=1)

        self.rect = self.image.get_rect()

        # Recorte do conteudo visivel dentro da imagem (ignora o padding transparente).
        # Serve de base para a hitbox seguir a esfera, e nao o quadrado de 512x512.
        self._bounds = self.image.get_bounding_rect()

        # Nasce centralizada no eixo Y e encostada na borda direita (fora da tela)
        self.rect.y = (ancora_y - self.rect.height) / 2
        self.rect.x = ancora_x

        # Posição X de destino: para de entrar quando estiver totalmente visível à direita
        self.destino_x = ancora_x - self.rect.width
        self.velocidade_entrada = 3
        self.entrando = True

        self.base_y = self.rect.y
        self.angulo = 0
        self.amplitude = 25
        self.velocidade_balanco = 0.02

        # --- Superlaser ---
        self.laser_estado = "recarregando"
        self.laser_timer = self.TEMPO_RECARGA
        self.laser_rect = None          # so existe na fase de disparo (colisao)
        self.prato_x = 0                # posicao do prato neste frame
        self.prato_y = 0
        self.laser_fase = 0             # avança sempre, gera a oscilacao de opacidade

    @property
    def hitbox(self):
        return self._bounds.move(self.rect.x, self.rect.y)

    def atualizar(self):
        if self.entrando:
            # Desliza para a esquerda até chegar no destino
            self.rect.x -= self.velocidade_entrada
            if self.rect.x <= self.destino_x:
                self.rect.x = self.destino_x
                self.entrando = False
        else:
            # Já entrou: oscila levemente para cima e para baixo
            self.angulo += self.velocidade_balanco
            self.rect.y = self.base_y + math.sin(self.angulo) * self.amplitude

        self._atualizar_laser()

    def _atualizar_laser(self):
        # Pulso de opacidade roda sempre, independente da fase do laser.
        self.laser_fase += 0.2

        # So começa a mirar depois de ter entrado totalmente na tela.
        if self.entrando:
            return

        # Posicao do prato neste frame (acompanha o balanço da esfera).
        self.prato_x = self.hitbox.left + 135
        self.prato_y = self.hitbox.top + 115

        # Avança o ciclo: quando o timer zera, passa para a proxima fase.
        self.laser_timer -= 1
        if self.laser_timer <= 0:
            if self.laser_estado == "recarregando":
                self.laser_estado = "carregando"
                self.laser_timer = self.TEMPO_CARGA
            elif self.laser_estado == "carregando":
                self.laser_estado = "disparando"
                self.laser_timer = self.TEMPO_DISPARO
            else:  # disparando
                self.laser_estado = "recarregando"
                self.laser_timer = self.TEMPO_RECARGA

        # O feixe reto so machuca enquanto dispara: rect de x=0 ate o foco.
        if self.laser_estado == "disparando":
            foco_x = self.prato_x - 90
            self.laser_rect = pygame.Rect(
                0, self.prato_y - self.ESPESSURA_FEIXE // 2,
                int(foco_x), self.ESPESSURA_FEIXE,
            )
        else:
            self.laser_rect = None

    def _linha_laser(self, camada, inicio, fim, largura):
        # Empilha camadas: glow largo e translucido -> nucleo fino branco-quente.
        r, g, b = self.LASER_COR
        pygame.draw.line(camada, (r, g, b, 60),  inicio, fim, largura * 3)
        pygame.draw.line(camada, (r, g, b, 120), inicio, fim, largura * 2)
        pygame.draw.line(camada, (r, g, b, 220), inicio, fim, largura)
        pygame.draw.line(camada, (255, 255, 255), inicio, fim, max(2, largura // 2))

    def desenhar_laser(self, tela):
        # Recarregando: nada na tela.
        if self.laser_estado == "recarregando":
            return

        px, py = self.prato_x, self.prato_y

        # Desenha numa camada propria; a opacidade global (pulso/fade) vai no fim.
        camada = pygame.Surface(tela.get_size(), pygame.SRCALPHA)

        # Triangulo de convergencia (aparece na carga e continua no disparo).
        topo = (px, py - 40)
        baixo = (px, py + 65)
        foco = (px - 90, py)
        reto = (px + 50, py)
        reto2 = (px - 50, py + 13)
        reto3 = (px, py + 13)
        self._linha_laser(camada, topo,  foco, 3)
        self._linha_laser(camada, baixo, foco, 3)
        self._linha_laser(camada, reto2, foco, 3)
        self._linha_laser(camada, reto3, foco, 3)
        self._linha_laser(camada, reto, (px - 85, py), 3)

        # Feixe reto: so na fase de disparo (e o que tem laser_rect).
        if self.laser_estado == "disparando":
            self._linha_laser(camada, foco, (0, py), self.ESPESSURA_FEIXE)

        if self.laser_estado == "carregando":
            # Pulsa enquanto carrega.
            camada.set_alpha(int(157 + 98 * math.sin(self.laser_fase)))
        else:
            # Disparando: comeca solido e some gradualmente conforme o timer zera.
            camada.set_alpha(int(255 * self.laser_timer / self.TEMPO_DISPARO))
        tela.blit(camada, (0, 0))

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)


class Obstacle:
    TIPOS = [
        (0.6, 5),   # pequeno → -5%
        (1.0, 10),  # médio   → -10%
        (1.5, 15),  # grande  → -15%
    ]

    def __init__(self, ancho_tela=800, alto_tela=600):
        scale, self.dano = random.choice(self.TIPOS)
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

class Enemies:
    def __init__(self, largura_tela, altura_tela, velocidade):
        
        try:
            self.image = pygame.image.load("assets/imagens/tiedefender.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (120, 120))
        except Exception:
            print("Aviso: Nao foi possivel carregar assets/imagens/tie_fighter.png")
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x = largura_tela
        
        self.rect.y = random.randint(50, altura_tela - 80)
        self.velocidade = velocidade
        self.vida = 1

        self._bounds = self.image.get_bounding_rect()

    @property
    def hitbox(self):
        return self._bounds.move(self.rect.x, self.rect.y)

    def atualizar(self, lista_lasers_enemies):
        self.rect.x -= self.velocidade

        if random.random() < 0.01:
            novo_laser = LaserEnemies(self.rect.left, self.rect.centery)
            lista_lasers_enemies.append(novo_laser)

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)

class LaserEnemies:
    def __init__(self, x, y):
        self.image = pygame.Surface((12, 4))
        
        self.image.fill((255, 50, 50))
        pygame.draw.rect(self.image, (255, 200, 200), (0, 1, 12, 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidade = 10

    def atualizar(self):
        self.rect.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)

class Bullet:
    def __init__(self, x, y):

        self.velocidade = 15
        self.dano = 5

        self.largura_laser = 26
        self.altura_laser = 4
        self.cor_laser = (50, 255, 90)
        self.rect = pygame.Rect(0, 0, self.largura_laser, self.altura_laser)
        self.rect.midleft = (x, y)

    def atualizar(self):
        self.rect.x += self.velocidade

    def desenhar(self, tela):
        camada = pygame.Surface((self.largura_laser + 20, self.altura_laser + 20), pygame.SRCALPHA)
        cx, cy = camada.get_width() // 2, camada.get_height() // 2

        r, g, b = self.cor_laser
        pygame.draw.rect(camada, (r, g, b, 60), (cx - self.largura_laser//2 - 4, cy - self.altura_laser//2 - 4, self.largura_laser + 8, self.altura_laser + 8))
        pygame.draw.rect(camada, (r, g, b, 140), (cx - self.largura_laser//2 - 2, cy - self.altura_laser//2 - 2, self.largura_laser + 4, self.altura_laser + 4))
        pygame.draw.rect(camada, (r, g, b, 255), (cx - self.largura_laser//2, cy - self.altura_laser//2, self.largura_laser, self.altura_laser))
        pygame.draw.rect(camada, (220, 255, 220, 255), (cx - self.largura_laser//2 + 4, cy - self.altura_laser//2 + 1, self.largura_laser - 8, self.altura_laser - 2))

        tela.blit(camada, (self.rect.centerx - camada.get_width()//2, self.rect.centery - camada.get_height()//2))