""" Software replication of Enigma Kriegsmarine M3 Device. Author: Spencer Little """

char1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z' ]
charu = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

rotor = [4, 10, 12, 5, 11, 6, 3, 16, 21, 25, 13, 19, 14, 22, 24, 7, 23, 20, 18, 15, 0, 8, 1, 17, 2, 9]
invrotor = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

rotor1 = [0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4]
invrotor1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

rotor2 = [1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14]
invrotor2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

reflectB = [4, 13, 10, 16, 0, 20, 24, 22, 9, 8, 2, 14, 15, 1, 11, 12, 3, 23, 25, 21, 5, 19, 7, 17, 6, 18]
reflectC = [17, 3, 14, 1, 9, 13, 19, 10, 21, 4, 7, 12, 11, 5, 2, 22, 25, 0, 23, 6, 24, 8, 15, 18, 20, 16]

plugb = []
paired = []
mapped = []

def plugboard():
    global plugb
    count = 0
    print("Enter up to ten plugboard pairs, format AB. Enter q when done")
    query = input()
    while query != "q":
        if len(query)!=2:
            print("Please enter correct format")
        elif query in plugb or query[::-1] in plugb: # should two letters map to the same character?
            print("Please don't enter duplicate letters")
        else:
            plugb.append(query.lower())
            count += 1
        query = input("Next pair: (q to quit)")
        if count == 10:
            query = "q"
    for pair in plugb:
        paired.append(pair[0])
        mapped.append(pair[1])

def parse_key(key, keys, index, trk): # key, list of empty three strings, starting int usually zero
    keyseg = ""
    for char in key[index:]:
        if char == '-':
            keys.append(keyseg)
            trk += 1
            index+=1
            klist = parse_key(key, keys, index, trk)
            if klist:
                return klist
        else:
            keyseg += char
            index+=1
    if trk == 2 and len(keys) == 2: # only return in the final iteration
        keys.append(keyseg)
        return keys

def rotate_rot(rotor): # moves the rotor one position forward
    new_rotor = []
    for i in range(26):
        if i == 0:
            rotor_con = rotor[25] + 1
            if rotor_con > 25:
                rotor_con -= 26
            new_rotor.append(rotor_con)
        else:
            rotor_con = rotor[i-1] + 1
            if rotor_con > 25:
                rotor_con -= 26
            new_rotor.append(rotor_con)
    return new_rotor

def shift_rotor(rotor): # shifts the alphabet around the rotor for the ringstellung setting
    new_rotor = []
    index = 0
    new_rotor.append(rotor[25])
    for entr in rotor[1:26]:
        new_rotor.append(rotor[index])
        index+=1
    return new_rotor

def map_back(rotor, invrotor): # maps the rotor connections backwards for decryption
    index = 0
    while index < 26:
        posind = 0
        for pos in rotor:
            if pos==index:
                invrotor[index] = posind
            posind+=1
        index+=1
    return invrotor

def rst_rotors():
    global rotor
    global rotor1
    global rotor2
    rotor = [4, 10, 12, 5, 11, 6, 3, 16, 21, 25, 13, 19, 14, 22, 24, 7, 23, 20, 18, 15, 0, 8, 1, 17, 2, 9]
    rotor1 = [0, 9, 3, 10, 18, 8, 17, 20, 23, 1, 11, 7, 22, 19, 12, 2, 16, 6, 25, 13, 15, 24, 5, 21, 14, 4]
    rotor2 = [1, 3, 5, 7, 9, 11, 2, 15, 17, 19, 23, 21, 25, 13, 24, 4, 8, 22, 6, 0, 10, 12, 20, 18, 16, 14]


def rotor_ciph(rotor, rotor1, rotor2, reflect, plain_t, startg, startr, walz): # rotors, text to be encrypted, three digit keys, and walz settings
    global invrotor
    global invrotor1
    global invrotor2
    global mapped
    global paired
    rst_rotors()
    ciphert = "" # this should text plaintext as an argument and construct the paried array
    charcnt = 0
    plaint = ""
    for char in plain_t: # plugboard substitions phase 1
        if char in paired:
            for pair in plugb:
                if char in pair:
                    char = pair[1]
    for i in range(int(startg[0])): # get rotors to appropriate positions based on grundestellung settings
        rotor = rotate_rot(rotor)
    for i in range(int(startg[1])):
        rotor1 = rotate_rot(rotor1)
    for i in range(int(startg[2])):
        rotor2 = rotate_rot(rotor2)
    # shift the ringstellung settings
    for i in range(int(startr[0])):
        rotor = shift_rotor(rotor)
    for i in range(int(startr[1])):
        rotor1 = shift_rotor(rotor1)
    for i in range(int(startr[2])):
        rotor2 = shift_rotor(rotor2)

    invrotor = map_back(rotor, invrotor)
    invrotor1 = map_back(rotor1, invrotor1)
    invrotor2 = map_back(rotor2, invrotor2)

    for char in plain_t:
    # rotors step before char is enciphered
        if char == ' ': # no spaces
            pass
        elif char not in char1 and char not in charu:
            print("Cannot encrypt special characters")
        else:
            if charcnt > 76: # whats the itnerval here 25-51-76 or 25-52-77?
                charcnt = 0
            elif charcnt < 26:
                if walz[0]==1: # rotor notch settings
                    if charcnt==16:
                        rotor1 = rotate_rot(rotor1) # this is WET necessary ?
                elif walz[0]==2:
                    if charcnt==4:
                        rotor1 = rotate_rot(rotor1)
                elif walz[0]==3:
                    if charcnt==21:
                        rotor1 = rotate_rot(rotor1)
                elif walz[0]==4:
                    if charcnt==9:
                        rotor1 = rotate_rot(rotor1)
                elif walz[0]==5:
                    if charcnt==25:
                        rotor1 = rotate_rot(rotor1)
                elif walz[0]==6 or walz[0]==7 or walz[0]==8:
                    if charcnt==25:
                        rotor1 = rotate_rot(rotor1)
                    elif charcnt==11:
                        rotor1 = rotate_rot(rotor1)
                rotor = rotate_rot(rotor)
            elif charcnt < 51:
                if walz[1]==1:
                    if charcnt==41:
                        rotor2 = rotate_rot(rotor2)
                elif walz[1]==2:
                    if charcnt==29:
                        rotor2 = rotate_rot(rotor2)
                elif walz[1]==3:
                    if charcnt==46:
                        rotor2 = rotate_rot(rotor2)
                elif walz[1]==4:
                    if charcnt==34:
                        rotor2 = rotate_rot(rotor2)
                elif walz[1]==5:
                    if charcnt==50:
                        rotor2 = rotate_rot(rotor2)
                elif walz[1]==6 or walz[1]==7 or walz[1]==8:
                    if charcnt==50:
                        rotor2 = rotate_rot(rotor2)
                    elif charcnt==36:
                        rotor2 = rotate_rot(rotor2)
                rotor1 = rotate_rot(rotor1)
            else:
                if walz[2]==1:
                    if charcnt==66:
                        rotor = rotate_rot(rotor)
                elif walz[2]==2:
                    if charcnt==54:
                        rotor = rotate_rot(rotor)
                elif walz[2]==3:
                    if charcnt==71:
                        rotor = rotate_rot(rotor)
                elif walz[2]==4:
                    if charcnt==59:
                        rotor = rotate_rot(rotor)
                elif walz[2]==5:
                    if charcnt==75:
                        rotor = rotate_rot(rotor)
                elif walz[2]==6 or walz[2]==7 or walz[2]==8:
                    if charcnt==75:
                        rotor = rotate_rot(rotor)
                    elif charcnt==61:
                        rotor = rotate_rot(rotor)
                rotor2 = rotate_rot(rotor2)
            invrotor = map_back(rotor, invrotor)
            invrotor1 = map_back(rotor1, invrotor1)
            invrotor2 = map_back(rotor2, invrotor2)

        index=0
        if char == ' ': # no spaces
            pass
        elif char not in char1 and char not in charu:
            print("Cannot encrypt special characters")
        else:
            for charr in char1: # find the characters index in the alphabet
                if (charr==char) or (charr.upper()==char):
                    break
                else:
                    index+=1

            onepass = rotor2[rotor1[rotor[index]]] # pass through rotors
            refl = reflect[onepass] # put intor reflector
            charn = invrotor[invrotor1[invrotor2[refl]]] # back through invrotors in reverse
            ctchar = char1[charn]
            if ctchar in paired: # plugboard, use paired ? for some reason ?
                for pair in plugb:
                    if ctchar in pair:
                        ctchar = pair[0] # plugboard substitutions phase 2
            ciphert += ctchar
            charcnt += 1

    return ciphert

allkeys = []
walzl = []
wind = 1
start = 0
listst = 0
trk = 0
ktrk = 0
kchk = False


plugboard()
plaint = input("Text to be encrypted:")

keyg = input("Enter Grundstellung key: format 00-00-00")
while len(keyg) > 8 or len(keyg) < 5: # needs more compmlex rules to check for -
    print("Please enter the correct format for the key")
    keyg = input("Key:")
for char in keyg:
    if char=='-':
        ktrk+=1
if ktrk!=2:
    kchk=True
while kchk == True:
    print("Please enter the correct format for the key (00-00-00)")
    keyg = input("Key:")
    ktrk = 0
    for char in keyg:
        if char=='-':
            ktrk+=1
    if ktrk!=2:
        kchk=True
    else:
        kchk=False
keysg = parse_key(keyg, allkeys, start, trk)


allkeys = []
chs = ["B", "C"]
ktrk = 0
kchk = False

keyr = input("Enter Ringstellung key: format 00-00-00")
while len(keyr) > 8 or len(keyr) < 5:
    print("Please enter the correct format for the key")
    keyr = input("Key:")
for char in keyr:
    if char=='-':
        ktrk+=1
if ktrk!=2:
    kchk=True
while kchk == True:
    print("Please enter the correct format for the key (00-00-00)")
    keyr = input("Key:")
    ktrk = 0
    for char in keyr:
        if char=='-':
            ktrk+=1
    if ktrk!=2:
        kchk=True
    else:
        kchk=False
keysr = parse_key(keyr, allkeys, start, trk)

print("Walzenlag settings (rotor notch, 1-8)")
while len(walzl) !=3:
    print("Rotor", wind, "Walzenlag setting:")
    walz = int(input())
    while walz < 1 or walz > 8:
        walz = input("Please enter an interger between 1-8")
    wind+=1
    walzl.append(walz)

reflinp = input("Reflector B or C?")
while len(reflinp) != 1 or reflinp not in chs:
    relfinp = input("Please choose reflector B or C")
if reflinp == "B":
    refl = reflectB
elif reflinp == "C":
    refl = reflectC
ciphert = rotor_ciph(rotor, rotor1, rotor2, refl, plaint, keysg, keysr, walzl)
print(ciphert)
print("Decrypted:")
plaint = rotor_ciph(rotor, rotor1, rotor2, refl, ciphert, keysg, keysr, walzl)
print(plaint)
x = input()
 # legitimitacy check to make sure no chars mapped to themselves
tind = 0
failed = False
for i in range(len(plaint)):
    if ciphert[tind]==plaint[tind]:
        print("Failed. There a character mapped to itself.")
        failed = True
if failed==False:
    print("Passed! No characters mapped to themselves")
    tind+=1
