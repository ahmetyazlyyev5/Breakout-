from graphics import Canvas
import time
import random

DEBUGGING = False

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 600
PADDLE_Y = CANVAS_HEIGHT - 30
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 15
BALL_RADIUS = 30 if DEBUGGING else 17

BRICK_GAP = 5
NUM_BRICKS = 10
BRICK_WIDTH = (CANVAS_WIDTH - BRICK_GAP*9) / NUM_BRICKS
BRICK_HEIGHT = 10
BRICK_COLORS = ["red", "orange", "yellow", "green", "cyan"]
TOP_GAP = BRICK_HEIGHT * 3 + BRICK_GAP * 2
LEFT_GAP = (CANVAS_WIDTH - (NUM_BRICKS * BRICK_WIDTH + BRICK_GAP * (NUM_BRICKS - 1))) / 2

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    change_x = random.choice([10, -10])
    change_y = 10 + random.randint(1, 3)
    total_bricks = NUM_BRICKS * NUM_BRICKS
    tries = 3
    # print(f"Left gap: {LEFT_GAP}")
    # print(f"Brick gap: {BRICK_GAP}")
    # print(f"brick width: {BRICK_WIDTH}")
    draw_bricks(canvas)
    p_x = (CANVAS_WIDTH - PADDLE_WIDTH) / 2
    paddle = canvas.create_rectangle(p_x, PADDLE_Y, p_x + PADDLE_WIDTH, PADDLE_Y+PADDLE_HEIGHT, "black")
    
    b_x = (CANVAS_WIDTH - BALL_RADIUS) / 2
    b_y = (CANVAS_HEIGHT - BALL_RADIUS) / 2
    ball = canvas.create_oval(b_x, b_y, b_x + BALL_RADIUS, b_y + BALL_RADIUS, "black")

    # game loop
    game_running = True
    fps = 120 if DEBUGGING else 40
    sleep_time = 1 / fps

    if not DEBUGGING:
        canvas.wait_for_click()
    while game_running:

        # check collision (update)
            # remove a brick
            # update velocity
        
        ball_left = canvas.get_left_x(ball)
        ball_right = ball_left + BALL_RADIUS
        ball_top = canvas.get_top_y(ball)
        ball_bot = ball_top + BALL_RADIUS
        if ball_left <= 0 or ball_right >= CANVAS_WIDTH:
            change_x = change_x * (-1)
        if ball_top <= 0:
            change_y = change_y * (-1)
        if ball_top >= CANVAS_HEIGHT:
            tries -= 1
            if tries > 0:
                canvas.moveto(ball, b_x, b_y)

        objs = canvas.find_overlapping(
            ball_left, 
            ball_top, 
            ball_right, 
            ball_bot
        )

        # simple logic. just revert y-velocity upon collision
        if len(objs) > 1:
            obj = objs[-2] # last item is the ball
            if obj == paddle and change_y > 0 and not DEBUGGING: # ball hit the paddle and was descending
                # nudge ball clear of the paddle so it’s no longer overlapping
                canvas.moveto(
                    ball,
                    ball_left,
                    PADDLE_Y - BALL_RADIUS - 1
                )
                change_y = 10 # to change after initial collision
                change_y *= -1
            elif obj != paddle:
                canvas.delete(obj)
                total_bricks -= 1
                change_y *= -1

        # move the paddle (redraws automatically)
        mouse_x = canvas.get_mouse_x()
        new_x = mouse_x - PADDLE_WIDTH / 2
        # print(f"Mouse x: {mouse_x}")
        canvas.moveto(paddle, new_x, PADDLE_Y)

        # move the ball (redraws automatically)
        if DEBUGGING:
            mouse_y = canvas.get_mouse_y()
            canvas.moveto(ball, mouse_x - BALL_RADIUS / 2, mouse_y - BALL_RADIUS / 2)
        else:
            canvas.move(ball, change_x, change_y)

        # check ending condition
        if total_bricks == 0:
            print("You won!")
            if not DEBUGGING:
                game_running = False
        elif tries == 0:
            print("You lost!")
            game_running = False

        # wait for a tiny bit
        time.sleep(sleep_time)

def draw_bricks(canvas):
    for j in range(NUM_BRICKS):
        for i in range(NUM_BRICKS):
            x = LEFT_GAP + i * BRICK_WIDTH + i * BRICK_GAP
            # x = LEFT_GAP + i * BRICK_WIDTH
            y = TOP_GAP + j * BRICK_HEIGHT + (j + 1) * BRICK_GAP
            color = BRICK_COLORS[j // 2]
            canvas.create_rectangle(x, y, x + BRICK_WIDTH, y + BRICK_HEIGHT, color)

if __name__ == '__main__':
    main()
