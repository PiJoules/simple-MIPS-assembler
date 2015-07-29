import sys
import re

registers = ["zero","at","v0","v1","a0","a1","a2","a3","t0","t1","t2","t3","t4","t5","t6","t7","s0","s1","s2","s3","s4","s5","s6","s7","t8","t9","k0","k1","gp","sp","fp","ra"]
formats = ["r","i","j"]

comment_pattern = re.compile("\#.*")
r_type_pattern = re.compile("^\s*add\s*\$(\w+)\s*,\s*\$(\w+)\s*,\s*\$(\w+)\s*$")
r_type_opcode = "000000"

commands = {
	"add": {
		"pattern": r_type_pattern,
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

lines = []
line_num = 1
for line in sys.stdin:
	line = re.sub(comment_pattern, "", line)
	unkown_line = True
	for key in commands:
		command = commands[key]
		r = re.search(command["pattern"], line)
		if r:
			result = command["opcode"]
			args = r.groups()
			for arg in args:
				if not arg in registers:
					print "unknown register", arg, "on line", str(line_num)
					sys.exit()
			f = command["format"]
			if f == "r":
				rs = registers.index(args[1])
				rt = registers.index(args[2])
				rd = registers.index(args[0])
				result += to_binary(rs) + to_binary(rt) + to_binary(rd) + command["shampt"] + command["funct"]
				lines.append(result)
		else:
			print "unknown pattern on line", str(line_num)
			sys.exit()
	line_num += 1

print "\n".join(lines)





