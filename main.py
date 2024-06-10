import json

def main():
    cfg = loadConfig("config.json")
    block_arr = readInput(cfg["inputName"], cfg["exceptions"])
    output(commandify(block_arr), cfg)
    
def output(commands, cfg):
    "Writes the list of connamds to a file"
    with open(cfg["outputName"], "w") as f:
        f.write("\n\n".join(commands))

def commandify(input_arr):
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
        commands.append(f"/setblock ~{-1-j} ~ ~ chest{{CustomName:\"\\\"{j+1}\\\"\",Items:[{tmp_command_text}]}} replace")
    tmp_command_arr = []
    for i in range(chest_remainder):
        tmp_command_arr.append(f"{{Slot:{i},id:{stack_arr[total][0]},Count:{stack_arr[total][1]}}}")
        total += 1
    tmp_command_text = ",".join(tmp_command_arr)
    j+=1
    commands.append(f"/setblock ~{-1-j} ~ ~ chest{{CustomName:\"\\\"{j+1}\\\"\",Items:[{tmp_command_text}]}} replace")
    
    return commands
    
def loadConfig(cfg_filename: str):
    "Loads the config"
    with open(cfg_filename) as f:
        cfg = json.load(f)
    return cfg

def parseName(name: str, exceptions):
    "Converts the English name of blocks into the Minecraft name"
    if name not in exceptions:
        lower_name = name.lower()
        name_arr = list(lower_name)
        for i in range(len(name_arr)):
            name_arr[i] = "_" if name_arr[i] == " " else name_arr[i]
        toReturn = "".join(name_arr)
        return toReturn
    else:
        return exceptions[name] 

def readInput(file_name: str, exceptions):
    "Looks at the Litematica Area Analysis file and converts it into a 2D array of block names and amounts"
    with open(file_name, "r") as f:
        lines = f.readlines()
    blocks = []
    for i in range(5, len(lines)-3):
        line_arr = lines[i].split("|")
        blocks.append([parseName(line_arr[1].strip(), exceptions), int(line_arr[2].strip())])
    return blocks

if __name__ == "__main__":
    main()