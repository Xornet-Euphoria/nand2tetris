import sys
from parser import Parser
from CommandType import CommandType
from CodeWriter import CodeWriter


if __name__ == "__main__":
    # args = sys.argv
    # if len(args) < 2:
    #     print("[+]: Usage: python vm_translator.py <file_name>")
    #     exit(0)

    # path = args[1]

    # p = Parser(path)
    # out_path = path.replace(".vm", "")

    dir = "FunctionCalls/StaticsTest/"
    out_path = dir + "StaticsTest"
    out = open(out_path + ".asm", "w")

    # init
    out.write("@261\n")
    out.write("D=A\n")
    out.write("@0\n")
    out.write("M=D\n")
    out.write("@1\n")
    out.write("M=D\n")
    out.write("@256\n")
    out.write("D=A\n")
    out.write("@2\n")
    out.write("M=D\n")
    out.write("@3\n")
    out.write("D=-A\n")
    out.write("@3\n")
    out.write("M=D\n")
    out.write("@4\n")
    out.write("D=-A\n")
    out.write("@4\n")
    out.write("M=D\n")

    files = ["Sys.vm", "Class1.vm", "Class2.vm"]
    for file in files:
        p = Parser(dir + file)
        print(p.command_list)
        cw = CodeWriter(file.split("/")[-1])

        while p.remain_command:
            command = p.get_command()

            out.write(cw.write_command(command))
            out.write("\n")

            p.next_command()

        del p

    out.close()