import pygame
import sys
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0) # For ball color
RED = (255, 0, 0)   # For AI winner text

PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PLAYER_PADDLE_SPEED = 8
AI_PADDLE_SPEED = 4

BALL_RADIUS = 10
BALL_SPEED_X_INITIAL = 5
BALL_SPEED_Y_INITIAL = 5

WINNING_SCORE = 7 # Game ends when a player reaches this score

# --- Setting up game ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Tennis (First to 7 Wins!)")
clock = pygame.time.Clock()
score_font = pygame.font.Font(None, 74)
game_over_font = pygame.font.Font(None, 100)
winner_font = pygame.font.Font(None, 60)

# --- Track game progress ---
player_score = 0
ai_score = 0
game_over = False
winner_text = ""

# --- Game Objects ---
player_paddle = pygame.Rect(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai_paddle = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x = BALL_SPEED_X_INITIAL * random.choice((1, -1))
ball_speed_y = BALL_SPEED_Y_INITIAL * random.choice((1, -1))


# --- Game Functions ---
def draw_game_elements():
    screen.fill(BLACK)

    if not game_over:
        # Draw active game elements
        pygame.draw.rect(screen, WHITE, player_paddle)
        pygame.draw.rect(screen, WHITE, ai_paddle)
        pygame.draw.ellipse(screen, GREEN, ball)
        pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

        player_text_surface = score_font.render(str(player_score), True, WHITE)
        screen.blit(player_text_surface, (SCREEN_WIDTH // 4 - player_text_surface.get_width() // 2, 20))

        ai_text_surface = score_font.render(str(ai_score), True, WHITE)
        screen.blit(ai_text_surface, (SCREEN_WIDTH * 3 // 4 - ai_text_surface.get_width() // 2, 20))
    else:
        # Draw Game Over screen
        game_over_surface = game_over_font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(game_over_surface, game_over_rect)

        winner_color = GREEN if "Player" in winner_text else RED # Green for player, Red for AI
        winner_surface = winner_font.render(winner_text, True, winner_color)
        winner_rect = winner_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(winner_surface, winner_rect)

        # Optional: Add restart prompt
        # restart_font = pygame.font.Font(None, 40)
        # restart_text = restart_font.render("Press R to Restart or Q to Quit", True, WHITE)
        # restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        # screen.blit(restart_text, restart_rect)

    pygame.display.flip()

def move_ball():
    global ball_speed_x, ball_speed_y, player_score, ai_score, game_over, winner_text

    if game_over: # Don't move ball if game is over
        return

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    if ball.colliderect(player_paddle) or ball.colliderect(ai_paddle):
        ball_speed_x *= -1

    if ball.left <= 0:
        ai_score += 1
        if ai_score >= WINNING_SCORE:
            winner_text = "AI Wins!"
            game_over = True
        reset_ball()
    if ball.right >= SCREEN_WIDTH:
        player_score += 1
        if player_score >= WINNING_SCORE:
            winner_text = "Player Wins!"
            game_over = True
        reset_ball()

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    if not game_over: # Only give speed if game is not over
        pygame.time.wait(500)
        ball_speed_x = BALL_SPEED_X_INITIAL * random.choice((1, -1))
        ball_speed_y = BALL_SPEED_Y_INITIAL * random.choice((1, -1))
    else: # If game is over, stop the ball
        ball_speed_x = 0
        ball_speed_y = 0


def handle_player_paddle_movement(keys_pressed):
    if game_over: # Don't move paddle if game is over
        return
    if keys_pressed[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= PLAYER_PADDLE_SPEED
    if keys_pressed[pygame.K_DOWN] and player_paddle.bottom < SCREEN_HEIGHT:
        player_paddle.y += PLAYER_PADDLE_SPEED

def move_ai_paddle():
    if game_over: # Don't move paddle if game is over
        return
    if ai_paddle.centery < ball.centery - AI_PADDLE_SPEED / 2 :
        ai_paddle.y += AI_PADDLE_SPEED
    elif ai_paddle.centery > ball.centery + AI_PADDLE_SPEED / 2:
        ai_paddle.y -= AI_PADDLE_SPEED

    if ai_paddle.top < 0: ai_paddle.top = 0
    if ai_paddle.bottom > SCREEN_HEIGHT: ai_paddle.bottom = SCREEN_HEIGHT

# --- Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Optional: Add restart and quit functionality here if game_over
        # if game_over and event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_r: # Restart Game
        #         player_score = 0
        #         ai_score = 0
        #         game_over = False
        #         winner_text = ""
        #         player_paddle.centery = SCREEN_HEIGHT // 2
        #         ai_paddle.centery = SCREEN_HEIGHT // 2
        #         reset_ball() # This will now give ball speed again
        #     elif event.key == pygame.K_q:
        #         running = False

    if not game_over:
        keys_pressed = pygame.key.get_pressed()
        handle_player_paddle_movement(keys_pressed)
        move_ai_paddle()
        move_ball() # Scoring and win condition check is now inside move_ball
    
    draw_game_elements() # Draws game or game over screen

    clock.tick(60)

pygame.quit()
sys.exit()