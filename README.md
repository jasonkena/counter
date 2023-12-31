# Counter Program Macro Transpiler
This repository implements a transpiler which enables macros to be used for counter program descriptions, as a project for Prof. Howard Straubing's `CSCI3384: Computability and Computational Complexity`.

The transpilation can be generated by running `python3 transpile_macros.py <input_file> <output_file>`. The `output_file` can now be run using `countermachine.py` since the macros are unwrapped.

Accepted instructions are of the form:
```
<label>:
goto <label>
goto <label> if <var>=0
inc <var>
dec <var>
halt
call <func> <var1> ... <varN>

macro <func> <var1> ... <varN>:
endmacro
```
Note that the identifiers are expected to be alphanumeric (+ underscore).

A few limitations:
- Macro definitions cannot be nested
- Macros can only call previously defined macros (this prevents infinite calling recursion)
- Macros can only modify variables which are passed in as arguments (allowing easy implementation of namespaces)
- Macros cannot "jump" to a label outside of the macro definition

All these conditions are verified by the transpiler.

The program resolves colliding labels (i.e., due to repeated macro calls) by incrementing a [hash](https://github.com/jasonkena/counter/blob/8bc9be833f9b613bbcf0b4476288f9b08988bd60/transpile_macros.py#L246C8-L246C8). Macros are unwrapped [recursively](https://github.com/jasonkena/counter/blob/8bc9be833f9b613bbcf0b4476288f9b08988bd60/transpile_macros.py#L217).

Sample cases are provided in `tests/`. Notably `ok_1.mcp`/`ok_1.cp` demonstrates how a 3-counter machine can be implemented using 2-counters via prime-factorization, aided by macros.
