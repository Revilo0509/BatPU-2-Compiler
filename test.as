LDI r14 10
LDI r15 0
STR r15 r14
LDI r15 0
LOD r15 r14
LDI r15 250
STR r15 r14
LDI r15 clear_chars_buffer
STR r15 r0
LDI r15 write_char
LDI r14 "H"
STR r15 r14
LDI r14 "e"
STR r15 r14
LDI r14 "l"
STR r15 r14
LDI r14 "l"
STR r15 r14
LDI r14 "o"
STR r15 r14
LDI r15 buffer_chars
STR r15 r0
LDI r14 32
LDI r15 1
STR r15 r14
LDI r14 123
LDI r15 250
STR r15 r14
LDI r15 1
LOD r15 r14
LDI r15 250
STR r15 r14
HLT