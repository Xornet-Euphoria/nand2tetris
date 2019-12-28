from parser import Parser
from CommandType import CommandType
from CodeWriter import CodeWriter


if __name__ == "__main__":
    path_and_name = "StackArithmetic/StackTest/StackTest"
    p = Parser(path_and_name + ".vm")
    out = open(path_and_name + ".asm", "w")

    cw = CodeWriter()

    while p.remain_command:
        command = p.get_command()

        out.write(cw.write_command(command))
        out.write("\n")

        p.next_command()

    out.close()