import sys

regs, program = sys.stdin.read().strip().split("\n\n")

regs = regs.splitlines()
reg_a = int(regs[0].split()[-1])
reg_b = int(regs[1].split()[-1])
reg_c = int(regs[2].split()[-1])

program = list(map(int, program.split()[-1].split(",")))


def run(program, reg_a, reg_b, reg_c, expected_output=None):

    def resolve_combo(operand, reg_a, reg_b, reg_c):
        match operand:
            case 0 | 1 | 2 | 3:
                return operand, "literal"
            case 4:
                return reg_a, "reg_a"
            case 5:
                return reg_b, "reg_b"
            case 6:
                return reg_c, "reg_c"
            case 7:
                assert False, "reserved"
            case _:
                assert False, f"unknown operand {operand}"

    output = []
    i = 0
    while i < len(program):
        opcode = program[i]
        operand = program[i + 1]
        match opcode:
            case 0:
                denominator, t = resolve_combo(operand, reg_a, reg_b, reg_c)
                reg_a = reg_a // (2**denominator)
                i += 2
            case 1:
                reg_b = reg_b ^ operand
                i += 2
            case 2:
                x, t = resolve_combo(operand, reg_a, reg_b, reg_c)
                reg_b = x % 8
                i += 2
            case 3:
                if reg_a != 0:
                    i = operand
                else:
                    i += 2
            case 4:
                reg_b = reg_b ^ reg_c
                i += 2
            case 5:
                x, t = resolve_combo(operand, reg_a, reg_b, reg_c)
                output.append(x % 8)
                i += 2
            case 6:
                denominator, t = resolve_combo(operand, reg_a, reg_b, reg_c)
                reg_b = reg_a // (2**denominator)
                i += 2
            case 7:
                denominator, t = resolve_combo(operand, reg_a, reg_b, reg_c)
                reg_c = reg_a // (2**denominator)
                i += 2
            case _:
                assert False, "unknown instruction"

    return output


output = run(program, reg_a, reg_b, reg_c)
print(f"Part 1: {','.join(map(str, output))}")


def get_len(a_init):
    output, *_ = run(program, a_init, 0, 0)
    return len(output)


def find_range_start(num_digits):
    lo = 0
    hi = 1000000000000000
    while lo < hi:
        mid = (lo + hi) // 2

        if len(run(program, mid, 0, 0)) < num_digits:
            lo = mid + 1
        else:
            hi = mid
    assert len(run(program, lo, 0, 0)) == num_digits
    assert len(run(program, lo - 1, 0, 0)) == num_digits - 1
    return lo


range_begin = find_range_start(len(program))
range_end = find_range_start(len(program) + 1)
print(f"Part 2: [{range_begin}, {range_end})")
