import numpy as np


row_num = 6
column_num = 7

AI1 = 0
AI2 = 1

EMPTY = 0
AI_PAWN1 = 1
AI_PAWN2 = 2

board = np.zeros((row_num,column_num))

def get_available_row(board, col):
	
    board= np.array(board)
    column= board[:,col]
    result=np.where(column==0)[0][0]
    return result
    
    
def column_is_available(col):
	if board[row_num-1][col] == 0:
		return True
	return False
	
	
def get_valid_locations(board):
    
    top_row= board[-1]
    valid_locations = [i for i in range(len(top_row)) if top_row[i] == 0] 
    return valid_locations



def check_adjacent(board, piece, row, column, row_action, col_action):  #yönümüze göre bizim taşımızdan ardışık kaç tane odlduğunu döndürüyor
    count = 0
    
    for i in range(4):
        
        if row < 0 or row > 5:
            return count 
            
        if  column < 0 or column > 6:
            return count
                       
        current_piece = board[row][column]
        if current_piece == piece:
            count += 1
        else :
            if i!=0:
            	continue
            	
        row += row_action
        column += col_action

                  
    return count
    

def check_adjacent_space(board, piece, row, column, delta_row, delta_col,number_of_space):  #yönümüze göre bizim taşımızdan ardışık kaç tane odlduğunu döndürüyor
    count = 0
    
    if row < 0 or row > 5:
            return count 
        
    if  column < 0 or column > 6:
            return count

                       
    for i in range(number_of_space):
        current_piece = board[row][column]
        if current_piece == 0:
            count += 1
        else:
            break
                     
        row += delta_row
        column += delta_col
        
        if row < 0 or row > 5:
            return count 
        
        if  column < 0 or column > 6 :
            return count
                   
    return count
    

def check_win(board, piece):
	# vertical
    for column in range(column_num):
        for row in range(row_num-3):
            if check_adjacent(board, piece, row, column, 1, 0) == 4:
                return True
    # horizontal
    for column in range(column_num-3):
        for row in range(row_num):
            if check_adjacent(board, piece, row, column, 0, 1) == 4:
                return True
	# positive slope diagonal
    for column in range(column_num-3):
        for row in range(row_num-3):
            if check_adjacent(board, piece, row, column, 1, 1) == 4:
                return True 
	#negative slope diagonal
    for column in range(column_num-3):
        for row in range(3, row_num):
            if check_adjacent(board, piece, row, column, -1, 1) == 4:
                return True
    return False


    
def evaluate_window(window, piece):
    score = 0
    opp_piece = AI_PAWN1
    if piece == AI_PAWN1:
        opp_piece = AI_PAWN2

    if window.count(piece) == 4:
        score += 100000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 15
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 7

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score
    
 
def check_2_3_combination(board, piece, row, column):  #checking 2 or 3 combination of all board
    score = 0

    window_size = 4
    ## Score center column
    center_array = [int(i) for i in list(board[:, column_num//2])]
    center_count = center_array.count(piece)
    score += center_count * 9
    

    ## Score Horizontal
    for r in range(row_num):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(column_num-3):
            window = row_array[c:c+window_size]
            score += evaluate_window(window, piece)


    ## Score Vertical
    for c in range(column_num):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(row_num-3):
            window = col_array[r:r+window_size]
            score += evaluate_window(window, piece)


    ## Score posiive sloped diagonal
    for r in range(row_num-3):
        for c in range(column_num-3):
            window = [board[r+i][c+i] for i in range(window_size)]
            score += evaluate_window(window, piece)


    for r in range(row_num-3):
        for c in range(column_num-3):
            window = [board[r+3-i][c+i] for i in range(window_size)]
            score += evaluate_window(window, piece)


    return score






def get_potencial_foursome(board, piece, row, col, agent):	

    score = 0


    #right
    value= check_adjacent(board, piece, row, col, 0, -1) 
    space = 0
    
    space += check_adjacent_space(board, piece, row, col-value, 0, -1, 4-value)  #value direction
    
    space += check_adjacent_space(board, piece, row, col+1 , 0, 1, 4-value) #opposite direction
    value += space
  	  	    	     
    if agent == 1 :
    	   if value == 3 :
    	   
             if space == 0:
                 score += 10000
             elif space == 1:
                 score += 3
    	     
    else: 
         if value == 4 :
         
             if space == 3:
                 score += 2
             elif space == 2:
                 score += 3
             elif space == 1:
                 score += 10
             elif space == 0:
                  score += 100000
	    	    
         else:
             if value == 2:
                 score -= 2
             elif value == 3:
                 score -= 4
	    	    
	  
	  
    #left
    value= check_adjacent(board, piece, row, col, 0, 1) 
    space = 0
  
    space+= check_adjacent_space(board, piece, row, col+value, 0, 1, 4-value)  #value direction
  	   
    space+= check_adjacent_space(board, piece, row, col-1 , 0, -1, 4-value) #opposite direction
    value += space
    
    
    if agent == 1 :
    	   if value == 3 :
    	   
             if space == 0:
                 score += 10000
             elif space == 1:
                 score += 3
    	     
    else: 
         if value == 4 :
         
             if space == 3:
                 score += 2
             elif space == 2:
                 score += 3
             elif space == 1:
                 score += 10
             elif space == 0:
                  score += 100000
	    	    
         else:
             if value == 2:
                 score -= 2
             elif value == 3:
                 score -= 4
	    
	    
	   
    #up
    value= check_adjacent(board, piece, row, col, -1, 0) 
    
    space= check_adjacent_space(board, piece, row+1, col, 1, 0, 4-value) #opposite direction
    value += space
   
   
    if agent == 1 :
    	   if value == 3 :
    	   
             if space == 0:
                 score += 10000
             elif space == 1:
                 score += 3
    	     
    else: 
         if value == 4 :
         
             if space == 3:
                 score += 2
             elif space == 2:
                 score += 3
             elif space == 1:
                 score += 10
             elif space == 0:
                  score += 100000
	    	    
         else:
             if value == 2:
                 score -= 2
             elif value == 3:
                 score -= 4
	     
	    
    #upper right
    value= check_adjacent(board, piece, row, col, -1, 1) 
    
    space= check_adjacent_space(board, piece, row-value, col+value, -1, 1, 4-value) #value direction
    space= check_adjacent_space(board, piece, row+1, col-1, 1, -1, 4-value) #opposite direction

    value += space
  	  	    
    if agent == 1 :
    	   if value == 3 :
    	   
             if space == 0:
                 score += 10000
             elif space == 1:
                 score += 3
    	     
    else: 
         if value == 4 :
             
             if space == 3:
                 score += 2
             elif space == 2:
                 score += 3
             elif space == 1:
                 score += 10
             elif space == 0:
                  score += 100000
	    	    
         else:
             if value == 2:
                 score -= 2
             elif value == 3:
                 score -= 4
	    
	   	    
	   	    	    
    #upper left
    value= check_adjacent(board, piece, row, col, -1, -1) 
    space= check_adjacent_space(board, piece, row-value, col-value, -1, -1, 4-value)#value direction
    space= check_adjacent_space(board, piece, row+1, col+1, 1, 1, 4-value)#opposite direction
    value += space	    
  	    
    if agent == 1 :
    	   if value == 3 :
    	   
             if space == 0:
                 score += 10000
             elif space == 1:
                 score += 3

    	     
    else: 
         if value == 4 :
             
             if space == 3:
                 score += 2
             elif space == 2:
                 score += 3
             elif space == 1:
                 score += 10
             elif space == 0:
                  score += 100000
	    	    
         else:
             if value == 2:
                 score -= 2
             elif value == 3:
                 score -= 4
      
    return score

        
def print_board(board):
   # print(np.flip(board, 0))
	print(board)



