# counter machine
# The low level code is a list of instructions.
# Each instruction is a string.
# The strings have the following format:
# I<let> (where <let> denotes any lower-case letter)
# D<let>
# B<let><n> where <n> denotes an integer constant--note that this is written
# without spaces
# B<n>
# H#

# The function below interprets the low-level code.  The second argument is
# a tuple of integers originally assigned to 'a','b',....


import string
import sys

letters = "abcdefghijklmnopqrstuvwxyz"
Letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
alphanum = letters + Letters + digits + "_"


def allin(s, charset):
    for c in s:
        if not (c in charset):
            return False
    return True


def interpret(program, *args, **kwargs):
    counters = [0] * 26
    for j in range(len(args)):
        counters[j] = args[j]
    if "verbose" in kwargs:
        verbose = kwargs["verbose"]
    else:
        verbose = False
    ip = 0
    while program[ip] != "H":
        current_instruction = program[ip]
        if ip > len(program):
            sys.exit("instruction pointer out of range")
        if current_instruction[0] == "I":
            variable = ord(current_instruction[1]) - ord("a")
            counters[variable] += 1

            if verbose:
                print(str(ip) + ": " + "inc " + current_instruction[1])
            ip += 1
        elif current_instruction[0] == "D":
            variable = ord(current_instruction[1]) - ord("a")
            counters[variable] = max(0, counters[variable] - 1)
            if verbose:
                print(str(ip) + ": " + "dec " + current_instruction[1])
            ip += 1

        elif current_instruction[0] == "B" and (current_instruction[1] in letters):
            variable = ord(current_instruction[1]) - ord("a")
            # print ip,variable
            target = int(current_instruction[2:])
            if verbose:
                print(
                    str(ip)
                    + ": "
                    + "goto "
                    + str(target)
                    + " if "
                    + current_instruction[1]
                    + "=0"
                )
            if counters[variable] == 0:
                ip = target
            else:
                ip += 1

        elif current_instruction[0] == "B":
            target = int(current_instruction[1:])
            if verbose:
                print(str(ip) + ": " + "goto " + str(target))
            ip = target
        if verbose:
            print(counters)

    return counters


# A source program is here represented as a sequence of lines, each
# line a list of strings.  Assemble the source program into the lower-level
# code used above, and return the low-level program.


def assemble(source):
    symbol_table = {}
    obj = []
    current = 0
    for line in source:
        # is it a label?
        # These have the form alphanum*:
        if (len(line) == 1) and (line[0][-1] == ":") and allin(line[0][:-1], alphanum):
            # print 'label'
            label = line[0][:-1]
            if label in symbol_table:
                sys.exit("redefinition of label " + label)
            else:
                symbol_table[label] = current

        # is it a conditional branch instruction?
        # These have the form goto label if x=0 but the parser
        # accepts anything of form goto label if lower-case letter followd by anything.
        elif (
            (len(line) >= 4)
            and (line[0] == "goto")
            and allin(line[1], alphanum)
            and (line[2] == "if")
            and (line[3][0] in letters)
        ):
            # print 'conditional branch'
            label = line[1]
            variable = line[3][0]
            obj.append("B" + variable + "#" + label)
            current += 1

        # is it an unconditional branch instruction?
        # These have the form goto label
        elif (len(line) == 2) and (line[0] == "goto") and allin(line[1], alphanum):
            # print 'unconditional branch'
            label = line[1]
            obj.append("B" + "#" + label)
            current += 1

        # is it a decrement instruction?
        # these have the form dec variable
        elif (
            (len(line) == 2)
            and (line[0] == "dec")
            and (len(line[1]) == 1)
            and (line[1][0] in letters)
        ):
            # print 'decrement'
            obj.append("D" + line[1][0])
            current += 1

        # is is an increment instruction?
        elif (
            (len(line) == 2)
            and (line[0] == "inc")
            and (len(line[1]) == 1)
            and (line[1][0] in letters)
        ):
            # print 'increment'
            obj.append("I" + line[1][0])
            current += 1

        # is it a halt instruction?
        elif (len(line) == 1) and (line[0] == "halt"):
            # print 'halt'
            obj.append("H")
            current += 1
    # resolve symbol table references
    for j in range(len(obj)):
        instruction = obj[j]
        if instruction[0] == "B":
            place = instruction.index("#")
            label = instruction[place + 1 :]
            if not label in symbol_table:
                sys.exit("undefined label " + label)
            else:
                instruction = instruction[:place] + str(symbol_table[label])
                obj[j] = instruction
    return obj


# Now produce object code from source file.  Skip comments and blank lines.
def assemble_from_file(filename):
    f = open(filename, "r")
    source = []
    for line in f:
        if (line[0] != "#") and not allin(line, string.whitespace):
            source.append(line.split())
    # print source
    return assemble(source)


# run a program from a file on a sequence of inputs
def runcp(filename, *args, **kwargs):
    obj = assemble_from_file(filename)
    result = interpret(obj, *args, **kwargs)
    if "limit" in kwargs:
        return result[: kwargs["limit"]]
    else:
        return result
