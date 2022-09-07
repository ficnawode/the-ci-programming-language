class Position:
    def __init__(
        self, id: int, column: int, linenumber: int, filename: str, filetxt: str
    ):
        self.id = id
        self.column = column
        self.linenumber = linenumber
        self.filename = filename
        self.filetxt = filetxt

    def advance(self, id_offset=0, column_offset=0, line_offset=0):
        self.id += id_offset
        self.linenumber += line_offset
        if line_offset > 0:
            self.column = 0
        self.column += column_offset
        return self

    def copy(self):
        return Position(
            self.id, self.linenumber, self.column, self.filename, self.filetxt
        )
