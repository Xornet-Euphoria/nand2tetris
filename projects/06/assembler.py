from parser import Parser
from code import CodeGenerator


if __name__ == "__main__":
    path_and_name = "add/Add"
    p = Parser(path_and_name + ".asm")
    out = open(path_and_name + ".hack", "w")

    # make symbol table
    p.symbol_parse()

    print("[+]: number of command: {}".format(len(p.ope_list)))

    # print("[+]: symbol table is here")
    # for key, item in p.symbol_table.items():
        # print(key, item)

    # symbol less
    while p.remain_command:
        instruction = []
        command = p.get_command()
        # type
        # print(command.command_type)
        com_type = command.command_type

        if com_type == -1:
            # todo: error handling
            print("ha?")
            exit()
        if com_type < 2:
            instruction.append(str(com_type))

        # under 15bits
        if com_type == 0:
            raw_value = command.symbol
            if raw_value.isdecimal():
                value = int(raw_value)
            else:
                value = p.symbol_table[raw_value]
            instruction.append(bin(value)[2:].zfill(15))
        else:
            gen = CodeGenerator()
            # comp
            # a bit
            instruction.append("11")
            comp = command.comp
            if "M" in comp:
                instruction.append("1")
                comp = comp.replace("M", "A")
            else:
                instruction.append("0")

            instruction.append(gen.comp(comp))

            # dest
            dest = command.dest
            instruction.append(gen.dest(dest))

            # jump
            jump = command.jump
            instruction.append(gen.jump(jump))

        # print(instruction)
        out.write("".join(instruction))
        out.write("\n")

        p.next_command()

    out.close()
    print("[+]: Completed")
