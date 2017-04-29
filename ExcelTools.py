import xlrd
import xlwt
import os


class Sheet:
    def __init__(self, data: dict, titulo: str):
        """        
        :param titulo: str 
        :param data: list
        """
        self.data = data
        self.titulo = titulo


class Book:
    def __init__(self, sheets: Sheet, path: str):
        """        
        :param sheets: ExportarSalas.Sheet 
        :param path: str
        """
        self.sheets = sheets
        self.path = path


class Excel:
    """
    Methods to manipulate the 'xlrd' library
    """
    def __init__(self):
        pass

    @staticmethod
    def get_workbook(path):
        """
        Get the workbook object from a given path
        :param path: Path to the .xls file
        :return: xlrd.book object
        """
        return xlrd.open_workbook(path)

    @staticmethod
    def read_workbook(path):
        """
        Read all lines and columns of all sheets of the given workbook path
        obs.: A workbook is represented by the .xls extension
        :param path: The path for a workbook (.xls) file
        :return: a list of sheets matrices
        """
        wb = Excel.get_workbook(path)
        workbook_sheets = []

        for sheet in wb.sheets():
            workbook_sheets.append(Excel.read_sheet(wb, sheet, 0, 0))

        return workbook_sheets

    @staticmethod
    def read_sheet(sheet, row, col, workbook=None):
        """
        Return a list of list representation of the sheet table needed
        :rtype: list
        :param sheet: A index or a  xlrd.sheet object
        :param row: A list of lines or a starting line index for the cursor
        :param col: A list of columns or a starting column index for the cursor
        :param workbook: A path for a .xls file or a xlrd.book object
        :return: A matrix representing the sheet spreadsheet
        """

        sheet = Excel.evaluate_sheet(sheet, workbook)

        table = []

        if isinstance(row, type(1)):
            rows = (x for x in range(row, sheet.nrows))
        elif isinstance(row, type([])):
            rows = row
        else:
            raise Exception('Invalid type for row (number or list of numbers)')

        if isinstance(col, type(1)):
            cols = (x for x in range(col, sheet.ncols))
        elif isinstance(col, type([])):
            cols = col
        else:
            raise Exception('Invalid type for col (number or list of numbers)')

        for i in rows:
            line = []
            for j in cols:
                line.append(sheet.cell(i, j).value)
            table.append(line)

        return table

    @staticmethod
    def evaluate_sheet(sheet, workbook):
        """
        Evaluate if the given sheet is a index or object returning
        a suitable object after evaluating the workbook path or object
        given
        :param sheet: Index or xlrd.sheet object
        :param workbook: the workbook to look for the Index
        :return: A xlrd.sheet object
        """
        if isinstance(sheet, type(1)):
            workbook = Excel.evaluate_book(workbook)
            sheet = workbook.sheet_by_index(sheet)
        elif not isinstance(sheet, type(xlrd.sheet)):
            raise Exception('Invalid type for sheet (xlrd.sheet or index on workbook)')
        return sheet

    @staticmethod
    def evaluate_book(workbook):
        """
        Evaluate if the given workbook is a path or a object
        returning a suitable xlrd.book object
        :param workbook: A xlrd.book or a path for a .xls file
        :return: xlrd.book object
        """
        if not isinstance(workbook, type(xlrd.book)):
            if os.path.exists(workbook):
                workbook = Excel.get_workbook(workbook)
            else:
                raise Exception('Invalid type for workbook (xlrd.book or a path to one .xls file path)')
        return workbook

    @staticmethod
    def evaluate_book_write(workbook):
        """
        Evaluate if the given workbook is a object
        returning a suitable xlwt.Workbook object
        :param workbook: A xlwt.Workbook or a path for a .xls file
        :return: xlwt.Workbook object
        """
        if isinstance(workbook, type(xlwt.Workbook)):
            raise Exception('Invalid type for workbook (xlwt.Workbook or a path to one .xls file path)')

        return workbook

    @staticmethod
    def write_workbook(book: Book):
        workbook = xlwt.Workbook()
        if book is None:
            raise Exception("book can't be 'None'")

        for sheet in book.sheets:
            sh = workbook.add_sheet(book.sheets[sheet].titulo, cell_overwrite_ok=True)
            for i, row in enumerate(book.sheets[sheet].data):
                for j, cell in enumerate(row):
                    if j is not None:
                        sh.write(i, j, cell)

        workbook.save(book.path)


if __name__ == '__main__':
    excel = Excel()
    excel.read_workbook(r'')

"""
book = {
    'sheets': [
        {
            'titulo': 'p1',
            'data': [
                ['col1', 'col2'], ['col1', 'col2']
            ]
        },
        {
            'titulo': 'p2',
            'data': [
                ['col1', 'col2'], ['col1', 'col2']
            ]
        }
    ],

    'titulo': 'book'
}
"""