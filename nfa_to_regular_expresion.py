from collections import deque

f = open("example_input.txt").readlines()

v = {}
initial_state = ""
end_states = []
alphabet = []
reverse_graph = {}
grades = {}

step = 0
for i, line in enumerate(f):
    line = line.strip().split()
    if step == 0:
        for word in line:
            v[word] = {}
            reverse_graph[word] = {}
        step += 1
    elif step == 1:
        for word in line:
            alphabet.append(word)
        step += 1
    elif step == 2:
        start = line[0]
        end = line[1]
        muchie = line[2]
        v[start][end] = muchie
        reverse_graph[end][start] = muchie
        grades[start] = grades.get(start, 0) + 1
        if(end != start):
            grades[end] = grades.get(end, 0) + 1
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

# NEW STATE, END STATE
v["new_state"] = {}
v["end_state"] = {}
reverse_graph["new_state"] = {}
reverse_graph["end_state"] = {}

v["new_state"][initial_state]= "lambda"
reverse_graph[initial_state]["new_state"] = "lambda"
grades["new_state"] =  grades.get("new_state", 0) + 1
grades[initial_state] = grades.get(initial_state,0) + 1
for state in end_states:
    v[state]["end_state"] = "lambda"
    reverse_graph["end_state"][state] = "lambda"
    grades["end_state"] =  grades.get("end_state", 0) + 1
    grades[state] = grades.get(state,0) + 1


sorted_grades = sorted(grades.items(), key = lambda item: item[1])

for node,degree in sorted_grades:
    if (node == "new_state" or node == "end_state"):
        continue
    out_states = []
    for out_node in v[node]:
        if(out_node != node):
            out_states.append(out_node)
    in_states = []
    for in_node in reverse_graph[node]:
        if(in_node != node):
            in_states.append(in_node)
    for in_node in in_states:
        for out_node in out_states:
            first_expresion = v[in_node][node]
            end_expresion = v[node][out_node]
            middle_expresion = ""
            total_expresion = first_expresion+end_expresion
            if(node in v[node]):
                middle_expresion ="(" + v[node][node] + ")*"
                total_expresion = first_expresion+middle_expresion+end_expresion
            if(out_node in v[in_node]):
                v[in_node][out_node] = v[in_node][out_node] + "∪" + total_expresion
                reverse_graph[out_node][in_node] = v[in_node][out_node] + "∪" + total_expresion
            else:
                v[in_node][out_node] = total_expresion
                reverse_graph[out_node][in_node] = total_expresion

print(v["new_state"]["end_state"].replace("lambda",""))