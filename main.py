import random
import os
import pygame

TOP_NORMAL = pygame.math.Vector2(0, 1)
BOTTOM_NORMAL = pygame.math.Vector2(0, -1)
LEFT_NORMAL = pygame.math.Vector2(1, 0)
RIGHT_NORMAL = pygame.math.Vector2(-1, 0)

FRAME_RATE = 60
PADDLE_HEIGHT = 90
BALL_WIDTH = 20
PADDLE_CIRCLE_RADIUS = (3 * BALL_WIDTH)

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
        self.rect.move_ip(dx, dy)


class App:
    def __init__(self):
        self.paddle_velocity = 8
        self.ball_velocity = 8
        self.running = True
        self.width, self.height = 1280, 720
        x, y = 40, 360
        self.left_paddle_state = PaddleState(x, y, BALL_WIDTH, PADDLE_HEIGHT)
        self.right_paddle_state = PaddleState(self.width - x, y, BALL_WIDTH, 80)

        self.ball_state = BallState(self.width // 2, y, BALL_WIDTH, BALL_WIDTH)

        self.left_paddle_move_command = PaddleMoveCommand()
        self.right_paddle_move_command = PaddleMoveCommand()

        self.ball_vector = pygame.math.Vector2()
        self.ball_vector.x = random.uniform(0.25, 1.0)  # make sure ball has horizontal momentum
        self.ball_vector.y = random.random()

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
                move_command.change(self.paddle_velocity)
            elif event.key == up_key:
                move_command.change(-self.paddle_velocity)
        elif pygame.KEYUP == event.type:
            if event.key == down_key:
                move_command.change(-self.paddle_velocity)
            elif event.key == up_key:
                move_command.change(self.paddle_velocity)

    def update(self):
        self.left_paddle_state.update(self.left_paddle_move_command.y)
        self.right_paddle_state.update(self.right_paddle_move_command.y)

        # move ball
        self.ball_state.update(int(self.ball_vector.x * self.ball_velocity),
                               int(self.ball_vector.y * self.ball_velocity))

        # detect ball collides with wall
        ball_rect = self.ball_state.rect
        if ball_rect.top <= 0:
            self.ball_vector.reflect_ip(TOP_NORMAL)
        elif ball_rect.bottom >= self.height:
            self.ball_vector.reflect_ip(BOTTOM_NORMAL)
        elif ball_rect.left <= 0:
            self.ball_vector.reflect_ip(LEFT_NORMAL)
        elif ball_rect.right >= self.width:
            self.ball_vector.reflect_ip(RIGHT_NORMAL)

        # detect ball collides with paddle
        left_paddle_rect = self.left_paddle_state.rect
        right_paddle_rect = self.right_paddle_state.rect
        if ball_rect.colliderect(left_paddle_rect):
            self.ball_vector = self.calculate_left_paddle_normal(ball_rect, left_paddle_rect)
        elif ball_rect.colliderect(right_paddle_rect):
            self.ball_vector = self.calculate_right_paddle_normal(ball_rect, right_paddle_rect)

        # if ball passes paddle, reset ball to center

    def render(self):
        self.surface.fill(BLACK)
        self.draw_entity(self.left_paddle_state)
        self.draw_entity(self.right_paddle_state)
        self.draw_entity(self.ball_state)
        pygame.display.update()

    def draw_entity(self, entity_state):
        pygame.draw.rect(self.surface, BLUE, entity_state.rect, 0)

    def calculate_left_paddle_normal(self, ball_rect, paddle_rect):
        # Imagine the paddle is actually a sixth of a circle.
        # When the ball hits the paddle off center, it will bounce like it collided with a rounded edge.
        circle_middle_x = paddle_rect.right - PADDLE_CIRCLE_RADIUS
        circle_middle_y = paddle_rect.centery
        return pygame.math.Vector2(ball_rect.centerx - circle_middle_x, ball_rect.centery - circle_middle_y).normalize()

    def calculate_right_paddle_normal(self, ball_rect, paddle_rect):
        # Imagine the paddle is actually a sixth of a circle.
        # When the ball hits the paddle off center, it will bounce like it collided with a rounded edge.
        circle_middle_x = paddle_rect.left - PADDLE_CIRCLE_RADIUS
        circle_middle_y = paddle_rect.centery
        return pygame.math.Vector2(circle_middle_x - ball_rect.centerx, ball_rect.centery - circle_middle_y).normalize()

    def run(self):
        while self.running:
            self.process_input()
            self.update()
            self.render()

            self.clock.tick(FRAME_RATE)


def main():
   app = App()
   app.run()

   pygame.quit()
   os.sys.exit()


if __name__ == "__main__":
    main()
