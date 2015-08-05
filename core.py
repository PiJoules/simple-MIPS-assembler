"""
Core instructions and registers used by MIPS
"""

import re

registers = ["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"]
# Some I formats have syntax of "rt, immed(rs)" (i1) instead of "rt, rs, immed" (i2)
formats = ["r","i1","i2","j"]

# Reusable regex patterns
comment_pattern = re.compile("\#.*")
breakpoint_inline_pattern = re.compile("^\s*(\w+)\:\s*\w+.*$") # Breakpoint is on the same line as the instruction
breakpoint_nextline_pattern = re.compile("^\s*(\w+)\:\s*$") # Breakpoint is only thing on the current line
r_pattern = lambda x: re.compile("^\s*" + x + "\s*\$(\w+)\s*,\s*\$(\w+)\s*,\s*\$(\w+)\s*$")
i1_pattern = lambda x: re.compile("^\s*" + x + "\s*\$(\w+)\s*,\s*(\d+)\s*\(\s*\$(\w+)\s*\)\s*$")
i2_pattern = lambda x: re.compile("^\s*" + x + "\s*\$(\w+)\s*,\s*\$(\w+)\s*,\s*(\w+|\d+)\s*$")
j_pattern = lambda x: re.compile("^\s*" + x + "\s*(\w+|\d+)\s*$")

r_type_opcode = "000000"

# The different unique mips commands
commands = {
	"add": {
		"opcode": r_type_opcode,
		"funct": "100000",
		"shampt": "00000",
		"format": "r"
	},
	"addi": {
		"opcode": "001000",
		"format": "i2"
	},
	"and": {
		"opcode": r_type_opcode,
		"funct": "100100",
		"shampt": "00000",
		"format": "r"
	},
	"beq": {
		"opcode": "000100",
		"format": "i2"
	},
	"bne": {
		"opcode": "000101",
		"format": "i2"
	},
	"j": {
		"opcode": "000010",
		"format": "j"
	},
	"lw": {
		"opcode": "100011",
		"format": "i1"
	},
	"or": {
		"opcode": r_type_opcode,
		"funct": "100101",
		"shampt": "00000",
		"format": "r"
	},
	"slt": {
		"opcode": r_type_opcode,
		"funct": "101010",
		"shampt": "00000",
		"format": "r"
	},
	"sw": {
		"opcode": "101011",
		"format": "i1"
	},
	"sub": {
		"opcode": r_type_opcode,
		"funct": "100010",
		"shampt": "00000",
		"format": "r"
	}
}