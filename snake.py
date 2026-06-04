import random
import tkinter as tk

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
GAME_SPEED = 100  # milliseconds between moves

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.score = 0
        self.direction = "Right"
        self.next_direction = self.direction

        self.canvas = tk.Canvas(
            master,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg="black",
        )
        self.canvas.pack()

        self.reset_game()
        self.master.bind('<Key>', self.on_key_press)
        self.running = True
        self.game_loop()

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.snake_length = 5
        self.place_food()
        self.update_score_text()

    def place_food(self):
        while True:
            self.food = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
            if self.food not in self.snake:
                break

    def update_score_text(self):
        self.master.title(f"Snake Game - Score: {self.score}")

    def on_key_press(self, event):
        key = event.keysym
        if key in ["Left", "Right", "Up", "Down"]:
            self.set_direction(key)
        elif key == "space" and not self.running:
            self.restart()

    def set_direction(self, key):
        opposite = {
            "Left": "Right",
            "Right": "Left",
            "Up": "Down",
            "Down": "Up",
        }
        if key != opposite.get(self.direction):
            self.next_direction = key

    def game_loop(self):
        if self.running:
            self.direction = self.next_direction
            self.move_snake()
            self.draw()
            self.master.after(GAME_SPEED, self.game_loop)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == "Left":
            head_x -= 1
        elif self.direction == "Right":
            head_x += 1
        elif self.direction == "Up":
            head_y -= 1
        elif self.direction == "Down":
            head_y += 1

        new_head = (head_x, head_y)

        if self.is_collision(new_head):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.snake_length += 1
            self.place_food()
            self.update_score_text()
        else:
            while len(self.snake) > self.snake_length:
                self.snake.pop()

    def is_collision(self, position):
        x, y = position
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return True
        if position in self.snake:
            return True
        return False

    def draw(self):
        self.canvas.delete("all")
        self.draw_cell(self.food, "red")
        for index, segment in enumerate(self.snake):
            color = "lime" if index == 0 else "green"
            self.draw_cell(segment, color)

    def draw_cell(self, position, color):
        x, y = position
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def game_over(self):
        self.running = False
        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE // 2,
            GRID_HEIGHT * CELL_SIZE // 2,
            text=f"Game Over\nScore: {self.score}\nPress Space to Restart",
            fill="white",
            font=("Arial", 18),
            justify="center",
        )

    def restart(self):
        self.score = 0
        self.direction = "Right"
        self.next_direction = self.direction
        self.snake_length = 5
        self.running = True
        self.reset_game()
        self.game_loop()

if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()
