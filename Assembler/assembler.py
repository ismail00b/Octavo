
"""Simple Octavo assembler for initial testing."""

thread_count        = 8
branch_entry_count  = 4
address_entry_count = 4   

def blank_memory(depth):
    return [0 for i in range(depth)]

A_Memory    = blank_memory(1024) 
B_Memory    = blank_memory(1024) 
I_Memory    = blank_memory(1024) 
OD_Memory   = blank_memory(16 * thread_count) 
DO_Memory   = blank_memory(1  * thread_count) 
PO_Memory   = blank_memory(branch_entry_count  * thread_count) 
AD_Memory   = blank_memory(address_entry_count * thread_count) 

# ---------------------------------------------------------------------

opcode_width    = 4
D_width         = 12
DA_width        = 6
DB_width        = 6
A_width         = 10
B_width         = 10

opcode_shift    = D_width + A_width + B_width
D_shift         = A_width + B_width
DA_shift        = A_width + B_width + DB_width
DB_shift        = A_width + B_width
A_shift         = B_width
B_shift         = 0

def width_mask(width):
    return (1 << width) - 1

def dump_format(width):
    """Numbers must be represented as zero-padded whole hex numbers"""
    characters  = width // 4
    remainder   = width % 4
    characters += min(1, remainder)
    format_string = "{:0" + str(characters) + "x}"
    return format_string

def mem_dump(memory, width, file_name):
    """Write a memory into a $readmemh() Verilog format."""
    # Lifted from Modelsim's output of $writememh
    file_header  = """// format=hex addressradix=h dataradix=h version=1.0 wordsperline=1 noaddress"""
    with open(file_name, 'w') as f:
        f.write(file_header + "\n")
        format_string = dump_format(width)
        for entry in memory:
            output = format_string.format(entry)
            f.write(output + "\n")

def assemble_simple_instruction(op, D, A, B):
    return (op << opcode_shift) | (D << D_shift) | (A << A_shift) | (B << B_shift)

def assemble_split_instruction(op, DA, DB, A, B):
    return (op << opcode_shift) | (DA << DA_shift) | (DB << DB_shift) | (A << A_shift) | (B << B_shift)

# ---------------------------------------------------------------------

dyadic_op_width     = 4

DYADIC_ALWAYS_ZERO  = 0b0000
DYADIC_A_AND_B      = 0b1000
DYADIC_A_AND_NOT_B  = 0b0100
DYADIC_A            = 0b1100
DYADIC_NOT_A_AND_B  = 0b0010
DYADIC_B            = 0b1010
DYADIC_A_XOR_B      = 0b0110
DYADIC_A_OR_B       = 0b1110
DYADIC_A_NOR_B      = 0b0001
DYADIC_A_XNOR_B     = 0b1001
DYADIC_NOT_B        = 0b0101
DYADIC_A_OR_NOT_B   = 0b1101
DYADIC_NOT_A        = 0b0011
DYADIC_NOT_A_OR_B   = 0b1011
DYADIC_A_NAND_B     = 0b0111
DYADIC_ALWAYS_ONE   = 0b1111

alu_op_width            = 20

TRIADIC_SINGLE          = 0b0
TRIADIC_DUAL            = 0b1
SELECT_R                = 0b00
SELECT_R_ZERO           = 0b01
SELECT_R_NEG            = 0b10
SELECT_S                = 0b11
SHIFT_NONE              = 0b00
SHIFT_RIGHT             = 0b01
SHIFT_RIGHT_SIGNED      = 0b10
SHIFT_LEFT              = 0b11
SPLIT_YES               = 0b1
SPLIT_NO                = 0b0
ADDSUB_A_PLUS_B         = 0b00
ADDSUB_MINUS_A_PLUS_B   = 0b01
ADDSUB_A_MINUS_B        = 0b10
ADDSUB_MINUS_A_MINUS_B  = 0b11

select_width    = 1
dyadic1_width   = 2
dyadic2_width   = 2
dual_width      = 1
addsub_width    = 2
dyadic3_width   = 2
shift_width     = 2
split_width     = 1

split_shift     = shift_width + dyadic3_width + addsub_width + dual_width + dyadic2_width + dyadic1_width + select_width
shift_shift     = dyadic3_width + addsub_width + dual_width + dyadic2_width + dyadic1_width + select_width
dyadic3_shift   = addsub_width + dual_width + dyadic2_width + dyadic1_width + select_width
addsub_shift    = dual_width + dyadic2_width + dyadic1_width + select_width
dual_shift      = dyadic2_width + dyadic1_width + select_width
dyadic2_shift   = dyadic1_width + select_width
dyadic1_shift   = select_width
select_shift    = 0

def configure_opcode(split, shift, dyadic3, addsub, dual, dyadic2, dyadic1, select):
    return (split << split_shift) | (shift << shift_shift) | (dyadic3 << dyadic3_shift) | (addsub << addsub_shift) | (dual << dual_shift) | (dyadic2 << dyadic2_shift) | (dyadic1 << dyadic1_shift) | (select << select_shift)

# ---------------------------------------------------------------------

# ---------------------------------------------------------------------

if __name__ == "__main__":
    print "Done!"

