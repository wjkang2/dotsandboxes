# ageelanwar's dots-and-boxes code with CMSC421 group 3's Alpha-Beta search applied

# Dots-and-Boxes code details:
# Author: aqeelanwar
# Created: 13 March,2020, 9:19 PM
# Email: aqeel.anwar@gatech.edu

from tkinter import *
import numpy as np

number_of_dots = 4
size_of_board = number_of_dots * 100
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
dot_color = '#7BC043'
player1_color = '#0492CF'
player1_color_light = '#67B0CF'
player2_color = '#EE4035'
player2_color_light = '#EE7E77'
Green_color = '#7BC043'
dot_width = 0.25*size_of_board/number_of_dots
edge_width = 0.1*size_of_board/number_of_dots
distance_between_dots = size_of_board / (number_of_dots)

class Dots_and_Boxes():
    # ------------------------------------------------------------------
    # Initialization functions
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('Dots_and_Boxes')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        self.player1_boxes = 0
        self.player2_boxes = 0
        self.refresh_board()
        self.play_again()

    def play_again(self):
        self.refresh_board()
        self.player1_boxes = 0
        self.player2_boxes = 0
        self.board_status = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))
        self.last_played = np.ones(shape=(number_of_dots - 1, number_of_dots - 1), dtype=bool)
        self.row_status = np.zeros(shape=(number_of_dots, number_of_dots - 1))
        self.col_status = np.zeros(shape=(number_of_dots - 1, number_of_dots))
        
        # Input from user in form of clicks
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.display_turn_text()

    def mainloop(self):
        self.window.mainloop()

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def is_grid_occupied(self, logical_position, type):
        r = logical_position[0]
        c = logical_position[1]
        occupied = True

        if type == 'row' and self.row_status[c][r] == 0:
            occupied = False
        if type == 'col' and self.col_status[c][r] == 0:
            occupied = False

        return occupied

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        position = (grid_position-distance_between_dots/4)//(distance_between_dots/2)

        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0]-1)//2)
            c = int(position[1]//2)
            logical_position = [r, c]
            type = 'row'
            # self.row_status[c][r]=1
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'

        return logical_position, type

    def mark_box(self):
        boxes = np.argwhere(self.board_status == 4)
        changed = False
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) !=[]:
                self.already_marked_boxes.append(list(box))
                # print("Box 1: " + str(box[0]) + "; Box 2: " + str(box[1]) + "; Val: " + str(self.last_played[box[0]][box[1]]))
                if self.last_played[box[0]][box[1]] == True:
                    self.player1_boxes += 1
                    color = player1_color_light
                else:
                    self.player2_boxes += 1
                    color = player2_color_light
                self.shade_box(box, color)
                changed = True
        if changed:
            self.player1_turn = not self.player1_turn
    
    # above function except without shading
    # also with a name that works with untemp_box
    # basically just appends boxes not already marked
    def temp_box(self):
        boxes = np.argwhere(self.board_status == 4)
        changed = False
        count = 0
        # box is a coordinate in a list: ex. [x,y]
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) !=[]:
                count += 1
                self.already_marked_boxes.append(list(box))
                # print("Box 1: " + str(box[0]) + "; Box 2: " + str(box[1]) + "; Val: " + str(self.last_played[box[0]][box[1]]))
                if self.last_played[box[0]][box[1]] == True:
                    self.player1_boxes += 1
                else:
                    self.player2_boxes += 1
                changed = True
        if changed:
            self.player1_turn = not self.player1_turn
        return count
    
    # (kinda) opposite of above function
    # only difference is it only pops one box instead of all of the marked ones
    def untemp_box(self):
        box = self.already_marked_boxes.pop()
        # print(box)
        if self.last_played[box[0]][box[1]] == True:
            self.player1_boxes -= 1
        else:
            self.player2_boxes -= 1
        # print(self.already_marked_boxes)
        if self.last_played[self.already_marked_boxes[-1][0]][self.already_marked_boxes[-1][1]] != self.last_played[box[0]][box[1]]:
            self.player1_turn = not self.player1_turn

    def update_board(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]

        # print("r-value: " + str(r) + "; c-value: " + str(c) + "; type: " + type)
        

        if c < (number_of_dots-1) and r < (number_of_dots-1):
            self.board_status[c][r] += 1
            

        if type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c-1][r] += 1
                self.last_played[c-1][r] = self.player1_turn
                # mark box to bottom if not on border
                if c < (number_of_dots-1):
                    self.last_played[c][r] = self.player1_turn
            # logic if top-most row marker
            else:
                self.last_played[c][r] = self.player1_turn

        elif type == 'col':
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r-1] += 1
                self.last_played[c][r-1] = self.player1_turn
                # mark box to right if not on border
                if r < (number_of_dots-1):
                    self.last_played[c][r] = self.player1_turn
            # logic if left-most column marker
            else:
                self.last_played[c][r] = self.player1_turn
        # print(self.player1_turn)

    def unupdate_board(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]

        # print("r-value: " + str(r) + "; c-value: " + str(c) + "; type: " + type)
        

        if c < (number_of_dots-1) and r < (number_of_dots-1):
            self.board_status[c][r] -= 1
            

        if type == 'row':
            self.row_status[c][r] = 0
            if c >= 1:
                self.board_status[c-1][r] -= 1
                self.last_played[c-1][r] = self.player1_turn
                # unmark box to bottom if not on border
                if c < (number_of_dots-1):
                    self.last_played[c][r] = self.player1_turn
            # logic if top-most row marker
            else:
                self.last_played[c][r] = self.player1_turn

        elif type == 'col':
            self.col_status[c][r] = 0
            if r >= 1:
                self.board_status[c][r-1] -= 1
                self.last_played[c][r-1] = self.player1_turn
                # unmark box to right if not on border
                if r < (number_of_dots-1):
                    self.last_played[c][r] = self.player1_turn
            # logic if left-most column marker
            else:
                self.last_played[c][r] = self.player1_turn
        # print(self.player1_turn)

    def is_gameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    # Problem: works for -1
    def make_edge(self, type, logical_position):
        if type == 'row':
            start_x = distance_between_dots/2 + logical_position[0]*distance_between_dots
            end_x = start_x+distance_between_dots
            start_y = distance_between_dots/2 + logical_position[1]*distance_between_dots
            end_y = start_y
        elif type == 'col':
            start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_y = start_y + distance_between_dots
            start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_x = start_x

        if self.player1_turn:
            color = player1_color
        else:
            color = player2_color
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=edge_width)

    def display_gameover(self):
        player1_score = self.player1_boxes
        player2_score = self.player2_boxes

        if player1_score > player2_score:
            # Player 1 wins
            text = 'Winner: Player 1 '
            color = player1_color
        elif player2_score > player1_score:
            text = 'Winner: Player 2 '
            color = player2_color
        else:
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'Player 1 : ' + str(player1_score) + '\n'
        score_text += 'Player 2 : ' + str(player2_score) + '\n'
        # score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    def refresh_board(self):
        for i in range(number_of_dots):
            x = i*distance_between_dots+distance_between_dots/2
            self.canvas.create_line(x, distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2,
                                    fill='gray', dash = (2, 2))
            self.canvas.create_line(distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(number_of_dots):
            for j in range(number_of_dots):
                start_x = i*distance_between_dots+distance_between_dots/2
                end_x = j*distance_between_dots+distance_between_dots/2
                self.canvas.create_oval(start_x-dot_width/2, end_x-dot_width/2, start_x+dot_width/2,
                                        end_x+dot_width/2, fill=dot_color,
                                        outline=dot_color)

    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = player1_color
        else:
            text += 'Player2'
            color = player2_color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board - 5*len(text),
                                                       size_of_board-distance_between_dots/8,
                                                       font="cmr 15 bold", text=text, fill=color)


    def shade_box(self, box, color):
        start_x = distance_between_dots / 2 + box[1] * distance_between_dots + edge_width/2
        start_y = distance_between_dots / 2 + box[0] * distance_between_dots + edge_width/2
        end_x = start_x + distance_between_dots - edge_width
        end_y = start_y + distance_between_dots - edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = player1_color
        else:
            text += 'Player2'
            color = player2_color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board - 5*len(text),
                                                       size_of_board-distance_between_dots/8,
                                                       font="cmr 15 bold",text=text, fill=color)

    def click(self, event):
        if not self.reset_board and self.player1_turn:
            print("if")
            grid_position = [event.x, event.y]
            logical_position, valid_input = self.convert_grid_to_logical_position(grid_position)
            print("Type: " + valid_input + ", Coords: " + str(logical_position))
            print(not self.is_grid_occupied(logical_position, valid_input))
            if valid_input and not self.is_grid_occupied(logical_position, valid_input):
                self.update_board(valid_input, logical_position)
                self.make_edge(valid_input, logical_position)
                self.mark_box()
                self.refresh_board()
                self.player1_turn = not self.player1_turn

                if self.is_gameover():
                    # self.canvas.delete("all")
                    self.display_gameover()
                else:
                    self.display_turn_text()
        elif not self.reset_board and not self.player1_turn:
            print("else")
            move = self.minmax()
            print("Type: " + move[0] + ", Coords: " + str(move[1]))
            print(not self.is_grid_occupied(move[1], move[0]))
            if move[0] != "none" and not self.is_grid_occupied(move[1], move[0]):
                print("I'm here!")
                # AI moves
                self.update_board(move[0], move[1])
                self.make_edge(move[0], move[1])
                self.mark_box()
                self.refresh_board()
                self.player1_turn = not self.player1_turn

                if self.is_gameover():
                    self.display_gameover()
                else:
                    self.display_turn_text()
        else:
            print("Goodbye")
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

    def minmax(self):
        minimum_Score = 1000
        pop = [0,0]
        # 3 is the depth, can increase
        result = self.max(3, minimum_Score)
        if minimum_Score > result[0]:
            minimum_Score = result[0]
            pop = result[2]

        return (result[1], pop)

    def max(self, depth, alpha):
        # meant to change these values to something different but forgot
        if self.is_gameover() or depth == 0:
            return (self.player1_boxes - self.player2_boxes,"none",[-1,-1])

        maximum_score = -1000

        px = 0
        py = 0
        type = "none"
        coords = [px,py]

        curr_turn = self.player1_turn

        # checks all moves for rows
        for i in range(0,len(self.row_status)-2):
            for j in range(0, len(self.row_status[0]-1)):
                # print("update i: " + str(i) + ", j: " + str(j))
                if not self.is_grid_occupied([i,j], "row"):
                    typer = 'row'
                    # moves board state forward to check other potential states
                    self.update_board(typer,[i,j])
                    num_updated = self.temp_box()

                    if curr_turn == self.player1_turn:
                        (maximum_score, type, coords) = self.max(depth - 1, alpha)
                        if type == "none":
                            type = "row"
                        if coords == [-1,-1]:
                            coords = [i, j]
                    else:
                        (m, type2, coords2) = self.min(depth - 1, maximum_score)
                        if m > maximum_score:
                            maximum_score = m
                            px = i
                            py = j
                            type = type2
                            coords = [px,py]
                    # resets board back to current state
                    # print("unupdate i: " + str(i) + ", j: " + str(j))
                    self.unupdate_board(typer,[i,j])
                    for k in range(0,num_updated-1):
                        self.untemp_box()
        
        # checks all moves for columns
        for i in range(0,len(self.col_status)-1):
            for j in range(0, len(self.col_status[0])-2):
                if not self.is_grid_occupied([i,j], "col"):
                    typec = 'col'
                    # moves board state forward to check other potential states
                    self.update_board(typec,[i,j])
                    num_updated = self.temp_box()

                    if curr_turn == self.player1_turn:
                        (maximum_score, type, coords) = self.max(depth - 1, alpha)
                        if type == "none":
                            type = "col"
                        if coords == [-1,-1]:
                            coords = [i, j]
                    else:
                        (m, type2, coords2) = self.min(depth - 1, maximum_score)
                        if m > maximum_score:
                            maximum_score = m
                            px = i
                            py = j
                            type = type2
                            coords = [px,py]
                    # resets board back to current state
                    self.unupdate_board(typec,[i,j])
                    for k in range(0,num_updated-1):
                        self.untemp_box()

        return (maximum_score, type, coords)

    def min(self, depth, beta):
        # also meant to change these values to something different but forgot
        if self.is_gameover() or depth == 0:
            return (self.player1_boxes - self.player2_boxes,"none",[0,0])
        minimum_score = 1000

        px = 0
        py = 0
        type = "none"
        coords = [px,py]

        curr_turn = self.player1_turn

        # finds min for rows
        for i in range(0,len(self.row_status)-2):
            for j in range(0, len(self.row_status[0])-1):
                if not self.is_grid_occupied([i,j], "row"):
                    typer = 'row'
                    # moves board state forward to check other potential states
                    self.update_board(type,[i,j])
                    num_updated = self.temp_box()

                    if curr_turn == self.player1_turn:
                        (minimum_score, typer, coords) = self.min(depth - 1, beta)
                        if type == "none":
                            type = "row"
                        if coords == [-1,-1]:
                            coords = [i, j]
                    else:
                        (m, type2, coords2) = self.max(depth - 1, minimum_score)
                        if m > minimum_score:
                            minimum_score = m
                            px = i
                            py = j
                            type = type2
                            coords = [px,py]
                    # resets board back to current state
                    self.unupdate_board(typer,[i,j])
                    for k in range(0,num_updated-1):
                        self.untemp_box()
        
        # finds max for columns
        for i in range(0,len(self.col_status)-1):
            for j in range(0, len(self.col_status[0])-2):
                if not self.is_grid_occupied([i,j], "col"):
                    typec = 'col'
                    # moves board state forward to check other potential states
                    self.update_board(typec,[i,j])
                    num_updated = self.temp_box()

                    if curr_turn == self.player1_turn:
                        (minimum_score, type, coords) = self.min(depth - 1, beta)
                        if type == "none":
                            type = "col"
                        if coords == [-1,-1]:
                            coords = [i, j]
                    else:
                        (m, type2, coords2) = self.max(depth - 1, minimum_score)
                        if m < minimum_score:
                            minimum_score = m
                            px = i
                            py = j
                            type = type2
                            coords = [px,py]
                    # resets board back to current state
                    self.unupdate_board(typec,[i,j])
                    for k in range(0,num_updated-1):
                        self.untemp_box()

        return (minimum_score, type, coords)



game_instance = Dots_and_Boxes()
game_instance.mainloop()

