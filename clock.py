import os
import sys
import random
import pygame
import pygame, sys
from button import Button
import pygame.freetype 
from pygame import mixer
import time
import pygame.freetype  # Import the freetype module.


pygame.mixer.init()

def laby():
        
    """
    A Labyrith maze is a path typically from an entrance to a goal
    This game consists a variation of the classic Labyrinth.
    Labyrinth maze starts the game with a path leading to a maze then to the destination

    """
    

    class Unit:
        """
        In this Labyrinth maze, "Unit" is a grid location that is surrounded
        by walls to the north, east, south, and west.

        """

        wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

        def __init__(self, x, y):
            """
            Initialize the cell at (x,y). Its is surrounded by walls all around.
            Create a two-dimensional grid of cells, where each cell has four walls:
            Top, right, bottom, and left
            Initially, all walls are intact, meaning there are no open paths between cells.
            """
            self.x, self.y = x, y
            self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
            

        def no_open_walls(self):
            """ Check if this cell still completely surrounded by walls?"""

            return all(self.walls.values())

        def break_wall(self, other, wall):
            """Break down the walls between cells."""

            self.walls[wall] = False
            other.walls[Unit.wall_pairs[wall]] = False


    class Maze:
        """A Labyrinth maze is composed of cell units."""

        def __init__(self, nx, ny, ix=0, iy=0):
            """
            Initialize the maze grid.
            The maze consists of nx x ny cells and the construction started
            at the cell indexed at (ix, iy).

            """

            self.nx, self.ny = nx, ny
            self.ix, self.iy = ix, iy
            self.maze_grid = [[Unit(x, y) for y in range(ny)] for x in range(nx)]

        def position(self, x, y):
            """Returns the position at (x,y)."""

            return self.maze_grid[x][y]

            
        def neighbour_with_dir(self, cell):
            """Return a list of unvisited neighbouring cells to the current cell."""

            co_ord = [('W', (-1, 0)),
                    ('E', (1, 0)),
                    ('S', (0, 1)),
                    ('N', (0, -1))]
            neighbours = []
            for dir, (dx, dy) in co_ord:
                x2, y2 = cell.x + dx, cell.y + dy
                if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                    neighbour = self.position(x2, y2)
                    if neighbour.no_open_walls():
                        neighbours.append((dir, neighbour))
            return neighbours

        def make_grid(self):
            # Total number of cells.
            n = self.nx * self.ny
            cell_track = []
            #starting with the initial position
            current_cell = self.position(self.ix, self.iy)
            # Total number of visited cells during maze construction.
            v = 1
            # recursive method to develop the maze
            while v < n:
                neighbours = self.neighbour_with_dir(current_cell)

                if not neighbours:
                    """
                    Dead end: backtrack - removes the item at the given 
                    index from the list and returns the removed item
                    moving the current cell to previous cells 
                    """
                    current_cell = cell_track.pop()
                    continue

                # Digging using the random neighbours picked, by removing the wall between them
                dir, next_cell = random.choice(neighbours)
                current_cell.break_wall(next_cell, dir)
                cell_track.append(current_cell)
                current_cell = next_cell
                v += 1

        def __str__(self):
            """To develop a string representation of the maze."""

            maze_rows = ['W' * ((self.nx * 2)+1) ]
            main.append(maze_rows)
            for y in range(self.ny):
                maze_row = ['W']
                for x in range(self.nx):
                    if self.maze_grid[x][y].walls['E']:
                        maze_row.append(' W')
                    else:
                        maze_row.append('  ')
                maze_rows.append(''.join(maze_row))
                maze_row = ['W']
                for x in range(self.nx):
                    if self.maze_grid[x][y].walls['S']:
                        maze_row.append('WW')
                    else:
                        maze_row.append(' W')
                maze_rows.append(''.join(maze_row))
            return '\n'.join(maze_rows)
        
    class Player(object):
        
        def __init__(self):
            self.rect = player_image.get_rect(center = (23,23))
    
        def move(self, dx, dy):
            
            # Move each axis separately. checks for collisions both times.
            if dx != 0:
                self.move_single_axis(dx, 0)
            if dy != 0:
                self.move_single_axis(0, dy)
        
        def move_single_axis(self, dx, dy):
            
            # Move the rect
            self.rect.x += dx
            self.rect.y += dy
    
            # If you collide with a wall, move 
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dx > 0: # right - when reached left side of the wall
                        self.rect.right = wall.rect.left
                    if dx < 0: # left; when reached right side of the wall
                        self.rect.left = wall.rect.right
                    if dy > 0: # down; when reached top side of the wall
                        self.rect.bottom = wall.rect.top
                    if dy < 0: # up; when reached bottom side of the wall
                        self.rect.top = wall.rect.bottom
    
    # walls
    class Wall(object):
        
        def __init__(self, pos):
            walls.append(self)
            self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

    
    score = 0
    stage = 1
    while(stage<3): 
        current_time = 0
        pygame.mixer.init()
        mixer.music.load("frontend/assets/alien.wav")
        mixer.music.play(-1)

        # Maze dimensions (no. of cols, no. of rows)
        nx, ny = (4* stage),(4*stage)
        # Maze entry position()
        ix, iy = 0, 0
        main = []
        levels = Maze(nx, ny, ix, iy)
        levels.make_grid()
        # level.splitlines()[1:]
        print(levels)
        print("\n")
        # print(main)
        print(main[0])

        # Initialise pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        # Set up the display
        cap = "Level "+ str(stage) + " Get to Wormhole!"
        pygame.display.set_caption(cap)
        screen = pygame.display.set_mode(((nx*33)+10,(nx*33)+70))
        
        clock = pygame.time.Clock()
        walls = [] # List to hold the walls

        player_image = pygame.image.load("play.png")
        player_image.convert()
        player = Player() # Create the player


        # Holds the level layout in a list of strings.
        level = main[0]
        u = len(level)
        u1 = len(level[0])
        print(" \n",u,u1)
        print("\n")


        #creating the maze in labyrinth
        print("breaking the walls1")
        i = 2
        j = 3
        print("the total dimentsion of this matrix", len(level),len(level[0]))
        while i < (len(level)-3):
            j = 3
            while j < (len(level[i])-3):
                if level[i][j]== 'W' and ((i+j)% 7 == 0 or (i+j) % 5 == 1):
                    l = ' '
                    ll = l.join([level[i][:j], level[i][j+1:]])
                    level[i] = ll
                j= j+1
            i= i+1
        


        #introduction  of an obstacle
        m = random.randint(u-5,u-2)
        n = random.randint(u1-5,u1-2)
        print("numbers",m,n)
        char = 'E'
        while main[0][m][n] == 'W':    
            m = random.randint(u-3,u-1)
            n = random.randint(u1-3,u1-1)
        levell = char.join([main[0][m][:n], main[0][m][n+1:]])
        print(levell)
        level[m] = levell
        print(level)

        worm = pygame.image.load("worm.png")
        # Parse the level string above. W = wall, E = exit
        x = y = 0
        for row in level:
            for col in row:
                if col == "W":
                    Wall((x, y))
                if col == "E":
                    end_rect = worm.get_rect(center = (x+6,y+7))
                x += 16
            y += 16
            x = 0
        
        running = True
        while running:
            current_time = pygame.time.get_ticks()
            clock.tick(60)
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False

            
            current_time = pygame.time.get_ticks()
            current_time /= 1000  # millisec to sec
        
            # Move the player if an arrow key is pressed
            arrow = pygame.key.get_pressed()
            if arrow[pygame.K_LEFT]:
                player.move(-2, 0)
            if arrow[pygame.K_RIGHT]:
                player.move(2, 0)
            if arrow[pygame.K_UP]:
                player.move(0, -2)
            if arrow[pygame.K_DOWN]:
                player.move(0, 2)
            if arrow[pygame.K_q]:
                #sys.exit()
                new_screen = pygame.display.set_mode((1278, 720))
                pygame.display.set_caption("Score Board")
                new_screen.fill((255, 255, 255))
                img = pygame.image.load("game_o.png")
                img_rect = img.get_rect(center = (640,260))
                game_font = pygame.freetype.Font("frontend/assets/font.ttf", 29)
                game_font.render_to(new_screen, (450, 500),"Your Time (sec): " + str(score), (255, 0, 0))
                new_screen.blit(img,img_rect)
                pygame.display.flip()
                time.sleep(5) 
                
                main_menu()
                pygame.display.flip()
            
            if player.rect.colliderect(end_rect):
                pygame.quit()
                score += int(current_time)
                stage += 1    
                pygame.mixer.init()
                mixer.music.load("frontend/assets/transition.wav")
                mixer.music.play(-1)
                time.sleep(0.5)         # sys.exit()
                break

        
            # Display the scene
            screen.fill((0, 0, 0))
            screen.blit(player_image,player.rect)
            screen.blit(worm,end_rect)
            for wall in walls:
                pygame.draw.rect(screen, (0,3, 212), wall.rect)
            #pygame.draw.rect(screen, (255, 49, 0), end_rect)
            #pygame.draw.rect(screen, (57, 255, 20), player.rect)
            game_font = pygame.freetype.Font("frontend/assets/font.ttf", 9)
            game_font.render_to(screen, (4, ((nx*33)+20)), "Press Q to exit", (255, 255,255))
            game_font.render_to(screen, (4, (nx*33)+40),"Time (sec) : " + str(score), (255, 255, 255))
            pygame.display.flip()
            clock.tick(360)
        pygame.quit()
    pygame.init()
    new_screen = pygame.display.set_mode((1278, 720))
    pygame.display.set_caption("Score Board")
    new_screen.fill((255, 255, 255))
    img = pygame.image.load("game_o.png")
    img_rect = img.get_rect(center = (640,260))
    game_font = pygame.freetype.Font("frontend/assets/font.ttf", 29)
    game_font.render_to(new_screen, (350, 500),"Your Time (sec) : " + str(score), (255, 0, 0))
    new_screen.blit(img,img_rect)
    pygame.display.flip()
    time.sleep(5) 
    main_menu()
    pygame.display.update()

pygame.init()

main_screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Labyrinth")

BG = pygame.image.load("bg.png")


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("frontend/assets/font.ttf", size)

def play():
    while True:
        
        labyrinth = laby()
        pygame.display.update()
    
def instr():
    while True:
        options_mouse_po = pygame.mouse.get_pos()
        main_screen.blit(BG, (0, 0))
        options_text = get_font(65).render("INSTRUCTION", True, "White")
        options_rect = options_text.get_rect(center=(640, 160))
        main_screen.blit(options_text, options_rect)

        str1 = "Your task is to find the wormhole and level up "
        str2 = "Press up and down arrows for vertical movement"
        str3 = "Press left and right arrows for horizontal movement"
        str4 = "Press q to Exit the loop"
        str5 = "Live long and Prosper!"

        options_text1 = get_font(25).render(str1, True, "White")
        options_rect1 = options_text1.get_rect(center=(640, 280))
        main_screen.blit(options_text1, options_rect1)


        options_text2 = get_font(15).render(str2, True, "White")
        options_rect2 = options_text2.get_rect(center=(640, 340))
        main_screen.blit(options_text2, options_rect2)


        options_text3 = get_font(15).render(str3, True, "White")
        options_rect3 = options_text3.get_rect(center=(640, 380))
        main_screen.blit(options_text3, options_rect3)


        options_text4 = get_font(35).render(str4, True, "Red")
        options_rect4 = options_text4.get_rect(center=(640, 460))
        main_screen.blit(options_text4, options_rect4)


        options_text5 = get_font(25).render(str5, True, "Green")
        options_rect5 = options_text5.get_rect(center=(640, 510))
        main_screen.blit(options_text5, options_rect5)

        options_back = Button(image=None, pos=(640, 590), 
                            text_input="BACK", font=get_font(25), base_color="White", hovering_color="Green")

        options_back.changeColor(options_mouse_po)
        options_back.update(main_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if options_back.checkForInput(options_mouse_po):
                    main_menu()
        pygame.display.update()


#Playerimage

def main_menu():
    pygame.init()

    main_screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Labyrinth")

    BG = pygame.image.load("bg.png")

    
    playerImg = pygame.image.load("frontend/assets/ufo.png")
    playerX =10
    playerY=0
    mixer.music.load("frontend/assets/background.wav")
    mixer.music.play(-1)

    def player12(x,y):
            main_screen.blit(playerImg,(x,y))

    running = True
    while running:
        main_screen.blit(BG, (0, 0))
        # Sound


        menu_mouse_po = pygame.mouse.get_pos()

        menu_text = get_font(100).render("LABYRINTH", True, "#FFFFFF")
        menu_rect = menu_text.get_rect(center=(640, 100))

        play_button = Button(image=pygame.image.load("frontend/assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#39FF14", hovering_color="White")
        options_button = Button(image=pygame.image.load("frontend/assets/Options Rect.png"), pos=(640, 400), 
                            text_input="INSTRUCTIIONS", font=get_font(35), base_color="#39FF14", hovering_color="White")
        quit_button = Button(image=pygame.image.load("frontend/assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#39FF14", hovering_color="White")

        main_screen.blit(menu_text, menu_rect)

        playerY += 0.5
    
        for button in [play_button, options_button, quit_button]:
            button.changeColor(menu_mouse_po)
            button.update(main_screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_po):
                    play()
                if options_button.checkForInput(menu_mouse_po):
                    instr()
                if quit_button.checkForInput(menu_mouse_po):
                    pygame.quit()
                    sys.exit()
                    running = False
        player12(playerX,playerY)
        pygame.display.update()

main_menu()


