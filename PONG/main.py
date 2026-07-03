import pygame
pygame.init()


'''Coloca as configurações iniciais da tela, sendo largura e altura (WIDTH, HEIGHT) e o título da janela (PONG)'''
WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")
loop = True
'''###Fim das configurações iniciais da tela###'''

'''Variáveis de controle do jogo'''

'''bola, sendo largura e altura (ball_width, ball_height), posição (ball_x, ball_y), direção (Xdirection, Ydirection) e velocidade (ball_speed)'''
ball_width = 7
ball_height = 7
ball_x = WIDTH//2 - ball_width
ball_y = HEIGHT//2 - ball_height
Xdirection, Ydirection = 1, 1
ball_speed = 1 #Velocidade da bola

'''Tamanho dos jogadores'''
jogador_width = 10
jogador_height = 100 

'''jogador esquerdo, sendo largura e altura (jogador_width, jogador_height) e posição (jogador_esquerdo_x, jogador_esquerdo_y)'''
jogador_esquerdo_x = 50
jogador_esquerdo_y = HEIGHT//2 - 50

'''jogador direito, sendo largura e altura (jogador_width, jogador_height) e posição (jogador_direito_x, jogador_direito_y)'''
jogador_direito_x = WIDTH - (jogador_width + 50)
jogador_direito_y = HEIGHT//2 - jogador_height


'''funções para mover os elementos do jogo (bolas, jogadores, etc)'''
def move_ball():
    global ball_x, ball_y, Xdirection, Ydirection

    '''Código para mover a bola na tela, verificando se ela bateu nas bordas da tela, ou nos jogadores, e invertendo a direção caso isso aconteça'''
    ball_x += ball_speed * Xdirection
    ball_y += ball_speed * Ydirection

    '''colisão com as bordas da tela'''
    if ball_x <= 0 or ball_x + ball_width >= WIDTH:
        Xdirection *= -1
    if ball_y <= 0 or ball_y + ball_height >= HEIGHT:
        Ydirection *= -1

    '''colisão com o jogador esquerdo'''
    if (ball_x <= jogador_esquerdo_x + jogador_width and 
        ball_y + ball_height >= jogador_esquerdo_y and 
        ball_y <= jogador_esquerdo_y + jogador_height and 
        ball_x >= jogador_esquerdo_x):
        Xdirection *= -1
        if (ball_x < jogador_esquerdo_x + jogador_width and
            ball_y + ball_height >= jogador_esquerdo_y and
            ball_y <= jogador_esquerdo_y + jogador_height):
            Ydirection *= -1

    '''colisão com o jogador direito'''
    if (ball_x + ball_width >= jogador_direito_x and 
        ball_y + ball_height >= jogador_direito_y and 
        ball_y <= jogador_direito_y + jogador_height and 
        ball_x + ball_width <= jogador_direito_x + jogador_width):
        Xdirection *= -1
        if (ball_x + ball_width > jogador_direito_x and
            ball_y + ball_height >= jogador_direito_y and
            ball_y <= jogador_direito_y + jogador_height):
            Ydirection *= -1


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
        jogador_esquerdo_y -= 1
        if jogador_esquerdo_y < 0: #Checa se o jogador está dentro da tela, caso contrário ele não se move
            jogador_esquerdo_y += 1
    if keys[pygame.K_s]:
        jogador_esquerdo_y += 1
        if jogador_esquerdo_y + jogador_height > HEIGHT: #Checa se o jogador está dentro da tela, caso contrário ele não se move
            jogador_esquerdo_y -= 1

def move_jogador_direito():
    global jogador_direito_x, jogador_direito_y, ball_x, ball_y

    '''Código para mover o jogador direito na tela, verificando se ele bateu nas bordas da tela e impedindo que ele saia da tela'''

    '''
    
    '''
    if ball_y < jogador_direito_y:
        jogador_direito_y -= 1
    if ball_y + ball_height > jogador_direito_y + jogador_height:
        jogador_direito_y += 1





'''Loop principal do jogo'''
while loop:

    '''Código para fechar o programa, caso o usuário clique no X da janela'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

    screen.fill((0,0,0)) #Preenche a tela com a cor preta

    '''Código para desenhar os elementos do jogo (bolas, jogadores, etc)'''

    pygame.draw.rect(screen, (255, 255, 255), (ball_x, ball_y, ball_width, ball_height)) #Desenha a bola na tela
    move_ball() #Move a bola na tela

    pygame.draw.rect(screen, (255, 255, 255), (jogador_esquerdo_x, jogador_esquerdo_y, jogador_width, jogador_height)) #Desenha o jogador esquerdo na tela
    move_jogador_esquerdo() #Move o jogador esquerdo na tela

    pygame.draw.rect(screen, (255, 255, 255), (jogador_direito_x, jogador_direito_y, jogador_width, jogador_height)) #Desenha o jogador direito na tela
    move_jogador_direito() #Move o jogador direito na tela

    '''Código para atualizar a tela do jogo(Tem de estar no final do loop principal)'''
    pygame.display.update()