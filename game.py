import pygame
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 0)
ORANGE = (255, 165, 0)
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (50, 205, 50)
FPS = 60

# --- Game Class ---
class Game:
    """A class to represent the Jumping Chick game.

    This class encapsulates all the game's attributes and methods,
    including the game loop, event handling, and game state updates.

    Attributes:
        screen (pygame.Surface): The main game screen.
        clock (pygame.time.Clock): The game clock for controlling the frame rate.
        score_font (pygame.font.Font): The font used for displaying the score.
        game_over_font (pygame.font.Font): The font used for the 'Game Over' message.
        chick_width (int): The width of the chick.
        chick_height (int): The height of the chick.
        chick_x (int): The x-coordinate of the chick.
        ground_level (int): The y-coordinate of the ground.
        chick_y (int): The y-coordinate of the chick.
        chick_y_velocity (int): The vertical velocity of the chick.
        gravity (float): The force of gravity acting on the chick.
        jump_strength (int): The initial velocity of the chick's jump.
        is_jumping (bool): A flag to indicate if the chick is currently jumping.
        egg_width (int): The width of the eggs.
        egg_height (int): The height of the eggs.
        egg_speed (int): The speed at which the eggs move.
        eggs (list): A list to store the egg obstacles.
        score (int): The player's score.
        game_over (bool): A flag to indicate if the game is over.
        running (bool): A flag to control the main game loop.
        ADD_EGG_EVENT (int): A custom event for adding new eggs.
    """
    def __init__(self):
        """Initializes the game and its attributes.

        This method sets up the Pygame environment, creates the game window,
        and calls reset_game() to initialize the game state.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jumping Chick")
        self.clock = pygame.time.Clock()
        self.score_font = pygame.font.Font(None, 50)
        self.game_over_font = pygame.font.Font(None, 80)
        self.reset_game()

    def reset_game(self):
        """Resets the game to its initial state.

        This method is called when the game first starts and can be used
        to restart the game after a 'Game Over'. It initializes all the
        game variables to their default values.
        """
        self.chick_width = 50
        self.chick_height = 40
        self.chick_x = 100
        self.ground_level = SCREEN_HEIGHT - 100
        self.chick_y = self.ground_level - self.chick_height
        self.chick_y_velocity = 0
        self.gravity = 0.8
        self.jump_strength = -18
        self.is_jumping = False

        self.egg_width = 30
        self.egg_height = 45
        self.egg_speed = 7
        self.eggs = []

        self.score = 0
        self.game_over = False
        self.running = True

        # Custom event for adding new eggs
        self.ADD_EGG_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADD_EGG_EVENT, 1200)

    def run(self):
        """The main game loop.

        This method contains the main loop that runs the game. It continuously
        handles events, updates the game state, and draws the game elements
        until the game is over or the user quits.
        """
        while self.running:
            self.handle_events()
            self.update_game_state()
            self.draw_elements()
            self.clock.tick(FPS)
        pygame.quit()

    def handle_events(self):
        """Handles all game events, including input.

        This method processes events from the Pygame event queue. It handles
        user input for jumping and quitting the game, as well as custom
        events for spawning new eggs.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if not self.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and not self.is_jumping:
                        self.is_jumping = True
                        self.chick_y_velocity = self.jump_strength
                if event.type == self.ADD_EGG_EVENT:
                    new_egg = pygame.Rect(SCREEN_WIDTH, self.ground_level - self.egg_height, self.egg_width, self.egg_height)
                    self.eggs.append({'rect': new_egg, 'passed': False})

    def update_game_state(self):
        """Updates the state of all game objects.

        This method is responsible for the game's logic. It updates the
        chick's position based on gravity and jumping, moves the eggs,
        updates the score, and checks for collisions.
        """
        if not self.game_over:
            # Update chick's position
            if self.is_jumping:
                self.chick_y_velocity += self.gravity
                self.chick_y += self.chick_y_velocity
                if self.chick_y >= self.ground_level - self.chick_height:
                    self.chick_y = self.ground_level - self.chick_height
                    self.is_jumping = False
                    self.chick_y_velocity = 0

            # Update eggs' positions and score
            for egg in self.eggs:
                egg['rect'].x -= self.egg_speed
                if egg['rect'].right < self.chick_x and not egg['passed']:
                    self.score += 1
                    egg['passed'] = True

            # Remove off-screen eggs
            self.eggs = [egg for egg in self.eggs if egg['rect'].right > 0]

            # Check for collisions
            chick_rect = pygame.Rect(self.chick_x, self.chick_y, self.chick_width, self.chick_height)
            for egg in self.eggs:
                if chick_rect.colliderect(egg['rect']):
                    self.game_over = True

    def draw_elements(self):
        """Draws all game elements to the screen.

        This method handles all the rendering. It draws the background,
        ground, chick, eggs, and score or 'Game Over' message to the screen.
        """
        self.screen.fill(SKY_BLUE)
        pygame.draw.rect(self.screen, GRASS_GREEN, (0, self.ground_level, SCREEN_WIDTH, 100))
        self.draw_chick(self.chick_x, self.chick_y)
        for egg in self.eggs:
            self.draw_egg(egg['rect'])
        if self.game_over:
            self.display_game_over()
        else:
            self.display_score()
        pygame.display.flip()

    def draw_chick(self, x, y):
        """Draws the chick on the screen.

        Args:
            x (int): The x-coordinate of the chick.
            y (int): The y-coordinate of the chick.
        """
        pygame.draw.ellipse(self.screen, YELLOW, (x, y, self.chick_width, self.chick_height))
        pygame.draw.ellipse(self.screen, YELLOW, (x - 10, y + 15, 20, 15))
        pygame.draw.circle(self.screen, BLACK, (int(x + self.chick_width * 0.7), int(y + self.chick_height * 0.3)), 4)
        beak_points = [(x + self.chick_width - 2, y + 20), (x + self.chick_width + 10, y + 25), (x + self.chick_width - 2, y + 30)]
        pygame.draw.polygon(self.screen, ORANGE, beak_points)

    def draw_egg(self, egg_rect):
        """Draws a single egg on the screen.

        Args:
            egg_rect (pygame.Rect): The rectangle representing the egg's
                position and size.
        """
        pygame.draw.ellipse(self.screen, WHITE, egg_rect)
        pygame.draw.ellipse(self.screen, BLACK, egg_rect, 2)

    def display_score(self):
        """Renders and displays the current score.

        This method creates a text surface with the current score and
        blits it to the top-left corner of the screen.
        """
        score_text = self.score_font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def display_game_over(self):
        """Displays the game over message.

        This method shows a 'GAME OVER' message in the center of the
        screen, along with the final score.
        """
        over_text = self.game_over_font.render("GAME OVER", True, BLACK)
        text_rect = over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40))
        self.screen.blit(over_text, text_rect)
        final_score_text = self.score_font.render(f"Final Score: {self.score}", True, BLACK)
        score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
        self.screen.blit(final_score_text, score_rect)

if __name__ == "__main__":
    game = Game()
    game.run()