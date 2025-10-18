numReactants = int(input("num reactants: "))
numProducts = int(input("num products: "))

numInputs = numReactants + numProducts
numFoundElements = 0
numInts = 0

finalStr = ""

foundElements = []
reactants = []
takenRow = []
takenCol = []
products = []
counts = []
seq2 = []
seq = []

resVals = {}
finals = {}
vars1 = {}
vars2 = {}
mains = {}

for i in range(numReactants):
    reactant = [{} for _ in range(int(input(f"num atoms in reactant #{i + 1}: ")))]

    for i in range(len(reactant)):
        idx = input(f"atom #{i + 1} name: ")

        if not idx in foundElements:
            numFoundElements += 1

            foundElements.append(idx)
        
        reactant[i][idx] = int(input("amount: "))
    
    reactants.append(reactant)

matrix = [[] for _ in range(numFoundElements)]

for i in range(numProducts):
    product = [{} for _ in range(int(input(f"num atoms in product #{i + 1}: ")))]

    for i in range(len(product)):
        idx = input(f"atom #{i + 1} name: ")
        
        product[i][idx] = int(input("amount: "))
    
    products.append(product)

for i, v in enumerate(reactants):
    v1: dict

    for v2 in v:
        for key in v2.keys():
            data = {i: v2[key]}

            if vars1.get(key):
                vars1[key] |= data
            else:
                vars1[key] = data

for i, v in enumerate(products):
    v2: dict

    for v2 in v:
        for key in v2.keys():
            data = {i + numReactants: -v2[key]}

            if vars2.get(key):
                vars2[key] |= data
            else:
                vars2[key] = data

for i, key in enumerate(vars1.keys()):
    z: dict = vars1[key] | vars2[key]

    matrix[i] = [0] * numInputs

    for key2 in z.keys():
        matrix[i][key2] = z[key2]

square = min(numFoundElements, numInputs)

neighborZeros = []

for i in range(numFoundElements):
    arr = []

    for _ in range(numInputs):
        arr.append(0)
    
    neighborZeros.append(arr)

for i in range(numFoundElements):
    for i2 in range(numInputs):
        if matrix[i][i2] == 0:
            continue

        for i3 in range(numFoundElements):
            if i3 != i and matrix[i3][i2] == 0:
                neighborZeros[i][i2] += 1

        for i3 in range(numInputs):
            if i3 != i2 and matrix[i][i3] == 0:
                neighborZeros[i][i2] += 1

goalVal = max([max(neighborZeros[i]) for i in range(numFoundElements)])

for i in range(goalVal, 0, -1):
    for i2 in range(numFoundElements):
        for i3 in range(numInputs):
            if neighborZeros[i2][i3] == i and not mains.get(i2) and not i2 in takenRow and not i3 in takenCol:
                mains[i2] = i3

                takenRow.append(i2)
                takenCol.append(i3)

for i, i2 in mains.items():
    divisor = -matrix[i][i2]

    for i3 in range(numInputs):
        matrix[i][i3] /= divisor

    matrix[i][i2] *= -1

for i in range(numFoundElements):
    if i in mains.keys():
        m = matrix[i].copy()

        m[mains[i]] = 0

        resVals[chr(65 + mains[i])] = m

for i in range(numInputs):
    short = []
    idx = False

    for i2 in range(numFoundElements):
        if matrix[i2][i] != 0:
            short.append(1)

            idx = i2

    if len(short) == 1 and idx and i in mains.keys():
        m = matrix[idx].copy()

        m[mains[idx]] = 0

        resVals[chr(65 + mains[idx])] = m

keys = list(resVals.keys())

keys.sort()

resVals = {i: resVals[i] for i in keys}

wanteds = [0] * numInputs

for i in range(numInputs):
    map = resVals.get(chr(65 + i))

    if not map:
        wanteds[i] = numInputs

        continue

    for i2, v in enumerate(map):
        if v != 0:
            wanteds[i] += 1

target = wanteds.index(max(wanteds))

for i in range(numInputs):
    finals[chr(65 + i)] = 0

while sum(1 for i in range(numInputs) if finals[chr(65 + i)] % 1 == 0 and finals[chr(65 + i)] != 0) != numInputs:
    targetChar = chr(65 + target)
    finals[targetChar] += 1

    for i in range(numInputs):
        if i != target:
            finals.pop(chr(65 + i))

    while len(finals) != numInputs:
        for i, v in resVals.items():
            sumRes = 0
            impossible = False

            for i2, v2 in enumerate(v):
                final = finals.get(chr(65 + i2))

                if not final:
                    if v2 != 0:
                        impossible = True

                    continue

                sumRes += final * v2

            if not impossible and i != targetChar:
                finals[i] = sumRes

keys = list(finals.keys())

keys.sort()

finals = {i: finals[i] for i in keys}

for i, v in enumerate(finals.values()):
    if i >= numReactants:
        continue

    mol = ""

    d: dict

    for d in reactants[i]:
        for atom, amount in d.items():
            mol += atom

            if amount != 1:
                mol += str(amount)

    if v == 1:
        seq.append(mol)
    else:
        seq.append(f"{int(v)} {mol}")

for i, v in enumerate(finals.values()):
    if i < numReactants:
        continue

    mol = ""

    d: dict

    for d in products[i - numReactants]:
        for atom, amount in d.items():
            mol += atom

            if amount != 1:
                mol += str(amount)

    if v == 1:
        seq2.append(mol)
    else:
        seq2.append(f"{int(v)} {mol}")

finalStr = f"\n{" + ".join(seq)} --> {" + ".join(seq2)}\n"

print(finalStr)