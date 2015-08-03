import sys
from core import *

"""
Just convert an integer to binary. Unfortunately, converting a negative number
invloves a slightly more complicated process since bin() doesn't work on 
negative numbers.
num - the int to convert into binary
n - the number of bits in the result
"""
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
	else:
		return "{0:b}".format(num).zfill(n)

"""
Check if a string is an integer
"""
def is_int(s):
	if len(s) < 1:
		return False
	if s[0] == "-":
		return s[1:].isdigit()
	return s.isdigit()

"""
Converts a list of mips instructions into a list of binary strings.
Returns a list of size 2. The first element is either a 0 or 1. 
0 indicates the program worked and the correct output is in the second element.
1 indicates the code wasn't properly formated and an error message is the second element.
"""
def translate(instructions):
	lines = []
	line_map = {} # Map the original instructions to the new lines in the lines list
	line_num = 1 # Variable for keeping track of errors
	current_line = 0 # The index of the current instruction being parsed

	# Find all breakpoints before parsing the commands
	for line in instructions:
		line = re.sub(comment_pattern, "", line) # Remove comments

		# Ignore empty lines
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

		# Ignore empty lines
		if line.strip() == "":
			line_num += 1
			continue

		# Ignore lines starting with breakpoints
		inline = re.search(breakpoint_inline_pattern, line)
		if inline:
			line = re.sub(breakpoint + ":", "", line) # Just remove the breakpoint; we already know the line number
		else:
			nextline = re.search(breakpoint_nextline_pattern, line)
			if nextline:
				line_num += 1 # Treat this line the same as an empy line
				continue

		# Find a matching command
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
						result += to_binary( line_map[immed]-current_line-1, 16) # -1 index because the PC automatically increments (+1 index)
					else:
						return [1, "breakpoint " + immed + " on line " + str(line_num) + " does not exist"]
					lines.append(result)

				unknown_command = False # Found an existing pattern
				break
		if unknown_command:
			return [1, "unknown pattern on line " + str(line_num)]

		line_num += 1
		current_line += 1
		
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





