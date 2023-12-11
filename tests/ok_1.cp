loop_decr_b:
loop_check_3_divide_0:
goto loop_check_3_restore_no_0 if a=0
dec a
goto loop_check_3_fail_1_0 if a=0
dec a
goto loop_check_3_fail_2_0 if a=0
dec a
inc b
goto loop_check_3_divide_0
loop_check_3_fail_1_0:
inc a
goto loop_check_3_restore_yes_0
loop_check_3_fail_2_0:
inc a
inc a
goto loop_check_3_restore_yes_0
loop_check_3_restore_no_0:
goto no_0 if b=0
dec b
inc a
inc a
inc a
goto loop_check_3_restore_no_0
loop_check_3_restore_yes_0:
goto yes_0 if b=0
dec b
inc a
inc a
inc a
goto loop_check_3_restore_yes_0
no_0:
inc b
yes_0:
goto loop_decr_c if b=0
dec b
loop_dec_3_divide_0:
goto loop_dec_3_cleanup_0 if a=0
dec a
goto loop_dec_3_fail_1_0 if a=0
dec a
goto loop_dec_3_fail_2_0 if a=0
dec a
inc b
goto loop_dec_3_divide_0
loop_dec_3_cleanup_0:
goto finish_0 if b=0
dec b
inc a
goto loop_dec_3_cleanup_0
loop_dec_3_fail_1_0:
inc a
goto loop_dec_3_restore_0
loop_dec_3_fail_2_0:
inc a
inc a
goto loop_dec_3_restore_0
loop_dec_3_restore_0:
goto finish_0 if b=0
dec b
inc a
inc a
inc a
goto loop_dec_3_restore_0
finish_0:
loop_inc_2_divide_1:
goto loop_inc_2_cleanup_1 if a=0
dec a
inc b
inc b
goto loop_inc_2_divide_1
loop_inc_2_cleanup_1:
goto finish_1 if b=0
dec b
inc a
goto loop_inc_2_cleanup_1
finish_1:
goto loop_decr_b
loop_decr_c:
loop_check_5_divide_1:
goto loop_check_5_restore_no_1 if a=0
dec a
goto loop_check_5_fail_1_1 if a=0
dec a
goto loop_check_5_fail_2_1 if a=0
dec a
goto loop_check_5_fail_3_1 if a=0
dec a
goto loop_check_5_fail_4_1 if a=0
dec a
inc b
goto loop_check_5_divide_1
loop_check_5_fail_1_1:
inc a
goto loop_check_5_restore_yes_1
loop_check_5_fail_2_1:
inc a
inc a
goto loop_check_5_restore_yes_1
loop_check_5_fail_3_1:
inc a
inc a
inc a
goto loop_check_5_restore_yes_1
loop_check_5_fail_4_1:
inc a
inc a
inc a
inc a
goto loop_check_5_restore_yes_1
loop_check_5_restore_no_1:
goto no_1 if b=0
dec b
inc a
inc a
inc a
inc a
inc a
goto loop_check_5_restore_no_1
loop_check_5_restore_yes_1:
goto yes_1 if b=0
dec b
inc a
inc a
inc a
inc a
inc a
goto loop_check_5_restore_yes_1
no_1:
inc b
yes_1:
goto finish if b=0
dec b
loop_dec_5_divide_2:
goto loop_dec_5_cleanup_2 if a=0
dec a
goto loop_dec_5_fail_1_2 if a=0
dec a
goto loop_dec_5_fail_2_2 if a=0
dec a
goto loop_dec_5_fail_3_2 if a=0
dec a
goto loop_dec_5_fail_4_2 if a=0
dec a
inc b
goto loop_dec_5_divide_2
loop_dec_5_cleanup_2:
goto finish_2 if b=0
dec b
inc a
goto loop_dec_5_cleanup_2
loop_dec_5_fail_1_2:
inc a
goto loop_dec_5_restore_2
loop_dec_5_fail_2_2:
inc a
inc a
goto loop_dec_5_restore_2
loop_dec_5_fail_3_2:
inc a
inc a
inc a
goto loop_dec_5_restore_2
loop_dec_5_fail_4_2:
inc a
inc a
inc a
inc a
goto loop_dec_5_restore_2
loop_dec_5_restore_2:
goto finish_2 if b=0
dec b
inc a
inc a
inc a
inc a
inc a
goto loop_dec_5_restore_2
finish_2:
loop_inc_2_divide_3:
goto loop_inc_2_cleanup_3 if a=0
dec a
inc b
inc b
goto loop_inc_2_divide_3
loop_inc_2_cleanup_3:
goto finish_3 if b=0
dec b
inc a
goto loop_inc_2_cleanup_3
finish_3:
goto loop_decr_c
finish:
halt