import pygame
import math

displaywidth = 600
display = pygame.display.set_mode((displaywidth, displaywidth))
pygame.display.set_caption('Path Finding Algorithm')

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot: 
    def __init__ (self, row, col, width):
        self.row  = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.parent = None

        self.g = 0
        self.h = 0
        self.f = 0

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent
        
    def get_pos(self):
        return self.row, self.col
    
    def is_barrier(self):
        return self.color == BLACK
    
    def reset(self): 
        self.color = WHITE
        
    def make_closed(self): 
        self.color = RED
    
    def make_open(self):
        self.color = BLUE
        
    def make_barrier(self):
        self.color = BLACK
    
    def make_end(self):
        self.color = TURQUOISE

    def make_start(self):
        self.color = ORANGE
    
    def make_path(self):
        self.color = GREEN
    
    def draw(self, display):
        pygame.draw.rect(display, self.color, (self.x, self.y, self.width, self.width))    
    
    def update_neighbours(self, grid):
        row = self.row
        col = self.col
        neighbours = [grid[row-1][col], grid[row+1][col], grid[row][col-1],
                      grid[row][col+1]]
        return neighbours 
    

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap)
            grid[i].append(spot)
            
    return grid

def draw_grid(display, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(display, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(display, GREY, (j*gap, 0), (j*gap, width))

def draw(display, grid, rows, width):
    display.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(display)
    draw_grid(display, rows, width)
    pygame.display.update()            
    
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x //gap
    return row, col


def astar_algorithm(start, end, grid):
    open_list = [start]
    closed_list = []
    current_spot = start
    begin_loop(open_list, closed_list, current_spot, start, end, grid)

def begin_loop(open_list, closed_list, current_spot, start, end, grid):
    endrow, endcol = end.get_pos()

    if current_spot != end:
        neighbours = current_spot.update_neighbours(grid)

        for spot in neighbours:
            if spot.is_barrier() is False:
                spotrow, spotcol = spot.get_pos()
                
                if spot in open_list:
                    if spot.g < current_spot.g + 1:
                        continue
                    else:
                        open_list.remove(spot)
                        if spot != end:
                            spot.reset()

                if spot in closed_list:
                    if spot.g < current_spot.g + 1:
                        continue
                    else:
                        closed_list.remove(spot)
                        if spot != end:
                            spot.reset()

                if spot not in open_list and spot not in closed_list:
                    spot.g = current_spot.g + 1
                    spot.h = (abs(endrow - spotrow)) + (abs(endcol - spotcol))
                    spot.f = spot.g + spot.h
                    spot.set_parent(current_spot)
                    if spot != start and spot != end:
                        spot.make_open()
                    open_list.append(spot)
                    
            else:
                continue

        f_values = []

        for each in open_list:
            f_values.append(each.f)

        index = f_values.index(min(f_values))
        current_spot = open_list[index]
        open_list.remove(current_spot)
        closed_list.append(current_spot)
        if current_spot != start and current_spot != end:
            current_spot.make_closed()
        pygame.display.flip()
    

    else:
        return construct_path(end, start)

    return begin_loop(open_list, closed_list, current_spot, start, end, grid)
            
def construct_path(end, start):       
    current = end
    path = []
    
    while current != start:
        if current != end:
            path.append(current)
        current = current.get_parent()

    for each in path:
            each.make_path()

def main(display, width):
    rows = 30
    grid = make_grid(rows, width)
    gap = width // rows
    startpt = False
    endpt = False
    clock = pygame.time.Clock()

    while True:
        draw(display, grid, rows, width)
        for event in pygame.event.get():
            if event.type == 'QUIT':
                pygame.quit()
                
            if event.type == 'START':
                continue
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, rows, width)

                if startpt is False:
                    start = grid[row][col]
                    start.make_start()
                    startpt = True

                elif endpt is False:
                    end = grid[row][col]
                    if end == start:
                        continue
                    else:
                        end.make_end()
                        endpt = True

                else:
                    barrier = grid[row][col]
                    if barrier == start or barrier == end:
                        continue
                    else:
                        barrier.make_barrier()

            if event.type == pygame.KEYDOWN:
                if event.key == 13:
                    astar_algorithm(start, end, grid)

        pygame.display.update()
        clock.tick(20)
                    

if __name__ == '__main__': main(display, displaywidth)
