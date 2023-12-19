add_setup_0:
goto add_loop_0 if a=0
dec a
inc e
goto add_setup_0
add_loop_0:
goto add_finish_0 if e=0
dec e
inc a
inc d
goto add_loop_0
add_finish_0:
multiply_loop_0:
goto multiply_finish_0 if d=0
dec d
add_setup_1:
goto add_loop_1 if b=0
dec b
inc e
goto add_setup_1
add_loop_1:
goto add_finish_1 if e=0
dec e
inc b
inc c
goto add_loop_1
add_finish_1:
goto multiply_loop_0
multiply_finish_0:
halt