import json

class Converter:
    
    def __init__(self, cfg="config.json", input_name=None, output_name=None, output_vessel=None, exceptions=None) -> None:
        loaded_cfg = self.__loadConfig(cfg)
        self.__input_name = loaded_cfg["inputName"] if input_name == None else input_name
        self.__output_name = loaded_cfg["outputName"] if output_name == None else output_name
        self.__output_vessel = loaded_cfg["outputVessel"] if output_vessel == None else output_vessel
        self.__exceptions = loaded_cfg["exceptions"] if exceptions == None else exceptions

    def output(self, commands, output_name=None):
        "Writes the list of connamds to a file"
        
        output_path = self.__output_name if output_name == None else output_name;
        with open(output_path, "w") as f:
            f.write("\n\n".join(commands))

    def commandify(self, input_arr):
        "Generates an array of commands from a 2d array of blocks and ammounts"
        stack_arr = []
        for item in input_arr:
            no_stacks = item[1] // 64
            remainder = item[1] % 64
            for i in range(no_stacks):
                stack_arr.append([item[0], 64])
            if remainder != 0:
                stack_arr.append([item[0], remainder])
                
        no_chests = len(stack_arr) // 27
        chest_remainder = len(stack_arr) % 27
        commands = []
        total = 0
        
        for j in range(no_chests):
            tmp_command_arr = []
            for i in range(27):
                tmp_command_arr.append(f"{{Slot:{i},id:{stack_arr[total][0]},Count:{stack_arr[total][1]}}}")
                total += 1
            tmp_command_text = ",".join(tmp_command_arr)
            commands.append(f"/setblock ~{-1-j} ~ ~ {self.__output_vessel}{{CustomName:\"\\\"{j+1}\\\"\",Items:[{tmp_command_text}]}} replace")
        tmp_command_arr = []
        for i in range(chest_remainder):
            tmp_command_arr.append(f"{{Slot:{i},id:{stack_arr[total][0]},Count:{stack_arr[total][1]}}}")
            total += 1
        tmp_command_text = ",".join(tmp_command_arr)
        j+=1
        commands.append(f"/setblock ~{-1-j} ~ ~ chest{{CustomName:\"\\\"{j+1}\\\"\",Items:[{tmp_command_text}]}} replace")
        
        return commands
        
    def __loadConfig(self, cfg_filename: str):
        "Loads the config"
        with open(cfg_filename) as f:
            cfg = json.load(f)
        return cfg

    def __parseName(self, name: str):
        "Converts the English name of blocks into the Minecraft name"
        if name not in self.__exceptions:
            lower_name = name.lower()
            name_arr = list(lower_name)
            for i in range(len(name_arr)):
                name_arr[i] = "_" if name_arr[i] == " " else name_arr[i]
            toReturn = "".join(name_arr)
            return toReturn
        else:
            return self.__exceptions[name]

    def readInput(self):
        "Looks at the Litematica Area Analysis file and converts it into a 2D array of block names and amounts"
        file_name = self.__input_name
        with open(file_name, "r") as f:
            lines = f.readlines()
        blocks = []
        for i in range(5, len(lines)-3):
            line_arr = lines[i].split("|")
            blocks.append([self.__parseName(line_arr[1].strip()), int(line_arr[2].strip())])
        return blocks