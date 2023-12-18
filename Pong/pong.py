from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.sound import *

#Game Loop
def game():

    janela = Window(800, 600)
    teclado = Window.get_keyboard()
    bola = Sprite("Assets/ball.png", 1)
    fundo = GameImage("Assets/BACK.png")

    #By 0f9ran 
    popSound = Sound("Sounds/pop.ogg")
    popSound.set_volume(40)

    #By NenadSimic
    winSound = Sound('Sounds/win.ogg')
    winSound.set_volume(100)

    janela.set_title("Pong")

    paddir = Sprite("Assets/pad.png")
    padesq = Sprite("Assets/pad.png")

    pad_esq = paddir
    pad_dir = padesq

    #Posição inicial da bola
    bola.x = (janela.width/2) - (bola.width/2)
    bola.y = (janela.height/2) - (bola.height/2)
    bola.set_position(x = bola.x, y = bola.y)

    #Velocidade da bola
    vel_x = 300
    vel_y = 300

    #Posição dos pads
    pad_esq.x = 7
    pad_esq.y = janela.height/2 - pad_esq.height/2
    pad_esq.set_position(x = pad_esq.x, y = pad_esq.y)

    pad_dir.x = 753
    pad_dir.y = janela.height/2 - pad_esq.height/2
    pad_dir.set_position(x = pad_dir.x, y = pad_dir.y)

    #Velocidade dos pads
    vel_pad = 350

    #Pontuação inicial
    pts_e = 0
    pts_d = 0

    fundo.draw()
    bola.draw()
    pad_esq.draw()
    pad_dir.draw()
    janela.draw_text(str(pts_e), 55, 10, size=50, color=(255, 255, 255), font_name="Arial", bold=True, italic=False)
    janela.draw_text(str(pts_d), janela.width - 75, 10, size=50, color=(255, 255, 255), font_name="Arial", bold=True, italic=False)
    espera = True
    while (True):
        
        if (teclado.key_pressed("ESC")):
                menu()

        dt = janela.delta_time()#A cada loop verifica a duração do frame

        if not espera:

            #atualizando a posição da bola para dar movimento
            bola.x = bola.x + vel_x * dt
            bola.y = bola.y + vel_y * dt

            #Collision of ball with walls

            #Colisão Horizontal
            if (bola.x <= 0):
                winSound.play()
                bola.set_position(janela.width / 2 - bola.width / 2, janela.height / 2 - bola.height / 2)
                pts_d += 1
                pad_esq.set_position(7, janela.height/2 - pad_esq.height/2)
                pad_dir.set_position(753, janela.height/2 - pad_esq.height/2)
                espera = True
                vel_x = 0
                vel_y = 0
                

            if (bola.x > janela.width - bola.width):
                winSound.play()
                bola.set_position(janela.width / 2 - bola.width / 2, janela.height / 2 - bola.height / 2)
                pts_e += 1
                pad_esq.set_position(7, janela.height/2 - pad_esq.height/2)
                pad_dir.set_position(753, janela.height/2 - pad_esq.height/2)
                espera = True
                vel_x = 0
                vel_y = 0
                
            #Colisão Vertical 
            if bola.y <= 0:
                bola.y = 0
                vel_y *= -1

            if bola.y > janela.height - bola.height:
                bola.y = janela.height - bola.height
                vel_y *= -1
            
            #Colisão da bola com os pads
            if (bola.collided(pad_esq)):
                popSound.play()
                bola.x = pad_esq.x + pad_esq.width
                vel_x *= -1 
                vel_x *= 1.1 
                vel_y *= 1.1 
                

            if (bola.collided(pad_dir)):
                popSound.play()
                bola.x = pad_dir.x - bola.width
                vel_x *= -1 
                vel_x *= 1.1 
                vel_y *= 1.1 
                

            #Movimento dos pads
            if (teclado.key_pressed("W")):
                pad_esq.y = pad_esq.y - (vel_pad * dt)
            if teclado.key_pressed("S"):
                pad_esq.y = pad_esq.y + (vel_pad * dt)


            #if (teclado.key_pressed("UP")):
                #pad_dir.y = pad_dir.y - (vel_pad * dt)
            #if teclado.key_pressed("DOWN"):
                #pad_dir.y = pad_dir.y + (vel_pad * dt)

            #Colisão dos pads nas paredes
            if (pad_esq.y <= 0):#pad esquerdo
                pad_esq.y = 0
            if (pad_esq.y > janela.height - pad_esq.height):
                pad_esq.y = janela.height - pad_esq.height

            if (pad_dir.y <= 0):#pad direito
                pad_dir.y = 0
            if (pad_dir.y > janela.height - pad_dir.height):
                pad_dir.y = janela.height - pad_dir.height

            #IA pad da direita
            if (bola.x > janela.width / 2):
                if bola.y < pad_dir.y + pad_dir.height / 2:
                    pad_dir.y -= vel_pad * dt
                if bola.y > pad_dir.y + pad_dir.height / 2:
                    pad_dir.y += vel_pad * dt

            #Drawing
            fundo.draw()
            bola.draw()
            pad_esq.draw()
            pad_dir.draw()
            janela.draw_text(str(pts_e), 55, 10, size=50, color=(255, 255, 255), font_name="Arial", bold=True, italic=False)
            janela.draw_text(str(pts_d), janela.width - 75, 10, size=50, color=(255, 255, 255), font_name="Arial", bold=True, italic=False)
            janela.update()
            
        else:
            bola.x = janela.width / 2 - bola.width / 2
            bola.y = janela.height / 2 - bola.height / 2
            bola.draw()
            janela.update()

            if teclado.key_pressed("SPACE"):
                espera = False
                vel_x = 300
                vel_y = 300

def menu():
    menu_janela = Window(800, 600)
    mouse = Window.get_mouse()
    menu_fundo = GameImage("Assets/Menu.png")
    botao_play = Sprite("Assets/PLAY.png")
    botao_play_2 = Sprite("Assets/PLAY_2.png")
    botao_exit = Sprite("Assets/EXIT.png")
    botao_exit_2 = Sprite("Assets/EXIT_2.png")

    #By Fupi
    clickSound = Sound("Sounds/click.ogg")
    clickSound.set_volume(100)

    play_x = 250
    play_y = 260
    botao_play.set_position(play_x, play_y)

    exit_x = 250
    exit_y = 410
    botao_exit.set_position(exit_x, exit_y)
    on_menu = True
    while(on_menu):

        menu_fundo.draw()
        botao_play.draw()
        botao_exit.draw()
        menu_janela.update()

        if(mouse.is_over_object(botao_play)):
            botao_play = botao_play_2
            botao_play.set_position(play_x, play_y)
            if(mouse.is_button_pressed(1)):
                clickSound.play()
                game()
        if(not(mouse.is_over_object(botao_play))):
            botao_play = Sprite("Assets/PLAY.png")
            botao_play.set_position(play_x, play_y)


        if(mouse.is_over_object(botao_exit)):
            botao_exit = botao_exit_2
            botao_exit.set_position(exit_x, exit_y)
            if(mouse.is_button_pressed(1)):
                menu_janela.close()
        if(not(mouse.is_over_object(botao_exit))):
            botao_exit = Sprite("Assets/EXIT.png")
            botao_exit.set_position(exit_x, exit_y)
menu()