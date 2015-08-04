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

r_type_opcode = "000000"

# The different unique mips commands
commands = {
	"add": {
		"pattern": re.compile("^\s*add\s*\$(\w+)\s*,\s*\$(\w+)\s*,\s*\$(\w+)\s*$"),
		"opcode": r_type_opcode,
		"funct": "100000",
		"shampt": "00000",
		"format": "r"
	},
	"addi": {
		"pattern": re.compile("^\s*addi\s*\$(\w+)\s*,\s*\$(\w+)\s*,\s*(\d+)\s*$"),
		"opcode": "001000",
		"format": "i2"
	},
	"and": {
		"pattern": re.compile("^\s*and\s*\$(\w+)\s*,\s*\$(\w+)\s*,\s*\$(\w+)\s*$"),
		"opcode": r_type_opcode,
		"funct": "100100",
		"shampt": "00000",
		"format": "r"
	},
	"beq": {
		"pattern": re.compile("^\s*beq\s*\$(\w+)\s*,\s*\$(\w+)\s*,\s*(\w+|\d+)\s*$"),
		"opcode": "000100",
		"format": "i2"
	},
	"bne": {
		"pattern": re.compile("^\s*bne\s*\$(\w+)\s*,\s*\$(\w+)\s*,\s*(\w+|\d+)\s*$"),
		"opcode": "000101",
		"format": "i2"
	},
	"j": {
		"pattern": re.compile("^\s*j\s*(\w+|\d+)\s*$"),
		"opcode": "000010",
		"format": "j"
	},
	"or": {
		"pattern": re.compile("^\s*or\s*\$(\w+)\s*,\s*\$(\w+)\s*,\s*\$(\w+)\s*$"),
		"opcode": r_type_opcode,
		"funct": "100101",
		"shampt": "00000",
		"format": "r"
	},
	"slt": {
		"pattern": re.compile("^\s*slt\s*\$(\w+)\s*,\s*\$(\w+)\s*,\s*\$(\w+)\s*$"),
		"opcode": r_type_opcode,
		"funct": "101010",
		"shampt": "00000",
		"format": "r"
	},
	"sub": {
		"pattern": re.compile("^\s*sub\s*\$(\w+)\s*,\s*\$(\w+)\s*,\s*\$(\w+)\s*$"),
		"opcode": r_type_opcode,
		"funct": "100010",
		"shampt": "00000",
		"format": "r"
	}
}