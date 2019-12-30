from Command import Command

class Parser:
    def __init__(self, file_path):
        self.command_list = []
        self.remain_command = True
        self.current_index = 0
        
        # read file
        with open(file_path) as f:
            raw_command_list = f.readlines()

        counter = 0
        # remove comment and lf
        for cm in raw_command_list:
            comment_index = cm.find("//")
            if comment_index != -1:
                cm = cm[:comment_index]
            cm = cm.replace("\n", "")

            if len(cm) == 0:
                continue

            counter += 1

            self.command_list.append(cm)

        if len(self.command_list) == 0:
            self.remain_command = False

    
    def get_command(self):
        return Command(self.command_list[self.current_index]) if self.remain_command else None


    def next_command(self):
        self.current_index += 1
        if self.current_index == len(self.command_list):
            self.remain_command = False