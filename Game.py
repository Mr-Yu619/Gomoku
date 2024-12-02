# -*- coding: utf-8
import pygame  
import re
import logging  
import time
logging.basicConfig(level='INFO')
  
# 初始化pygame  
pygame.init()

# 定义棋盘的大小和每个格子的尺寸  
BOARD_SIZE = 17 
CELL_SIZE = 40  
  
# 定义窗口的大小  
WINDOW_SIZE = (CELL_SIZE * BOARD_SIZE, CELL_SIZE * BOARD_SIZE)  
BOARD = [[' ' for _ in range(16)] for _ in range(16)]


# 创建窗口  
screen = pygame.display.set_mode(WINDOW_SIZE)  
pygame.display.set_caption('五子棋游戏')  
  
# 定义颜色  
YELLOW = (255, 235, 189)
BLACK = (0,0,0)
RED = (255,150,0)
# 绘制棋盘的函数  
def draw_chessboard(screen):
    for x in range(1,16):
        for y in range(1,16):
            pygame.draw.rect(screen,BLACK,(x*CELL_SIZE,y*CELL_SIZE,CELL_SIZE,CELL_SIZE),1)
    pygame.draw.circle(screen,BLACK,(4*CELL_SIZE,4*CELL_SIZE),4)
    pygame.draw.circle(screen,BLACK,(4*CELL_SIZE,13*CELL_SIZE),4)
    pygame.draw.circle(screen,BLACK,(13*CELL_SIZE,4*CELL_SIZE),4)
    pygame.draw.circle(screen,BLACK,(13*CELL_SIZE,13*CELL_SIZE),4)

# 画棋子
def draw_chess(x,y,iswhite):
    color = (255,255,255) if iswhite else (0,0,0)
    pygame.draw.circle(screen,color,(x,y),15)

# 一个搜索模块，看在一个二维列表的一行是否出现过5个相同的棋子
def search(list):
    for line in list:
        if re.search('X'*5,''.join(line)):
            return 1
        elif re.search('O'*5,''.join(line)):
            return -1
    return 0

# 评估行结果
def access_row(list):
    return search(list)

# 评估列结果
def access_col(list2):
    tran_list = list(zip(*list2))
    return search(tran_list)

# 评估正对角线结果
def access_diag(list):
    tran_list = [[] for _ in range(31)]
    for x in range(16):
        for y in range(16):
            tran_list[x-y+15].append(list[x][y])
    return search(tran_list)

# 评估斜对角线结果
def access_diagr(list):
    tran_list = [[] for _ in range(31)]
    for x in range(16):
        for y in range(16):
            tran_list[x+y].append(list[x][y])
    return search(tran_list)

# 综合评估
def access(list):
    access_list = [access_row(list),access_col(list),access_diag(list),access_diagr(list)]
    logging.debug("结果："+''.join(str(access_list)))
    if 1 in access_list:
        return 1
    elif -1 in access_list:
        return -1
    else:
        return 0

# 绘制背景和棋盘
screen.fill(YELLOW)
draw_chessboard(screen)

# 开始循环检测
running = True
epoch = True
while running:
    # 这一步能保证棋盘是一直显示的
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event. type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            tmp_x = max(40,min(640,pos[0]))
            tmp_y = max(40,min(640,pos[1]))
            resultX = tmp_x//40 * 40 + (40 if tmp_x%40>20 else 0)
            resultY = tmp_y//40 * 40 + (40 if tmp_y%40>20 else 0)
            if BOARD[(resultY-40)//40][(resultX-40)//40] == ' ':
                epoch = not epoch
                draw_chess(resultX,resultY,epoch)
                logging.debug((resultX,resultY))
                logging.debug(((resultX-40)//40,(resultY-40)//40))
                BOARD[(resultY-40)//40][(resultX-40)//40] = 'X' if epoch else 'O'
                stat = access(BOARD)
                logging.debug(stat)
                if stat == 1:
                    font = pygame.font.Font(None, 74)  
                    text = font.render("White Win", True, RED)  
                    screen.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2, WINDOW_SIZE[1] // 2 - text.get_height() // 2))  
                    pygame.display.flip()  
                    time.sleep(5)  
                    BOARD = [[' ' for _ in range(16)] for _ in range(16)]  
                    screen.fill(YELLOW)  
                    draw_chessboard(screen) 
                elif stat == -1:
                    font = pygame.font.Font(None, 74)  
                    text = font.render("Black Win", True, RED)  
                    screen.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2, WINDOW_SIZE[1] // 4 - text.get_height() // 2))  
                    pygame.display.flip()  
                    time.sleep(5)  
                    BOARD = [[' ' for _ in range(16)] for _ in range(16)]  
                    screen.fill(YELLOW)  
                    draw_chessboard(screen)  

        pygame.display.flip()

pygame.quit()