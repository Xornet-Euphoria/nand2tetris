from CommandType import CommandType


class Command:
    str_com = ""
    command = ""
    arg1 = None
    arg2 = None
    command_type = None


    def __init__(self, str_com):
        self.str_com = str_com

        com_list = str_com.split()

        self.command = com_list[0]
        
        if len(com_list) >= 2:
            self.arg1 = com_list[1]
        
        if len(com_list) == 3:
            self.arg2 = com_list[2]
        
        arithmetic_commands = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

        if self.command in arithmetic_commands:
            self.command_type = CommandType.C_ARITHMETIC
        elif self.command == "push":
            self.command_type = CommandType.C_PUSH
        elif self.command == "pop":
            self.command_type = CommandType.C_POP
        elif self.command == "label":
            self.command_type = CommandType.C_LABEL
        elif self.command == "goto":
            self.command_type = CommandType.C_GOTO
        elif self.command == "if-goto":
            self.command_type = CommandType.C_IF