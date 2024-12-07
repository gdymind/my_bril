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
            # if the current block is not empty, yield it
            if current_block:
                yield current_block
            current_block = [instr]

    if current_block:
        yield current_block

def label_blocks(blocks):
    mapping = {}
    i = 0
    for block in blocks:
        if 'label' in block[0]:
            name = block[0]['label']
            block.pop(0)
        else:
            name = f"BLK_{i}"
            i += 1
        mapping[name] = block
    return mapping

def add_edges(name2block):
    for _, block in name2block.items():
        last_instr = block[-1]
        if last_instr['op'] in TERMINATORS:
            print(last_instr)

def mycfg():
    program =  json.load(sys.stdin)
    for function in program['functions']:
        blocks = list(form_blocks(function['instrs']))
        for block in blocks:
            print(block)
        name2block = label_blocks(blocks)
        print(name2block)
        # for name, block in name2block.items():
        #     print(name)
        #     for instr in block:
        #         print(instr)
        #     last_instr = block[-1]
        #     # if the last instruction is a jump instruction,
        #     # we need to add an edge
        #     if last_instr['op'] == 'jmp':
        #         print(last_instr)
if __name__ == "__main__":
    mycfg()
 