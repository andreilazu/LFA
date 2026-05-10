from collections import deque

f = open("example_input.txt").readlines()

v = {}
initial_state = ""
end_states = []
alphabet = []

step = 0
for i, line in enumerate(f):
    line = line.strip().split()
    if step == 0:
        for word in line:
            v[word] = []
        step += 1
    elif step == 1:
        for word in line:
            alphabet.append(word)
        step += 1
    elif step == 2:
        start = line[0]
        end = line[1]
        muchie = line[2]
        v[start].append((end, muchie))
        if len(f[i+1].strip().split()) <= 1:
            step += 1
    elif step == 3:
        initial_state = line[0]
        step += 1
    elif step == 4:
        for state in line:
            end_states.append(state)
        step += 1
    else:
        print("Prea multe linii")
        break

def lambda_closure(states):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        for next_state, edge in v.get(state, []):
            if edge == "lambda" and next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)
    return sorted(closure)

DFA = {}
Q = deque()

initial_closure = lambda_closure([initial_state])
Q.append(initial_closure)

while Q:
    current_states = Q.popleft()
    current_tuple = tuple(current_states)
    if current_tuple in DFA:
        continue
    DFA[current_tuple] = {}
    for symbol in alphabet:
        reachable = set()
        for state in current_states:
            for next_state, edge in v.get(state, []):
                if edge == symbol:
                    reachable.add(next_state)
        if reachable:
            next_states = lambda_closure(reachable)
            next_tuple = tuple(next_states)
            DFA[current_tuple][symbol] = next_tuple
            if next_tuple not in DFA:
                Q.append(next_states)
        else:
            DFA[current_tuple][symbol] = ()

dead_state = ()
if dead_state not in DFA:
    DFA[dead_state] = {symbol: dead_state for symbol in alphabet}

# Identify final states in DFA
dfa_final_states = []
for dfa_state in DFA:
    if any(original_final in dfa_state for original_final in end_states):
        dfa_final_states.append(dfa_state)

print("=== DFA before minimization ===")
print("DFA States:", list(DFA.keys()))
print("DFA Transitions:")
for state, transitions in DFA.items():
    print(f"{state}: {transitions}")
print("DFA Final States:", dfa_final_states)

# ---------- Minimization ----------
# Map each DFA state to an index
state_to_idx = {state: i for i, state in enumerate(DFA.keys())}
idx_to_state = list(DFA.keys())
n = len(DFA)

# Table of distinguishable pairs (only i < j)
dist = [[False] * n for _ in range(n)]

# Mark final vs non-final
for i in range(n):
    for j in range(i+1, n):
        s_i = idx_to_state[i]
        s_j = idx_to_state[j]
        if (s_i in dfa_final_states) != (s_j in dfa_final_states):
            dist[i][j] = True

# Iteratively mark distinguishable pairs
changed = True
while changed:
    changed = False
    for i in range(n):
        for j in range(i+1, n):
            if dist[i][j]:
                continue
            for letter in alphabet:
                next_i = state_to_idx[DFA[idx_to_state[i]][letter]]
                next_j = state_to_idx[DFA[idx_to_state[j]][letter]]
                a, b = min(next_i, next_j), max(next_i, next_j)
                if dist[a][b]:
                    dist[i][j] = True
                    changed = True
                    break

# Union‑find for indistinguishable states
parent = list(range(n))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(x, y):
    rx, ry = find(x), find(y)
    if rx != ry:
        parent[ry] = rx

for i in range(n):
    for j in range(i+1, n):
        if not dist[i][j]:   # dist[i][j] = indistinguishable
            union(i, j)

rep_to_new = {}
new_idx = 0
for i in range(n):
    root = find(i)
    if root not in rep_to_new:
        rep_to_new[root] = new_idx
        new_idx += 1

# Build minimized DFA transitions
minimized_dfa = {}
for root, new_state_id in rep_to_new.items():
    original_state = idx_to_state[root]
    transitions = {}
    for letter in alphabet:
        next_state = DFA[original_state][letter]
        next_idx = state_to_idx[next_state]
        next_root = find(next_idx)
        new_next = rep_to_new[next_root]
        transitions[letter] = new_next
    minimized_dfa[new_state_id] = transitions

minimized_final = []
for root, new_id in rep_to_new.items():
    class_states = [idx_to_state[i] for i in range(n) if find(i) == root]
    if any(st in dfa_final_states for st in class_states):
        minimized_final.append(new_id)

print("\n=== Minimized DFA ===")
print("States:", list(minimized_dfa.keys()))
print("Transitions:")
for state, trans in minimized_dfa.items():
    print(f"{state}: {trans}")
print("Final states:", minimized_final)