from CommandType import CommandType


class CodeWriter:
    binary_functions = ["add", "sub", "eq", "gt", "lt", "and", "or"]
    unary_functions = ["neg", "not"]
    label_index = 0

    def __init__(self):
        pass


    def write_command(self, command):
        com_type = command.command_type

        if com_type == CommandType.C_ARITHMETIC:
            return self.write_arithmetic(command)

        if com_type == CommandType.C_PUSH:
            return self.write_push(command)
        
        if com_type == CommandType.C_PUSH:
            return self.write_pop(command)

    
    def write_arithmetic(self, command):
        operator = command.command
        
        commands_str = []
        # 第1引数をpop
        commands_str.append("@SP")
        commands_str.append("M=M-1")
        commands_str.append("@SP")
        commands_str.append("A=M")
        commands_str.append("D=M")

        if operator in self.binary_functions:
            # 第2引数をpop
            commands_str.append("@SP")
            commands_str.append("M=M-1")
            commands_str.append("@SP")
            commands_str.append("A=M")

        # 演算子
        if operator == "add":
            commands_str.append("D=D+M")
        elif operator == "sub":
            commands_str.append("D=M-D")
        elif operator == "neg":
            commands_str.append("D=-D")
        elif operator == "eq":
            commands_str.append("D=M-D")
            commands_str.append("@eq{}".format(self.label_index))
            commands_str.append("D;JEQ")
            commands_str.append("D=0")
            commands_str.append("@end{}".format(self.label_index))
            commands_str.append("0;JMP")
            commands_str.append("(eq{})".format(self.label_index))
            commands_str.append("D=-1")
            commands_str.append("(end{})".format(self.label_index))
            self.label_index += 1
        elif operator == "gt":
            commands_str.append("D=M-D")
            commands_str.append("@jgt{}".format(self.label_index))
            commands_str.append("D;JGT")
            commands_str.append("D=0")
            commands_str.append("@end{}".format(self.label_index))
            commands_str.append("0;JMP")
            commands_str.append("(jgt{})".format(self.label_index))
            commands_str.append("D=-1")
            commands_str.append("(end{})".format(self.label_index))
            self.label_index += 1
        elif operator == "lt":
            commands_str.append("D=M-D")
            commands_str.append("@jlt{}".format(self.label_index))
            commands_str.append("D;JLT")
            commands_str.append("D=0")
            commands_str.append("@end{}".format(self.label_index))
            commands_str.append("0;JMP")
            commands_str.append("(jlt{})".format(self.label_index))
            commands_str.append("D=-1")
            commands_str.append("(end{})".format(self.label_index))
            self.label_index += 1
        elif operator == "and":
            commands_str.append("D=D&M")
        elif operator == "or":
            commands_str.append("D=D|M")
        elif operator == "not":
            commands_str.append("D=!D")


        # 結果のpush
        commands_str.append("@SP")
        commands_str.append("A=M")
        commands_str.append("M=D")
        commands_str.append("@SP")
        commands_str.append("M=M+1")

        return "\n".join(commands_str)



    def write_push(self, command):
        segment = command.arg1
        index = command.arg2

        if segment is None or index is None:
            # todo: error handling
            print("[+]: argment error")
            exit(1)
        
        commands_str = []
        # セグメントから値を抽出
        if segment == "constant":
            commands_str.append("@{}".format(index))
            commands_str.append("D=A")

        # スタックへ格納
        commands_str.append("@SP")
        commands_str.append("A=M")
        commands_str.append("M=D")

        # スタックポインタのインクリメント
        commands_str.append("@SP")
        commands_str.append("M=M+1")

        return "\n".join(commands_str)


    def write_pop(self, command):
        pass