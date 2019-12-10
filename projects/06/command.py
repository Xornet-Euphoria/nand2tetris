class Command:
    str_com = ""
    symbol = None
    comp = ""
    dest = None
    jump = None

    def __init__(self, str_com):
        self.str_com = str_com

        if str_com[0] == '@':
            self.command_type = 0
            self.symbol = str_com[1:]
        elif str_com[0] == '(' and str_com[-1] == ')':
            self.command_type = 2
        else:
            self.command_type = 1
            equal_index = str_com.find('=')
            semicolon_index = str_com.find(';')
            if equal_index == -1 and semicolon_index == -1:
                self.comp = str_com
            elif equal_index != -1:
                self.dest = str_com[0:equal_index]
                if semicolon_index != -1:
                    self.comp = str_com[equal_index + 1:semicolon_index]
                    self.jump = str_com[semicolon_index + 1:]
                else:
                    self.comp = str_com[equal_index + 1:]
            else:
                self.comp = str_com[0:semicolon_index]
                self.jump = str_com[semicolon_index + 1:]
