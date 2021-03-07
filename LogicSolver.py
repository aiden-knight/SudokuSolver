import copy


def check(firstRun, grid):
    for i in range(9):  # Row = i
        for j in range(9):  # Column = j
            if grid[i][j] == None:
                possibleValues = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            elif isinstance(grid[i][j], list):
                possibleValues = list(grid[i][j])
            else:
                possibleValues = []

            if len(possibleValues) > 0:
                possibleValues = checkColumn(possibleValues, j, grid)
                possibleValues = checkRow(possibleValues, i, grid)
                possibleValues = checkSquare(possibleValues, i, j, grid)
                checkValues(possibleValues, i, j, firstRun, grid)


def cleverCheck(grid):
    checkSubRows(grid)
    checkSubColumns(grid)


def checkColumn(possibleValues, pos, grid):
    for k in range(9):
        for value in possibleValues:
            if grid[k][pos] == value:
                possibleValues.remove(value)
    return possibleValues


def checkRow(possibleValues, pos, grid):
    for k in range(9):
        for value in possibleValues:
            if grid[pos][k] == value:
                possibleValues.remove(value)
    return possibleValues


def checkSquare(possibleValues, pos1, pos2, grid):
    pos1 = int(pos1/3) * 3
    pos2 = int(pos2/3) * 3

    for k in range(3):
        for l in range(3):
            for value in possibleValues:
                if value == grid[pos1+k][pos2+l]:
                    possibleValues.remove(value)
    return possibleValues


def checkValues(possibleValues, pos1, pos2, firstRun, grid):
    if len(possibleValues) == 1:
        grid[pos1][pos2] = possibleValues[0]
        return
    elif not firstRun:
        if checkUniqueSquare(possibleValues, pos1, pos2, grid):
            return
        if checkUniqueColumn(possibleValues, pos1, pos2, grid):
            return
        if checkUniqueRow(possibleValues, pos1, pos2, grid):
            return
    grid[pos1][pos2] = possibleValues


def checkUniqueSquare(possibleValues, pos1, pos2, grid):
    posForCheck1 = int(pos1/3) * 3
    posForCheck2 = int(pos2/3) * 3

    values = []  # Add Values that could be other possibilities in square
    for k in range(3):
        for l in range(3):
            if pos1 != posForCheck1 + k or pos2 != posForCheck2 + l:  # Not comparing with own cell
                cell = grid[posForCheck1+k][posForCheck2+l]
                values = checkPossibleValues(values, cell, grid)
    return checkUnique(possibleValues, values, pos1, pos2, grid)


def checkUniqueColumn(possibleValues, pos1, pos2, grid):
    values = []
    for k in range(9):  # check columns
        if k != pos1:  # Don't compare with own cell
            cell = grid[k][pos2]
            values = checkPossibleValues(values, cell, grid)
    return checkUnique(possibleValues, values, pos1, pos2, grid)


def checkUniqueRow(possibleValues, pos1, pos2, grid):
    values = []
    for l in range(9):  # check rows
        if l != pos2:  # Don't compare with own cell
            cell = grid[pos1][l]
            values = checkPossibleValues(values, cell, grid)
    return checkUnique(possibleValues, values, pos1, pos2, grid)


def checkUnique(possibleValues, values, pos1, pos2, grid):
    for number in possibleValues:
        if not number in values:
            grid[pos1][pos2] = number
            return True
    return False


def checkPossibleValues(values, cell, grid):
    if not isinstance(cell, list):
        if not cell in values:
            values.append(cell)
    else:
        for number in cell:
            if not number in values:
                values.append(number)
    return values


def checkSubColumns(grid):
    for column in range(9):
        for square in range(3):
            cellValue1 = grid[(square*3)][column]
            cellValue2 = grid[(square*3)+1][column]
            cellValue3 = grid[(square*3)+2][column]

            # Compare first cell with second
            common1 = common2 = common3 = []
            if isinstance(cellValue1, list) and isinstance(cellValue2, list):
                common1 = intersection(cellValue1, cellValue2)

            # Compare first cell with third
            if isinstance(cellValue1, list) and isinstance(cellValue3, list):
                common2 = intersection(cellValue1, cellValue3)

            # Compare second cell with third
            if isinstance(cellValue2, list) and isinstance(cellValue3, list):
                common3 = intersection(cellValue2, cellValue3)

            allCommon = list(set(common1) | set(common2) |
                             set(common3))  # Union 3 common lists
            allCommon = removeNonUniqueInSquareColumns(
                allCommon, square, column, grid)
            if len(allCommon) > 0:
                removeCommonFromColumn(allCommon, square, column, grid)


def checkSubRows(grid):
    for row in range(9):
        for square in range(3):
            cellValue1 = grid[row][(square*3)]
            cellValue2 = grid[row][(square*3)+1]
            cellValue3 = grid[row][(square*3)+2]

            # Compare first cell with second
            common1 = common2 = common3 = []
            if isinstance(cellValue1, list) and isinstance(cellValue2, list):
                common1 = intersection(cellValue1, cellValue2)

            # Compare first cell with third
            if isinstance(cellValue1, list) and isinstance(cellValue3, list):
                common2 = intersection(cellValue1, cellValue3)

            # Compare second cell with third
            if isinstance(cellValue2, list) and isinstance(cellValue3, list):
                common3 = intersection(cellValue2, cellValue3)

            allCommon = list(set(common1) | set(common2) |
                             set(common3))  # Union 3 common lists
            allCommon = removeNonUniqueInSquareRows(
                allCommon, square, row, grid)
            if len(allCommon) > 0:
                removeCommonFromRow(allCommon, square, row, grid)


def removeNonUniqueInSquareColumns(values, square, valuesColumn, grid):
    for column in range(3):
        if column == (valuesColumn % 3):
            continue  # Don't remove from values column
        for row in range(3):
            cellValue = grid[(square*3)+row][(int(valuesColumn/3)*3)+column]
            if isinstance(cellValue, list):
                clashing = intersection(values, cellValue)
                values = [value for value in values if value not in clashing]
    return values


def removeNonUniqueInSquareRows(values, square, valuesRow, grid):
    for row in range(3):
        if row == (valuesRow % 3):
            continue  # Don't remove from values row
        for column in range(3):

            cellValue = grid[(int(valuesRow/3)*3)+row][(square*3)+column]
            if isinstance(cellValue, list):
                clashing = intersection(values, cellValue)
                values = [value for value in values if value not in clashing]
    return values


def removeCommonFromColumn(values, valuesSquare, valuesColumn, grid):
    for square in range(3):
        if square == valuesSquare:
            continue
        for row in range(3):
            cellValue = grid[(square*3)+row][valuesColumn]
            if isinstance(cellValue, list):
                cellValue = [
                    value for value in cellValue if value not in values]
                if len(cellValue) == 1:
                    grid[(square*3)+row][valuesColumn] = cellValue[0]
                else:
                    grid[(square*3)+row][valuesColumn] = cellValue


def removeCommonFromRow(values, valuesSquare, valuesRow, grid):
    for square in range(3):
        if square == valuesSquare:
            continue
        for column in range(3):
            cellValue = grid[valuesRow][(square*3)+column]
            if isinstance(cellValue, list):
                cellValue = [
                    value for value in cellValue if value not in values]
                if len(cellValue) == 1:
                    grid[valuesRow][(square*3)+column] = cellValue[0]
                else:
                    grid[valuesRow][(square*3)+column] = cellValue


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def removeNumber(grid, row, column, number):
    removeNumberFromRow(grid, row, column, number)
    removeNumberFromColumn(grid, row, column, number)
    removeNumberFromSquare(grid, row, column, number)


def removeNumberFromRow(grid, numberRow, numberColumn, number):
    # rowValues = [number]
    for column in range(9):
        if column == numberColumn:
            continue  # Don't remove self
        if isinstance(grid[numberRow][column], list):
            try:
                grid[numberRow][column].remove(number)
            except:
                pass
            if len(grid[numberRow][column]) == 1:
                grid[numberRow][column] = grid[numberRow][column][0]
                removeNumber(grid, numberRow, column, grid[numberRow][column])
        # if isinstance(grid[numberRow][column], int):
        #     cellNumber = grid[numberRow][column]
        #     if cellNumber in rowValues:
        #         return False  # Invalid row
        #     rowValues.append(cellNumber)
    return True


def removeNumberFromColumn(grid, numberRow, numberColumn, number):
    # columnValues = [number]
    for row in range(9):
        if row == numberRow:
            continue  # Don't remove self
        if isinstance(grid[row][numberColumn], list):
            try:
                grid[row][numberColumn].remove(number)
            except:
                pass
            if len(grid[row][numberColumn]) == 1:
                grid[row][numberColumn] = grid[row][numberColumn][0]
                removeNumber(grid, row, numberColumn, grid[row][numberColumn])
        # if isinstance(grid[row][numberColumn], int):
        #     cellNumber = grid[row][numberColumn]
        #     if cellNumber in columnValues:
        #         return False  # Invalid column
        #     columnValues.append(cellNumber)
    return True


def removeNumberFromSquare(grid, numberRow, numberColumn, number):
    startSquareRow = int(numberRow/3) * 3
    startSquareColumn = int(numberColumn/3) * 3

    # squareValues = [number]
    for k in range(3):
        for l in range(3):
            row = startSquareRow+k
            column = startSquareColumn+l
            if row == numberRow and column == numberColumn:
                continue  # Don't remove self
            if isinstance(grid[row][column], list):
                try:
                    grid[row][column].remove(number)
                except:
                    pass
                if len(grid[row][column]) == 1:
                    grid[row][column] = grid[row][column][0]
                    removeNumber(grid, row, column, grid[row][column])
            # if isinstance(grid[row][column], int):
            #     cellNumber = grid[row][column]
            #     if cellNumber in squareValues:
            #         return False  # Invalid square
            #     squareValues.append(cellNumber)
    return True


def checkNumber(grid, row, column, number):
    if not checkNumberFromRow(grid, row, column, number):
        return False
    if not checkNumberFromColumn(grid, row, column, number):
        return False
    if not checkNumberFromSquare(grid, row, column, number):
        return False
    return True


def checkNumberFromRow(grid, numberRow, numberColumn, number):
    rowValues = [number]
    for column in range(9):
        if column == numberColumn:
            continue  # Don't check self
        if isinstance(grid[numberRow][column], int):
            cellNumber = grid[numberRow][column]
            if cellNumber in rowValues:
                return False
            else:
                rowValues.append(cellNumber)
    return True


def checkNumberFromColumn(grid, numberRow, numberColumn, number):
    columnValues = [number]
    for row in range(9):
        if row == numberRow:
            continue  # Don't check self
        if isinstance(grid[row][numberColumn], int):
            cellNumber = grid[row][numberColumn]
            if cellNumber in columnValues:
                return False
            else:
                columnValues.append(cellNumber)
    return True


def checkNumberFromSquare(grid, numberRow, numberColumn, number):
    startSquareRow = int(numberRow/3) * 3
    startSquareColumn = int(numberColumn/3) * 3

    squareValues = [number]
    for k in range(3):
        for l in range(3):
            row = startSquareRow+k
            column = startSquareColumn+l
            if row == numberRow and column == numberColumn:
                continue  # Don't check self
            if isinstance(grid[row][column], int):
                cellNumber = grid[row][column]
                if cellNumber in squareValues:
                    return False
                else:
                    squareValues.append(cellNumber)
    return True


def checkValid(grid):
    for row in range(9):
        columnValues = []
        for column in range(9):
            if isinstance(grid[row][column], int):
                cellNumber = grid[row][column]
                if cellNumber in columnValues:
                    return False  # Invalid column
                columnValues.append(cellNumber)

    for column in range(9):
        rowValues = []
        for row in range(9):
            if isinstance(grid[row][column], int):
                cellNumber = grid[row][column]
                if cellNumber in rowValues:
                    return False  # Invalid row
                rowValues.append(cellNumber)

    for squareRow in range(3):
        for squareColumn in range(3):
            squareValues = []
            for cellRow in range(3):
                for cellColumn in range(3):
                    row = (squareRow*3)+cellRow
                    column = (squareColumn*3)+cellColumn
                    if isinstance(grid[row][column], int):
                        cellNumber = grid[row][column]
                        if cellNumber in squareValues:
                            return False  # Invalid row
                        squareValues.append(cellNumber)
    return True

def recursiveSolve(grid):
    solved = True
    for row in range(9):
        for column in range(9):
            if grid[row][column]==None:
                solved = False
                possibleValues = [1,2,3,4,5,6,7,8,9]
                possibleValues = checkColumn(possibleValues, column, grid)
                possibleValues = checkRow(possibleValues, row, grid)
                possibleValues = checkSquare(possibleValues, row, column, grid)
                newGrid = copy.deepcopy(grid)
                # Check possible values against logic possible values
                for possibleValue in possibleValues:
                    newGrid[row][column] = possibleValue
                    solvedGrid = recursiveSolve(newGrid)
                    if solvedGrid != None:
                        return solvedGrid
                return None
    if solved:   
        return grid
            
def solve(grid):
    check(True, grid)
    i = 1
    while True:
        # print("Iteration %d" % i)
        i += 1
        stable = False
        j = 1
        while not stable:
            # print("  Sub-Iteration %d" % j)
            j += 1
            previousGrid = copy.deepcopy(grid)
            check(False, grid)
            if previousGrid == grid:
                stable = True
        previousGrid = copy.deepcopy(grid)
        cleverCheck(grid)
        if previousGrid == grid:
            return grid