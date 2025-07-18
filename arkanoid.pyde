
screenWidth = 600
screenHeight = 400


cols = 8
rows = 4
brickWidth = 60
brickHeight = 20

#parametry przycisku restartu
restart_button_x = screenWidth // 2 - 50
restart_button_y = screenHeight // 2 + 20
restart_button_w = 100
restart_button_h = 30

#flaga końca gry
game_over = False

#efekt błysku 
flash_timer = 0

#KLASY OBIEKTÓW GRY 

#KLASA PLATFORMY GRACZA
class Paddle:
    def __init__(self, width, height, y):
        self.width = width  # szerokość platformy
        self.height = height  # wysokość platformy
        self.y = y  # pozycja pionowa platformy
        self.x = 0  # pozycja pozioma platformy (ustawiana później)

    #aktualizacja pozycji platformy na podstawie ruchu myszki
    def update(self):
        self.x = constrain(mouseX - self.width / 2, 0, width - self.width)

    #rysowanie platformy
    def draw(self):
        fill(200)
        rect(self.x, self.y, self.width, self.height)

#KLASA PIŁKI
class Ball:
    def __init__(self, x, y, size, speedX, speedY):
        self.x = x  # pozycja pozioma piłki
        self.y = y  # pozycja pionowa piłki
        self.size = size  # średnica piłki
        self.speedX = speedX  # prędkość pozioma
        self.speedY = speedY  # prędkość pionowa

    #aktualizacja pozycji piłki oraz odbicia od ścian
    def update(self):
        self.x += self.speedX
        self.y += self.speedY

        if self.x <= 0 or self.x >= width:
            self.speedX *= -1  # odbicie od lewej/prawej krawędzi
        if self.y <= 0:
            self.speedY *= -1  # odbicie od górnej krawędzi

    #sysowanie piłki
    def draw(self):
        fill(255, 100, 100)
        ellipse(self.x, self.y, self.size, self.size)

    #sprawdzenie kolizji z platformą
    def check_paddle(self, paddle):
        if (self.y + self.size / 2 >= paddle.y and
            paddle.x < self.x < paddle.x + paddle.width):
            self.speedY *= -1  # odbicie piłki
            self.y = paddle.y - self.size / 2  # pozycja piłki nad platformą

    #sprawdzenie, czy piłka wypadła poza dół ekranu
    def check_bottom(self):
        return self.y > height

#KLASA CEGIEŁKI
class Brick:
    def __init__(self, x, y, row):
        self.x = x  # pozycja pozioma cegiełki
        self.y = y  # pozycja pionowa cegiełki
        self.row = row
        self.alive = True  # flaga stanu (czy cegiełka jest zniszczona)
# kolor cegiełki w zależności od wiersza
        colors = [
            color(255, 100, 100),  # czerwony
            color(255, 200, 100),  # pomarańczowy
            color(100, 200, 255),  # niebieski
            color(100, 255, 150)   # zielony
        ]
        self.color = colors[row % len(colors)]

    #rysowanie cegiełki
    def draw(self):
        if self.alive:
            fill(self.color)
            rect(self.x, self.y, brickWidth, brickHeight)

    #sprawdzenie kolizji cegiełki z piłką
    def check_collision(self, ball):
        global flash_timer, score
        if not self.alive:
            return
        if (ball.x + ball.size / 2 > self.x and ball.x - ball.size / 2 < self.x + brickWidth and
            ball.y + ball.size / 2 > self.y and ball.y - ball.size / 2 < self.y + brickHeight):
            ball.speedY *= -1
            self.alive = False  # cegiełka zostaje zniszczona
            score += 10
            flash_timer = 5  # efekt błysku na 5 klatek

#OBIEKTY GLOBALNE 
paddle = None
ball = None
bricks = []
score = 0
high_score = 0 #najlepszy wynik

#inicjalizacja gry
def setup():
    global paddle, ball, bricks, game_over, score
    size(screenWidth, screenHeight)

    paddle = Paddle(80, 15, height - 30)
    ball = Ball(width / 2, height / 2, 15, 4, -4)

    bricks = []
    for i in range(cols):
        for j in range(rows):
            brickX = i * (brickWidth + 10) + 35
            brickY = j * (brickHeight + 10) + 40
            bricks.append(Brick(brickX, brickY, j))

    game_over = False
    score = 0  # resetujemy wynik przy starcie gry
    loop()

#główna pętla rysująca
def draw():
    global game_over, high_score, flash_timer
    if flash_timer > 0:
        fill(255, 255, 255, 150)
        rect(0, 0, width, height)
        flash_timer -= 1
      
    else:
        fill(30, 30, 30, 60)  # efekt smugi za piłką
        noStroke()
        rect(0, 0, width, height)

    #rysowanie i aktualizacja platformy
    paddle.update()
    paddle.draw()

    #rysowanie i aktualizacja piłki
    ball.update()
    ball.check_paddle(paddle)
    ball.draw()

    #rysowanie i sprawdzanie kolizji z cegiełkami
    for brick in bricks:
        brick.check_collision(ball)
        brick.draw()

    # wyświetlanie wyniku    
    fill(255)
    textSize(18)
    textAlign(LEFT, TOP)
    text("Score: " + str(score), 10, 10)
    text("High Score: " + str(high_score), 90, 10)

    #warunek zwycięstwa
    all_destroyed = all(not brick.alive for brick in bricks)
    if all_destroyed and not game_over:
        game_over = True
        noLoop()
        if score > high_score:
            high_score = score  # aktualizacja high score
        textSize(32)
        textAlign(CENTER, CENTER)
        fill(255)
        text("You Win!", width / 2, height / 2)
        draw_restart_button()
        return

    #warunek porażki (piłka spadła)
    if ball.check_bottom():
        if not game_over:
            game_over = True
            noLoop()
            if score > high_score:
                high_score = score  # aktualizacja high score
        textSize(32)
        textAlign(CENTER, CENTER)
        fill(255)
        text("Game Over", width / 2, height / 2)
        draw_restart_button()

#rysowanie przycisku „Restart”
def draw_restart_button():
    fill(180)
    rect(restart_button_x, restart_button_y, restart_button_w, restart_button_h, 8)
    fill(0)
    textSize(16)
    textAlign(CENTER, CENTER)
    text("Restart", restart_button_x + restart_button_w / 2, restart_button_y + restart_button_h / 2)

#obsługa kliknięcia myszką (przycisk restartu)
def mousePressed():
    global game_over
    if game_over:
        if (restart_button_x <= mouseX <= restart_button_x + restart_button_w and
            restart_button_y <= mouseY <= restart_button_y + restart_button_h):
            setup()  # restart gry
