from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *

janela = Window(800, 600)
teclado = Window.get_keyboard()
bola = Sprite("Assets/ball.png", 1)
fundo = GameImage("Assets/background.png")
padhalf = Sprite("Assets/padhalf.png")

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
pad_esq.x = 0
pad_esq.y = janela.height/2 - pad_esq.height/2
pad_esq.set_position(x = pad_esq.x, y = pad_esq.y)

pad_dir.x = 760
pad_dir.y = janela.height/2 - pad_esq.height/2
pad_dir.set_position(x = pad_dir.x, y = pad_dir.y)

#Velocidade dos pads
vel_pad = 350

#Pontuação inicial
pts_e = 0
pts_d = 0

espera = False

#Game Loop

while (True):
    
    dt = janela.delta_time()#A cada loop verifica a duração do frame

    if not espera:

        #atualizando a posição da bola para dar movimento
        bola.x = bola.x + vel_x * dt
        bola.y = bola.y + vel_y * dt

        #Collision of ball with walls

        #Colisão Horizontal
        if (bola.x <= 0):
            bola.set_position(janela.width / 2 - bola.width / 2, janela.height / 2 - bola.height / 2)
            pts_d += 1
            pad_esq = padhalf
            pad_esq.set_position(0, janela.height/2 - pad_esq.height/2)
            pad_dir = paddir
            pad_dir.set_position(750, janela.height/2 - pad_esq.height/2)
            espera = True
            vel_x = 0
            vel_y = 0
            

        if (bola.x > janela.width - bola.width):
            bola.set_position(janela.width / 2 - bola.width / 2, janela.height / 2 - bola.height / 2)
            pts_e += 1
            pad_esq = padesq
            pad_esq.set_position(0, janela.height/2 - pad_esq.height/2)
            pad_dir = padhalf
            pad_dir.set_position(750, janela.height/2 - pad_esq.height/2)
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
            bola.x = pad_esq.x + pad_esq.width
            vel_x *= -1 
            vel_x *= 1.1 
            vel_y *= 1.1 
            

        if (bola.collided(pad_dir)):
            bola.x = pad_dir.x - bola.width
            vel_x *= -1 
            vel_x *= 1.1 
            vel_y *= 1.1 
            

        #Movimento dos pads
        if (teclado.key_pressed("W")):
            pad_esq.y = pad_esq.y - (vel_pad * dt)
        if teclado.key_pressed("S"):
            pad_esq.y = pad_esq.y + (vel_pad * dt)


        if (teclado.key_pressed("UP")):
            pad_dir.y = pad_dir.y - (vel_pad * dt)
        if teclado.key_pressed("DOWN"):
            pad_dir.y = pad_dir.y + (vel_pad * dt)

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
        janela.draw_text(str(pts_e), 10, 10, size=50, color=(0, 0, 0), font_name="Arial", bold=False, italic=False)
        janela.draw_text(str(pts_d), janela.width - 50, 20, size=50, color=(0, 0, 0), font_name="Arial", bold=False, italic=False)
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
