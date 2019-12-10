from command import Command


class Parser:
    ope_list = []
    remain_command = True
    current_index = 0
    symbol_table = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "R0": 0,
        "R1": 1,
        "R2": 2,
        "R3": 3,
        "R4": 4,
        "R5": 5,
        "R6": 6,
        "R7": 7,
        "R8": 8,
        "R9": 9,
        "R10": 10,
        "R11": 11,
        "R12": 12,
        "R13": 13,
        "R14": 14,
        "R15": 15,
        "SCREEN": 16384,
        "KBD": 24576,
    }
    
    def __init__(self, file_path):
        with open(file_path) as f:
            raw_ope_list = f.readlines()

        counter = 0
        for ope in raw_ope_list:
            comment_index = ope.find("//")
            if comment_index != -1:
                ope = ope[:comment_index]
            ope = ope.replace(" ", "")
            ope = ope.replace("\n", "")

            if len(ope) == 0:
                continue

            if ope[0] == "(" and ope[-1] == ")":
                symbol = ope[1:-1]
                if symbol not in self.symbol_table:
                    self.symbol_table[symbol] = counter
                    continue
                else:
                    print("label must be unique in program.")
                    exit(1)
            else:
                counter += 1

            self.ope_list.append(ope)

        if len(self.ope_list) == 0:
            self.remain_command = False

        print("[+]: removing space completed")


    def symbol_parse(self):
        addr = 16
        for ope in self.ope_list:
            symbol = None
            if ope[0] == "@":
                symbol = ope[1:]
                if not symbol.isdecimal() and symbol not in self.symbol_table:
                    self.symbol_table[symbol] = addr
                    addr += 1


    def get_command(self):
        return Command(self.ope_list[self.current_index]) if self.remain_command else None


    def next_command(self):
        self.current_index += 1
        if self.current_index == len(self.ope_list):
            self.remain_command = False
