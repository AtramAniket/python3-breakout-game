import tkinter as tk


class BreakoutGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Breakout")

        self.width = 800
        self.height = 600

        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg="#111827",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.is_game_running = True

        self.paddle_width = 120
        self.paddle_height = 15
        self.paddle_speed = 8
        self.paddle_bottom_margin = 50

        self.left_pressed = False
        self.right_pressed = False

        self.ball_size = 18
        self.ball_dx = 4
        self.ball_dy = -4

        self.bricks = []
        self.brick_rows = 5
        self.brick_cols = 10
        self.brick_width = 70
        self.brick_height = 25
        self.brick_padding = 5

        self.score = 0
        self.lives = 3

        self.score_text = self.canvas.create_text(
            20,
            20,
            text=f"Score: {self.score}",
            fill="white",
            font=("Arial", 14),
            anchor="w",
        )

        self.lives_text = self.canvas.create_text(
            self.width - 20,
            20,
            text=f"Lives: {self.lives}",
            fill="white",
            font=("Arial", 14),
            anchor="e",
        )

        self.create_paddle()
        self.create_ball()
        self.create_bricks()

        self.root.bind("<KeyPress-Left>", self.on_left_press)
        self.root.bind("<KeyRelease-Left>", self.on_left_release)
        self.root.bind("<KeyPress-Right>", self.on_right_press)
        self.root.bind("<KeyRelease-Right>", self.on_right_release)

        self.game_loop()
        self.root.mainloop()

    def create_paddle(self):
        center_x = self.width / 2

        left = center_x - self.paddle_width / 2
        right = center_x + self.paddle_width / 2

        top = self.height - self.paddle_bottom_margin
        bottom = top + self.paddle_height

        self.paddle = self.canvas.create_rectangle(
            left,
            top,
            right,
            bottom,
            fill="#38bdf8",
            outline="",
        )

    def create_ball(self):
        center_x = self.width / 2
        center_y = self.height / 2

        left = center_x - self.ball_size / 2
        top = center_y - self.ball_size / 2
        right = center_x + self.ball_size / 2
        bottom = center_y + self.ball_size / 2

        self.ball = self.canvas.create_oval(
            left,
            top,
            right,
            bottom,
            fill="#facc15",
            outline="",
        )

    def create_bricks(self):
        start_x = 30
        start_y = 50

        for row in range(self.brick_rows):
            for col in range(self.brick_cols):
                x1 = start_x + col * (self.brick_width + self.brick_padding)
                y1 = start_y + row * (self.brick_height + self.brick_padding)

                x2 = x1 + self.brick_width
                y2 = y1 + self.brick_height

                brick = self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="#ef4444",
                    outline="",
                )

                self.bricks.append(brick)

    def on_left_press(self, event):
        self.left_pressed = True

    def on_left_release(self, event):
        self.left_pressed = False

    def on_right_press(self, event):
        self.right_pressed = True

    def on_right_release(self, event):
        self.right_pressed = False

    def move_paddle(self):
        x1, y1, x2, y2 = self.canvas.coords(self.paddle)

        if self.left_pressed and x1 > 0:
            self.canvas.move(self.paddle, -self.paddle_speed, 0)

        if self.right_pressed and x2 < self.width:
            self.canvas.move(self.paddle, self.paddle_speed, 0)

    def game_loop(self):
        if self.is_game_running:
            self.move_paddle()
            self.move_ball()

        self.root.after(16, self.game_loop)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)

        ball_coords = self.canvas.coords(self.ball)
        x1, y1, x2, y2 = ball_coords

        if x1 <= 0 or x2 >= self.width:
            self.ball_dx *= -1

        if y1 <= 0:
            self.ball_dy *= -1

        if y2 >= self.height:
            self.lose_life()
            return

        paddle_coords = self.canvas.coords(self.paddle)

        if self.is_collision(ball_coords, paddle_coords):
            self.ball_dy = -abs(self.ball_dy)

        for brick in self.bricks[:]:
            brick_coords = self.canvas.coords(brick)

            if self.is_collision(ball_coords, brick_coords):
                self.canvas.delete(brick)
                self.bricks.remove(brick)

                self.score += 10

                self.canvas.itemconfig(
                    self.score_text,
                    text=f"Score: {self.score}",
                )

                # Check win condition
                if not self.bricks:
                    self.win_game()
                    return

                self.ball_dy *= -1
                break

    def lose_life(self):
        self.lives -= 1

        self.canvas.itemconfig(
            self.lives_text,
            text=f"Lives: {self.lives}",
        )

        if self.lives <= 0:
            self.game_over()
            return

        self.reset_ball()

    def reset_ball(self):
        self.canvas.delete(self.ball)
        self.create_ball()

        self.ball_dx = 4
        self.ball_dy = -4

    def win_game(self):
        self.is_game_running = False

        self.canvas.create_text(
            self.width / 2,
            self.height / 2,
            text="YOU WIN!",
            fill="#22c55e",
            font=("Arial", 36, "bold"),
        )

    def game_over(self):
        self.is_game_running = False

        self.canvas.create_text(
            self.width / 2,
            self.height / 2,
            text="GAME OVER",
            fill="white",
            font=("Arial", 36, "bold"),
        )

    def is_collision(self, ball, item):
        ball_left, ball_top, ball_right, ball_bottom = ball
        item_left, item_top, item_right, item_bottom = item

        return (
            ball_right >= item_left
            and ball_left <= item_right
            and ball_bottom >= item_top
            and ball_top <= item_bottom
        )


if __name__ == "__main__":
    BreakoutGame()