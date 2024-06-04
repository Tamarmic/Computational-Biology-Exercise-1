import tkinter as tk
# import matplotlib.pyplot as plt
import numpy as np
import random

"""
Class for running the game in the GUI
"""

result_arrays = []


class GameOfZebra:
    def __init__(self, root, rows=80, cols=80, cell_size=5):
        self.root = root
        self.rows = rows
        self.cols = cols

        # Cell size in the GUI
        self.cell_size = cell_size

        # Bool to check if the game is running
        self.is_running = False

        # Table of cells where the game is being played
        self.canvas = tk.Canvas(
            root, width=cols * cell_size, height=rows * cell_size, bg="white"
        )
        self.canvas.pack()

        # Start the game where half of the cells are white and half are black
        half_elements = rows * cols // 2
        elements = [0] * half_elements + [1] * half_elements
        np.random.shuffle(elements)
        self.grid = np.array(elements).reshape((cols, rows))
        self.result_array = np.array([0])

        # Create the buttons and the counter at the bottom of the screen
        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.counter = 0
        self.start_button = tk.Button(root, text="Start", command=self.start_game)
        self.start_button.pack(side=tk.LEFT)
        self.iter_button = tk.Button(root, text="iterate once", command=self.iter_once)
        self.iter_button.pack(side=tk.LEFT)
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_game)
        self.stop_button.pack(side=tk.LEFT)
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_grid)
        self.clear_button.pack(side=tk.LEFT)
        # self.iter_button = tk.Button(
        #     root, text="Plot Accuracy Graph", command=self.plot_accuracy_graph
        # )
        self.iter_button.pack(side=tk.LEFT)
        self.counter_label = tk.Label(root, text=str(self.counter))
        self.counter_label.pack(side=tk.LEFT)

        # A function to draw the table
        self.draw_grid()

    """
    A function to draw the table
    Locicly transposed for easier calculations from now on
    """

    def draw_grid(self):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.cols):
                color = "black" if self.grid[col][row] == 1 else "white"
                self.canvas.create_rectangle(
                    col * self.cell_size,
                    row * self.cell_size,
                    (col + 1) * self.cell_size,
                    (row + 1) * self.cell_size,
                    outline="gray",
                    fill=color,
                )

    """
    Return a score from 1 to 100 as of how many cells on the grid have all their neighbors in the right color
    """

    def rate_grid(self):
        count = 0

        # seperate neighbors from the sides and the same lane
        sides = [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)]
        lane = [(0, -1), (0, 1)]

        # Check for each cell whether its neighbors are in the right color
        for row in range(self.rows):
            for col in range(self.cols):
                good = True
                current = self.grid[row][col]

                # For each of the neighbors
                for dr, dc in sides:
                    if (
                            self.grid[(row + dr) % self.rows][(col + dc) % self.cols]
                            == current
                    ):
                        good = False
                for dr, dc in lane:
                    if (
                            self.grid[(row + dr) % self.rows][(col + dc) % self.cols]
                            != current
                    ):
                        good = False

                # If all the neighbors are in the right color then add 1 to the count
                if good:
                    count += 1

        # Return the precentage of good cells
        return (count * 100) / (self.rows * self.cols)

    '''
    If a square is clicked then change its color
    Used mostly for checks
    '''

    def toggle_cell(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        self.grid[col][row] = 1 if self.grid[col][row] == 0 else 0
        self.draw_grid()

    '''
    Starts the game
    '''

    def start_game(self):
        if not self.is_running:
            self.is_running = True
            self.update_grid()

    '''
    Does one step of the game
    '''

    def iter_once(self):
        if not self.is_running:
            self.is_running = True
            self.update_grid()
            self.is_running = False

    '''
    Guess yourself what this one does
    '''

    def stop_game(self):
        self.is_running = False

    ''' 
    Clear the grid and resets it
    Also resets the counter
    '''

    def clear_grid(self):
        # Reset the grid
        half_elements = self.rows * self.cols // 2
        elements = [0] * half_elements + [1] * half_elements
        np.random.shuffle(elements)
        self.grid = np.array(elements).reshape((self.rows, self.cols))
        self.draw_grid()

        # Reset the counter and the previous scores of the grid
        self.counter = 0
        self.result_array = np.array([0])
        self.counter_label.config(text=str(self.counter))

    '''
    A function for ploting the accuracy graph    
    '''

    def plot_accuracy_graph(self):
        result_arrays.append(self.result_array)
        self.clear_grid()
        if len(result_arrays) == 10:
            self.plot_accuracy_graphs_side_by_side()
            self.plot_accuracy_graph1()
            self.plot_accuracy_graphs_side_by_side()
        # self.is_running = False
        # plt.plot(self.result_array)
        # plt.title(f"Plot of {self.counter} Iterations")
        # plt.xlabel("Index")
        # plt.ylabel("Accuracy")
        # plt.grid(True)
        # plt.show()

    '''
    The logic of the game
    Updates each of the cells according to its neighbors
    '''

    def update_grid(self):
        # Make sure the game is in running mode
        if not self.is_running:
            return

        # create a new grid to update the old one
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        # Choose for each cell in the grid its new color according to its neighbors
        for row in range(self.rows):
            for col in range(self.cols):
                good_neighbors = self.count_good_neighbors(row, col)

                # 17 is a random threshold that is the expetation of expectations of the sum of the neighbors in the right color
                change = 0 if 17 < good_neighbors else 1

                # Change the color of the cell if needed
                if change == 1:
                    new_grid[row][col] = 1 - self.grid[row][col]
                else:
                    new_grid[row][col] = self.grid[row][col]

        # Update the grid to be the new grid
        self.grid = new_grid

        # Update the counter and draw the grid
        self.counter += 1
        self.counter_label.config(text=str(self.counter))
        self.draw_grid()

        # Keep the loop running
        self.root.after(100, self.update_grid)
        self.result_array = np.append(self.result_array, self.rate_grid())

        # After 250 iterations print the results graph
        if self.counter == 250:
            self.plot_accuracy_graph()

    '''
    Aid function for 'update_grid'
    Returns a score of how good are the neighbors
    The avarage is 17
    Uses non-deterministic choices
    '''

    def count_good_neighbors(self, row, col):
        directions = [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)]
        score = 0

        # For all neighbors on the sides
        for dr, dc in directions:
            r, c = row + dr, col + dc

            # If out of bounds
            if r >= self.rows:
                if self.grid[row][col]:
                    score += random.randint(3, 7)
            elif c >= self.cols:
                if self.grid[row][col] != row % 2:
                    return 0
                return 20

            # For any other case
            else:
                if self.grid[r][c] != self.grid[row][col]:
                    score += random.randint(3, 7)

        # Add score for the cells above and below
        directions = [(0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = (row + dr) % self.rows, (col + dc) % self.cols
            if self.grid[r][c] == self.grid[row][col]:
                score += random.randint(1, 3)
        return score

    # def plot_accuracy_graph1(self):
    #     plt.figure(figsize=(10, 6))
    #     for i, result in enumerate(result_arrays):
    #         plt.plot(result, label=f'Iteration {i + 1}')
    #     plt.title("Plot of 10 Iterations")
    #     plt.xlabel("Index")
    #     plt.ylabel("Accuracy")
    #     plt.legend()
    #     plt.grid(True)
    #     plt.savefig('all_iterations_on_single_plot.png')  # Save the figure
    #     print("hi")
    #     plt.show()
    #
    # def plot_accuracy_graphs_side_by_side(self):
    #     fig, axs = plt.subplots(2, 5, figsize=(20, 8), sharey=True)
    #     fig.suptitle("Plots of 10 Iterations Side by Side")
    #     for i, result in enumerate(result_arrays):
    #         row, col = divmod(i, 5)
    #         axs[row, col].plot(result)
    #         axs[row, col].set_title(f'Iteration {i + 1}')
    #         axs[row, col].set_xlabel("Index")
    #         axs[row, col].set_ylabel("Accuracy")
    #         axs[row, col].grid(True)
    #     plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    #     plt.savefig('side_by_side_iterations.png')  # Save the figure
    #     print("hi")
    #     plt.show()
    #

"""
Main function
"""
if __name__ == "__main__":
    # for i in range(3):
    root = tk.Tk()
    root.title("Tamar's and Sarel's Game of Zebra")
    game = GameOfZebra(root)
    root.mainloop()
    print(result_arrays)
    # plot_accuracy_graphs_side_by_side()
    # plot_accuracy_graph1()
    # plot_accuracy_graphs_side_by_side()
