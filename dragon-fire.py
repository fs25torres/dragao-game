import pygame as pg
import sys

pg.init()

# mouse oculto
pg.mouse.set_visible (False) 

# Parâmetros de tela
largura = 1366
altura = 768

# Fonte
fonte = pg.font.Font(None, 70)

# Cor da tela
preto = (0, 0, 0)
branco = (255, 255, 255)

# Carrega e define o ícone
icone = pg.image.load('assets/menu/dragon-icon.png')  # Substitua pelo caminho da sua imagem de ícone
pg.display.set_icon(icone)

# Tela do jogo
tela = pg.display.set_mode((largura, altura))
pg.display.set_caption("Dragon-fire")

# Imagens da tela de menu
menu_bg = pg.image.load('assets/menu/menu dragão.png').convert_alpha()
menu_bg = pg.transform.scale(menu_bg, (largura, altura))

# Imagens da tela do jogo
fundo = pg.image.load('assets/background/skylua.png').convert_alpha()
fundo = pg.transform.scale(fundo, (largura, altura))

# Função para desenhar texto na tela
def desenha_texto(texto, fonte, cor, x, y):
    imagem_texto = fonte.render(texto, True, cor)
    tela.blit(imagem_texto, (x, y))

# classes
class DragaoPlayer(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Carregar as imagens do dragão e redimensionar para um único tamanho
        self.images = [
            pg.image.load('assets/classes game/sprites/dragon_play/dragonplay1.png').convert_alpha(),
            pg.image.load('assets/classes game/sprites/dragon_play/dragonplay2.png').convert_alpha(),
            pg.image.load('assets/classes game/sprites/dragon_play/dragonplay3.png').convert_alpha()
        ]
        self.images = [pg.transform.scale(img, (200, 200)) for img in self.images]  # Redimensionar todas as imagens do dragão
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(largura // 2, altura - 100))  # Colocar o dragão no centro da parte inferior
        self.index = 0
        self.velocidade = 5
        self.tempo_animacao = 200  # Tempo entre animações
        self.ultimo_tempo_animacao = pg.time.get_ticks()
        self.projeteis = pg.sprite.Group()  # Grupo de projéteis do jogador

    def update(self):
        # Animação do dragão
        agora = pg.time.get_ticks()
        if agora - self.ultimo_tempo_animacao > self.tempo_animacao:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            self.ultimo_tempo_animacao = agora

        # Movimento do dragão (esquerda, direita, cima e baixo)
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidade
        if keys[pg.K_DOWN] and self.rect.bottom < altura:
            self.rect.y += self.velocidade
        if keys[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if keys[pg.K_RIGHT] and self.rect.right < largura:
            self.rect.x += self.velocidade

        # Atualiza os projéteis
        self.projeteis.update()
     
    def atirar(self):
        # Ajustar o ponto de disparo para a cabeça do dragão
        pos_projetil_x = self.rect.centerx
        pos_projetil_y = self.rect.top + 70  # Ajuste para aproximar da cabeça do dragão
        novo_projetil = ProjetilPlayer(pos_projetil_x, pos_projetil_y)
        self.projeteis.add(novo_projetil)

class ProjetilPlayer(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carregar as imagens da animação do projétil e redimensionar
        self.images = [
            pg.image.load('assets/classes game/sprites/proj.player/fire_play1.png').convert_alpha(),
            pg.image.load('assets/classes game/sprites/proj.player/fire_play2.png').convert_alpha()
        ]
        self.images = [pg.transform.scale(img, (200, 200)) for img in self.images]  # Redimensionar para um único tamanho
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = -10  # Projétil vai se mover para cima
        self.tempo_animacao = 100  # Tempo entre animações
        self.ultimo_tempo_animacao = pg.time.get_ticks()

    def update(self):
        # Atualizar a animação do projétil
        agora = pg.time.get_ticks()
        if agora - self.ultimo_tempo_animacao > self.tempo_animacao:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            self.ultimo_tempo_animacao = agora

        # Movimento do projétil para cima
        self.rect.y += self.velocidade
        # Remover o projétil se ele sair da tela
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Animação do inimigo
        self.images = [
            pg.image.load('assets/classes game/sprites/inidrag/enedrag1.png').convert_alpha(),
            pg.image.load('assets/classes game/sprites/inidrag/enedrag2.png').convert_alpha(),
            pg.image.load('assets/classes game/sprites/inidrag/enedrag3.png').convert_alpha()
        ]
        self.images = [pg.transform.scale(img, (600, 600)) for img in self.images]  # Redimensionar todas as imagens do inimigo
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(largura // 2, 200))  # Colocar o inimigo no topo
        self.velocidade_x = 3
        self.tempo_animacao = 200  # Tempo entre animações
        self.ultimo_tempo_animacao = pg.time.get_ticks()
        self.direcao = 1  # Direção de movimento
        self.ultimo_tempo_tiro = pg.time.get_ticks()
        self.tempo_tiro = 2000  # Intervalo de tiro em milissegundos
        self.projeteis = pg.sprite.Group()  # Grupo de projéteis do inimigo

    def update(self):
        # Animação do inimigo
        agora = pg.time.get_ticks()
        if agora - self.ultimo_tempo_animacao > self.tempo_animacao:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            self.ultimo_tempo_animacao = agora

        # Movimento lateral do inimigo
        self.rect.x += self.velocidade_x * self.direcao
        if self.rect.left <= 0 or self.rect.right >= largura:
            self.direcao *= -1  # Mudar direção ao atingir as bordas

        # Atualiza os projéteis
        self.projeteis.update()

    def atirar(self):
        pos_projetil_inimigo_x = self.rect.centerx
        pos_projetil_inimigo_y = self.rect.top + 300
        agora = pg.time.get_ticks()
        if agora - self.ultimo_tempo_tiro > self.tempo_tiro:
            novo_projetil = ProjetilEnemy(pos_projetil_inimigo_x, pos_projetil_inimigo_y)
            self.projeteis.add(novo_projetil)
            self.ultimo_tempo_tiro = agora

class ProjetilEnemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Carregar animação de projétil inimigo
        self.images = [
            pg.image.load('assets/classes game/sprites/proj.inimigo/proj_enemy1.png').convert_alpha(),
            pg.image.load('assets/classes game/sprites/proj.inimigo/proj_enemy2.png').convert_alpha()
        ]
        self.images = [pg.transform.scale(img, (400, 400)) for img in self.images]  # Redimensionar para um único tamanho=
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidade = 5  # Ajuste conforme necessário
        self.tempo_animacao = 100  # Tempo entre animações
        self.ultimo_tempo_animacao = pg.time.get_ticks()

    def update(self):
        # Atualizar a animação do projétil
        agora = pg.time.get_ticks()
        if agora - self.ultimo_tempo_animacao > self.tempo_animacao:
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            self.ultimo_tempo_animacao = agora

        # Movimento do projétil
        self.rect.y += self.velocidade
        # Remover o projétil se ele sair da tela
        if self.rect.top > altura:
            self.kill()

# Definição do menu do jogo
def menu():
    menu = True
    while menu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                   pg.quit()
                   sys.exit()

        # Desenha o fundo do menu
        tela.blit(menu_bg, (0, 0))
        desenha_texto('Pressione Enter para começar', fonte, branco, largura // 2 - 200, altura // 2 - 100)
        desenha_texto('Pressione Esc para sair', fonte, branco, largura // 2 - 200, altura // 2 - 15)

        pg.display.flip()
        # Aguarda pressionar a tecla Enter
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN]:
            jogo()

# Função do jogo
def jogo():
    clock = pg.time.Clock()

    # Criar instâncias
    dragao = DragaoPlayer()
    inimigo = Enemy()

    # Grupos de sprites
    todos_sprites = pg.sprite.Group()
    todos_sprites.add(dragao)
    todos_sprites.add(inimigo)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # Atirar com a barra de espaço
                    dragao.atirar()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                   menu()
                
        # Atualização
        todos_sprites.update()
        inimigo.atirar()

        # Desenhar na tela
        tela.blit(fundo, (0, 0))
        todos_sprites.draw(tela)
        dragao.projeteis.draw(tela)  # Desenhar projéteis do jogador
        inimigo.projeteis.draw(tela)  # Desenhar projéteis do inimigo

        # Atualizar a tela
        pg.display.flip()
        clock.tick(60)  # 60 quadros por segundo

menu()
