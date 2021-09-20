import pygame

board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


def print_board(b):
    for i, row in enumerate(b):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j, _ in enumerate(row):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(b[i][j])
            else:
                print(f'{b[i][j]} ', end="")


def find_empty(b):
    for i, row in enumerate(b):
        for j, num in enumerate(row):
            if num == 0:
                return i, j
    return None


def is_valid(b, number, position):
    # Check row
    for i, column in enumerate(b[position[0]]):
        if column == number and position[1] != i:
            return False

    # Check column
    for i, row in enumerate(b):
        if row[position[1]] == number and position[0] != i:
            return False

    # Check box
    box_x = position[1] // 3
    box_y = position[0] // 3
    for i, row in enumerate(b[box_y * 3:box_y * 3 + 3]):
        for j, column in enumerate(row[box_x * 3:box_x * 3 + 3]):
            if column == number and (i, j) != position:
                return False

    return True


def solve(b):
    position = find_empty(b)

    if not position:
        return True
    else:
        row, col = position

    for i in range(1, 10):
        if is_valid(board, i, position):
            b[row][col] = i

            if solve(b):
                return True

            b[row][col] = 0

    return False


def draw_grid(win, height, width, padding):
    for i in range(0, 10):
        if i % 3 == 0 or i == 0 or i == 10:
            color = (0, 0, 0)
        else:
            color = (125, 125, 125)
        pygame.draw.line(win, color, ((width - padding[2]) / 9 * i + padding[0], padding[1]),
                         ((width - padding[2]) / 9 * i + padding[0], height + padding[1] - padding[3]), 1)
        pygame.draw.line(win, color, (padding[0], (height - padding[3]) / 9 * i + padding[1]),
                         (width + padding[0] - padding[2], (height - padding[3]) / 9 * i + padding[1]), 1)


def draw(win, height, width, padding, b):
    win.fill((0, 255, 255))
    draw_board(win, padding, height - padding[1], width - padding[0], b)


def draw_board(win, padding, height, width, b):
    x, y = padding[:2]
    pygame.draw.rect(win, (255, 255, 255), pygame.Rect(x, y, width - padding[2], height - padding[3]))
    draw_grid(win, height, width, padding)

    for i, rows in enumerate(b):
        for j, columns in enumerate(rows):
            if b[i][j] != 0:
                write_number(win, b[i][j], ((width / 18) + (width - padding[2]) / 9 * j + padding[0],
                                            (height / 18) + (height - padding[3]) / 9 * i + padding[1]))

    pygame.display.update()


def write_number(win, number, position):
    font = pygame.font.Font('freesansbold.ttf', 32)
    surface = font.render(str(number), True, (0, 0, 0))
    rect = surface.get_rect()
    rect.center = position
    win.blit(surface, rect)


HEIGHT = 500
WIDTH = 500

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")

run = True

while run:
    draw(window, HEIGHT, WIDTH, (20, 20, 20, 20), board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                success = solve(board)

pygame.quit()


