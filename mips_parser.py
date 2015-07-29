import sys
import re

# Static stuff
registers = ["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"]
formats = ["r","i","j"]

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
	# "addi": {

	# }
	# "and",
	# "or",
	# "slt",
	# "sub"
}

def to_binary(num):
	return "{0:b}".format(num).zfill(5)

# Converts a list of mips instructions into a list of binary strings.
# Returns a list of size 2. The first element is either a 0 or 1. 
# 0 indicates the program worked and the correct output is in the second element.
# 1 indicates the code wasn't properly formated and an error message is the second element.
def translate(instructions):
	lines = []
	line_num = 1
	for line in instructions:
		line = re.sub(comment_pattern, "", line) # Remove comments
		unkown_line = True
		for key in commands:
			command = commands[key]
			r = re.search(command["pattern"], line) # Check for an existing pattern
			if r:
				result = command["opcode"] # Line always starts with the opcode
				args = r.groups() # Get the arguments
				for arg in args: # Check if valid register
					if not arg in registers:
						return [1, "unknown register " + arg + " on line " + str(line_num)]
				f = command["format"]
				if f == "r":
					rs = registers.index(args[1])
					rt = registers.index(args[2])
					rd = registers.index(args[0])
					result += to_binary(rs) + to_binary(rt) + to_binary(rd) + command["shampt"] + command["funct"]
					lines.append(result)
			else:
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





