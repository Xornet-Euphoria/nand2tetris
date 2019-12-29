import sys
from parser import Parser
from CommandType import CommandType
from CodeWriter import CodeWriter


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("[+]: Usage: python vm_translator.py <file_name>")
        exit(0)

    path = args[1]

    p = Parser(path)
    out_path = path.replace(".vm", "")
    out = open(out_path + ".asm", "w")

    cw = CodeWriter(out_path.split("/")[-1])

    while p.remain_command:
        command = p.get_command()

        out.write(cw.write_command(command))
        out.write("\n")

        p.next_command()

    out.close()