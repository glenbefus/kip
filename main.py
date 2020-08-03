import random
import os
import pygame

BALL_WIDTH = 20

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


class PaddleMoveCommand:
    def __init__(self):
        self.y = 0

    def change(self, dy):
        self.y += dy


class EntityState:
    def __init__(self, center_x, center_y, width, height):
        half_width = width // 2
        half_height = height // 2
        self.rect = pygame.Rect(center_x - half_width, center_y - half_height, width, height)


class PaddleState(EntityState):
    def update(self, dy):
        self.rect.y += dy


class BallState(EntityState):
    def update(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


class App:
    def __init__(self):
        self.velocity = 8
        self.running = True
        self.width, self.height = 1280, 720
        x, y = 40, 360
        self.left_paddle_state = PaddleState(x, y, BALL_WIDTH, 80)
        self.right_paddle_state = PaddleState(self.width - x, y, BALL_WIDTH, 80)

        self.ball_state = BallState(self.width // 2, y, BALL_WIDTH, BALL_WIDTH)

        self.left_paddle_move_command = PaddleMoveCommand()
        self.right_paddle_move_command = PaddleMoveCommand()

        self.clock = pygame.time.Clock()

        pygame.init()
        pygame.display.set_caption("Kip")
        self.surface = pygame.display.set_mode((self.width, self.height), pygame.SWSURFACE)

    def process_input(self):
        for event in pygame.event.get():
            if pygame.QUIT == event.type:
                self.running = False

            self.process_input_for_paddle(event, self.left_paddle_move_command, pygame.K_w, pygame.K_s)
            self.process_input_for_paddle(event, self.right_paddle_move_command, pygame.K_UP, pygame.K_DOWN)

    def process_input_for_paddle(self, event, move_command, up_key, down_key):
        if pygame.KEYDOWN == event.type:
            if event.key == down_key:
                move_command.change(self.velocity)
            elif event.key == up_key:
                move_command.change(-self.velocity)
        elif pygame.KEYUP == event.type:
            if event.key == down_key:
                move_command.change(-self.velocity)
            elif event.key == up_key:
                move_command.change(self.velocity)

    def update(self):
        self.left_paddle_state.update(self.left_paddle_move_command.y)
        self.right_paddle_state.update(self.right_paddle_move_command.y)

        #move ball
        #detect ball collides with paddle
        # detect where on paddle ball collides to create new angle
        # if ball passes paddle, reset ball to center

    def render(self):
        self.surface.fill(BLACK)
        self.draw_entity(self.left_paddle_state)
        self.draw_entity(self.right_paddle_state)
        self.draw_entity(self.ball_state)
        pygame.display.update()

    def draw_entity(self, entity_state):
        pygame.draw.rect(self.surface, BLUE, entity_state.rect, 0)

    def run(self):
        while self.running:
            self.process_input()
            self.update()
            self.render()

            self.clock.tick(60)


def main():
   app = App()
   app.run()

   pygame.quit()
   os.sys.exit()


if __name__ == "__main__":
    main()
