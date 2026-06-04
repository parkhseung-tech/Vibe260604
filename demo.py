import tkinter as tk
import random

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_SIZE = 16
BRICK_ROWS = 5
BRICK_COLS = 8
BRICK_WIDTH = 68
BRICK_HEIGHT = 20
BRICK_PADDING = 5
TOP_OFFSET = 50
LIVES = 3

class BrickBreaker:
    def __init__(self, root):
        self.root = root
        root.title("블럭깨기 게임")
        root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="#222")
        self.canvas.pack()

        self.score = 0
        self.lives = LIVES
        self.game_over = False
        self.ball_dx = 4
        self.ball_dy = -4

        self.paddle = self.canvas.create_rectangle(
            (WINDOW_WIDTH - PADDLE_WIDTH) // 2,
            WINDOW_HEIGHT - 40,
            (WINDOW_WIDTH + PADDLE_WIDTH) // 2,
            WINDOW_HEIGHT - 40 + PADDLE_HEIGHT,
            fill="#4FC3F7",
        )

        self.ball = self.canvas.create_oval(
            WINDOW_WIDTH // 2 - BALL_SIZE // 2,
            WINDOW_HEIGHT - 70 - BALL_SIZE,
            WINDOW_WIDTH // 2 + BALL_SIZE // 2,
            WINDOW_HEIGHT - 70,
            fill="#E91E63",
        )

        self.bricks = []
        self.create_bricks()

        self.status_text = self.canvas.create_text(
            10,
            10,
            text=self.get_status_text(),
            anchor="nw",
            fill="#FFFFFF",
            font=("Helvetica", 14, "bold"),
        )

        root.bind("<Left>", self.move_left)
        root.bind("<Right>", self.move_right)
        root.bind("<space>", self.start_game)

        self.is_running = False
        self.update()

    def create_bricks(self):
        colors = ["#FF5722", "#FF9800", "#FFEB3B", "#8BC34A", "#2196F3"]
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x1 = col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
                y1 = row * (BRICK_HEIGHT + BRICK_PADDING) + TOP_OFFSET
                x2 = x1 + BRICK_WIDTH
                y2 = y1 + BRICK_HEIGHT
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[row], width=0)
                self.bricks.append(brick)

    def get_status_text(self):
        return f"점수: {self.score}   남은 목숨: {self.lives}   스페이스바: 시작/재시작"

    def move_left(self, event=None):
        if self.game_over:
            return
        x1, y1, x2, y2 = self.canvas.coords(self.paddle)
        if x1 > 0:
            self.canvas.move(self.paddle, -25, 0)

    def move_right(self, event=None):
        if self.game_over:
            return
        x1, y1, x2, y2 = self.canvas.coords(self.paddle)
        if x2 < WINDOW_WIDTH:
            self.canvas.move(self.paddle, 25, 0)

    def start_game(self, event=None):
        if self.game_over:
            self.reset_game()
        else:
            self.is_running = True

    def reset_ball_and_paddle(self):
        self.canvas.coords(
            self.ball,
            WINDOW_WIDTH // 2 - BALL_SIZE // 2,
            WINDOW_HEIGHT - 70 - BALL_SIZE,
            WINDOW_WIDTH // 2 + BALL_SIZE // 2,
            WINDOW_HEIGHT - 70,
        )
        self.canvas.coords(
            self.paddle,
            (WINDOW_WIDTH - PADDLE_WIDTH) // 2,
            WINDOW_HEIGHT - 40,
            (WINDOW_WIDTH + PADDLE_WIDTH) // 2,
            WINDOW_HEIGHT - 40 + PADDLE_HEIGHT,
        )
        self.ball_dx = random.choice([-4, 4])
        self.ball_dy = -4

    def reset_game(self):
        self.canvas.delete("all")
        self.score = 0
        self.lives = LIVES
        self.game_over = False
        self.is_running = False
        self.bricks.clear()
        self.create_bricks()

        self.paddle = self.canvas.create_rectangle(
            (WINDOW_WIDTH - PADDLE_WIDTH) // 2,
            WINDOW_HEIGHT - 40,
            (WINDOW_WIDTH + PADDLE_WIDTH) // 2,
            WINDOW_HEIGHT - 40 + PADDLE_HEIGHT,
            fill="#4FC3F7",
        )

        self.ball = self.canvas.create_oval(
            WINDOW_WIDTH // 2 - BALL_SIZE // 2,
            WINDOW_HEIGHT - 70 - BALL_SIZE,
            WINDOW_WIDTH // 2 + BALL_SIZE // 2,
            WINDOW_HEIGHT - 70,
            fill="#E91E63",
        )

        self.status_text = self.canvas.create_text(
            10,
            10,
            text=self.get_status_text(),
            anchor="nw",
            fill="#FFFFFF",
            font=("Helvetica", 14, "bold"),
        )

    def update_status(self):
        self.canvas.itemconfig(self.status_text, text=self.get_status_text())

    def update(self):
        if self.is_running and not self.game_over:
            self.move_ball()
            self.check_collisions()
            if not self.bricks:
                self.win_game()
        self.root.after(16, self.update)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        x1, y1, x2, y2 = self.canvas.coords(self.ball)

        if x1 <= 0 or x2 >= WINDOW_WIDTH:
            self.ball_dx = -self.ball_dx
        if y1 <= 0:
            self.ball_dy = -self.ball_dy
        if y2 >= WINDOW_HEIGHT:
            self.lives -= 1
            self.update_status()
            self.is_running = False
            if self.lives <= 0:
                self.end_game(False)
            else:
                self.reset_ball_and_paddle()

    def check_collisions(self):
        ball_coords = self.canvas.coords(self.ball)
        overlapping = self.canvas.find_overlapping(*ball_coords)
        for item in overlapping:
            if item == self.paddle:
                self.ball_dy = -abs(self.ball_dy)
                paddle_coords = self.canvas.coords(self.paddle)
                paddle_center = (paddle_coords[0] + paddle_coords[2]) / 2
                ball_center = (ball_coords[0] + ball_coords[2]) / 2
                offset = (ball_center - paddle_center) / (PADDLE_WIDTH / 2)
                self.ball_dx = 6 * offset
                break
            if item in self.bricks:
                self.bricks.remove(item)
                self.canvas.delete(item)
                self.score += 10
                self.ball_dy = -self.ball_dy
                self.update_status()
                break

    def end_game(self, won):
        self.game_over = True
        self.is_running = False
        message = "승리! 다시 플레이하려면 스페이스바를 누르세요." if won else "게임 오버! 다시 시작하려면 스페이스바를 누르세요."
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            text=message,
            fill="#FFFFFF",
            font=("Helvetica", 20, "bold"),
            tags="end_message",
        )

    def win_game(self):
        self.end_game(True)

if __name__ == "__main__":
    root = tk.Tk()
    game = BrickBreaker(root)
    root.mainloop()

