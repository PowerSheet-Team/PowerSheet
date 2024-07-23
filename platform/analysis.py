import re

cellPattern = re.compile(r'([A-Za-z]+)(\d+)')
replyPattern = re.compile(r'<CELL>(.*?)</CELL>')


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

    def get_index_str(self):
        return f"{self.col}{self.row}"


class Section:
    def __init__(self, sheet: str, cellL: Cell, cellR: Cell, data: list):
        self.sheet, self.cellL, self.cellR, self.data = sheet, cellL, cellR, data
        self.width, self.height = self.cellR - self.cellL
        self.range = f"{self.cellL.get_index_str()}:{self.cellR.get_index_str()}"
        pass


def getSection(input: str, data: list):
    sheet, r = input.split("!")
    cells = [Cell(x) for x in r.split(":")]
    if len(cells) == 1:
        cellL = cellR = cells[0]
    else:
        cellL, cellR = cells
    return Section(sheet, cellL, cellR, data)


class Analysis:
    def __init__(self, msg: dict):
        self.inputSection = getSection(msg['inputRange'], msg['inputData'])
        self.outputSection = getSection(msg['outputRange'], msg['outputData'])
        self.desc = msg['description']
        pass

    def gen_query(self):
        query_str = (
            f"I have an Excel sheet, and a section from {self.inputSection.cellL.get_index_str()} to {self.inputSection.cellR.get_index_str()}. The content is {self.inputSection.data}. "
            f"Now I want you to fill {self.outputSection.cellL.get_index_str()} and {self.outputSection.cellR.get_index_str()} with data or formula. I want to fill in the way that \"{self.desc}\". "
            f"You should output the content of each cell, in column-major order, one line for a single cell. WRAP THE CELL "
            f"CONTENT in <CELL></CELL> and only wrap them ONCE. You are expected to output at least "
            f"{self.outputSection.width * self.outputSection.height} lines. You are encouraged to use formula if it "
            f"is appliable. You should only generate one possible solution, and only output ONCE for each cell in "
            f"<CELL></CELL>. Don't output the additional evaluated result of formulas. Think step by step.")
        return query_str

    def apply_reply(self, reply: str):
        cell_contents = replyPattern.findall(reply)
        print(cell_contents)
        index = 0
        print(self.outputSection.data)
        for col in range(len(self.outputSection.data)):
            for row in range(len(self.outputSection.data[col])):
                self.outputSection.data[col][row] = cell_contents[index]
                index += 1
        print(cell_contents)
        return self.outputSection.data
        pass
