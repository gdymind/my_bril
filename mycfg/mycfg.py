import json
import sys
from collections import OrderedDict
from graphviz import Digraph
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
            name = f"BLK{i}"
            i += 1
        mapping[name] = block
    return mapping

def get_cfg(name2block):
    cfg = OrderedDict() # maintain the order of insertion
    for i, (name, block) in enumerate(name2block.items()):
        last_instr = block[-1]
        if last_instr['op'] in ['jmp', 'br']:
            cfg[name] = last_instr['labels']
        elif last_instr['op'] == 'ret':
            cfg[name] = []
        else:
            # add an edge to the next block if it exists
            if i < len(name2block) - 1:
                cfg[name] = [list(name2block.keys())[i+1]]
            else:
                cfg[name] = []
    return cfg

def mycfg():
    program =  json.load(sys.stdin)
    for function in program['functions']:
        blocks = list(form_blocks(function['instrs']))
        name2block = label_blocks(blocks)
        cfg = get_cfg(name2block)
        for label, next_labels in cfg.items():
            print(f"{label} -> {next_labels}")
        
        # visualize the CFG using graphviz
        dot = Digraph(comment='CFG')
        for label, next_labels in cfg.items():
            for next_label in next_labels:
                dot.edge(label, next_label)
        dot.render(f"{function['name']}", view=True)

if __name__ == "__main__":
    mycfg()
 