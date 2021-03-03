import numpy as np
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
	
	
def draw_board(board):

	square_size = 100
	
	for c in range(column_num):
		for r in range(row_num):
			pygame.draw.rect(display, GRAY, (c*square_size, r*square_size+square_size, square_size, square_size))
			pygame.draw.circle(display, WHITE, (int(c*square_size+square_size/2), int(r*square_size+square_size+square_size/2)), 45)
	
	for c in range(column_num):
		for r in range(row_num):		
			if board[r][c] == 1:
				pygame.draw.circle(display, ORANGE, (int(c*square_size+square_size/2), 700-int(r*square_size+square_size/2)), 45)
			elif board[r][c] == 2: 
				pygame.draw.circle(display, GREEN, (int(c*square_size+square_size/2), 700-int(r*square_size+square_size/2)), 45)
	pygame.display.update()
	
	


board = np.zeros((row_num,column_num))
print_board(board)

pygame.init()
pygame.display.set_caption('Connect-Four Game')
display = pygame.display.set_mode((700, 700))
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)
draw_board(board)

game_continue = True
turn = 0

while game_continue:

	for action in pygame.event.get():
		if action.type == pygame.QUIT:
			sys.exit()

		if action.type == pygame.MOUSEMOTION:
			pygame.draw.rect(display, GRAY, (0,0, 700, 100))
			posx = action.pos[0]
			if turn == 0:
				pygame.draw.circle(display, ORANGE, (posx, int(50)), 45)
			else: 
				pygame.draw.circle(display, GREEN, (posx, int(50)), 45)
		pygame.display.update()

		if action.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(display, GRAY, (0,0, 700, 100))
			#print(action.pos)
			# Ask for Player 1 Input
			if turn == 0:

				col = int(math.floor(action.pos[0]/100))

				if  column_is_available(col): #if column is available
				
					row = get_available_row(board, col)
					board[row][col] = 1


					if check_win(board, 1):
						label = myfont.render("Player 1 wins!!", 1, ORANGE)
						display.blit(label, (40,10))
						game_continue = False
						
				turn = 1


			# # Ask for Player 2 Input
			else:				
			
				col = int(math.floor(action.pos[0]/100))

				if  column_is_available(col): #if column is available
				
					row = get_available_row(board, col)
					board[row][col] = 2

					if check_win(board, 2):
						label = myfont.render("Player 2 wins!!", 1, GREEN)
						display.blit(label, (40,10))
						game_continue = False

				turn = 0
				
			print_board(board)
			draw_board(board)


			if not game_continue:
				pygame.time.wait(3000)
