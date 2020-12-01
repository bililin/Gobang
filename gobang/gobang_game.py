import pygame
import sys
from pygame.locals import *

# Error code
positon_placed = -4
range_error = -3
status_error = -2
game_error = -1

# status code
G_Ongoing = 0
G_DRAW = 1
G_WIN = 2


class game:
    '''
    Class that describe the basic logic of this game
    **Parameters**
        board_size: *int*
            The number of lines of a board in horizontal or vertical direction
    '''

    def __init__(self, board_size=15):

        # The board size of gobang game is 15*15
        self.board_size = board_size

        # creat a 2D list to represent the game
        self.board = [[0 for x in range(board_size)]
                      for y in range(board_size)]
        # creat a list to record every move
        self.history = []

        self.status = 0
        self.winner = 0

    def __repr__(self):
        '''
        The debugger's representation of the object.
        '''
        s1 = 'status is :' + str(self.status)
        s2 = 'winner is :' + str(self.winner)
        s3 = 'Last move is :' + str(self.history)
        return '\n'.join([s1, s2, s3])

    def start_move(self):
        '''
        To set the status of the beginning
        '''
        self.status = 'Black'

    def get_last_step(self):
        '''
        To achieve the undo function, we need to know the last step
        '''
        return self.history[-1]

    def winner(self):
        '''
        To show who is the winner
        '''
        return self.winner

    def number_of_steps(self):
        '''
        To show the number of steps now
        '''
        return len(self.history)

    def check_winner(self):
        '''
        To win a gobang game, we need five pieces in a line.
        '''

        # Check how many pieces are already in a line
        # We only need to check four directions at the position of last move

        pieces_number = 0
        last_step = self.history[-1]

        # Check the horizontal line
        for x in range(self.board_size):
            if x > 0 and self.board[x][last_step[2]] !=\
                    self.board[x - 1][last_step[2]]:
                pieces_number = 0
            else:
                pieces_number += self.board[x][last_step[2]]
            # print(abs(pieces_number))
            if abs(pieces_number) == 4:
                # print('1')
                return last_step[0]

        # Check the vertical line
        pieces_number = 0
        for y in range(self.board_size):
            if y > 0 and self.board[last_step[1]][y] !=\
                    self.board[last_step[1]][y - 1]:
                pieces_number = 0
            else:
                pieces_number += self.board[last_step[1]][y]
            if abs(pieces_number) == 4:
                # print('2')
                return last_step[0]

        # Check the line from top left to bottom right
        pieces_number = 0
        min_value = min(last_step[1], last_step[2])
        top_point = [last_step[1] - min_value, last_step[2] - min_value]
        for x in range(self.board_size):

            # when out of board, stop
            if top_point[0] + x > self.board_size - 1\
                    or top_point[1] + x > self.board_size - 1:
                break

            if x > 0 and self.board[top_point[0] + x][top_point[1] + x] \
                    != self.board[top_point[0] + x - 1][top_point[1] + x - 1]:
                pieces_number = 0
            else:
                pieces_number += self.board[top_point[0] + x][top_point[1] + x]
            if abs(pieces_number) == 4:
                # print('3')
                return last_step[0]

        # Check the line from top right to bottom left
        pieces_number = 0
        min_value = min(self.board_size - 1 - last_step[1], last_step[2])
        top_point = [last_step[1] + min_value, last_step[2] - min_value]
        for x in range(self.board_size):
            # when out of board, stop
            if top_point[0] - x < 0 or top_point[1] + x > self.board_size - 1:
                break
            if x > 0 and self.board[top_point[0] - x][top_point[1] + x] !=\
                    self.board[top_point[0] - x + 1][top_point[1] + x - 1]:
                pieces_number = 0
            else:
                pieces_number += self.board[top_point[0] - x][top_point[1] + x]
            if abs(pieces_number) == 4:
                # print('4')
                return last_step[0]
        return G_Ongoing

    def check_status(self):
        '''
        To check the status of a game
        '''
        # print('self winner', self.check_winner())

        # when the board is full, this game is a draw
        if len(self.history) >= self.board_size ** 2:
            return G_DRAW

        if self.check_winner() != 0:
            self.winner = self.check_winner()
            return G_WIN
        return G_Ongoing

    def move(self, x, y):
        '''
        make a move and change the board list and history list
        **Parameters**
            x,y: *int*
                The coordinate of the piece that you want to put
        '''

        # exclude some errors might happen
        if self.status != 'Black' and self.status != 'White':
            return status_error
        if self.board_size <= x or x < 0 or self.board_size <= y or y < 0:
            return range_error_ERR
        if self.board[x][y] != 0:
            return positon_placed

        # according to current status, make changes
        if self.status == 'Black':
            self.board[x][y] = 1
        elif self.status == 'White':
            self.board[x][y] = -1
        self.history.append((self.board[x][y], x, y))

        if self.check_status() == G_WIN:
            self.status = 'Win'
            return G_WIN
        if self.check_status() == G_DRAW:
            self.status = 'Draw'
            return G_DRAW

        last_step = self.history[-1]
        if last_step[0] == 1:
            self.status = 'White'
        else:
            self.status = 'Black'
        return G_Ongoing

    def undo(self):
        '''
        To achieve the undo function
        '''

        # At the beginning of the game, we can not undo
        if len(self.history) == 0:
            return game_error

        step = self.history.pop()
        self.board[step[1]][step[2]] = 0

        if step[0] == 1:
            self.status = 'Black'
        elif step[0] == -1:
            self.status = 'White'
        else:
            return game_error

        return G_Ongoing


class game_window(game):
    '''
    Use the pygame package to create a window to play the game
    **Parameters**
        board_size: *int*
            The number of lines of a board in horizontal or vertical direction
        unit: *int*
            The side length of a small square in a board
    '''

    def __init__(self, board_size=15, unit=40):
        self.size = board_size
        self.unit = unit

        # The title of the window
        self.title = 'Gobang game'

        # The width of right panel
        self.panel_width = 200

        # The distance between the most marginal line and the border of board
        self.border_width = 50

        # calculate the range to place a piece
        self.range_x = [self.border_width,
                        self.border_width + (self.size - 1) * self.unit]
        self.range_y = [self.border_width,
                        self.border_width + (self.size - 1) * self.unit]

        # calculate the range of the right panel
        self.panel_x = [self.border_width + (self.size - 1) * self.unit,
                        (self.border_width + (self.size - 1) * self.unit + (
                         self.panel_width))]
        self.panel_y = [self.border_width,
                        self.border_width + (self.size - 1) * self.unit]

        # calculate the size of window
        self.window_width = self.border_width * 2 + \
            self.panel_width + (self.size - 1) * self.unit
        self.window_height = self.border_width * \
            2 + (self.size - 1) * self.unit

        # call the object from game class
        super(game_window, self).__init__(board_size=board_size)

        # Initialize the game
        self.initialize_game()

    def draw_panel(self):
        '''
        draw the right panel to display present status
        '''

        pygame.draw.rect(self.screen, (222, 151, 97),
                         [self.panel_x[0] + 30, 0,
                          1000, 1000])

        self.panel_font = pygame.font.SysFont('simhei', 20)

        # display the status
        # print('2status', self.status)
        if self.status == 0:
            stat_str = 'Enjoy your new game!'
        elif self.status == 'Black':
            stat_str = 'Waiting for black'
        elif self.status == 'White':
            stat_str = 'Waiting for white'
        elif self.status == 'Draw':
            stat_str = 'Unfortunately there was no winner'
        elif self.status == 'Win':
            winner = self.winner
            if winner == 1:
                stat_str = 'The black wins！'
            else:
                stat_str = 'The white wins！'

        self.surface_stat = self.panel_font.render(
            stat_str, False, (0, 0, 0))
        self.screen.blit(self.surface_stat, [
            self.panel_x[0] + 50, self.panel_y[0] + 50])

        # show the number of steps
        steps = self.number_of_steps()
        self.surface_steps = self.panel_font.render(
            f'Number of steps: {steps}', False, (0, 0, 0))
        self.screen.blit(self.surface_steps, [
            self.panel_x[0] + 50, self.panel_y[0] + 150])

        # make buttons for user
        # set sizes for buttons
        offset_x = self.panel_x[0] + 65
        offset_y = self.panel_y[0] + 400
        btn_h = 50
        btn_w = 150
        btn_gap = 20
        btn_text_x = 35
        btn_text_y = 15

        # new game button
        self.BTN_RANGE_NEW_START_X = [offset_x, offset_x + btn_w]
        self.BTN_RANGE_NEW_START_Y = [offset_y, offset_y + btn_h]
        pygame.draw.rect(self.screen, (0, 0, 0),
                         [offset_x, offset_y,
                          btn_w, btn_h])
        self.surface_btn = self.panel_font.render(
            f'New game', False, (255, 255, 255))
        self.screen.blit(self.surface_btn,
                         [offset_x + btn_text_x, offset_y + btn_text_y])

        # Exit button
        self.BTN_RANGE_EXIT_GAME_X = [offset_x, offset_x + btn_w]
        self.BTN_RANGE_EXIT_GAME_Y = [offset_y + btn_h + btn_gap,
                                      offset_y + btn_h + btn_gap + btn_h]
        pygame.draw.rect(self.screen, (0, 0, 0),
                         [offset_x, offset_y + btn_h + btn_gap,
                          btn_w, btn_h])
        self.surface_btn = self.panel_font.render(
            f'Exit game', False, (255, 255, 255))
        self.screen.blit(self.surface_btn,
                         [offset_x + btn_text_x,
                          offset_y + btn_h + btn_gap + btn_text_y])

        # undo button
        self.BTN_RANGE_RB_X = [offset_x, offset_x + btn_w]
        self.BTN_RANGE_RB_Y = [offset_y + (btn_h + btn_gap) * 2,
                               offset_y + (btn_h + btn_gap) * 2 + btn_h]
        pygame.draw.rect(self.screen, (0, 0, 0),
                         [offset_x, offset_y + (btn_h + btn_gap) * 2,
                          btn_w, btn_h])
        self.surface_btn = self.panel_font.render(
            f'Undo', False, (255, 255, 255))
        self.screen.blit(self.surface_btn,
                         [offset_x + btn_text_x,
                          offset_y + (btn_h + btn_gap) * 2 + btn_text_y])

    def draw_board(self):
        '''
        Use functions to draw the board which can place a piece
        '''

        # choose a font
        font = pygame.font.SysFont('arial', 16)

        # draw lines of rows
        for row in range(self.size):
            pygame.draw.line(self.screen,
                             (0, 0, 0),
                             [self.border_width,
                              self.border_width + row * self.unit],
                             [self.border_width + (self.size - 1) * self.unit,
                              self.border_width + row * self.unit], 1)
            surface = font.render(f'{row + 1}', True, (0, 0, 0))
            self.screen.blit(
                surface, [self.border_width - 30,
                          self.border_width + row * self.unit - 10])

        # draw lines of columns
        for col in range(self.size):
            pygame.draw.line(self.screen,
                             (0, 0, 0),
                             [self.border_width + col * self.unit,
                              self.border_width],
                             [self.border_width + col * self.unit,
                              self.border_width + (self.size - 1) * self.unit],
                             1)
            surface = font.render(chr(ord('A') + col), True, (0, 0, 0))
            self.screen.blit(
                surface, [self.border_width + col * self.unit - 5,
                          self.border_width - 30])

        # draw the star position
        pos = [(3, 3), (11, 3), (3, 11), (11, 11), (7, 7)]
        for i in pos:
            x = self.border_width + i[0] * self.unit
            y = self.border_width + i[1] * self.unit
            pygame.draw.circle(self.screen, (0, 0, 0),
                               [x, y], int(self.unit / 8))

    def draw_piece(self):
        '''
        use functions to draw a piece
        '''
        pieces = self.history
        for piece in pieces:
            x = self.border_width + piece[1] * self.unit
            y = self.border_width + piece[2] * self.unit
            if piece[0] == 1:
                piece_color = (0, 0, 0)
            else:
                piece_color = (255, 255, 255)
            pygame.draw.circle(self.screen, piece_color,
                               [x, y], int(self.unit / 2.5))

    def refresh(self):
        '''
        Refresh the interface
        '''
        self.screen.blit(pygame.image.load(r"bg.jpg"), (0, 0))
        self.draw_board()
        self.draw_piece()
        self.draw_panel()

    def initialize_game(self):
        '''
        Game initialization
        '''
        pygame.init()

        # set the size of window
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height))

        # set the title
        pygame.display.set_caption(self.title)

        # set background image
        self.screen.blit(pygame.image.load(r"bg.jpg"), (0, 0))

        # draw board
        self.draw_board()

        # draw panel
        self.draw_panel()

    def MOVE(self, position):
        '''
        Make a move
        **Parameters**
            position: *tuple*
                The coordinate of the position that user clicks
        '''
        # print(position)
        if position[0] < self.range_x[0] or position[0] > self.range_x[1] \
                or position[1] < self.range_y[0] \
                or position[1] > self.range_y[1]:
            return range_error

        # locate the position that user clicks on
        s_x = round((position[0] - self.border_width) / self.unit)
        s_y = round((position[1] - self.border_width) / self.unit)
        x = self.border_width + self.unit * s_x
        y = self.border_width + self.unit * s_y

        if self.move(s_x, s_y) < 0:
            return game_error

        last_move = self.get_last_step()
        if last_move[0] == 1:
            piece_color = (0, 0, 0)
        else:
            piece_color = (255, 255, 255)
        pygame.draw.circle(self.screen, piece_color, [
                           x, y], int(self.unit / 2.5))

        self.draw_panel()

    def UNDO(self):
        '''
        Undo the move after clicking the button
        '''
        if self.undo() == G_Ongoing:
            self.refresh()

    def New_game(self):
        '''
        Start a new game after clicking the button
        '''
        self.__init__()
        self.process()

    def check_button(self, position):
        '''
        Check if user click the button
        **Parameters**
            position: *tuple*
                The coordinate of the position that user clicks
        '''
        if self.BTN_RANGE_NEW_START_X[0] < position[0] < \
            self.BTN_RANGE_NEW_START_X[1] \
                and self.BTN_RANGE_NEW_START_Y[0] < position[1] < \
                self.BTN_RANGE_NEW_START_Y[1]:
            self.New_game()
            return G_Ongoing
        elif self.BTN_RANGE_EXIT_GAME_X[0] < position[0] < \
            self.BTN_RANGE_EXIT_GAME_X[1] \
                and self.BTN_RANGE_EXIT_GAME_Y[0] < position[1] < \
                self.BTN_RANGE_EXIT_GAME_Y[1]:
            sys.exit()
        elif self.BTN_RANGE_RB_X[0] < position[0] < self.BTN_RANGE_RB_X[1] \
                and self.BTN_RANGE_RB_Y[0] < position[1] < \
                self.BTN_RANGE_RB_Y[1]:
            self.UNDO()
            return G_Ongoing
        else:
            return game_error

    def process(self):
        '''
        The main process of how pygame works
        '''
        self.start_move()
        self.draw_panel()

        # pygame detect the behavior of user and then perform
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONUP:
                    if self.check_button(event.pos) < 0:
                        self.MOVE(event.pos)

            pygame.display.update()
            # print(self.__repr__())


if __name__ == '__main__':
    GAME = game_window()
    GAME.process()
