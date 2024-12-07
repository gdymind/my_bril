import json
import sys

# note that   'call' is not a terminator,
# because it will return to the instruction following it
TERMINATORS = ['ret', 'jmp', 'br']

def form_blocks(instrs):
    current_block = []
     
    for instr in instrs:
        if 'op' in instr: # actual instruction
            current_block.append(instr) 
            # check for terminators
            if instr['op'] in TERMINATORS:
                yield current_block
                current_block = []
        else: # label 
            yield current_block
            current_block = [instr]

    yield current_block

def mycfg():
    program =  json.load(sys.stdin)
    for function in program['functions']:
        for block in form_blocks(function['instrs']):
            print(block)
 
if __name__ == "__main__":
    mycfg()
 