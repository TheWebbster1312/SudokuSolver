# Sudoku Solver
import time
import math
#======= Sudoku grid

class soduku_grid:
    def __init__(self):
        self.grid = [[0 for x in range(1, 10)] for x in range(1,10)]
        self.possibilities_grid = [[[] for x in range(1, 10)] for x in range(1,10)]
        self.ref_nums = [_ for _ in range(1, 10)]

    def show(self):
        print_str = ""
        for i, x in enumerate(self.grid):
            if i == 0:
                print_str += " ┌───────┬───────┬───────┐\n"
            elif i % 3 == 0:
                print_str += " ├───────┼───────┼───────┤\n"

            for j, y in enumerate(x):
                if j == 0 or j % 3 == 0:
                    print_str += " │"

                print_str += " " + str(y) 
            print_str += " │\n"
        print_str += " └───────┴───────┴───────┘\n"
        print(print_str)

    def set_row(self, a, b):
        if type(a) == int and type(b) == list:
            self.grid[a] = b
        else:
            self.grid[a, b]
    
    def set(self, x, y, a):
        self.grid[y][x] = a
    
    def get(self, x, y):
        return self.grid[y][x]
    
    def get_flat_grid(self):
        return_list = [x for sub in self.grid for x in sub]
        
        return return_list
    
    def get_col(self, x, y):
        return_list = []

        for i in self.grid:
            return_list.append(i[x])
        return return_list
    
    def get_row(self, x, y):
        return self.grid[y]
    
    def get_subgrid_bounds(self, x, y):
        # x bounds 
        xbounds = []
        if x > 2 and x < 6:
            xbounds = [_ for _ in range(3, 6)]
        elif x > 5:
            xbounds = [_ for _ in range(6, 9)]
        else:
            xbounds = [_ for _ in range(0, 3)]
        
        # y bounds 
        ybounds = []
        if y > 2 and y < 6:
            ybounds = [_ for _ in range(3, 6)]
        elif y > 5:
            ybounds = [_ for _ in range(6, 9)]
        else:
            ybounds = [_ for _ in range(0, 3)]
        
        return [xbounds, ybounds]
    
    def get_subgrid(self, x, y):
        
        # getting bounds
        
        xbounds, ybounds = self.get_subgrid_bounds(x, y)
        
        return_list = []

        for y in ybounds:
            for x in xbounds:
                return_list.append(self.get(x, y))
        
        return return_list
    
    def get_subgrid_possibilities(self, x, y):
        # getting bounds
        
        xbounds, ybounds = self.get_subgrid_bounds(x, y)
        
        return_list = []
        
        for y in ybounds:
            for x in xbounds:
                return_list.append(self.get_possibilities(x, y))
                
        return return_list
    

    def get_possibilities(self, x, y):
        if self.get(x, y) != 0:
            return []
        
        # get data
        cols = self.get_col(x, y)
        rows = self.get_row(x, y)
        box = self.get_subgrid(x, y)

        # compare to reference list

        possibilities = [x for x in self.ref_nums if (x not in cols and x not in rows and x not in box)]
        self.possibilities_grid[y][x] = possibilities

        return possibilities
    
    def subgrid_context_refinement(self, x, y):
        # get subgrid possibilities
        
        data = self.get_subgrid_possibilities(x, y)
        
        # counting frequency of numbers
        
        frequency_tally = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
        
        for i in data:
            for j in i:
                frequency_tally[j] += 1
            
        certainties = []
        
        for number, frequency in frequency_tally.items():
            if frequency == 1:
                certainties.append(number)
        
        # for certainties 
        
        xbounds, ybounds = self.get_subgrid_bounds(x, y)
        
        base_grid_coord = [xbounds[0], ybounds[0]]
        
        for number in certainties:
            for index, possibilities in enumerate(data):
                    if number in possibilities:
                        x_ = base_grid_coord[0] + index % 3
                        y_ = base_grid_coord[1] + math.floor(index / 3)
                        self.set(x_, y_, number)
                        print("│")
                        print(f"└─ Filling in ({x_}, {y_}) as {number}")
        if len(certainties) > 0:
            return True
        else:
            return False
        
                      
        

    def is_solved(self):
        if 0 in self.get_flat_grid():
            return False
        else:
            return True
    
    def check_list(self, sample):
        return_bool = True
        for i in self.ref_nums:
            if i not in sample:
                return_bool = False
        return return_bool

    
    def check_solution(self):
        for i in range(0, 9):
            if not self.check_list(self.get_col(i, 0)):
                return False
        for i in range(0, 9):
            if not self.check_list(self.get_row(0, i)):
                return False
        return True
        


    def solve(self):
        while not self.is_solved():
            changes = 0
            previous_grid = [x for x in self.grid]
            for x in range(0, 9):
                for y in range(0, 9):
                    num = self.get(x, y)
                    if num != 0:
                        continue
                    possibilities = self.get_possibilities(x, y)
                    #print(f"({x}, {y}): {possibilities}")

                    if len(possibilities) == 1:
                        print("│")
                        print(f"└─ Filling in ({x}, {y}) as {possibilities[0]}")
                        self.set(x, y, possibilities[0])
                        changes += 1
                    else:
                        if self.subgrid_context_refinement(x, y):
                            changes += 1
                        
            self.show()
            time.sleep(5)
            #time.sleep(5)
        
            if changes == 0:
               print("==========Unsolvable by this algorythim!=============")
               break
        print("Finished!")
        print(f"Checking solution: {self.check_solution()}")

        


puzzle = soduku_grid()

puzzle.set_row(0, [0, 5, 8, 0, 0, 0, 0, 0, 0])
puzzle.set_row(1, [0, 0, 2, 0, 8, 7, 9, 0, 0])
puzzle.set_row(2, [0, 0, 0, 0, 0, 4, 0, 0, 0])

puzzle.set_row(3, [0, 6, 0, 0, 0, 0, 0, 3, 0])
puzzle.set_row(4, [3, 0, 0, 0, 6, 0, 5, 0, 0])
puzzle.set_row(5, [0, 0, 0, 5, 0, 8, 7, 0, 4])

puzzle.set_row(6, [0, 9, 6, 3, 0, 0, 0, 7, 0])
puzzle.set_row(7, [0, 0, 1, 0, 0, 0, 0, 0, 9])
puzzle.set_row(8, [0, 0, 0, 8, 0, 0, 2, 5, 0])

puzzle.show()

print(puzzle.get_row(0, 0))
print(puzzle.get_col(0, 0))
print(puzzle.get_subgrid(3, 8))

puzzle.subgrid_context_refinement(5, 4)

puzzle.is_solved()

puzzle.solve()


