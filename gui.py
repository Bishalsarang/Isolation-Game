from tkinter import Tk, Canvas, Frame, Label, PhotoImage, NW
from random import randint

grid = [['_' for _ in range(7)] for _ in range(7)]

graphics_grid = [
    [(50,130), (130,130), (210,130), (290,130),(370,130),(450,130),(530,130) ],
[(50,210), (130,210), (210,210), (290,210),(370,210),(450,210),(530,210) ],
[(50,290), (130,290), (210,290), (290,290),(370,290),(450,290),(530,290) ],
[(50,370), (130,370), (210,370), (290,370),(370,370),(450,370),(530,370) ],
[(50,450), (130,450), (210,450), (290,450),(370,450),(450,450),(530,450) ],
[(50,530), (130,530), (210,530), (290,530),(370,530),(450,530),(530,530) ],
[(50,610), (130,610), (210,610), (290,610),(370,610),(450,610),(530,610) ]
]


directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
white_turn = True
grid[0][0] = 'W'

grid[6][6] = 'B'


BOX_WIDTH = 80
BOX_HEIGHT = 80


WHITE_BOX_PATH = "images/brown_80x80.png"
BLACK_BOX_PATH = "images/ghee_80x80.png"
WHITE_KNIGHT_PATH = "images/white_knight_80x80.png"
BLACK_KNIGHT_PATH = "images/black_knight_80x80.png"
OCCUPIED_PATH = "images/occupied_80x80.png"

def onCLick(event):
    obj = event.widget.find_closest(event.x, event.y)

    # print(canvas.coords(obj))

def find_piece_position(piece_name):
    for i in range(7):
        for j in range(7):
            if grid[i][j] == piece_name:
                return i, j

def clicked(event):
    global white_turn
    obj = event.widget.find_closest(event.x, event.y)
    x, y = canvas.coords(obj)

    y += BOX_HEIGHT
    row, col = graphics_coords_to_index(x, y)

    if white_turn:
        white_x, white_y = find_piece_position('W')
        print(white_x, white_y)
        for offset_x, offset_y in directions:
            next_white_x, next_white_y = white_x + offset_x, white_y + offset_y

            if is_valid(next_white_x, next_white_y) and grid[next_white_x][next_white_y] != 'X' and row == next_white_x and col == next_white_y:
                grid[white_x][white_y] = 'X'
                grid[next_white_x][next_white_y] = 'W'

                white_turn = not white_turn
                break
        root.after(300, draw_board)
    else:
        black_x, black_y = find_piece_position('B')
        for offset_x, offset_y in directions:
            next_black_x, next_black_y = black_x + offset_x, black_y + offset_y

            if is_valid(next_black_x, next_black_y) and grid[next_black_x][next_black_y] != 'X' and row == next_black_x and col == next_black_y:
                grid[black_x][black_y] = 'X'
                grid[next_black_x][next_black_y] = 'B'
                white_turn = not white_turn
                break
        root.after(300, draw_board)



def is_valid(row, col):
    return row >= 0 and col >= 0 and row < 7 and col < 7

def graphics_coords_to_index(x, y):
    for i in range(7):
        for j in range(7):
            if graphics_grid[i][j] == (x, y):
                return i, j


print(graphics_coords_to_index(130, 370))

def draw_board():
    x, y = 50, 50
    coords = set()
    for i in range(7):
        for j in range(7):

            x1, y1 = graphics_grid[i][j]
            # x1 -= BOX_WIDTH
            y1 -= BOX_HEIGHT

            obj = None
            if (i + j) % 2 == 0:
                obj = canvas.create_image(x1, y1, image=black_box, anchor=NW, tag="black_box")
            else:
                obj = canvas.create_image(x1, y1, image=white_box, anchor=NW, tag="white_box")
                #Black
            if grid[i][j] == '_':
                pass
            elif grid[i][j] == 'W':
                obj = canvas.create_image(x1, y1, image=white_knight, anchor=NW)
            elif grid[i][j] == 'B':
                obj = canvas.create_image(x1, y1, image=black_knight, anchor=NW)
            else:
                obj = canvas.create_image(x1, y1, image=occupied, anchor=NW)

            canvas.tag_bind(obj, '<Button-1>', clicked)
            bottom_corner_coordinates = (x + i * BOX_WIDTH, y + j * BOX_HEIGHT)
            top_corner_coordinates = (x + (i + 1) * BOX_WIDTH, y + (j + 1) * BOX_HEIGHT)

            coords.add(bottom_corner_coordinates)
            coords.add(top_corner_coordinates)
            canvas.create_rectangle(bottom_corner_coordinates, top_corner_coordinates)

root = Tk()
root.geometry('1024x768')
root.resizable(False, False)
board_frame = Frame()
moves_frame = Frame()

board_frame.grid(row=0, column=0)
moves_frame.grid(row=0, column=3)

# Board Canvas
canvas = Canvas(board_frame, width=720, height=700)
canvas.bind('<Button-1>', onCLick)


# Labels
lb = Label(moves_frame, text="Details")
lb.grid(row=0, column=0)

white_box = PhotoImage(file=WHITE_BOX_PATH)
black_box = PhotoImage(file=BLACK_BOX_PATH)
white_knight = PhotoImage(file=WHITE_KNIGHT_PATH)
black_knight = PhotoImage(file=BLACK_KNIGHT_PATH)
occupied = PhotoImage(file=OCCUPIED_PATH)
draw_board()

# canvas.create_image(400, 128, image=black_box, anchor=NW)
canvas.pack()
root.mainloop()