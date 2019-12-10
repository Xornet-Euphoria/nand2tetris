class CodeGenerator:
    def __init__(self):
        pass


    def comp(self, comp):
        if comp == "0":
            return "101010"
        elif comp == "1":
            return "111111"
        elif comp == "-1":
            return "111010"
        elif comp == "D":
            return "001100"
        elif comp == "A":
            return "110000"
        elif comp == "!D":
            return "001101"
        elif comp == "!A":
            return "110001"
        elif comp == "-D":
            return "001111"
        elif comp == "-A":
            return "110011"
        elif comp == "D+1":
            return "011111"
        elif comp == "A+1":
            return "110111"
        elif comp == "D-1":
            return "001110"
        elif comp == "A-1":
           return "110010"
        elif comp == "D+A":
            return "000010"
        elif comp == "D-A":
            return "010011"
        elif comp == "A-D":
            return "000111"
        elif comp == "D&A":
            return "000000"
        elif comp == "D|A":
            return "010101"
        else:
            print("Unsupported mnemonic: {}".format(comp))
            exit(1)


    def dest(self, dest):
        if dest is None:
            return "000"
        elif dest == "M":
            return "001"
        elif dest == "D":
            return "010"
        elif dest == "MD":
            return "011"
        elif dest == "A":
            return "100"
        elif dest == "AM":
            return "101"
        elif dest == "AD":
            return "110"
        elif dest == "AMD":
            return "111"
        else:
            print("Unsupported mnemonic: {}".format(dest))
            exit(1)


    def jump(self, jump):
        if jump is None:
            return "000"
        elif jump == "JGT":
            return "001"
        elif jump == "JEQ":
            return "010"
        elif jump == "JGE":
            return "011"
        elif jump == "JLT":
            return "100"
        elif jump == "JNE":
            return "101"
        elif jump == "JLE":
            return "110"
        elif jump == "JMP":
            return "111"
        else:
            print("Unsupported mnemonic: {}".format(jump))
            exit(1)
