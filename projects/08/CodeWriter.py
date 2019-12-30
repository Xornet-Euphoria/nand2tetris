from CommandType import CommandType


class CodeWriter:
    binary_functions = ["add", "sub", "eq", "gt", "lt", "and", "or"]
    unary_functions = ["neg", "not"]
    label_index = 0

    def __init__(self, file_name):
        self.file_name = file_name


    def write_command(self, command):
        com_type = command.command_type

        if com_type == CommandType.C_ARITHMETIC:
            return self.write_arithmetic(command)

        if com_type == CommandType.C_PUSH:
            return self.write_push(command)
        
        if com_type == CommandType.C_POP:
            return self.write_pop(command)

        if com_type == CommandType.C_LABEL:
            return self.write_label(command)

        if com_type == CommandType.C_GOTO:
            return self.write_goto(command)
        
        if com_type == CommandType.C_IF:
            return self.write_if(command)

        if com_type == CommandType.C_FUNCTION:
            return self.write_function(command)

        if com_type == CommandType.C_RETURN:
            return self.write_return(command)

        if com_type == CommandType.C_CALL:
            return self.write_call(command)

    
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
        elif segment == "local":
            commands_str.append("@LCL")
            commands_str.append("D=M")
            commands_str.append("@{}".format(index))
            commands_str.append("A=D+A")
            commands_str.append("D=M")
        elif segment == "argument":
            commands_str.append("@ARG")
            commands_str.append("D=M")
            commands_str.append("@{}".format(index))
            commands_str.append("A=D+A")
            commands_str.append("D=M")
        elif segment == "this":
            commands_str.append("@THIS")
            commands_str.append("D=M")
            commands_str.append("@{}".format(index))
            commands_str.append("A=D+A")
            commands_str.append("D=M")
        elif segment == "that":
            commands_str.append("@THAT")
            commands_str.append("D=M")
            commands_str.append("@{}".format(index))
            commands_str.append("A=D+A")
            commands_str.append("D=M")
        elif segment == "pointer":
            commands_str.append("@3")
            commands_str.append("D=A")
            commands_str.append("@{}".format(index))
            commands_str.append("A=D+A")
            commands_str.append("D=M")
        elif segment == "temp":
            commands_str.append("@5")
            commands_str.append("D=A")
            commands_str.append("@{}".format(index))
            commands_str.append("A=D+A")
            commands_str.append("D=M")
        elif segment == "static":
            commands_str.append("@{}.{}".format(self.file_name, index))
            commands_str.append("D=M")

        # スタックへ格納
        commands_str.append("@SP")
        commands_str.append("A=M")
        commands_str.append("M=D")

        # スタックポインタのインクリメント
        commands_str.append("@SP")
        commands_str.append("M=M+1")

        return "\n".join(commands_str)


    def write_pop(self, command):
        segment = command.arg1
        index = command.arg2

        if segment is None or index is None:
            # todo: error handling
            print("[+]: argment error")
            exit(1)
        
        commands_str = []

        # target addrをR13レジスタへ格納
        if segment == "static":
            commands_str.append("@{}.{}".format(self.file_name, index))
            commands_str.append("D=A")
        else:
            if segment == "local":
                commands_str.append("@LCL")
                commands_str.append("D=M")
            elif segment == "argument":
                commands_str.append("@ARG")
                commands_str.append("D=M")
            elif segment == "this":
                commands_str.append("@THIS")
                commands_str.append("D=M")
            elif segment == "that":
                commands_str.append("@THAT")
                commands_str.append("D=M")
            elif segment == "pointer":
                commands_str.append("@3")
                commands_str.append("D=A")
            elif segment == "temp":
                commands_str.append("@5")
                commands_str.append("D=A")

            commands_str.append("@{}".format(index))
            commands_str.append("D=D+A")

        commands_str.append("@R13")
        commands_str.append("M=D")
        
        # Dレジスタにスタックトップを格納
        commands_str.append("@SP")
        commands_str.append("M=M-1")
        commands_str.append("A=M")
        commands_str.append("D=M")

        # R13レジスタ中のアドレスへDの値を格納
        commands_str.append("@R13")
        commands_str.append("A=M")
        commands_str.append("M=D")

        return "\n".join(commands_str)

    def write_label(self, command):
        label = command.arg1

        if label is None:
            # todo: error handling
            print("[+]: argment error")
            exit(1)

        return "({})".format(label)
        

    def write_goto(self, command):
        dest = command.arg1
        
        if dest is None:
            # todo: error handling
            print("[+]: argment error")
            exit(1)

        return "@{}\n0;JMP".format(dest)


    def write_if(self, command):
        dest = command.arg1
        
        if dest is None:
            # todo: error handling
            print("[+]: argment error")
            exit(1)

        commands_str = []

        # pop
        commands_str.append("@SP")
        commands_str.append("M=M-1")
        commands_str.append("@SP")
        commands_str.append("A=M")

        # popした値が0でないなら移動
        commands_str.append("D=M")
        commands_str.append("@{}".format(dest))
        commands_str.append("D;JNE")

        return "\n".join(commands_str)

    
    def write_function(self, command):
        f_name = command.arg1
        argc_str = command.arg2
        
        if f_name is None or argc_str is None:
            # todo: error handling
            print("[+]: argment error")
            exit(1)

        commands_str = []

        commands_str.append("({})".format(f_name))
        argc = int(argc_str)

        for _ in range(argc):
            commands_str.append("@SP")
            commands_str.append("A=M")
            commands_str.append("M=0")
            commands_str.append("@SP")
            commands_str.append("M=M+1")

        return "\n".join(commands_str)


    def write_return(self, command):
        commands_str = []

        # return addr -> R15
        commands_str.append("@LCL")
        commands_str.append("D=M")
        commands_str.append("@5")
        commands_str.append("D=D-A")
        commands_str.append("A=D")
        commands_str.append("D=M")
        commands_str.append("@R15")
        commands_str.append("M=D")

        # 結果のpop
        commands_str.append("@SP")
        commands_str.append("M=M-1")
        commands_str.append("@SP")
        commands_str.append("A=M")
        commands_str.append("D=M")

        # 呼び出し元スタックトップへ格納
        commands_str.append("@ARG")
        commands_str.append("A=M")
        commands_str.append("M=D")

        # SPを呼び出し元に合わせる
        commands_str.append("@ARG")
        commands_str.append("D=M")
        commands_str.append("@SP")
        commands_str.append("M=D+1")

        # 呼び出し元情報のベースアドレス -> R14
        commands_str.append("@LCL")
        commands_str.append("D=M-1")
        commands_str.append("@R14")
        commands_str.append("M=D")

        # 呼び出し元の復元
        commands_str.append("A=D")
        commands_str.append("D=M")
        commands_str.append("@THAT")
        commands_str.append("M=D")

        commands_str.append("@R14")
        commands_str.append("M=M-1")
        commands_str.append("A=M")
        commands_str.append("D=M")
        commands_str.append("@THIS")
        commands_str.append("M=D")

        commands_str.append("@R14")
        commands_str.append("M=M-1")
        commands_str.append("A=M")
        commands_str.append("D=M")
        commands_str.append("@ARG")
        commands_str.append("M=D")

        commands_str.append("@R14")
        commands_str.append("M=M-1")
        commands_str.append("A=M")
        commands_str.append("D=M")
        commands_str.append("@LCL")
        commands_str.append("M=D")

        # return addr
        commands_str.append("@R15")
        commands_str.append("A=M")
        commands_str.append("0;JMP")

        return "\n".join(commands_str)

    def write_call(self, command):
        f_name = command.arg1
        argc_str = command.arg2

        if f_name is None or argc_str is None:
            # todo: error handling
            print("[+]: argment error")
            exit(1)

        argc = int(argc_str)

        commands_str = []

        # return addr
        commands_str.append("@ret.{}.{}.{}".format(f_name, self.file_name, self.label_index))
        commands_str.append("D=A")
        commands_str.append("@SP")
        commands_str.append("A=M")
        commands_str.append("M=D")
        commands_str.append("@SP")
        commands_str.append("M=M+1")
        
        # old local
        commands_str.append("@LCL")
        commands_str.append("D=M")
        commands_str.append("@SP")
        commands_str.append("A=M")
        commands_str.append("M=D")
        commands_str.append("@SP")
        commands_str.append("M=M+1")

        # old argument
        commands_str.append("@ARG")
        commands_str.append("D=M")
        commands_str.append("@SP")
        commands_str.append("A=M")
        commands_str.append("M=D")
        commands_str.append("@SP")
        commands_str.append("M=M+1")

        # old this
        commands_str.append("@THIS")
        commands_str.append("D=M")
        commands_str.append("@SP")
        commands_str.append("A=M")
        commands_str.append("M=D")
        commands_str.append("@SP")
        commands_str.append("M=M+1")

        # old that
        commands_str.append("@THAT")
        commands_str.append("D=M")
        commands_str.append("@SP")
        commands_str.append("A=M")
        commands_str.append("M=D")
        commands_str.append("@SP")
        commands_str.append("M=M+1")

        # new local
        commands_str.append("@SP")
        commands_str.append("D=M")
        commands_str.append("@LCL")
        commands_str.append("M=D")

        # new argument
        commands_str.append("@SP")
        commands_str.append("D=M")
        commands_str.append("@{}".format(argc + 5))
        commands_str.append("D=D-A")
        commands_str.append("@ARG")
        commands_str.append("M=D")
        commands_str.append("@{}".format(f_name))
        commands_str.append("0;JMP")
        
        commands_str.append("(ret.{}.{}.{})".format(f_name, self.file_name, self.label_index))

        self.label_index += 1

        return "\n".join(commands_str)