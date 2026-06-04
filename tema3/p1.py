import sys
from collections import deque

def solve():
    # Citim tot input-ul de la tastatura / fisier
    input_data = sys.stdin.read().splitlines()
    
    # Curatam liniile de spatii libere si ignoram liniile complet goale
    lines = [line.strip() for line in input_data if line.strip()]
    if not lines:
        return

    # Parsarea datelor de intrare
    non_terminals = set(lines[0].split())
    terminals = set(lines[1].split())
    P = int(lines[2])

    productions = []
    for i in range(3, 3 + P):
        parts = lines[i].split()
        lhs = parts[0]
        
        # Daca productia are o parte dreapta, unim elementele
        # Daca e lambda, o salvam ca sir vid ""
        if len(parts) > 1:
            rhs = "".join(parts[1:])
            if rhs == "λ" or rhs == "lambda":
                rhs = ""
        else:
            rhs = ""
            
        productions.append((lhs, rhs))

    start_symbol = lines[3 + P]
    X = int(lines[3 + P + 1])

    # PASUL 1: Precalcularea numarului minim de terminale pe care le poate genera fiecare simbol
    min_t = {t: 1 for t in terminals}
    for nt in non_terminals:
        min_t[nt] = float('inf')

    changed = True
    while changed:
        changed = False
        for lhs, rhs in productions:
            cost = 0
            for sym in rhs:
                if sym in min_t:
                    cost += min_t[sym]
                else:
                    cost = float('inf')
                    
            if cost < min_t[lhs]:
                min_t[lhs] = cost
                changed = True

    # PASUL 2: Generarea BFS cu derivare de stanga
    queue = deque([start_symbol])
    visited = {start_symbol}
    results = set()
    
    #Limita de siguranta extra pentru a preveni bucle de tip lambda care cresc doar in non-terminale
    max_len_form = 2 * X + len(non_terminals) + 10

    while queue:
        curr = queue.popleft()


        is_all_terminals = True
        for sym in curr:
            if sym in non_terminals:
                is_all_terminals = False
                break
        if is_all_terminals:
            if len(curr) == X:
                results.add(curr)
            continue

        # PASUL 3: Pruning
        current_min_len = 0
        valid_form = True
        for sym in curr:
            if sym in min_t:
                current_min_len += min_t[sym]
            else:
                valid_form = False
                break
                

        if not valid_form or current_min_len > X:
            continue


        if len(curr) > max_len_form:
            continue

        # PASUL 4: Expansiunea sirului
        first_nt_idx = -1
        for idx, sym in enumerate(curr):
            if sym in non_terminals:
                first_nt_idx = idx
                break

        if first_nt_idx != -1:
            nt = curr[first_nt_idx]
            # Incercam sa inlocuim non-terminalul cu toate productiile sale
            for lhs, rhs in productions:
                if lhs == nt:
                    new_form = curr[:first_nt_idx] + rhs + curr[first_nt_idx + 1:]
                    if new_form not in visited:
                        visited.add(new_form)
                        queue.append(new_form)


    if not results:
        print("NU EXISTA")
    else:
        for word in sorted(list(results)):
            if word == "":
                print("λ")
            else:
                print(word)

if __name__ == "__main__":
    solve()
