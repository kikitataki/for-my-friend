import pygame
import sys 
import math 

pygame.init() #pygameを初期化し実行するために必要

gamenn = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
gamenn_w, gamenn_h = gamenn.get_size()  
font = pygame.font.SysFont("msgothic", 80) #この80は文字の大きさ
scene = "movie"
titletmp = font.render("Hosaka my friends", False, (255, 255, 255)) #falseでギザギザ
font_movie = pygame.font.SysFont("arial", 40)
movie_y = gamenn_h


#円周率の演出はchatGPTにお願いしました.ご了承ください。
font_movie = pygame.font.SysFont("arial", 200, bold=True) # 太字に
font_push = pygame.font.SysFont("msgothic", 60) # PUSH ENTERも少し大きく
PI_100 = "π = 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
PI_LINES = [PI_100[i:i+10] for i in range(0, len(PI_100), 10)]
movie_y = gamenn_h
scene = "movie"

#titleに関する変数
titlealpha = 0
titlemove = 0
jam = 0

#フェードアウト用の黒いSurfaceを作成
fade_surface = pygame.Surface((gamenn_w, gamenn_h))
fade_surface.fill((0, 0, 0)) # 真っ黒に塗る
fade_alpha = 0               # 最初は透明（0）
startgamen = True

# 準備：時間を測るための変数
loading_start_time = 0

try:
    bg_image = pygame.image.load("assets/game_start_bg.png").convert()
    bg_image = pygame.transform.scale(bg_image, (gamenn_w, gamenn_h))
    print("無問題")
except:
    print("画像が見つかりません: assets/game_start_bg.png")
    # 代わりの真っ暗なSurfaceを作成（エラー落ち防止）
    bg_image = pygame.Surface((gamenn_w, gamenn_h))

# 背景用の透明度
bg_alpha = 0

# ---------------------------------------------------------
# 画面を制圧する movie 関数
# ---------------------------------------------------------
def movie(y_pos):
    line_height = 250    # 行の間隔
    letter_spacing = 60  # ★ここが重要！文字と文字の間の隙間

    for i, line in enumerate(PI_LINES):
        # 行全体の幅を計算（中央揃えにするため）
        # (1文字の幅 + 余白) × 文字数 でおおよその横幅を出す
        total_line_width = len(line) * (120 + letter_spacing) 
        start_x = gamenn_w // 2 - total_line_width // 2

        # 1文字ずつループして描画
        for j, char in enumerate(line):
            # 1文字だけレンダー
            char_surface = font_movie.render(char, True, (255, 255, 0))
            
            # X座標 = 開始位置 + (何文字目か * (文字幅 + 余白))
            char_x = start_x + (j * (120 + letter_spacing))
            # Y座標 = 基準位置 + (何行目か * 行間)
            char_y = y_pos + (i * line_height)
            
            gamenn.blit(char_surface, (char_x, char_y))


def loading():
    gamenn.fill((0, 0, 0)) # 画面を黒でクリア
    
    ticks = pygame.time.get_ticks()
    center_x, center_y = gamenn_w // 2, gamenn_h // 2
    radius = 60    # 円の半径
    dot_radius = 8 # ドットの大きさ
    
    # 8個のドットを描画
    for i in range(8):
        # 各ドットの角度を計算 (45度ずつずらす)
        angle = math.radians(i * 45 + ticks * 0.5) # 0.5は回転速度
        
        # 三角関数で座標を計算 (x = cos, y = sin)
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius
        
        # 透明度（色の濃さ）を位置によって変えるときれいです
        color_val = 255 - (i * 25) 
        pygame.draw.circle(gamenn, (color_val, color_val, color_val), (int(x), int(y)), dot_radius)

    # 「NOW LOADING」のテキスト
    load_text = font_push.render("NOW LOADING...", True, (255, 255, 255))
    tw, th = load_text.get_size()
    gamenn.blit(load_text, (center_x - tw // 2, center_y + radius + 40))

def startgamen(alpha):
    global titlemove
    
    gamenn.fill((0, 0, 0))
    if alpha < 255:
        alpha += 5
        titletmp.set_alpha(alpha)
        gamenn.blit(titletmp, (gamenn_w // 2 - titletmp.get_width() // 2, gamenn_h // 2 - titletmp.get_height() // 2)) #タイトルを画面の中心に表示
    else:
        if titlemove + gamenn_h // 2 > gamenn_h // 4: 
            titlemove -= 1
        else :
                # PUSH ENTERの点滅描画（ここは前と同じ）
            ticks = pygame.time.get_ticks()
            if (ticks // 500) % 2 == 0:
                push_text = font_push.render("PUSH ENTER", True, (255, 255, 255))
                p_w, p_h = push_text.get_size()
                gamenn.blit(push_text, (gamenn_w // 2 - p_w // 2, gamenn_h - 120))
                    
        titletmp.set_alpha(alpha)
        gamenn.blit(titletmp, (gamenn_w // 2 - titletmp.get_width() // 2, gamenn_h // 2 - titletmp.get_height() // 2 + titlemove)) #タイトルを画面の中心に表示

def start():
    print("start")
    global bg_alpha
    if bg_alpha < 255:
        bg_alpha += 2  
        if bg_alpha > 255: bg_alpha = 255

    bg_image.set_alpha(bg_alpha)
    gamenn.blit(bg_image, (0, 0))
    print("tmp")
    
def fade_out():
    global fade_alpha
    
    if fade_alpha < 255:
        fade_alpha += 1 # ここの数字を小さくすると、よりゆっくり暗くなります
        if fade_alpha > 255: fade_alpha = 255
        
    fade_surface.set_alpha(fade_alpha)
    # 全ての描画が終わった一番最後に blit するのがコツ！
    gamenn.blit(fade_surface, (0, 0))
    
    # 完全に真っ黒になったか判定を返すと便利（C++のbool値のようなイメージ）
    return fade_alpha >= 255



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if scene == "title":
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_RETURN:
                    gamenn.fill((0, 0, 0))
                    scene = "out"
        if scene == "movie":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    scene = "title"
                    continue
        
    gamenn.fill((0, 0, 0))
    
    
    match scene: #やってることはswitch文とおなじ
        case "title":
            titlealpha += 1
            startgamen(titlealpha)

        case "movie":
            movie_y -= 2 
            movie(movie_y)
            if movie_y < -2650:
                scene = "title"
                
        case "game1":
            start()
        
        case "out":
            if startgamen :
                startgamen(255)  
            is_done = fade_out()
            if is_done :
                if startgamen :
                    scene = "loading"
                    startgamen = False
        
        case "loading":
            loading()
            if pygame.time.get_ticks() - loading_start_time > 8000:
                scene = "game1"
                # 次のためにフェード変数をリセットしておくと便利
                fade_alpha = 255 # 次は明るくしたい(fade_in)ので255からスタート
            
    #画面を更新
    pygame.display.flip()