import random
import tkinter as tk

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
GAME_SPEED = 100  # milliseconds between moves

DIRECTIONS = {
    "Left": (-1, 0),
    "Right": (1, 0),
    "Up": (0, -1),
    "Down": (0, 1),
}
OPPOSITE = {
    "Left": "Right",
    "Right": "Left",
    "Up": "Down",
    "Down": "Up",
}

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake vs AI")

        self.canvas = tk.Canvas(
            master,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg="black",
        )
        self.canvas.pack()

        self.master.bind('<Key>', self.on_key_press)
        self.running = True
        self.reset_game()
        self.game_loop()

    def reset_game(self):
        self.human = {
            "body": [
                (GRID_WIDTH // 4, GRID_HEIGHT // 2),
                (GRID_WIDTH // 4 - 1, GRID_HEIGHT // 2),
                (GRID_WIDTH // 4 - 2, GRID_HEIGHT // 2),
            ],
            "direction": "Right",
            "next_direction": "Right",
            "length": 3,
            "score": 0,
            "alive": True,
        }
        self.ai = {
            "body": [
                (GRID_WIDTH * 3 // 4, GRID_HEIGHT // 2),
                (GRID_WIDTH * 3 // 4 + 1, GRID_HEIGHT // 2),
                (GRID_WIDTH * 3 // 4 + 2, GRID_HEIGHT // 2),
            ],
            "direction": "Left",
            "next_direction": "Left",
            "length": 3,
            "score": 0,
            "alive": True,
        }
        self.place_food()
        self.update_score_text()
        self.running = True

    def place_food(self):
        while True:
            food = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1),
            )
            if food not in self.human["body"] and food not in self.ai["body"]:
                self.food = food
                break

    def update_score_text(self):
        self.master.title(
            f"Snake vs AI - Human: {self.human['score']}  AI: {self.ai['score']}"
        )

    def on_key_press(self, event):
        key = event.keysym
        if key in DIRECTIONS:
            self.set_direction(self.human, key)
        elif key == "space" and not self.running:
            self.restart()

    def set_direction(self, snake, key):
        if key != OPPOSITE[snake["direction"]]:
            snake["next_direction"] = key

    def game_loop(self):
        if not self.running:
            return

        if self.human["alive"]:
            self.human["direction"] = self.human["next_direction"]
        if self.ai["alive"]:
            self.ai_decide()
            self.ai["direction"] = self.ai["next_direction"]

        self.move_snake(self.human)
        self.move_snake(self.ai)
        self.draw()

        if self.human["alive"] or self.ai["alive"]:
            self.master.after(GAME_SPEED, self.game_loop)
        else:
            self.game_over()

    def move_snake(self, snake):
        if not snake["alive"]:
            return

        head_x, head_y = snake["body"][0]
        dx, dy = DIRECTIONS[snake["direction"]]
        new_head = (head_x + dx, head_y + dy)

        if self.is_collision(new_head, snake):
            snake["alive"] = False
            return

        snake["body"].insert(0, new_head)

        if new_head == self.food:
            snake["score"] += 10
            snake["length"] += 1
            self.place_food()
            self.update_score_text()
        else:
            while len(snake["body"]) > snake["length"]:
                snake["body"].pop()

    def is_collision(self, position, snake):
        x, y = position
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return True
        if position in snake["body"]:
            return True
        opponent = self.ai if snake is self.human else self.human
        if position in opponent["body"]:
            return True
        return False

    def ai_decide(self):
        if not self.ai["alive"]:
            return

        head = self.ai["body"][0]
        options = []
        for key, (dx, dy) in DIRECTIONS.items():
            if key == OPPOSITE[self.ai["direction"]]:
                continue
            candidate = (head[0] + dx, head[1] + dy)
            if self.is_collision(candidate, self.ai):
                continue
            distance = abs(candidate[0] - self.food[0]) + abs(candidate[1] - self.food[1])
            options.append((distance, key))

        if options:
            self.ai["next_direction"] = min(options, key=lambda item: item[0])[1]

    def draw(self):
        self.canvas.delete("all")
        self.draw_cell(self.food, "red")

        if self.ai["alive"]:
            for index, segment in enumerate(self.ai["body"]):
                color = "cyan" if index == 0 else "blue"
                self.draw_cell(segment, color)

        if self.human["alive"]:
            for index, segment in enumerate(self.human["body"]):
                color = "yellow" if index == 0 else "lime"
                self.draw_cell(segment, color)

        score_text = (
            f"Human: {self.human['score']}  AI: {self.ai['score']}"
            + ("  (Press Space to Restart)" if not self.running else "")
        )
        self.canvas.create_text(
            10,
            10,
            anchor="nw",
            text=score_text,
            fill="white",
            font=("Arial", 12),
        )

    def draw_cell(self, position, color):
        x, y = position
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def game_over(self):
        self.running = False
        winner = self.determine_winner()
        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE // 2,
            GRID_HEIGHT * CELL_SIZE // 2,
            text=(
                f"Game Over\n"
                f"Human: {self.human['score']}  AI: {self.ai['score']}\n"
                f"Winner: {winner}\n"
                "Press Space to Restart"
            ),
            fill="white",
            font=("Arial", 18),
            justify="center",
        )

    def determine_winner(self):
        if self.human["score"] > self.ai["score"]:
            return "Human"
        if self.ai["score"] > self.human["score"]:
            return "AI"
        return "Draw"

    def restart(self):
        self.reset_game()
        self.game_loop()

if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()
