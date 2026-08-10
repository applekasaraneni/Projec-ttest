import pygame
import random
import sys

WIDTH = 432
HEIGHT = 768
PIPE_WIDTH = 80
PIPE_GAP = 200
PIPE_SPEED = 4
BIRD_SIZE = 30
GRAVITY = 0.35
FLAP_STRENGTH = -8


def draw_text(surface, text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, rect)


def create_pipe_pair():
    gap_y = random.randint(150, HEIGHT - 250)
    top_pipe = pygame.Rect(WIDTH, 0, PIPE_WIDTH, gap_y)
    bottom_pipe = pygame.Rect(WIDTH, gap_y + PIPE_GAP, PIPE_WIDTH, HEIGHT - gap_y - PIPE_GAP)
    return top_pipe, bottom_pipe


def reset_game():
    bird = pygame.Rect(100, HEIGHT // 2 - BIRD_SIZE // 2, BIRD_SIZE, BIRD_SIZE)
    velocity = 0
    pipes = []
    for i in range(3):
        pipe_x = WIDTH + i * 250
        top_pipe, bottom_pipe = create_pipe_pair()
        top_pipe.x = pipe_x
        bottom_pipe.x = pipe_x
        pipes.append({"top": top_pipe, "bottom": bottom_pipe, "scored": False})
    score = 0
    game_active = True
    return bird, velocity, pipes, score, game_active


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    bird, velocity, pipes, score, game_active = reset_game()
    floor_y = HEIGHT - 100
    frame_count = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_active:
                        velocity = FLAP_STRENGTH
                    else:
                        bird, velocity, pipes, score, game_active = reset_game()

        if game_active:
            velocity += GRAVITY
            bird.y += int(velocity)

            if bird.top <= 0:
                bird.top = 0
                velocity = 0

            if bird.bottom >= floor_y:
                bird.bottom = floor_y
                game_active = False

            for pipe_pair in pipes:
                top_pipe = pipe_pair["top"]
                bottom_pipe = pipe_pair["bottom"]
                top_pipe.x -= PIPE_SPEED
                bottom_pipe.x -= PIPE_SPEED

                if top_pipe.right < 0:
                    top_pipe.x = WIDTH + 250
                    bottom_pipe.x = WIDTH + 250
                    gap_y = random.randint(150, HEIGHT - 250)
                    top_pipe.height = gap_y
                    bottom_pipe.y = gap_y + PIPE_GAP
                    bottom_pipe.height = HEIGHT - gap_y - PIPE_GAP
                    pipe_pair["scored"] = False

                if top_pipe.right < bird.left and not pipe_pair["scored"]:
                    score += 1
                    pipe_pair["scored"] = True

                if bird.colliderect(top_pipe) or bird.colliderect(bottom_pipe):
                    game_active = False

            frame_count += 1

        screen.fill((25, 150, 255))
        pygame.draw.rect(screen, (80, 210, 80), (0, floor_y, WIDTH, HEIGHT - floor_y))

        for pipe_pair in pipes:
            top_pipe = pipe_pair["top"]
            bottom_pipe = pipe_pair["bottom"]
            pygame.draw.rect(screen, (40, 160, 40), top_pipe)
            pygame.draw.rect(screen, (40, 160, 40), bottom_pipe)
            pygame.draw.rect(screen, (0, 100, 0), top_pipe.inflate(-10, -10))
            pygame.draw.rect(screen, (0, 100, 0), bottom_pipe.inflate(-10, -10))

        pygame.draw.ellipse(screen, (255, 255, 0), bird)
        pygame.draw.circle(screen, (255, 120, 0), bird.center, BIRD_SIZE // 2, 4)

        draw_text(screen, f"Score: {score}", 40, WIDTH // 2, 50)

        if not game_active:
            draw_text(screen, "Game Over", 72, WIDTH // 2, HEIGHT // 2 - 40)
            draw_text(screen, "Press SPACE to restart", 36, WIDTH // 2, HEIGHT // 2 + 30)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
