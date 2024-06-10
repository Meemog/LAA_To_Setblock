import json

def main():
    cfg = loadConfig("config.json")
    block_arr = readInput(cfg["inputName"], cfg["exceptions"])
    print(commandify(block_arr))
    
def commandify(input_arr):
    #[{slot:0,item:{id:\"comparator\",count:1}},{slot:1,item:{id:\"bamboo_button\",count:3}}]
    #{slot:0,item:{id:\"comparator\",count:1}}
    stack_arr = []
    for item in input_arr:
        no_stacks = item[1] // 64
        remainder = item[1] % 64
        for i in range(no_stacks):
            stack_arr.append([item[0], 64])
        if remainder != 0:
            stack_arr.append([item[0], remainder])
    command_arr = []
    for i in range(len(stack_arr)):
        command_arr.append(f"{{Slot:{i},id:{stack_arr[i][0]},Count:{stack_arr[i][1]}}}")
    
    command_text = ",".join(command_arr)
    name = "test"
        
    return f"/setblock ~ ~ ~1 chest{{CustomName:\"\\\"{name}\\\"\",Items:[{command_text}]}} replace"
    
def loadConfig(cfg_filename: str):
    with open(cfg_filename) as f:
        cfg = json.load(f)
    return cfg

def parseName(name: str, exceptions):
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
    with open(file_name, "r") as f:
        lines = f.readlines()
    blocks = []
    for i in range(5, len(lines)-3):
        line_arr = lines[i].split("|")
        #print(parseName(line_arr[1].strip()), line_arr[2].strip())
        blocks.append([parseName(line_arr[1].strip(), exceptions), int(line_arr[2].strip())])
    return blocks

if __name__ == "__main__":
    main()