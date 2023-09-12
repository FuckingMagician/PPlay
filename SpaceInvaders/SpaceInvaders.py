from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
import datetime
import random

janela = Window(600, 600)
mouse = janela.get_mouse()
teclado = janela.get_keyboard()

def start_game(dif):
    running = True
    fundo = GameImage("assets/fundo.png")
    starship = Sprite("assets/player.png")

    # Creating the starship
    starship.x = janela.width / 2 - starship.width / 2
    starship.y = janela.height - starship.height - 10
    starship.set_position(starship.x, starship.y)
    starship_speed = 50 * dif
    shot_list = []
    shot_speed = 200
    tempo = 0

    # Creating the monster matrix
    monster_width = 40
    monster_height = 32
    space = monster_width // 2
    mat_x = janela.width // 2 - (5 * monster_width // 2)
    mat_y = 0
    mat_speed = 50 * dif
    mshot_list = []
    mshot_speed = 200
    tempom = 0
    mat = [[], [], [], []]

    for i in range(4):
        for j in range(7):
            monster = Sprite("assets/yellow.png")
            monster_x = mat_x + j * (monster_width + space) - monster_width // 2
            monster_y = mat_y + i * (monster_height + space)
            monster.set_position(monster_x, monster_y)
            mat[i].append(monster)

    fps = 0
    counter = 0
    tempo = 0
    pts = 0
    lives = 3
    invtime = 0   
    invincible = False
    game_over = False

    start = False

    # Game Loop
    while running:
        
        dt = janela.delta_time()
        tempo += dt
        tempom += dt
        counter += dt
        

        #Drawing score and lives
        janela.draw_text(('Pts: '), 2, 550, size=30, color=(255, 255, 255), font_name="Arial", bold=True, italic=False)
        janela.draw_text(str(pts), 70, 550, size=30, color=(255, 255, 255), font_name="Arial", bold=True, italic=False)
        janela.draw_text(('Lives: '), 500, 550, size=30, color=(255, 255, 255), font_name="Arial", bold=True, italic=False)
        janela.draw_text(str(lives), 580, 550, size=30, color=(255, 255, 255), font_name="Arial", bold=True, italic=False)

        # Controlling FPS
        if  counter >= 1:
            fps = int(1 / dt)
            counter = 0
        janela.draw_text(str(fps), 10, 10, size=20, color=(255, 255, 255), font_name="Arial", bold=False, italic=False)
        

        # Moving starship
        if start:
            if teclado.key_pressed("A"):
                starship.x -= starship_speed * dt
            if teclado.key_pressed("D"):
                starship.x += starship_speed * dt

        # Starship collision with walls
        if starship.x < 0:
            starship.x = 0
        if starship.x >= janela.width - starship.width:
            starship.x = janela.width - starship.width

        # Starship Shooting
        if teclado.key_pressed("SPACE") and tempo > 0.2:
            tempo = 0
            shot = Sprite("assets/tiro.png")
            shot.x = starship.x + starship.width / 2 - shot.width / 2
            shot.y = starship.y - shot.height
            shot_list.append(shot)

        if shot_list != []:
            for shot in shot_list:
                shot.draw()
                if shot.y <= 0:
                    shot_list.remove(shot)
                shot.y -= shot_speed * dt

        # Drawing the monsters
        for i in range(4):
            for j in range(7):
                if mat[i][j] is not None:
                    monster = mat[i][j]
                    monster.draw()
        
        # Moving the monsters
        if start:
            inverte = False
            desce = False

            for i in range(4):
                for j in range(7):
                    if mat[i][j] is not None:
                        monster = mat[i][j]
                        monster.x += mat_speed * dt

                        if monster.x <= 0 or monster.x >= janela.width - monster.width:
                            inverte = True

                if inverte:
                    mat_speed *= -1
                    break

            if inverte and not desce:
                desce = True
                for linha in mat:
                    for m in linha:
                        if m is not None:
                            m.y += 40

                    if monster.y + monster.height >= starship.y and not game_over:
                            game_over = True

        if teclado.key_pressed("SPACE") and not start:
            start = True

        if game_over:
            running = False
            nome = input("Digite seu nome: ")
            data_atual = datetime.datetime.now().strftime("%d/%m/%Y")
            with open("ranking.txt", "a") as arquivo:
                arquivo.write(f"{nome} - Pontuação: {pts} - Data: {data_atual}\n")
            
        #Monster Shooting
        if start:
            posm = []
            for i in range(4):
                for j in range(7):
                    if mat[i][j] is not None:
                        posm.append((i, j))
                        
            if tempom > 1.5:
                tempom = 0
                shotm = Sprite("assets/tiro.png")
                if posm != []:
                    pos = random.choice(posm)
                    i, j = pos
                    shotm.x = mat[i][j].x + monster.width / 2 - shotm.width / 2
                    shotm.y = mat[i][j].y + monster.height - shotm.height
                    mshot_list.append(shotm)

            if mshot_list != []:
                for shot in mshot_list:
                    shot.draw()
                    if shot.y <= 0:
                        mshot_list.remove(shot)
                    shot.y += shot_speed * dt

            


        # Collision of shots with monsters
        for s in shot_list:
                for i in range(4):
                    for j in range(7):
                        if mat[i][j] is not None and s.collided(mat[i][j]):
                            shot_list.remove(s)
                            alt = mat[i][j].y // 100
                            mat[i][j] = None
                            if alt >= 1:
                                pts += (10 + alt) * dif
                                pts = int(pts)
                            else:
                                pts += 10 * dif
                                pts = int(pts)

        all_elim = all(monster is None for row in mat for monster in row)

        if all_elim:
            dif *= 1.2
            mat = [[], [], [], []]

            for i in range(4):
                for j in range(7):
                    monster = Sprite("assets/yellow.png")
                    monster_x = mat_x + j * (monster_width + space) - monster_width // 2
                    monster_y = mat_y + i * (monster_height + space)
                    monster.set_position(monster_x, monster_y)
                    mat[i].append(monster)

        # Collision of shots with the player
        for s in mshot_list:
            if not invincible:
                if s.collided(starship):
                    mshot_list.remove(s)
                    lives -= 1
                    starship.set_position(janela.width / 2 - starship.width / 2, janela.height - starship.height - 10)
                    invincible = True
                    invtime = 0
                    
        # Invincible
        if invincible:
            invtime += dt
            if invtime < 2:
                if int(invtime * 10) % 2 == 0:
                    starship.hide()
                else:
                    starship.unhide()
            else:
                starship.unhide()
                invincible = False

        # No more lives
        if lives == 0:
            game_over = True

        if teclado.key_pressed("ESC"):
            running = False
            main_menu()

        janela.update()
        fundo.draw()
        starship.draw()


def main_menu():
    on_menu = True

    fundo_menu = GameImage("assets/menuback.png")

    play_button = Sprite("assets/jogar.png", 1)
    set_button = Sprite("assets/dificuldade.png", 1)
    rank_button = Sprite("assets/ranking.png", 1)
    exit_button = Sprite("assets/sair.png", 1)

    play_button.set_position((janela.width - play_button.width) / 2, (janela.height - play_button.height) / 3.5)
    set_button.set_position((janela.width - play_button.width) / 2, play_button.y + play_button.height + 15)
    rank_button.set_position((janela.width - play_button.width) / 2, set_button.y + set_button.height + 15)
    exit_button.set_position((janela.width - play_button.width) / 2, rank_button.y + rank_button.height + 15)

    dif = 1
    
    while on_menu:
        click = False
        
        #Mouse sobre botao
        if mouse.is_over_object(play_button):
            play_button = Sprite("assets/jogar1.png", 1)
            play_button.set_position((janela.width - play_button.width) / 2, (janela.height - play_button.height) / 3.5)
        else:
            play_button = Sprite("assets/jogar.png")
            play_button.set_position((janela.width - play_button.width) / 2, (janela.height - play_button.height) / 3.5)

        if mouse.is_over_object(set_button):
            set_button = Sprite("assets/dificuldade1.png")
            set_button.set_position((janela.width - play_button.width) / 2, play_button.y + play_button.height + 15)
        else:
            set_button = Sprite("assets/dificuldade.png")
            set_button.set_position((janela.width - play_button.width) / 2, play_button.y + play_button.height + 15)

        if mouse.is_over_object(rank_button):
            rank_button = Sprite("assets/ranking1.png")
            rank_button.set_position((janela.width - play_button.width) / 2, set_button.y + set_button.height + 15)
        else:
            rank_button = Sprite("assets/ranking.png")
            rank_button.set_position((janela.width - play_button.width) / 2, set_button.y + set_button.height + 15)

        if mouse.is_over_object(exit_button):
            exit_button = Sprite("assets/sair1.png")
            exit_button.set_position((janela.width - play_button.width) / 2, rank_button.y + rank_button.height + 15)
        else:
            exit_button = Sprite("assets/sair.png")
            exit_button.set_position((janela.width - play_button.width) / 2, rank_button.y + rank_button.height + 15)

        if mouse.is_button_pressed(1):
            click = True

        if mouse.is_over_object(play_button):
            if click:
                start_game(dif)
        
        if mouse.is_over_object(exit_button):
            if click:
                on_menu = False
                janela.close()
            
        if mouse.is_over_object(set_button):
            if click:
                settings()

        if mouse.is_over_object(rank_button):
            if click:
                rank()

        fundo_menu.draw()
        play_button.draw()
        set_button.draw()
        rank_button.draw()
        exit_button.draw()

        janela.update()


def settings():
    on_settings = True
    allow = False
    
    fundo_menu_dif = GameImage("assets/menudifback.png")

    dificil = Sprite("assets/dificil.png", 1)
    medio = Sprite("assets/medio.png", 1)
    facil = Sprite("assets/facil.png", 1)
    dif = 0
    while on_settings:
        
        facil.set_position((janela.width - facil.width) / 2,(janela.height - facil.height) / 6)
        medio.set_position((janela.width - medio.width) / 2,(facil.y + facil.height) + 40)
        dificil.set_position((janela.width - dificil.width) / 2,(medio.y + medio.height) + 40)

        if mouse.is_over_object(facil):
            facil = Sprite("Assets/facil1.png")
            facil.set_position(janela.width/2 - facil.width/2, (janela.height - facil.height) / 6)
        else:
            facil = Sprite("Assets/facil.png")
            facil.set_position(janela.width/2-facil.width/2, (janela.height - facil.height) / 6)

        if mouse.is_over_object(medio):
            medio = Sprite("Assets/medio1.png")
            medio.set_position(janela.width/2-medio.width/2, ((janela.height - facil.height) / 6) + 150)
        else:
            medio = Sprite("Assets/medio.png")
            medio.set_position(janela.width/2-medio.width/2, ((janela.height - facil.height) / 6) + 150)

        if mouse.is_over_object(dificil):
            dificil = Sprite("Assets/dificil1.png")
            dificil.set_position(janela.width/2-dificil.width/2, (((janela.height - facil.height) / 6) + 150) + 150)
        else:
            dificil = Sprite("Assets/dificil.png")
            dificil.set_position(janela.width/2-dificil.width/2, (((janela.height - facil.height) / 6) + 150) + 150)

        if not(mouse.is_button_pressed(1)):
            allow = True
            
        if allow:
            if mouse.is_button_pressed(1) and mouse.is_over_object(facil):
                dif = 1
                start_game(dif)

        if allow:
            if mouse.is_button_pressed(1) and mouse.is_over_object(medio):
                dif = 1.5
                start_game(dif)

        if allow:
            if mouse.is_button_pressed(1) and mouse.is_over_object(dificil):
                dif = 2
                start_game(dif)
            
        
        if teclado.key_pressed("ESC"):
            on_settings = False
            main_menu()

        fundo_menu_dif.draw()
        facil.draw()
        medio.draw()
        dificil.draw()
        
        janela.update()


def extrair_pontuacao(linha):
    # Extrai a pontuação da linha e converte para inteiro
    return int(linha.split('- Pontuação: ')[1].split(' -')[0].strip())

def rank():

    janela = Window(600, 600)
    teclado = janela.get_keyboard()

    # Ler o conteúdo do arquivo
    with open('ranking.txt', 'r') as arquivo:
        linhas = arquivo.readlines()

    # Ordenar as linhas de acordo com a pontuação em ordem decrescente
    linhas_ordenadas = sorted(linhas, key=extrair_pontuacao, reverse=True)

    # Escrever as linhas ordenadas de volta para o arquivo
    with open('ranking.txt', 'w') as arquivo:
        arquivo.writelines(linhas_ordenadas)

    while True:
        s = 100
        janela.draw_text("RANKING", 20, 20, size = 30, color = (255,255,255), font_name = "Arial", bold = False, italic = False)
        with open("ranking.txt", "r") as file:
            count = 0
            for line in file:
                if count < 5:
                    janela.draw_text(line, 20, s, size = 30, color = (255,255,255), font_name = "Arial", bold = False, italic = False)
                    s += 100
                    count += 1
                else:
                    break

        if teclado.key_pressed("ESC"):
            main_menu()
            
        janela.update()



main_menu()
