import openpyxl

class ExcelWriter:
    def __init__(self):

        self.workbook = openpyxl.Workbook()
        self.sheet = self.workbook.active

    def add_data(self, data, fields):
        
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
        for i in range(0, len(fields)):
            self.sheet[f"{letters[i]}1"] = fields[i]

            for j in range(1, len(data[fields[i]])):
                self.sheet[f"{letters[i]}{j+1}"] = data[fields[i]][j]
    
    def save_data(self, filename):
        self.workbook.save(filename=filename + ".xlsx")