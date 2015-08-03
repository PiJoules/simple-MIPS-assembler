import sys
import re

# Static stuff
registers = ["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"]
# Some I formats have syntax of "rt, immed(rs)" (i1) instead of "rt, rs, immed" (i2)
formats = ["r","i1","i2","j"]

# Reusable stuff
comment_pattern = re.compile("\#.*")
breakpoint_inline_pattern = re.compile("^\s*(\w+)\:\s*\w+.*$") # breakpoint is on the same line as the instruction
breakpoint_nextline_pattern = re.compile("^\s*(\w+)\:\s*$") # breakpoint is only thing on the current line

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
	"beq": {
		"pattern": re.compile("^\s*beq\s*\$(\w+)\s*,\s*\$(\w+)\s*,\s*(\w+|\d+)\s*$"),
		"opcode": "000100",
		"format": "i2"
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
	if num < 0:
		# bin() of a negative number returns -thesignednum (bin(-5) => -0b101 instead of 1011)
		# Run the process for multiplying a positive number by -1
		result = bin(num)[3:].zfill(n)
		for i in range(len(result)): # Flip the bits
			if result[i] == "0":
				result = result[:i] + "1" + result[i+1:]
			else:
				result = result[:i] + "0" + result[i+1:]
		# Add 1
		carry = 0
		for i in range(len(result)-1,-1,-1):
			if result[i] == "0" and carry == 0:
				result = result[:i] + "1" + result[i+1:]
				break
			elif result[i] == "1" and carry == 0:
				carry = 1
				result = result[:i] + "0" + result[i+1:]
			elif result[i] == "0" and carry == 1:
				result = result[:i] + "1" + result[i+1:]
				break
			elif result[i] == "1" and carry == 1:
				result = result[:i] + "0" + result[i+1:]
		return result
	return "{0:b}".format(num).zfill(n)

def find_breakpoints(instructions):
	breakpoints = {}
	for i in range(len(instructions)):
		line = instructions[i]
		inline = re.search(breakpoint_inline_pattern, line)
		if inline:
			breakpoint = inline.groups()[0]
			breakpoints[breakpoint] = i+1
			continue
		nextline = re.search(breakpoint_nextline_pattern, line)
		if nextline:
			breakpoint = nextline.groups()[0]
			breakpoints[breakpoint] = i+1
			continue
	return breakpoints

def is_int(s):
	if len(s) < 1:
		return False
	if s[0] == "-":
		return s[1:].isdigit()
	return s.isdigit()

# Converts a list of mips instructions into a list of binary strings.
# Returns a list of size 2. The first element is either a 0 or 1. 
# 0 indicates the program worked and the correct output is in the second element.
# 1 indicates the code wasn't properly formated and an error message is the second element.
def translate(instructions):
	lines = []
	breakpoints = []
	line_map = {} # Map the original instructions to the new lines in the lines list
	line_num = 1 # Variable for keeping track of errors
	current_line = 0 # The index of the current instruction being parsed

	# Find all breakpoints before parsing the commands
	for line in instructions:
		line = re.sub(comment_pattern, "", line) # Remove comments

		if line.strip() == "":
			continue

		inline = re.search(breakpoint_inline_pattern, line)
		if inline:
			breakpoint = inline.groups()[0]
			line_map[breakpoint] = current_line
		else:
			nextline = re.search(breakpoint_nextline_pattern, line)
			if nextline:
				breakpoint = nextline.groups()[0]
				line_map[breakpoint] = current_line
				continue
		current_line += 1

	current_line = 0 # Reset the counter
	for line in instructions:
		unknown_command = True
		line = re.sub(comment_pattern, "", line) # Remove comments

		if line.strip() == "":
			line_num += 1
			continue

		# Ignore lines starting with breakpoints
		inline = re.search(breakpoint_inline_pattern, line)
		if inline:
			line = re.sub(breakpoint + ":", "", line) # Just remove the breakpoint
		else:
			nextline = re.search(breakpoint_nextline_pattern, line)
			if nextline:
				line_num += 1 # Treat this line the same as an empy line
				continue

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
				elif f == "i2":
					if not args[0] in registers:
						return [1, "unknown register " + args[0] + " on line " + str(line_num)]
					if not args[1] in registers:
						return [1, "unknown register " + args[1] + " on line " + str(line_num)]

					rs = registers.index(args[0])
					rt = registers.index(args[1])
					immed = args[2]

					result += to_binary(rs) + to_binary(rt)

					if is_int(immed): # Check if integer
						result += to_binary(int(immed),16)
					elif immed in line_map:
						result += to_binary( line_map[immed]-current_line )
						print to_binary( line_map[immed]-current_line )
						print current_line, immed
					else:
						return [1, "breakpoint " + immed + " on line " + str(line_num) + " does not exist"]

				unknown_command = False
				break
		if unknown_command:
			return [1, "unknown pattern on line " + str(line_num)]
		line_num += 1
		current_line += 1
	print line_map
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





