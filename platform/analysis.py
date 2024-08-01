import re

cellPattern = re.compile(r'([A-Za-z]+)(\d+)')
replyPattern = re.compile(r'<CELL>(.*?)</CELL>')
codePattern = re.compile(r'<CODE>(.*?)</CODE>')
warnPattern = re.compile(r'<WARN>(.*?)</WARN>')
passPattern = re.compile(r'<PASS>(.*?)</PASS>')
typePattern = re.compile(r'<TYPE>(.*?)</TYPE>')
titlePattern = re.compile(r'<TITLE>(.*?)</TITLE>')
formulaList = ["SUM", "AVERAGE", "COUNT", "SUBTOTAL", "MODULUS", "POWER", "CEILING", "FLOOR", "CONCATENATE", "LEN",
               "REPLACE", "SUBSTITUTE", "LEFT", "RIGHT", "MID", "UPPER", "LOWER", "PROPER", "TIME", "VLOOKUP",
               "COUNTIF", "SUMIF"]
chartTypes = ["Line", "Pie", "Waterfall", "Radar"]


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
        if "outputRange" in msg.keys():
            self.outputSection = getSection(msg['outputRange'], msg['outputData'])
        self.desc = msg['description']
        pass

    def gen_query(self):
        query_str = (
            f"I have an Excel sheet, and a section from {self.inputSection.cellL.get_index_str()} to {self.inputSection.cellR.get_index_str()}."
            f"Now I want you to fill {self.outputSection.cellL.get_index_str()} to {self.outputSection.cellR.get_index_str()} with data or formula. I want to fill in the way that \"{self.desc}\". ")
        return query_str

    def gen_summary_query(self):
        query_str = (
            f"I have an Excel sheet, and a section from {self.inputSection.cellL.get_index_str()} to {self.inputSection.cellR.get_index_str()}. The content is {self.inputSection.data}. "
            f"Now I want you to output the summary of these data.")
        return query_str

    def gen_exp_explain_query(self):
        query_str = (
            f"I have an Excel sheet, and a section of formulas from {self.inputSection.cellL.get_index_str()} to {self.inputSection.cellR.get_index_str()}. The content is {self.inputSection.data}. "
            f"Now I want you to explain these formulas. You should be consice.")
        return query_str

    def gen_formula_pbe_query(self):
        query_str = (
            f"I have an Excel sheet, and a section from {self.inputSection.cellL.get_index_str()} to {self.inputSection.cellR.get_index_str()}. The content is {self.inputSection.data}. "
            f"Now I want you to fill {self.outputSection.cellL.get_index_str()} to {self.outputSection.cellR.get_index_str()} with formula, "
            f"which would yield result of {self.outputSection.data}. I want to fill in the way that \"{self.desc}\". "
            f"You should output the content of each cell, in column-major order, one line for a single cell. WRAP THE CELL "
            f"CONTENT in <CELL></CELL> and only wrap them ONCE. You are expected to output at least "
            f"{self.outputSection.width * self.outputSection.height} lines. You should only generate one possible solution,"
            f" and only output ONCE for each cell in "
            f"<CELL></CELL>. Don't output the additional evaluated result of formulas. Think step by step.")
        return query_str

    @staticmethod
    def gen_range_sel_query(requirement: str):
        query_str = (
            f"I have an variable named \"value\", and I want you to output a very simple javascript one-line statement that, if {requirement}, the statement will be evaluated to true, otherwise it will be evaluated to false"
            f"You are required to output the one-line statement wrapped in <CODE></CODE>. Think step by step.")
        return query_str

    @staticmethod
    def gen_batchproc_query(requirement: str):
        query_str = (
            f"I have an variable named \"value\", and I want you to output a very simple javascript one-line expression that, the value evaluated to {requirement}."
            f"You are required to output the one-line expression wrapped in <CODE></CODE>. Think step by step.")
        return query_str

    def gen_formula_chk_query(self):
        query_str = (
            "It is known that Microsoft Excel has some compatibility issue with LibreOffice Calc. "
            "1. Functions like XLOOKUP may not be supported in LibreOffice. "
            "2. Formulas related to date and time may be not compatible. "
            "3. Formulas with brace {} may be not compatible."
            "4. Formulas with \"|\" may be not compatible. "
            f"I have a range of data with formula: {self.inputSection.data}."
            f"I want you to output the potential compatibility problem."
            f"You should output the problems wrapped in <WARN></WARN>."
            f"If there are not compatibility problems, output a check passed message in <PASS></PASS>. "
            f"Think step by step.")
        return query_str

    def gen_create_visual_query(self):
        query_str = (
            f"I have an Excel sheet, and a section from {self.inputSection.cellL.get_index_str()} to {self.inputSection.cellR.get_index_str()}. The content is {self.inputSection.data}. "
            f"Now I want to create a chart, in the way that {self.desc} and I want you to:"
            f"1. Select an appropriate chart type based on the data content."
            f"2. Output a title for the chart."
            f"You can pick one chart type from \"Line\", \"Pie\", \"Radar\", \"Waterfall\", and output the chart type. "
            f"You should output a title for the chart in another <TITLE></TITLE>. "
            f"Think step by step.")

        return query_str

    def apply_reply(self, reply: str, forceFormula: bool = False):
        reply = reply.replace("\n", " ")
        cell_contents = replyPattern.findall(reply)
        print(cell_contents)
        index = 0
        print(self.outputSection.data)
        for col in range(len(self.outputSection.data)):
            for row in range(len(self.outputSection.data[col])):
                cell_contents[index] = cell_contents[index].strip()
                if forceFormula or any(substr in self.outputSection.data[col] for substr in formulaList):
                    if cell_contents[index][0] != '=':
                        cell_contents[index] = f"={cell_contents[index]}"

                self.outputSection.data[col][row] = cell_contents[index]
                index += 1
        print(cell_contents)
        return self.outputSection.data

    def apply_formula_chk(self, reply: str):
        reply = reply.replace("\n", " ")
        warns = warnPattern.findall(reply)
        passes = passPattern.findall(reply)
        return warns, passes

    def apply_create_visual(self, reply: str):
        reply = reply.replace("\n", " ")
        title = titlePattern.findall(reply)[0]
        cType = "Line"
        for chartType in chartTypes:
            if chartType in reply:
                cType = chartType

        return title, cType

    @staticmethod
    def apply_code(reply: str):
        reply = reply.replace("\n", " ")
        code = codePattern.findall(reply)
        return code[0]
