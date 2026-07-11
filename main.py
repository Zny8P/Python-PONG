import pygame
pygame.init()
import random


'''Coloca as configurações iniciais da tela, sendo largura e altura (WIDTH, HEIGHT) e o título da janela (PONG)'''
WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")
loop = True
estado = "menu"
'''###Fim das configurações iniciais da tela###'''



'''Variáveis de controle do jogo'''

Resetar_bola = False #Variável para resetar a bola quando ela passar da borda da tela
delay = 1000 #milissegundos de delay para resetar a bola, caso ela passe da borda da tela
timer_delay = 0
clock = pygame.time.Clock()
FPS_LIMIT = 60



'''Placar'''
pontos_esquerdo = 0
pontos_direito = 0
ultimo_ponto = None
resetando = False

'''bola, sendo largura e altura (ball_width, ball_height), posição (ball_x, ball_y), direção (Xdirection, Ydirection) e velocidade (ball_speed)'''
ball_width = 7
ball_height = 7
ball_x = WIDTH//2 - ball_width
ball_y = HEIGHT//2 - ball_height
Xdirection, Ydirection = 1, 1
BALL_SPEED = 300
ball_speed = BALL_SPEED * 0.75  #Velocidade da bola em pixel por segundo
ball_rect = pygame.Rect(ball_x, ball_y, ball_width, ball_height)

'''Variavel iguais de ambos dos jogadores'''
jogador_width = 10
jogador_height = 100 
PLAYER_SPEED = 500 #velocidade dos jogadores em pixel por segundo

'''jogador esquerdo, sendo largura e altura (jogador_width, jogador_height) e posição (jogador_esquerdo_x, jogador_esquerdo_y)'''
jogador_esquerdo_x = 50
jogador_esquerdo_y = HEIGHT//2 - 50
esquerdo_rect = pygame.Rect(jogador_esquerdo_x, jogador_esquerdo_y, jogador_width, jogador_height)

'''jogador direito, sendo largura e altura (jogador_width, jogador_height) e posição (jogador_direito_x, jogador_direito_y)'''
jogador_direito_x = WIDTH - (jogador_width + 50)
jogador_direito_y = HEIGHT//2 - jogador_height
direito_rect = pygame.Rect(jogador_direito_x, jogador_direito_y, jogador_width, jogador_height)
chance_errar = 0.3 #10% de chance para a IA do jogador direito não se mova


'''funções para mover os elementos do jogo (bolas, jogadores, etc)'''

'''Funções para mover a bola na tela, verificando se ela bateu nas bordas da tela, ou nos jogadores, e invertendo a direção caso isso aconteça'''


def colisões_x():
    global pontos_esquerdo, pontos_direito, ultimo_ponto, Resetar_bola, Xdirection, ball_speed

    if ball_rect.colliderect(esquerdo_rect):
        ball_rect.x = esquerdo_rect.x + esquerdo_rect.width +1
        ball_speed = BALL_SPEED
        Xdirection *= -1

    if ball_rect.colliderect(direito_rect):
        ball_rect.x = direito_rect.x - ball_rect.width 
        ball_speed = BALL_SPEED
        Xdirection *= -1

    if ball_rect.left < 0:
        pontos_direito += 1
        ultimo_ponto = "direito"
        Resetar_bola = True
        return True

    if ball_rect.right > WIDTH:
        pontos_esquerdo += 1
        ultimo_ponto = "esquerdo"
        Resetar_bola = True
        return True


def colisões_y():
    global Ydirection

    if ball_rect.top < 0 + 10:
        ball_rect.y = 0 + 10
        Ydirection *= -1
    
    if ball_rect.bottom > HEIGHT - 10:
        ball_rect.y = (HEIGHT - 10) - ball_rect.height
        Ydirection *= -1

def move_ballx():
    ball_rect.x += ball_speed * Xdirection * delta_time


def move_bally():
    ball_rect.y += ball_speed * Ydirection * delta_time



def move_ball():
    global ball_speed, Xdirection, Ydirection, pontos_direito, pontos_esquerdo, Resetar_bola, timer_delay, ultimo_ponto, resetando
    '''Movimenta a bola na tela, verificando se ela bateu nas bordas da tela, ou nos jogadores, e invertendo a direção caso isso aconteça'''


    '''Código para resetar a bola no meio do campo após o ponto, e também adiciona o tempo de delay.'''
    if Resetar_bola:
        ball_rect.x = WIDTH//2 - ball_width
        ball_rect.y = HEIGHT//2 - ball_height
        timer_delay = pygame.time.get_ticks()

        resetando =  True
        Resetar_bola = False

    if resetando:
        if pygame.time.get_ticks() - timer_delay < delay:
            return
            
        resetando = False

        if ultimo_ponto == "esquerdo":
            Xdirection *= 1
        elif ultimo_ponto == "direito":
            Xdirection *= -1
        else:
            move_ballx(random.choice ([-1, 1])) #Escolhe aleatoriamente a direção da bola no eixo x

        Ydirection *= random.choice ([-1, 1]) #Escolhe aleatoriamente a direção da bola no eixo y
        ball_speed *= 0.75 # Velocidade reduzida no ínicio de cada restarts

    move_ballx()
    colisões_x()
    move_bally()
    colisões_y()

def move_jogador_esquerdo():
    global jogador_esquerdo_x, jogador_esquerdo_y

    '''Código para mover o jogador esquerdo na tela, verificando se ele bateu nas bordas da tela e impedindo que ele saia da tela'''

    '''
    lê os inputs do teclado:
     W = cima
     S = baixo
         
    Além de checar se o jogador está dentro da tela, caso contrário ele não se move
    '''

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        esquerdo_rect.y -= PLAYER_SPEED * delta_time
        if esquerdo_rect.top < 0: #Checa se o jogador está dentro da tela, caso contrário ele não se move
            esquerdo_rect.y = 0 
    if keys[pygame.K_s]:
        esquerdo_rect.y += PLAYER_SPEED * delta_time
        if esquerdo_rect.bottom > HEIGHT: #Checa se o jogador está dentro da tela, caso contrário ele não se move
            esquerdo_rect.y = HEIGHT - esquerdo_rect.height

def move_jogador_direito():
    global jogador_direito_x, jogador_direito_y, ball_x, ball_y

    '''Código para mover o jogador direito na tela, verificando se ele bateu nas bordas da tela e impedindo que ele saia da tela'''

    '''
    O código vê a posição y da bola, e efetua uma ação dependendo desse valor

    Caso ball_y for menor que o y do jogador direito, essa raquete sobe (jogador_direito_y -= 1)
    Caso ball_y for maior que o y (ponta de baixo) do jogador direito, esse jogador desce (jogador_direito_y += 1)
    '''


    if random.random() < chance_errar: # "chance_errar"% de chance da IA errar
        return

    if ball_rect.y < direito_rect.y:
        direito_rect.y -= PLAYER_SPEED * delta_time
        if direito_rect.top < 0: #Checa se o jogador está dentro da tela, caso contrário ele não se move
            direito_rect.y = 0


    if ball_rect.y + ball_rect.height > direito_rect.y + direito_rect.height:
        direito_rect.y += PLAYER_SPEED * delta_time
        if direito_rect.bottom > HEIGHT: #Checa se o jogador está dentro da tela, caso contrário ele não se move
            direito_rect.y = HEIGHT - direito_rect.height

def desenha_jogo():
    global estado, pontos_esquerdo, pontos_direito

    '''Código para desenhar os elementos do jogo (bolas, jogadores, etc)'''
    pygame.display.set_caption(f"PONG — Placar: {pontos_esquerdo} X {pontos_direito}") #Muda o nome da janela, para o placar atual do jogo


    pygame.draw.rect(screen, (255, 128, 128), (0, 0, 10, 600)) #borda da esquerda
    pygame.draw.rect(screen, (128, 128, 255), (790, 0, 10, 600)) #borda da direita
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 800, 10)) #borda de cima
    pygame.draw.rect(screen, (255, 255, 255), (0, 590, 800, 10)) #borda de baixo

    pygame.draw.rect(screen, (255, 0, 0), esquerdo_rect) #Desenha o jogador esquerdo na tela
    move_jogador_esquerdo() #Move o jogador esquerdo na tela

    pygame.draw.rect(screen, (0, 0, 255), direito_rect) #Desenha o jogador direito na tela
    move_jogador_direito() #Move o jogador direito na tela

    pygame.draw.rect(screen, (255, 255, 255),ball_rect) #Desenha a bola na tela
    move_ball() #Move a bola na tela


def menu():

    '''Desenha o titulo do jogo: "PONG" '''
    fonte1 = pygame.font.SysFont("Consolas", 60)
    texto = fonte1.render(
        "PONG",
        True,
        (255, 255, 255)
        )
    texto_rect = texto.get_rect()
    texto_rect.centerx = WIDTH // 2
    texto_rect.centery = HEIGHT // 4
    screen.blit(texto, texto_rect)

    '''Instrução p/ começar o jogo: "Press Space to start"'''

    tick = pygame.time.get_ticks()
    fonte2 = pygame.font.SysFont("Consolas", 20)
    texto2 = fonte2.render(
        "Press Space to start",
        True,
        (255, 255, 255)
    )
    texto2_rect = texto2.get_rect()
    texto2_rect.centerx = WIDTH // 2
    texto2_rect.centery =  HEIGHT * 0.75 
    texto2.set_alpha(255 // 4)
    if (tick // 500) % 2 == 0:
        screen.blit(texto2, texto2_rect)
    
def vitoria():
    '''Tela de vitória'''

    '''Desenha na tela: "You WIN" '''
    fonte = pygame.font.SysFont("Consolas", 50)
    texto = fonte.render(
        "You WIN :D",
        True,
        (255, 255, 255)
        )
    texto_rect = texto.get_rect()
    texto_rect.centerx = WIDTH // 2  
    texto_rect.centery = HEIGHT // 2 - 100
    screen.blit(texto, texto_rect)

    if pontos_esquerdo == 10 and pontos_direito == 0: #Caso o jogador esquerdo ganhe sem perder nenhum pontoS
        

        fonte_easteregg = pygame.font.SysFont("Consolas", 15)
        texto_easteregg = fonte_easteregg.render(
            "Flawless victory XD \n (10 — 0)",
            True,
            (255,255,255)
        )
        texto_easteregg.set_alpha(255 // 4)
        texto_easter_rect = texto_easteregg.get_rect()
        texto_easter_rect.centerx = WIDTH // 2
        texto_easter_rect.centery = HEIGHT // 2 - 30
        screen.blit(texto_easteregg, texto_easter_rect)

    '''Instrução p/ começar o jogo: "Press Space to restart"'''

    tick = pygame.time.get_ticks()
    fonte2 = pygame.font.SysFont("Consolas", 20)
    texto2 = fonte2.render(
        "Press Space to restart",
        True,
        (255, 255, 255)
    )

    texto2_rect = texto2.get_rect()
    texto2_rect.centerx = WIDTH // 2
    texto2_rect.centery =  HEIGHT * 0.75 
    texto2.set_alpha(255 // 4)
    if (tick // 500) % 2 == 0:
        screen.blit(texto2, texto2_rect)


def derrota():
    '''Tela de Derrota'''

    '''Desenha na tela: "You LOSE" '''
    fonte = pygame.font.SysFont("Consolas", 50)
    texto = fonte.render(
        "You LOSE :(",
        True,
        (255, 255, 255)
        )
    texto_rect = texto.get_rect()
    texto_rect.centerx = WIDTH // 2  
    texto_rect.centery = HEIGHT // 2 - 100
    screen.blit(texto, texto_rect)

    if pontos_esquerdo == 0 and pontos_direito == 10: #Caso o jogador esquerdo ganhe sem perder nenhum pontoS

        fonte_easteregg = pygame.font.SysFont("Consolas", 15)
        texto_easteregg = fonte_easteregg.render(
            "Aw Man ;-; \n (0 — 10)",
            True,
            (255,255,255)
        )
        texto_easteregg.set_alpha(255 // 4)
        texto_easter_rect = texto_easteregg.get_rect()
        texto_easter_rect.centerx = WIDTH // 2
        texto_easter_rect.centery = HEIGHT // 2 - 30
        screen.blit(texto_easteregg, texto_easter_rect)
    

    '''Instrução p/ começar o jogo: "Press Space to restart to try again"'''

    tick = pygame.time.get_ticks()
    fonte2 = pygame.font.SysFont("Consolas", 20)
    texto2 = fonte2.render(
        "Press Space to restart",
        True,
        (255, 255, 255)
    )

    texto2_rect = texto2.get_rect()
    texto2_rect.centerx = WIDTH // 2
    texto2_rect.centery =  HEIGHT * 0.75 
    texto2.set_alpha(255 // 4)
    if (tick // 500) % 2 == 0:
        screen.blit(texto2, texto2_rect)


def estado_jogo():
    global loop, estado
    '''Essa função muda o estado do jogo, além de fechar o jogo quandoo "x" da página é clicado'''

    for event in pygame.event.get():

        '''Código para fechar o programa, caso o usuário clique no X da janela'''
        if event.type == pygame.QUIT:
            loop = False
        '''troca de estado'''
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if estado == "menu":
                estado = "jogo"
            elif estado == "vitoria" or estado == "derrota":
                estado = "menu"
    if pontos_esquerdo == 10:
        estado = "vitoria"
    if pontos_direito == 10:
        estado = "derrota"


'''Loop principal do jogo'''
while loop:

    delta_time = clock.tick(FPS_LIMIT) / 1000.0 #Calcula o delta time para manter a velocidade do jogo constante, independente da taxa de quadros por segundo (FPS)

    estado_jogo()

    screen.fill((0,0,0)) #Preenche a tela com a cor preta

    if estado == "menu":
        menu()
    elif estado == "jogo":   
        desenha_jogo()
    elif estado == "vitoria":
        vitoria()
    elif estado == "derrota":
        derrota()


    '''Código para atualizar a tela do jogo(Tem de estar no final do loop principal)'''
    pygame.display.update()