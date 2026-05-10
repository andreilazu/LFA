n = int(input().strip())

for i in range(n):
    stare = input().strip()

m = int(input().strip())

dic = {}
alfabet = set()

for i in range(m):
    stari = input().strip().split()
    start = stari[0]
    end = stari[1]
    litera = stari[2]

    if litera != "lambda":  
        alfabet.add(litera)

    if (start,litera) not in dic:
        dic[(start,litera)] = []
    dic[(start,litera)].append(end)

print("Alfabetul automatului este:", " ".join(sorted(list(alfabet))))

stare_initiala = input().strip()

stari_finale_numar = int(input().strip())

stari_finale = []

for i in range(stari_finale_numar):
    stare = input().strip()
    stari_finale.append(stare)

def lambda_func(stari_curente,dic):
    stiva = list(stari_curente)
    rezultat = list(stari_curente)

    while len(stiva) > 0:
        el = stiva.pop()
        if (el,"lambda") in dic:
            for vecin in dic[(el,"lambda")]:
                if vecin not in rezultat:
                    stiva.append(vecin)
                    rezultat.append(vecin)

    return rezultat

Q = int(input().strip())

coada = []

for i in range(Q):
    info = input().strip()
    coada= [stare_initiala]
    coada = lambda_func(coada,dic)
    for litera in info:
        stari_urmatoare = []
        for stare in coada:
            if(stare,litera) in dic:
                for muchie in dic[(stare,litera)]:
                    if muchie not in stari_urmatoare:
                        stari_urmatoare.append(muchie)
        coada = lambda_func(stari_urmatoare,dic)
    
    acceptat = False
    for stare in coada:
        if stare in stari_finale:
            acceptat = True
            break
            
    if acceptat:
        print("DA")
    else:
        print("NU")