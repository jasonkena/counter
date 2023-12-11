import string
import sys
import argparse

# valid characters for identifiers (labels, variables, function names)
letters = "abcdefghijklmnopqrstuvwxyz"
Letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
alphanum = letters + Letters + digits + "_"


def allin(s, charset):
    for c in s:
        if not (c in charset):
            return False
    return True


def valid_identifier(s):
    return len(s) > 0 and allin(s, alphanum)


# valid instructions
"""
<label>:
goto <label>
goto <label> if <var>=0
inc <var>
dec <var>
halt
call <func> <var1> ... <varN>

macro <func> <var1> ... <varN>:
endmacro

"""
# macro definitions should not be nested, although you can call a macro from within a macro definition
# macro only allowed to call macros defined before it (to prevent infinite call recursion)
# macros are "pure" in the sense that they do not modify any global variables and only variables passed in

# instruction representations:
# ("label", "<label>")
# ("goto", "<label>")
# ("goto_if", "<label>", "<var>")
# ("inc", "<var>")
# ("dec", "<var>")
# ("halt",)
# ("call", "<func>", ["<var1>", ..., "<varN>"])
# {"<func>": (["<var1>", ..., "<varN>"], ["<instruction1>", ..., "<instructionN>"])}


def validate_scope(instructions, macro_names):
    # macros is a list of macro_names
    # return list of labels, variables, and functions in the given instructions
    def_labels = []  # label definitions
    jump_labels = []  # goto and goto_if labels
    variables = []
    functions = []

    for instruction in instructions:
        if instruction[0] == "label":
            def_labels.append(instruction[1])
        elif instruction[0] == "goto":
            jump_labels.append(instruction[1])
        elif instruction[0] == "goto_if":
            jump_labels.append(instruction[1])
            variables.append(instruction[2])
        elif instruction[0] == "inc":
            variables.append(instruction[1])
        elif instruction[0] == "dec":
            variables.append(instruction[1])
        elif instruction[0] == "call":
            functions.append(instruction[1])
            variables += instruction[2]
        else:
            assert instruction[0] == "halt"
    assert len(def_labels) == len(
        set(def_labels)
    ), f"Duplicate label definitions: {def_labels}"
    assert all(
        [label in def_labels for label in jump_labels]
    ), f"Jump to undefined label: {jump_labels}"
    assert all(
        [func in macro_names for func in functions]
    ), f"Call to undefined function: {functions}"

    return def_labels, jump_labels, variables, functions


def parse(input_file):
    with open(input_file, "r") as f:
        lines = f.readlines()
    # strip all comments
    lines = [line.split("#")[0] for line in lines]
    # strip all whitespace
    lines = [line.strip() for line in lines]
    # remove empty lines
    lines = [line for line in lines if line]

    instructions = []
    macros = []
    in_macro = False

    for line in lines:
        tokens = line.split()
        if len(tokens) == 1 and tokens[0][-1] == ":":
            # label
            label = tokens[0][:-1]
            assert valid_identifier(label), "Invalid label: {}".format(label)
            (instructions if not in_macro else macro_instructions).append(
                ("label", label)
            )
        elif len(tokens) == 2 and tokens[0] == "goto":
            # goto
            label = tokens[1]
            assert valid_identifier(label), "Invalid label: {}".format(label)
            (instructions if not in_macro else macro_instructions).append(
                ("goto", label)
            )
        elif len(tokens) == 4 and tokens[0] == "goto" and tokens[2] == "if":
            # goto_if
            label = tokens[1]
            assert valid_identifier(label), "Invalid label: {}".format(label)
            assert tokens[3][-2:] == "=0", "Invalid goto_if condition: {}".format(
                tokens[3]
            )
            var = tokens[3][:-2]
            assert valid_identifier(var), "Invalid variable: {}".format(var)
            (instructions if not in_macro else macro_instructions).append(
                ("goto_if", label, var)
            )
        elif len(tokens) == 2 and tokens[0] == "inc":
            # inc
            var = tokens[1]
            assert valid_identifier(var), "Invalid variable: {}".format(var)
            (instructions if not in_macro else macro_instructions).append(("inc", var))
        elif len(tokens) == 2 and tokens[0] == "dec":
            # dec
            var = tokens[1]
            assert valid_identifier(var), "Invalid variable: {}".format(var)
            (instructions if not in_macro else macro_instructions).append(("dec", var))
        elif len(tokens) == 1 and tokens[0] == "halt":
            # halt
            (instructions if not in_macro else macro_instructions).append(("halt",))
        elif len(tokens) >= 2 and tokens[0] == "call":
            # call
            func = tokens[1]
            assert valid_identifier(func), "Invalid function name: {}".format(func)
            vars = tokens[2:]
            for var in vars:
                assert valid_identifier(var), "Invalid variable: {}".format(var)
            (instructions if not in_macro else macro_instructions).append(
                ("call", func, vars)
            )
        elif len(tokens) >= 2 and tokens[0] == "macro":
            # macro
            macro_func = tokens[1]
            assert valid_identifier(macro_func), "Invalid function name: {}".format(
                macro_func
            )
            assert not in_macro, "Cannot define a macro within a macro"
            macro_vars = tokens[2:]
            for var in macro_vars:
                assert valid_identifier(var), "Invalid variable: {}".format(var)
            in_macro = True
            macro_instructions = []
        elif len(tokens) == 1 and tokens[0] == "endmacro":
            # endmacro
            assert in_macro, "endmacro without a macro definition"
            in_macro = False
            assert macro_func not in macros
            macros.append((macro_func, macro_vars, macro_instructions))
        else:
            raise Exception("Invalid instruction: {}".format(line))
    assert not in_macro, "Unclosed macro definition"
    macro_names = [macro[0] for macro in macros]
    validate_scope(instructions, macro_names)
    for i, macro in enumerate(macros):
        # macro only allowed to call macros defined before it
        _, _, used_variables, _ = validate_scope(macro[2], macro_names[:i])
        for var in used_variables:
            # enforcing pure macros
            assert var in macro[1], f"Macro {macro[0]} uses undefined variable {var}"
    macros = {macro[0]: (macro[1], macro[2]) for macro in macros}

    return instructions, macros


def remap_scope(instructions, vars, labels):
    # mapping from old labels to new labels
    new_instructions = []
    for instruction in instructions:
        if instruction[0] == "label":
            new_instructions.append(("label", labels[instruction[1]]))
        elif instruction[0] == "goto":
            new_instructions.append(("goto", labels[instruction[1]]))
        elif instruction[0] == "goto_if":
            new_instructions.append(
                ("goto_if", labels[instruction[1]], vars[instruction[2]])
            )
        elif instruction[0] == "inc":
            new_instructions.append(("inc", vars[instruction[1]]))
        elif instruction[0] == "dec":
            new_instructions.append(("dec", vars[instruction[1]]))
        elif instruction[0] == "call":
            new_instructions.append(
                ("call", instruction[1], [vars[var] for var in instruction[2]])
            )
        else:
            assert instruction[0] == "halt"
            new_instructions.append(("halt",))
    return new_instructions


def unwrap_macros(instructions, macros):
    # return list of instructions with macros unwrapped
    while any([instruction[0] == "call" for instruction in instructions]):
        # these two lines could be optimized using the walrus operator, but eh
        idx = min(
            [
                i
                for i, instruction in enumerate(instructions)
                if instruction[0] == "call"
            ]
        )
        func = instructions[idx][1]
        variables = instructions[idx][2]
        remap_variables = {
            macros[func][0][i]: variables[i] for i in range(len(variables))
        }

        # verify that labels are unique (may not be the case due to multiple calls to macros), otherwise make them, using hash

        hash = 0
        def_labels, _, _, _ = validate_scope(instructions, macros.keys())
        assert (
            func in macros
        ), f"Call to undefined function: {func}, this should have been caught by validate_scope"
        macro_def_labels, _, _, _ = validate_scope(macros[func][1], macros.keys())
        remap_labels = {
            macro_def_labels[i]: f"{macro_def_labels[i]}_{hash}"
            for i in range(len(macro_def_labels))
        }

        macro_instructions = remap_scope(macros[func][1], remap_variables, remap_labels)
        # while the labels are not unique, increment the hash and try again
        while any(
            [
                label in def_labels
                for label in validate_scope(macro_instructions, macros.keys())[0]
            ]
        ):
            hash += 1
            remap_labels = {
                macro_def_labels[i]: f"{macro_def_labels[i]}_{hash}"
                for i in range(len(macro_def_labels))
            }
            macro_instructions = remap_scope(
                macros[func][1], remap_variables, remap_labels
            )

        instructions = instructions[:idx] + macro_instructions + instructions[idx + 1 :]

    return instructions


def write_instructions(output_file, instructions):
    output = []
    for instruction in instructions:
        if instruction[0] == "label":
            output.append(f"{instruction[1]}:")
        elif instruction[0] == "goto":
            output.append(f"goto {instruction[1]}")
        elif instruction[0] == "goto_if":
            output.append(f"goto {instruction[1]} if {instruction[2]}=0")
        elif instruction[0] == "inc":
            output.append(f"inc {instruction[1]}")
        elif instruction[0] == "dec":
            output.append(f"dec {instruction[1]}")
        elif instruction[0] == "halt":
            output.append("halt")
        else:
            raise Exception(
                "Invalid instruction: {}, this should be unreachable".format(
                    instruction
                )
            )
    with open(output_file, "w") as f:
        f.write("\n".join(output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transpile macros")
    parser.add_argument("input", type=str, help="input file")
    parser.add_argument("output", type=str, help="output file")
    args = parser.parse_args()

    instructions, macros = parse(args.input)
    instructions = unwrap_macros(instructions, macros)
    write_instructions(args.output, instructions)
