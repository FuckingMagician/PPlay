from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.sound import *
import datetime
import random

janela = Window(600, 600)
mouse = janela.get_mouse()
teclado = janela.get_keyboard()
janela.set_title("Space Invaders")
backs_list = ["backs/back1.png", "backs/back2.png", "backs/back3.png", "backs/back4.png", "backs/back5.png", "backs/back6.png", "backs/back7.png"]
monster_list = ["monster/green.png", "monster/red.png", "monster/yellow.png"]

def start_game(dif, shot_cooldown):

    running = True
    fundo = GameImage(random.choice(backs_list))
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
    mat_x = janela.width // 2 - (5 * monster_width) + 15
    mat_y = 0
    mat_speed = 50 * dif
    mshot_list = []
    mshot_speed = 200 * dif
    tempom = 0
    mat = [[], [], [], []]

    for i in range(4):
        for j in range(7):
            monster = Sprite(random.choice(monster_list))
            monster_x = mat_x + j * (monster_width + space) - monster_width // 2
            monster_y = mat_y + i * (monster_height + space)
            monster.set_position(monster_x, monster_y)
            mat[i].append(monster)

    tempo = 0
    pts = 0
    lives = 3
    invtime = 0   
    invincible = False
    game_over = False

    start = False

    #Game music
    if dif == 1:
        gameMusic = Sound("Music/music1.ogg")

    if dif == 1.5:
        gameMusic = Sound("Music/music2.ogg")

    if dif == 2:
        gameMusic = Sound("Music/music3.ogg")

    #By Jan125
    gameMusic.set_volume(30)
    gameMusic.set_repeat(True)

    # Game Loop
    while running:
        
        gameMusic.play()

        dt = janela.delta_time()
        tempo += dt
        tempom += dt
        
        #Drawing score and lives
        janela.draw_text(('Pts: '), 2, 550, size=30, color=(255, 255, 255), font_name="Arial", bold=True, italic=False)
        janela.draw_text(str(pts), 70, 550, size=30, color=(255, 255, 255), font_name="Arial", bold=True, italic=False)
        janela.draw_text(('Lives: '), 500, 550, size=30, color=(255, 255, 255), font_name="Arial", bold=True, italic=False)
        janela.draw_text(str(lives), 580, 550, size=30, color=(255, 255, 255), font_name="Arial", bold=True, italic=False)

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
        if teclado.key_pressed("SPACE") and tempo > shot_cooldown:
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

                        if monster.x <= 0:
                            monster.set_position(0, monster.y)
                            inverte = True

                        if monster.x >= janela.width - monster.width:
                            monster.set_position(janela.width - monster.width, monster.y)
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
            gameMusic.stop()
            #nome = input("Digite seu nome: ")
            data_atual = datetime.datetime.now().strftime("%d/%m/%Y")
            with open("ranking.txt", "a") as arquivo:
                arquivo.write("Pontuação: " + str(pts) + " - Data: " + data_atual + "\n")
            main_menu()


        mshot_cooldown = 0
        if dif == 1:
            mshot_cooldown = 1
        if dif == 1.5:
            mshot_cooldown = 0.8
        if dif == 2:
            mshot_cooldown = 0.6
            

        #Monster Shooting
        if start:
            posm = []
            for i in range(4):
                for j in range(7):
                    if mat[i][j] is not None:
                        posm.append((i, j))
                        
            if tempom > mshot_cooldown:
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
            dif *= 2
            mat = [[], [], [], []]

            for i in range(4):
                for j in range(7):
                    monster = Sprite(random.choice(monster_list))
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
            gameMusic.stop()
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

    #By Nia Mi
    menuSound = Sound("Music/menuMusic.ogg")
    menuSound.set_volume(20)

    while on_menu:

        menuSound.play()
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
                menuSound.stop()
                start_game(dif, 0.4*dif)
        
        if mouse.is_over_object(exit_button):
            if click:
                on_menu = False
                janela.close()
            
        if mouse.is_over_object(set_button):
            if click:
                settings(menuSound)

        if mouse.is_over_object(rank_button):
            if click:
                menuSound.stop()
                display_ranking()

        fundo_menu.draw()
        play_button.draw()
        set_button.draw()
        rank_button.draw()
        exit_button.draw()

        janela.update()

def settings(menuSound):
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
                menuSound.stop()
                start_game(dif, 0.4)

        if allow:
            if mouse.is_button_pressed(1) and mouse.is_over_object(medio):
                dif = 1.5
                menuSound.stop()
                start_game(dif, 0.5)

        if allow:
            if mouse.is_button_pressed(1) and mouse.is_over_object(dificil):
                dif = 2
                menuSound.stop()
                start_game(dif, 0.6)
        
        if teclado.key_pressed("ESC"):
            on_settings = False
            main_menu()

        fundo_menu_dif.draw()
        facil.draw()
        medio.draw()
        dificil.draw()
        
        janela.update()

def extrair_pontuacao(linha):
    try:
        # Extract the score from the line and convert it to an integer
        score = int(linha.split('Pontuação: ')[1].split(' -')[0].strip())
        return score
    except (IndexError, ValueError):
        # Handle cases where the expected patterns are not found or conversion fails
        return 0

def display_ranking():
    janela = Window(600, 600)
    teclado = janela.get_keyboard()
    fundo = GameImage("assets/rankingBack.png")

    # Ler o conteúdo do arquivo
    with open('ranking.txt', 'r') as arquivo:
        linhas = arquivo.readlines()

    # Ordenar as linhas de acordo com a pontuação em ordem decrescente
    linhas_ordenadas = sorted(linhas, key=extrair_pontuacao, reverse=True)

    fundo.draw()
    # Escrever as linhas ordenadas de volta para o arquivo
    with open('ranking.txt', 'w') as arquivo:
        arquivo.writelines(linhas_ordenadas)
    while True:
        s = 100
        with open("ranking.txt", "r") as file:
            count = 0
            for line in file:
                if count < 5:
                    janela.draw_text(line, 20, s, size=30, color=(255, 255, 255), font_name="Arial", bold=True, italic=False)
                    s += 100
                    count += 1
                else:
                    break

        if teclado.key_pressed("ESC"):
            main_menu()

        janela.update()

main_menu()
