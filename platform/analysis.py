import re

cellPattern = re.compile(r'([A-Za-z]+)(\d+)')


def column_to_num(col: str):
    num = 0
    for char in col:
        num = num * 26 + (ord(char.upper()) - ord('A') + 1)
    return num


class Cell:
    def __init__(self, input: str):
        match = cellPattern.match(input)
        self.col, self.row = match.group(1), int(match.group(2))

    def __sub__(self, other):
        assert (isinstance(other, Cell))
        return self.row - other.row + 1, column_to_num(self.col) - column_to_num(other.col) + 1


class Section:
    def __init__(self, sheet: str, cellL: Cell, cellR: Cell, data: list):
        self.sheet, self.cellL, self.cellR, self.data = sheet, cellL, cellR, data
        self.width, self.height = self.cellR - self.cellL
        pass


def getSection(input: str, data: list):
    sheet, r = input.split("!")
    cellL, cellR = [Cell(x) for x in r.split(":")]
    return Section(sheet, cellL, cellR, data)


class Analysis:
    def __init__(self, msg: dict):
        self.inputSection = getSection(msg['inputRange'], msg['inputData'])
        self.outputSection = getSection(msg['outputRange'], msg['outputData'])
        pass
