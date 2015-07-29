import sys
import re

# Static stuff
registers = ["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"]
# Some I formats have syntax of "rt, immed(rs)" instead of "rt, rs, immed"
formats = ["r","i1","i2","j"]

# Reusable stuff
comment_pattern = re.compile("\#.*")
r_type_opcode = "000000"

# The differen unique mips commands
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
		"format": "i1"
	},
	"and": {
		"pattern": re.compile("^\s*and\s*\$(\w+)\s*,\s*\$(\w+)\s*,\s*\$(\w+)\s*$"),
		"opcode": r_type_opcode,
		"funct": "100100",
		"shampt": "00000",
		"format": "r"
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

def to_binary(num, n=5):
	return "{0:b}".format(num).zfill(n)

# Converts a list of mips instructions into a list of binary strings.
# Returns a list of size 2. The first element is either a 0 or 1. 
# 0 indicates the program worked and the correct output is in the second element.
# 1 indicates the code wasn't properly formated and an error message is the second element.
def translate(instructions):
	lines = []
	line_num = 1
	for line in instructions:
		if line.strip() == "":
			line_num += 1
			continue

		unknown_command = True
		line = re.sub(comment_pattern, "", line) # Remove comments
		for key in commands:
			command = commands[key]
			r = re.search(command["pattern"], line) # Check for an existing pattern
			if r:
				result = command["opcode"] # Line always starts with the opcode
				f = command["format"]
				args = r.groups() # Get the arguments
				if f == "r":
					# Check if valid register
					if not args[0] in registers:
						return [1, "unknown register " + args[0] + " on line " + str(line_num)]
					if not args[1] in registers:
						return [1, "unknown register " + args[1] + " on line " + str(line_num)]
					if not args[2] in registers:
						return [1, "unknown register " + args[2] + " on line " + str(line_num)]

					rs = registers.index(args[1])
					rt = registers.index(args[2])
					rd = registers.index(args[0])
					result += to_binary(rs) + to_binary(rt) + to_binary(rd) + command["shampt"] + command["funct"]
					lines.append(result)
				elif f == "i1":
					if not args[0] in registers:
						return [1, "unknown register " + args[0] + " on line " + str(line_num)]
					if not args[1] in registers:
						return [1, "unknown register " + args[1] + " on line " + str(line_num)]

					rs = registers.index(args[1])
					rt = registers.index(args[0])
					immed = int(args[2])
					result += to_binary(rs) + to_binary(rt) + to_binary(immed,16)
					lines.append(result)
				unknown_command = False
				break
		if unknown_command:
			return [1, "unknown pattern on line " + str(line_num)]
		line_num += 1
	return [0, lines]


if __name__ == "__main__":
	lines = []
	for line in sys.stdin:
		lines.append(line)
	result = translate(lines)
	if result[0] == 0:
		print "\n".join(result[1])
	else:
		print result[1]





