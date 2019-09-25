# Jucimar Jr 2019
# pong em turtle python https://docs.python.org/3.3/library/turtle.html
# baseado em http://christianthompson.com/node/51
# fonte Press Start 2P https://www.fontspace.com/codeman38/press-start-2p
# som pontuacao https://freesound.org/people/Kodack/sounds/258020/

from sys import argv, exit
from UtilsPong import show_error_log, show_help_information
import os
from time import sleep
import turtle

playing = True

# Funcao para criar a janela (screen)
def create_screen(title, width, height):
    screen = turtle.Screen()
    screen.title(title)
    screen.bgcolor("black")
    screen.setup(width=width, height=height)
    screen.tracer(0)
    return screen

# Funcao que e chamada ao fechar a janela
# Usada para finalizar o game loop
def close_screen():
    global playing
    playing = not playing

# Funcao para criar o turtle das raquetes
def create_paddle(x, y, width, height, color):
    paddle = turtle.Turtle()
    paddle.speed(0)
    paddle.shape("square")
    paddle.color(color)
    paddle.shapesize(stretch_wid=width, stretch_len=height)
    paddle.penup()
    paddle.goto(x, y)
    return paddle

# Funcao para criar o turtle da bola
def create_ball(x, y, color):
    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("circle")
    ball.color(color)
    ball.penup()
    ball.goto(x, y)
    ball.dx = 1
    ball.dy = 1
    return ball

def create_hud():
    hud = turtle.Turtle()
    hud.speed(0)
    hud.shape("square")
    hud.color("white")
    hud.penup()
    hud.hideturtle()
    hud.goto(0, 250)
    return hud

# mover raquete 1
def paddle_1_up():
    y = paddle_1.ycor()
    if y + 20 < 250:
        y += 20
    paddle_1.sety(y)

def paddle_1_down():
    y = paddle_1.ycor()
    if y - 20 > -250:
        y += -20
    paddle_1.sety(y)

def paddle_2_up():
    y = paddle_2.ycor()
    if y + 20 < 250:
        y += 20
    paddle_2.sety(y)

def paddle_2_down():
    y = paddle_2.ycor()
    if y - 20 > -250:
        y += -20
    paddle_2.sety(y)

def collision_1(paddle, ball):
    px, py = paddle.xcor(), paddle.ycor()
    bx, by = ball.xcor(), ball.ycor()

    if by - 10 <= py + 50 and by + 10 >= py - 50 and bx - 10 <= px + 10 and bx + 10 >= px - 10:
        ball.dx *= -1
        ball.dx += 0.2 if ball.dx > 0 else -0.2
        if abs(by - py) < 10:
            ball.dy = 0
        elif abs(by - py) < 20:
            ball.dy = ball.dx if by > py else ball.dx * -1
        elif abs(by - py) < 30:
            ball.dy = ball.dx + 0.8 if by > py else (ball.dx + 0.8) * -1
        elif abs(by - py) < 40:
            ball.dy = ball.dx + 0.4 if by > py else (ball.dx + 0.4) * -1
        else:
            ball.dy = ball.dx + 0.2 if by > py else (ball.dx + 0.2) * -1
        os.system("aplay bounce.wav&")
    
    if bx + 10 <= px - 10 and bx - 10 >= px + 10 and (by - 10 <= py + 50 or by + 10 >= py - 50):
        ball.dx *= -1
        ball.dy *= -1
        os.system("aplay bounce.wav&")


def collision_2(paddle, ball):
    px, py = paddle.xcor(), paddle.ycor()
    bx, by = ball.xcor(), ball.ycor()

    if by - 10 <= py + 50 and by + 10 >= py - 50 and bx + 10 >= px - 10 and bx - 10 <= px + 10:
        ball.dx *= -1
        ball.dx += 0.2 if ball.dx > 0 else -0.2
        if abs(by - py) < 10:
            ball.dy = 0
        elif abs(by - py) < 20:
            ball.dy = ball.dx if by < py else ball.dx * -1
        elif abs(by - py) < 30:
            ball.dy = ball.dx - 0.8 if by < py else (ball.dx + 0.8) * -1
        elif abs(by - py) < 40:
            ball.dy = ball.dx - 0.4 if by < py else (ball.dx + 0.4) * -1
        else:
            ball.dy = ball.dx - 0.2 if by < py else (ball.dx + 0.2) * -1
        os.system("aplay bounce.wav&")

    if bx - 10 >= px + 10 and bx + 10 <= px - 10 and (by - 10 <= py + 50 or by + 10 >= py - 50):
        ball.dx *= -1
        ball.dy *= -1
        os.system("aplay bounce.wav&")
    
def collider_walls (t1, t2):
    if t2.ycor() > 295 and t1.ycor() + 15 > t2.ycor():
        os.system("aplay bounce.wav&")
        t1.dy *= -1
    if t2.ycor() < -280 and t1.ycor() - 15 < t2.ycor():
        os.system("aplay bounce.wav&")
        t1.dy *= -1

# atualiza placar
def update_score():
    os.system("aplay 258020__kodack__arcade-bleep-sound.wav&")
    ball.goto(0,0)
    ball.dx *= -1
    ball.dy *= -1

# verificacao de parametros e error_showcase
parameters = argv[1:]
number_of_parameters = len(parameters)
num_players = 2

if number_of_parameters == 1:
    arg = ""
    try:
        arg = argv[1]
    except Exception:
        show_error_log()
        exit()

    if arg == "-help":
        show_help_information()
        exit()

    elif arg == "-1":
        num_players = 1

    else:
        show_error_log()
        exit()
    
screen = create_screen("My Pong", 800, 600)
root = screen.getcanvas().winfo_toplevel()
root.protocol("WM_DELETE_WINDOW", close_screen)

paddle_1 = create_paddle(-350, 0, 5, 1, "red")
paddle_2 = create_paddle(350, 0, 5, 1, "blue")

ball = create_ball(0, 0, "white")

north_wall = create_paddle(0, 300, 0.5, 40, "black")
south_wall = create_paddle(0, -295, 0.5, 40, "black")
left_wall = create_paddle(-400, 0, 30, 0.5, "red")
right_wall = create_paddle(395, 0, 30, 0.5, "red")

left_player_score = 0
right_player_score = 0

hud = create_hud()
hud.write("{} : {}".format(left_player_score, right_player_score), align="center", font=("Press Start 2P",24,"normal"))
   
screen.listen()
# mapeando as teclas modo 2 Players
if (num_players == 2):
    screen.onkeypress(paddle_1_up, "w")
    screen.onkeypress(paddle_1_down, "s")
    screen.onkeypress(paddle_2_up, "Up")
    screen.onkeypress(paddle_2_down, "Down")

if (num_players == 1):
    screen.onkeypress(paddle_1_up, "w")
    screen.onkeypress(paddle_1_down, "s")

while playing:
    # Colisão da raquete 1
    collision_1(paddle_1, ball)

    # Colisão da raquete 2
    collision_2(paddle_2, ball)

    hud.clear()
    hud.write("{} : {}".format(left_player_score, right_player_score), align="center", font=("Press Start 2P",24,"normal"))

    # movimentacao da bola
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # movimentacao da raquete 2 em 1 Player
    if (num_players == 1):
        y = ball.ycor()
        if y > 240:
            y = 240
        elif y < -240:
            y = -240
        paddle_2.sety(y)

    # colisao com parede superior
    collider_walls(ball, north_wall)
    
    # colisao com parede inferior
    collider_walls(ball, south_wall)

    # colisao com parede esquerda
    if ball.xcor() < left_wall.xcor():
        right_player_score += 1
        update_score()
        ball.dx = 1
        ball.dy = 1
    
    # colisao com parede direita
    if ball.xcor() > right_wall.xcor():
        left_player_score += 1
        update_score()

    # testa se um dos jogadores já conseguiu atingir 5 pontos
    if left_player_score == 5 or right_player_score == 5:
        winner = "Player 1" if left_player_score == 5 else "Player 2"
        winner_hud = create_hud()
        winner_hud.goto(0, 0)
        winner_hud.write("{} is the winner! Press ENTER to restart".format(winner), align="center", font=("Press Start 2P",24,"normal"))

    screen.update()
