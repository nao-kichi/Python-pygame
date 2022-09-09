# pygameをインポート
# 最初に、pip3 installをターミナルで実行する。
# python3 main.pyで実行をかける。
# 途中で止まっているものがあれば、clearをかける。
# ゲームが面白くなるのは、超ハイスピード(83行目)でキャラ変すること！
import pygame
from pygame import mixer
import random
import math

# pygameを最初に初期化する。
pygame.init()

# スクリーンのサイズを設定する。
screen = pygame.display.set_mode((1000, 600))
# screen.fill((150, 150, 150))
# スクリーン上のタイトルを「Invaders Game」に変更する。
pygame.display.set_caption('Invaders Game')

# pygameのplayer画像をロードする。
# Player 下は座標
# Player0でその場所に留まるようにする。
playerImg = pygame.image.load('player.png')
playerX, playerY = 370, 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('enemy.png')
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_change, enemyY_change = 4, 40

# Bullet ready=球を打てる状態
bulletImg = pygame.image.load('bullet.png')
bulletX, bulletY = 0, 480
bulletX_change, bulletY_change = 0, 3
bullet_state = 'ready'

# Score
score_value = 0

# playerの表示
def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

# 球が発射されたらfire(休止)状態にする。
def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) +
                         math.pow(enemyY - bulletY, 2))
    # trueが命中 falseがミス
    if distance < 27:
        return True
    else:
        return False

# whileがないと1回で止まってしまう。
running = True
while running:
    screen.fill((0, 0, 0))

# pygameの中に、幾つかのイベントがあり、それを引っ張って来る。
    for event in pygame.event.get():
      # イベントの種類が「止める。」だったら終了する。
        if event.type == pygame.QUIT:
            running = False

    # 以下fire_bulletはコピペすること。
    # K_LEFT左を押したら1.5移動
        if event.type == pygame.KEYDOWN:
          # K_LEFT左を押したら移動
            if event.key == pygame.K_LEFT:
                playerX_change = -1.5
                # K_RIGHT左を押したら1.5移動
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.5
                # K_SPACEスペースを押したら打つ
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

# KEYUPを取得してくる。
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # Player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy 敵が440よりも下に来たらゲームを終了する。
    if enemyY > 440:
        break
    enemyX += enemyX_change
    if enemyX <= 0:  # 左端に来たらここで止まる
        enemyX_change = 4
        enemyY += enemyY_change
    elif enemyX >= 736:  # 右端に来たらここで止まる
        enemyX_change = -4
        enemyY += enemyY_change

    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = 'ready'
        score_value += 1
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)

    # Bullet Movement 球を外したら戻す
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Score
    font = pygame.font.SysFont(None, 32)  # フォントの作成　Noneはデフォルトのfreesansbold.ttf
    # テキストを描画したSurfaceの作成
    score = font.render(f"Score : {str(score_value)}", True, (255, 255, 255))
    screen.blit(score, (20, 50))

# プレイヤーと敵を出現させる。
    player(playerX, playerY)
    enemy(enemyX, enemyY)

# 画面を変えたら必ずアップデートを加える。
    pygame.display.update()
