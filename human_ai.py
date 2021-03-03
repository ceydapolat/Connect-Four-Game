import numpy as np
import random
import pygame
import sys
import math
from common_functions import * 


WHITE = '#ffffff'
GRAY  = '#514a55'
ORANGE= '#f6904d'
GREEN = '#79f289'

row_num = 6
column_num = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PAWN = 1
AI_PAWN = 2


print("Select heuristic type for AI Player: \n1.Heuristic 1\n2.Heuristic 2\n3.Heuristic 3")
heuristic_type = input()

 

def draw_board(board):
    for c in range(column_num):
        for r in range(row_num):
            pygame.draw.rect(display, GRAY, (c*100, r*100+100, 100, 100))
            pygame.draw.circle(display, WHITE, (int(c*100+50), int(r*100+150)), 45)
    
    for c in range(column_num):
        for r in range(row_num):        
            if board[r][c] == PLAYER_PAWN:
                pygame.draw.circle(display, ORANGE, (int(c*100+50), 700-int(r*100+50)), 45)
            elif board[r][c] == AI_PAWN: 
                pygame.draw.circle(display, GREEN, (int(c*100+50), 700-int(r*100+50)), 45)
    pygame.display.update()




def calculate_score(board, piece, row, column):
	score=0
	
	if heuristic_type == '1' :
		score += check_2_3_combination(board, piece, row, column)
		
	elif heuristic_type == '2' :
		score += get_potencial_foursome(board, piece, row, column, 0)  #for ai 
		score += get_potencial_foursome(board, (piece+1)%2, row, column, 1)/2  #for person   
	elif heuristic_type == '3' :

		score += check_2_3_combination(board, piece, row, column)
		score += get_potencial_foursome(board, piece, row, column,0)  #for ai 
		#tam olarak piyonu koyduğumuz yerde bizim 4lü yapma şansımız var mı?? 
		#Eğer varsa şuan potansiyel 4lünü kaçıncısını koyduk?
		
		score += get_potencial_foursome(board, (piece+1)%2, row, column, 1)/2  #for person   
		#şu an koyduğumuz piyon, karşı tarafın 4 lü olma potasniyeli olan bir şeyi engelledi mi? engelldiyse kaçlısını engelledi? (yani hali hazırda kaç tane combinasyonu vardı)
		
	#print(board)
	#print("row: ", row , "column: " , column)
	#print("piece" , piece)
	#print("score: " , score)
	
	return score


def minimax(board, depth, alpha, beta, maximizingPlayer, row, column):
    valid_locations = get_valid_locations(board)
    is_terminal = False
    
    if check_win(board, AI_PAWN1) or check_win(board, AI_PAWN2) or len(valid_locations) == 0:
        is_terminal = True
    
        
    if is_terminal:
        if is_terminal:
            if check_win(board, AI_PAWN):
                return (None, 100000000000000, None)
            elif check_win(board, PLAYER_PAWN):
                return (None, -10000000000000,None)
            else: # Game is over, no more valid moves
                return (None, 0,None)
    
    if depth == 0 :
            return (None, calculate_score(board, AI_PAWN, row, column), None)
     
    
    if maximizingPlayer:
        value = -math.inf
        column = valid_locations[0]
        for col in valid_locations: 
            row = get_available_row(board, col)
            b_copy = board.copy()
            b_copy[row][col] = AI_PAWN  #move piece to specified location
            
            new_score = minimax(b_copy, depth-1, alpha, beta, False, row, col)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
                
        row = get_available_row(board, column)
        return column, value, row
    
    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_available_row(board, col)
            b_copy = board.copy()
            b_copy[row][col] = PLAYER_PAWN  #move piece to specified location
            
            new_score = minimax(b_copy, depth-1, alpha, beta, True, row, col)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
               break
        row = get_available_row(board, column)
        return column, value,row



board = np.zeros((row_num, column_num))
print_board(board)

pygame.init()
pygame.display.set_caption('Connect-Four Game')
display = pygame.display.set_mode((700, 700))
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)
draw_board(board)

game_continue = True
turn = random.randint(PLAYER, AI)

while game_continue :

    #it's AI turn
    if turn == AI:                

            col, minimax_score ,row = minimax(board, 5, -math.inf, math.inf, True, 0, 0)
            if column_is_available(col): #if column is available
               board[row][col] = AI_PAWN  #move piece to specified location
            
               if check_win(board, AI_PAWN):
                    label = myfont.render("AI wins!!", 1, GREEN)
                    display.blit(label, (40,10))
                    game_continue = False
                
            print_board(board)
            draw_board(board)

            turn = 0 #give turn to the player
            
            
    for action in pygame.event.get():
        if action.type == pygame.QUIT:
            sys.exit()

        if action.type == pygame.MOUSEMOTION:
            pygame.draw.rect(display, WHITE, (0,0, 700, 100))
            posx = action.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(display, ORANGE, (posx, int(50)), 45)

        pygame.display.update()

        if action.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(display, WHITE, (0,0, 700, 100))

            # Ask for Player 1 Input
            if turn == PLAYER:
                col = int(math.floor(action.pos[0]/100))

                if  column_is_available(col): #if column is available
                
                    row = get_available_row(board, col)
                    board[row][col] = PLAYER_PAWN  #move piece to specified location

                    if check_win(board, PLAYER_PAWN):
                        label = myfont.render("Player 1 wins!!", 1, ORANGE)
                        display.blit(label, (40,10))
                        game_continue = False

                    turn = 1 #give turn to the AI

                    print_board(board)
                    draw_board(board)

    if not game_continue :
        pygame.time.wait(3000)
        break	


        

