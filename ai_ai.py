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

AI1 = 0
AI2 = 1

EMPTY = 0
AI_PAWN1 = 1
AI_PAWN2 = 2


print("Select heuristic type for first AI Player: \n1.Heuristic 1\n2.Heuristic 2\n3.Heuristic 3")
heuristic_type1 = input()

print("Select heuristic type for second AI Player: \n1.Heuristic 1\n2.Heuristic 2\n3.Heuristic 3")
heuristic_type2 = input()

#res_list = [i for i in range(len(test_list)) if test_list[i] == 3] 
def calculate_score(board, piece, row, column, heuristic_type):
	score=0
	
	if(heuristic_type == '1'):
		score += check_2_3_combination(board, piece, row, column)
		
	elif(heuristic_type == '2'):
		score += get_potencial_foursome(board, piece, row, column, 0)  #for ai 
		score += get_potencial_foursome(board, (piece+1)%2, row, column, 1)/2  #for person   
		
	elif(heuristic_type == '3'):

		score += check_2_3_combination(board, piece, row, column)
		score += get_potencial_foursome(board, piece, row, column,0)  #for ai 
		#tam olarak piyonu koyduğumuz yerde bizim 4lü yapma şansımız var mı?? 
		#Eğer varsa şuan potansiyel 4lünü kaçıncısını koyduk?
		
		score += get_potencial_foursome(board, (piece+1)%2, row, column,1)/2  #for person   
		#şu an koyduğumuz piyon, karşı tarafın 4 lü olma potasniyeli olan bir şeyi engelledi mi? engelldiyse kaçlısını engelledi? (yani hali hazırda kaç tane combinasyonu vardı)
	
	#print(board)
	#print("row: ", row , "column: " , column)
	#print("piece" , piece)
	#print("score: " , score)
	
	return score
	

def minimax(board, depth, alpha, beta, maximize, row, column,heuristic_type, turn):
    valid_locations = get_valid_locations(board)
    

    if turn == 0:
            if check_win(board, 1):
                return (None, 100000000000000, None)
            elif check_win(board, 2):
                return (None, -10000000000000,None)
            elif len(valid_locations) == 0: # Game is over, no more valid moves
                return (None, 0,None)
                
            if depth == 0 :
                return (None, calculate_score(board, 1, row, column,heuristic_type), None)
    else :
            if check_win(board, 2):
                return (None, 100000000000000, None)
            elif check_win(board, 1):
                return (None, -10000000000000,None)
            elif len(valid_locations) == 0: # Game is over, no more valid moves
                return (None, 0,None)
            if depth == 0 :
                return (None, calculate_score(board, 2, row, column, heuristic_type), None)
    
   
    
    if maximize:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations: 
            row = get_available_row(board, col)
            b_copy = board.copy()
            b_copy[row][col] = turn+1  #move piece to specified location, pieces are 1 and 2
            
            new_score = minimax(b_copy, depth-1, alpha, beta, False, row, col,heuristic_type, turn)[1]
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
            b_copy[row][col] = ((turn+1)%2)+1  #move piece to specified location
            
            new_score = minimax(b_copy, depth-1, alpha, beta, True, row, col,heuristic_type, (turn+1)%2 )[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
               break
        row = get_available_row(board, column)
        return column, value,row



def draw_board(board):
    for c in range(column_num):
        for r in range(row_num):
            pygame.draw.rect(display, GRAY, (c*100, r*100+100, 100, 100))
            pygame.draw.circle(display, WHITE, (int(c*100+50), int(r*100+150)), 45)
    
    for c in range(column_num):
        for r in range(row_num):        
            if board[r][c] == AI_PAWN2:
                pygame.draw.circle(display, ORANGE, (int(c*100+50), 700-int(r*100+50)), 45)
            elif board[r][c] == AI_PAWN1: 
                pygame.draw.circle(display, GREEN, (int(c*100+50), 700-int(r*100+50)), 45)
    pygame.display.update()







board = np.zeros((row_num, column_num))
print_board(board)

pygame.init()
pygame.display.set_caption('Connect-Four Game')
display = pygame.display.set_mode((700, 700))
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)
draw_board(board)

game_continue = True
turn = random.randint(AI1, AI2)

while game_continue:

    #it's AI 1 turn
    if turn == 0:                

            col, minimax_score ,row = minimax(board, 5, -math.inf, math.inf, True, 0, 0,heuristic_type1, turn)

            board[row][col] = AI_PAWN1  #move piece to specified location
            
            if check_win(board, AI_PAWN1):
                label = myfont.render("AI 1 wins!!", 1, GREEN)
                print("Heuristic " +heuristic_type1 + " WON")
                display.blit(label, (40,10))
                game_continue = False
                
            print_board(board)
            draw_board(board)

            turn = 1 #give turn to the player
            
            
    #it's AI 2 turn
    else:              

            col, minimax_score ,row = minimax(board, 5, -math.inf, math.inf, True, 0, 0,heuristic_type2,turn)

            board[row][col] = AI_PAWN2  #move piece to specified location
            
            if check_win(board, AI_PAWN2):
                label = myfont.render("AI 2 wins!!", 1, ORANGE)
                print("Heuristic " +heuristic_type2 + " WON")
                display.blit(label, (40,10))
                game_continue = False
                
            print_board(board)
            draw_board(board)

            turn = 0 #give turn to the player
                      
         
    if not game_continue :
        pygame.time.wait(3000)
        break	


