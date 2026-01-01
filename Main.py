labels = []
variables = ["zr","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null","null"]


if_counter = 0
for_counter = 0
linecount = 0   

branch_lut = {
    ">=":"l",
    "<=":"g",
    "==":"ne",
    "!=":"eq",
    ">":"le",
    "<":"ge"
}

def is_int(input_):
    for char in input_:
        if char not in "0123456789":
            return False
    return True


def varset(line):    #format: variable = reg
    line = line.split()
    reg = line[2]
    global variables 
    variables.insert(reg[1:],line[1])    
    e = vars.index(line[0])
    return(f"sub {e},{e},{e}")

def setvar(line):
    line = line.split()
    e = vars.index(line[0])
    return(f"sub {e},{e},{e}\
           addi {e},{line[2]},{e}")

def if_(line):
    var = ""
    output = "cmp "
    jumpstore = "b"
    for char in line[2:]:
        if char != " ":
            var += char
        else:
            if var not in "<><=>=!==":
                if is_int(var):
                    output += var
                else:
                    output += variables.index(var)
            else:
                jumpstore += branch_lut(var)
    jumpstore += f"if__{if_counter}"
    global if_counter
    if_counter += 1
    return(output + jumpstore)

def for_(line):
    global labels
    labels.append([linecount],f"for_label__{for_counter}")
    for char in line[3:]:
        if char != " ":
            var += char
        else:
            if var not in "<><=>=!==":
                if is_int(var):
                    output += var
                else:
                    output += variables.index(var)
            else:
                jumpstore += branch_lut(var)

def define(line):
    line = line.split()


def main_(lines):
    output = ""
    if_list = []
    for line in lines:
        if line[0] == "/":
            output += line[2:]
        print(line)
        indent = (len(line)-len(line.lstrip()))//4

        #error handling
        if line[0:3] == "def " and indent >= 1:
            raise KeyError("cannot have function definitions inside if or for loops")
        
        #handle if statements
        if "if " in line:
            output += if_(line)
            if_list.push(if_counter)
        elif "if_end" in line:
            output += f"if__{if_list.pop()}"

        #handle for statements


        global linecount
        linecount += 1
