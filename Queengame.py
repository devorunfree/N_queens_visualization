import pygame
from pygame import QUIT
import Winner


class LadyBugGame:

    def __init__(self, n, cell_w=50, cell_h=50):
        self._screen = None
        self._lady_bug = None
        self._clock = pygame.time.Clock()
        self._background_color = (160, 160, 160)  # gray rgb
        self._cell_background_color = (255, 255, 255)  # white rgb
        self._cell_background_color1 = (0, 0, 0)  # black rgb
        self._gap = 5
        self._window_width = ((n * cell_w) + ((n+1) * 5))
        self._window_height = ((n * cell_w) + ((n+1) * 5))
        self._cell_width = cell_w
        self._cell_height = cell_h
        self._grid_rows = n
        self._grid_columns = n
        self.prev_coords = []
        self.matrix = []
        for i in range(int(n)):
            self.matrix.append([])
            for j in range(int(n)):
                self.matrix[i].append(0)
        self.check_sol = []  # we will multiply this nx1 column matrix by the grid to check if the game is complete
        for i in range(int(n)):
            self.check_sol.append([1])
        # rand_x = random.randint(1, self._grid_columns)
        # rand_y = random.randint(1, self._grid_rows)
        # self._bug_x = ((rand_x * self._cell_width) + (rand_x * self._gap)) - (self._cell_width / 2)
        # self._bug_y = ((rand_y * self._cell_height) + (rand_y * self._gap)) - (self._cell_height / 2)

    def setup(self):
        pygame.init()

        # Set window size using a tuple
        self._screen = pygame.display.set_mode((self._window_width, self._window_height))
        # Set the window title
        pygame.display.set_caption("Queen game")
        # Load the bug image
        self._lady_bug = pygame.image.load('queen.png')
        self.draw_grid()

    def draw_grid(self):
        self._screen.fill(self._background_color)
        colors = [self._cell_background_color, self._cell_background_color1]
        for row in range(self._grid_rows):
            for column in range(self._grid_columns):
                color = colors[((row + column) % 2)]
                # Make rectangle as [start_x, start_y, width, height]
                # or [surface, color, [start_x, start_y, width, height]]
                pygame.draw.rect(self._screen, color, [(self._gap + self._cell_width) * column +
                                                       self._gap, (self._gap + self._cell_height) * row + self._gap,
                                                       self._cell_width, self._cell_height])

    def place_bug(self, coords):
        image_rect = self._lady_bug.get_rect()
        # image_rect.center = (pos[0]//(self._cell_width + self._gap), pos[1]//(self._cell_height + self._gap))
        image_rect.center = ((((coords[0] * self._cell_width) + ((coords[0]) * self._gap)) - (self._cell_width / 2)),
                             (((coords[1] * self._cell_width) + ((coords[1]) * self._gap)) - (self._cell_width / 2)))
        self._screen.blit(self._lady_bug, image_rect)
        place = pygame.mixer.Sound("place.mp3")
        pygame.mixer.Sound.play(place)

    def update_ui(self):
        self.draw_grid()
        self._clock.tick(60)  # set to 60 FPS
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    left, middle, right = pygame.mouse.get_pressed()
                    if left:  # if left click
                        pos = pygame.mouse.get_pos()  # pos is a tuple (x, y)
                        new_col = (pos[0] // (self._cell_width + self._gap))  # getting matrix coordinates
                        new_row = (pos[1] // (self._cell_height + self._gap))
                        if self.matrix[new_row][new_col] == 0:  # checking if queen is already there
                            coords = (new_col + 1, new_row + 1)  # assign coords
                            if len(self.prev_coords) > 0:  # if the first move has been made
                                for elem in self.prev_coords:  # checking previous moves
                                    if coords[0] == elem[0] or coords[1] == elem[1] or \
                                            (abs(coords[0] - elem[0]) == abs(coords[1] - elem[1])):
                                        # checks if queen can attack in all directions based on previous moves
                                        # if attack is possible, error sound plays
                                        error_sound = pygame.mixer.Sound("err_sound.mp3")
                                        pygame.mixer.Sound.play(error_sound)
                                        print("Queen can attack!", coords)
                                        break  # cannot place queen here, breaks the loop

                                else:  # conditions are satisfied to allow queen placement
                                    self.matrix[new_row][new_col] = 1
                                    self.prev_coords.append(coords)
                                    self.place_bug(coords)
                                    print(pos, coords)
                                    result = []
                                    for X_row in self.matrix:
                                        result.append([sum(a * b for a, b in zip(X_row, Y_col)) for Y_col in
                                                       zip(*self.check_sol)])
                                    total = 0
                                    for r in result:
                                        total += r[0]
                                    print(total)
                                    if total == self._grid_rows:
                                        Winner.wingui()
                                    # break

                            else:  # this is for the first move only
                                self.matrix[new_row][new_col] = 1
                                self.prev_coords.append(coords)
                                self.place_bug(coords)
                                break

                        else:  # this is for if there has been a queen placed on the clicked space
                            error_sound = pygame.mixer.Sound("err_sound.mp3")
                            pygame.mixer.Sound.play(error_sound)
                            print("Queen is already at", coords)
                        # for row in self.matrix:
                        #     print(row)

            # flip allows only a portion of the screen to be updated instead of the entire area
            pygame.display.flip()
            # iterate through rows of X

    def quit(self):
        pygame.quit()
