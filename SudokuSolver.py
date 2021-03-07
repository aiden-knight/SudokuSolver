import LogicSolver
import RecursiveSolver
import time

def solver(grid):
    grid = LogicSolver.solve(grid)
    if checkIfSolved(grid):
        start = time.time()
        grid = convertGridToString(grid)
        print(time.time()-start)
        return (grid,False)
    else:
        grid = convertGridToString(grid)
        grid = RecursiveSolver.solve(grid)
    return (grid,True)

def convertGridToString(grid):
    gridAsText = ""
    for i in range(9):
        for j in range(9):
            if isinstance(grid[i][j],list):
                gridAsText+="0"
            else:
                gridAsText += str(grid[i][j])
    grid = None
    return gridAsText

def checkIfSolved(grid):
    for i in range(9):
        for j in range(9):
            if isinstance(grid[i][j], list):
                return False
    return True