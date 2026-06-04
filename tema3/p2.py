import sys

def solve():
    input_data = sys.stdin.read().splitlines()
    lines = [line.strip() for line in input_data if line.strip()]
    if not lines:
        return

    non_terminals = set(lines[0].split())
    terminals = set(lines[1].split())
    P = int(lines[2])
    
    productions = []
    for i in range(3, 3 + P):
        parts = lines[i].split()
        lhs = parts[0]
        rhs = "".join(parts[1:]) if len(parts) > 1 else ""
        if rhs == "λ" or rhs == "lambda":
            rhs = ""
        productions.append((lhs, rhs))
        
    start_symbol = lines[3 + P]

    available_nts = [chr(i) for i in range(ord('A'), ord('Z') + 1) if chr(i) not in non_terminals]

    s_on_rhs = any(start_symbol in rhs for _, rhs in productions)
    if s_on_rhs:
        new_start = available_nts.pop(0)
        non_terminals.add(new_start)
        productions.append((new_start, start_symbol))
        start_symbol = new_start

    nullable = set()
    changed = True
    while changed:
        changed = False
        for lhs, rhs in productions:
            if lhs not in nullable:
                if all(sym in nullable for sym in rhs):
                    nullable.add(lhs)
                    changed = True

    def get_combinations(rhs, index):
        if index == len(rhs):
            return [""]
        rest = get_combinations(rhs, index + 1)
        res = []
        for r in rest:
            res.append(rhs[index] + r)
            if rhs[index] in nullable:
                res.append(r)
        return list(set(res))

    step1_prods = set()
    for lhs, rhs in productions:
        if rhs == "":
            continue
        combs = get_combinations(rhs, 0)
        for c in combs:
            if c != "":
                step1_prods.add((lhs, c))
                
    if start_symbol in nullable:
        step1_prods.add((start_symbol, ""))

    unit_pairs = set((nt, nt) for nt in non_terminals)
    changed = True
    while changed:
        changed = False
        for A, B in list(unit_pairs):
            for lhs, rhs in step1_prods:
                if lhs == B and len(rhs) == 1 and rhs in non_terminals:
                    if (A, rhs) not in unit_pairs:
                        unit_pairs.add((A, rhs))
                        changed = True

    step2_prods = set()
    for A, B in unit_pairs:
        for lhs, rhs in step1_prods:
            if lhs == B and not (len(rhs) == 1 and rhs in non_terminals):
                step2_prods.add((A, rhs))

    productive = set(terminals)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in step2_prods:
            if lhs not in productive:
                if all(sym in productive for sym in rhs) or rhs == "":
                    productive.add(lhs)
                    changed = True

    step3a_prods = set((l, r) for l, r in step2_prods if l in productive and (all(s in productive for s in r) or r == ""))

    reachable = set([start_symbol])
    changed = True
    while changed:
        changed = False
        for lhs, rhs in step3a_prods:
            if lhs in reachable:
                for sym in rhs:
                    if sym in non_terminals and sym not in reachable:
                        reachable.add(sym)
                        changed = True

    step3_prods = set((l, r) for l, r in step3a_prods if l in reachable)

    step4_prods = set()
    term_to_nt = {}
    
    for lhs, rhs in step3_prods:
        if len(rhs) >= 2:
            new_rhs = ""
            for sym in rhs:
                if sym in terminals:
                    if sym not in term_to_nt:
                        new_nt = available_nts.pop(0)
                        non_terminals.add(new_nt)
                        term_to_nt[sym] = new_nt
                        step4_prods.add((new_nt, sym))
                    new_rhs += term_to_nt[sym]
                else:
                    new_rhs += sym
            
            curr_lhs = lhs
            while len(new_rhs) > 2:
                new_nt = available_nts.pop(0)
                non_terminals.add(new_nt)
                step4_prods.add((curr_lhs, new_rhs[0] + new_nt))
                curr_lhs = new_nt
                new_rhs = new_rhs[1:]
            step4_prods.add((curr_lhs, new_rhs))
        else:
            step4_prods.add((lhs, rhs))

    final_list = list(step4_prods)
    final_list.sort(key=lambda x: (x[0] != start_symbol, x[0], len(x[1]), x[1]))
    
    for lhs, rhs in final_list:
        if rhs == "":
            print(f"{lhs} λ")
        else:
            print(f"{lhs} {rhs}")

if __name__ == "__main__":
    solve()
