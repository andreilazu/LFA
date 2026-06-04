from collections import deque

f = open("pda_input.txt").readlines()

states = []
input_alphabet = []
stack_alphabet = []
transitions = []
initial_state = ""
initial_stack_symbol = ""
final_states = []
input_string = ""

step = 0
for i, line in enumerate(f):
    line = line.strip().split()
    if not line and step != 7: continue

    if step == 0:
        states = line
        step += 1
    elif step == 1:
        input_alphabet = line
        step += 1
    elif step == 2:
        stack_alphabet = line
        step += 1
    elif step == 3:
        transitions.append((line[0], line[1], line[2], line[3], line[4]))
        if i + 1 < len(f) and len(f[i+1].strip().split()) == 1:
            step += 1
    elif step == 4:
        initial_state = line[0]
        step += 1
    elif step == 5:
        initial_stack_symbol = line[0]
        step += 1
    elif step == 6:
        final_states = line
        step += 1
    elif step == 7:
        if line:
            input_string = line[0]
        else:
            input_string = ""
        step += 1

queue = deque([(initial_state, input_string, initial_stack_symbol)])
accepted = False

visited_configs = set()

while queue:
    curr_state, curr_str, curr_stack = queue.popleft()

    if not curr_str and curr_state in final_states:
        accepted = True
        break

    config_id = (curr_state, curr_str, curr_stack)
    if config_id in visited_configs:
        continue
    visited_configs.add(config_id)

    for (q_from, char, pop_val, q_to, push_val) in transitions:
        if q_from == curr_state:

            match_input = False
            next_str = curr_str
            if char == "lambda":
                match_input = True
            elif curr_str and curr_str[0] == char:
                match_input = True
                next_str = curr_str[1:]

            if not match_input:
                continue

            match_stack = False
            next_stack = curr_stack
            if pop_val == "lambda":
                match_stack = True
            elif curr_stack and curr_stack[0] == pop_val:
                match_stack = True
                next_stack = curr_stack[1:]

            if not match_stack:
                continue

            if push_val != "lambda":

                next_stack = push_val + next_stack

            queue.append((q_to, next_str, next_stack))

if accepted:
    print("ACCEPTAT")
else:
    print("RESPINS")
