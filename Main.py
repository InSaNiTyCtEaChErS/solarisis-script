labels = []


if_counter = 0
for_counter = 0
linecount = 0

jump_lut = {
    ">=":"l",
    "<=":"g",
    "==":"ne",
    "!=":"eq",
    ">":"le",
    "<":"ge"

}


def compile(line):
    variables = ["zr","for_temp"]
    spaces = (len(line.lstrip())-len(line))/4
    line = line.lstrip()
    print(f"compiling{line}")
    if (line[0] != "#") and (line != ""):
        output = ""
        if line[0:2] == "def":
            output = ""
            labels += line[4:-1]

        elif line[0:2] == "set":   #format: set r1 = variable
            tokens = line.split()
            variables += tokens[3]
            output = "" 

        elif line[0] == "<":
            tokens = line.split()
            output = tokens[0] + tokens[1] #allows for comments

        elif line[0:3] == "for ":
            if_counter += 1
            tokens = line.split()
            labels.append([f"labelf_{for_counter}__os",linecount])
            output = f"sub {tokens[3]},1,{tokens[3]}"
            output += f"cmpi {tokens[3]},0"
            

        elif line[0:5] == "forbit":  #forbit means to interpret it as a binary number instead of as a integer
            if_counter += 1
            tokens = line.split()
            labels.append([f"labelf_{for_counter}__os",linecount])
            output = "sub r1,r1,r1"
            output += f"muli r{tokens[3]},2,r{tokens[3]}"
            output += f"andi r{tokens[3]},1,r1"

        elif line[0:3] == "exit":
            labels.append([f"labelf_{for_counter}_exit__os",linecount])
            output = f"jae labelf_{for_counter}__os"

        elif line == "break":
            output = f"jump labelf_{for_counter}_exit__os"

        elif line[0:1] == "if":
            output = "cmp"
            tokens = line.split()
            if not(tokens[3] in variables):
                output += "i"
            output += tokens[1] + tokens[3]
            output += f"j{jump_lut[tokens[2]]}label_{if_counter}_exit__os"

        elif line == "if exit":
            labels.append([f"label_{if_counter}_exit__os",linecount])
            output = ""

    else:
        output = ""

    print(f"line compiled: {line} -> {output}")
    linecount += 1

compile("set r1 = base")
