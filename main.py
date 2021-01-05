class monster(object):
    def __init__(self, genes, parents, line, sex, name, age=0):
        self.age = age
        self.genes = genes
        self.stats = [0,0,0,0]
        self.skills = [0,0,0,0]
        self.genstats()
        self.parents = parents
        self.line = line
        self.id = randint(100000,999999)
        self.sex = sex
        self.name = name
        self.rest = 1
    def __str__(self):
        if self.sex==0:
            icon = "M"
        elif self.sex==1:
            icon = "F"
        else:
            icon = "I"
        return """%s (%s %i) F%i S%i B%i C%i"""%(self.name,icon,self.age,self.stats[0],self.stats[1],self.stats[2],self.stats[3])
    def fullprint(self):
        if self.sex==0:
            icon = "Male"
        elif self.sex==1:
            icon = "Female"
        else:
            icon = "Intersex"
        return """%s (%s, %i months)
Force: %i (%i, %i, %i)
Speed: %i (%i, %i, %i)
Brain: %i (%i, %i, %i)
Charm: %i (%i, %i, %i)"""%(self.name,icon,self.age,self.stats[0],self.genes[0][0],self.genes[0][1],self.genes[0][2],self.stats[1],self.genes[1][0],self.genes[1][1],self.genes[1][2],self.stats[2],self.genes[2][0],self.genes[2][1],self.genes[2][2],self.stats[3],self.genes[3][0],self.genes[3][1],self.genes[3][2])
    def passtime(self):
        self.age += 1
        self.rest = 1
    def genstats(self):
        self.stats=[0,0,0,0]
        for i in range(0,4):
            self.stats[i]=sum(self.genes[i])+self.skills[i]
    def rename(self):
        print("\nWhat should %s's new name be?\nLeave blank to cancel."%(self.name))
        newname = input("> ")
        if newname != "":
            self.name=newname.capitalize()

from random import randint

def breed(mom, dad, sex=None):
    print("%s and %s are trying to make a new monster."%(mom.name,dad.name))
    penalty, line = inbreeding(mom,dad)
    parents = [mom.id,dad.id]
    testpass = alert(mom,dad,penalty)
    if not testpass:
        genes=[[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        for i in range(0,4):
            genes[i][0]=mom.genes[i][randint(0,2)]
            genes[i][1]=dad.genes[i][randint(0,2)]
            genes[i][2]=randint(1,4)
        while penalty != 0:
            genes[randint(0,3)][randint(0,2)]=0
            penalty -= 1
        if sex == None:
            sex = randint(0,1)
        return monster(genes,parents,line,sex,namegen())
    else:
        return None

def alert(mom,dad,penalty):
    alert=False
    if mom.age==1 or mom.age==0:
        print("%s is too young to have offspring."%(mom.name))
        alert=True
    if dad.age==1 or dad.age==0:
        print("%s is too young to have offspring."%(dad.name))
        alert=True
    if mom.sex==dad.sex and mom.sex!=2:
        print("%s and %s are the same sex; they can't mate."%(mom.name,dad.name))
        alert=True
    if penalty==2:
        print("%s and %s are closely related.\nTheir offspring will be much weaker than normal."%(mom.name,dad.name))
    if penalty==1:
        print("%s and %s are related.\nTheir offspring will be weaker than normal."%(mom.name,dad.name))
    return alert

def inbreeding(mom, dad):
    penalty = 0
    baseline = mom.parents+dad.parents
    idlist = [mom.id,dad.id]
    baseline[:] = [x for x in baseline if x != 0]
    line=[]
    for i in range(0,len(baseline)):
        if baseline[i] in line:
            penalty=2
            break
        else:
            line.append(baseline[i])
    for i in range(0,1):
        if idlist[i] in line:
            penalty=2
            break
    if penalty==0:
        oldline = mom.line+dad.line+line
        oldline[:] = [x for x in oldline if x != 0]
        cleanline = []
        for i in range(0,len(oldline)):
            if oldline[i] in cleanline:
                penalty=1
                break
            else:
                cleanline.append(oldline[i])
    return (penalty, line)

def displaybox(box):
    print()
    for i in range(0,len(box)):
        print(str(i+1)+": "+str(box[i]))
    print()

def namegen():
    cons=["p", "t", "k", "s", "m", "n", "b", "d", "g"]
    vowel=["a","e","i","o","u"]
    nas=["m","n"]
    rolls=randint(1,3)
    masterroll=rolls
    name = ""
    while rolls != 0:
        name=name+cons[randint(0,len(cons)-1)]
        name=name+vowel[randint(0,len(vowel)-1)]
        if randint(0,masterroll+1)==0:
            name=name+nas[randint(0,len(nas)-1)]
        rolls-=1
    return name.capitalize()

def randomgene():
    genes=[[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    for i in range(0,4):
        for j in range(0,3):
            genes[i][j]=randint(1,3)
    return genes

def newmonth(box):
    for i in range(0,len(box)):
        box[i].passtime()

def inspect(box):
    while True:
        displaybox(box)
        print("Which monster do you want to inspect?\nInput 0 to exit or N to enter rename mode.")
        lookup = input("> ")
        print(lookup)
        if lookup == "0":
            break
        elif lookup == "N" or lookup == "n":
            while True:
                displaybox(box)
                print("Which monster do you want to rename?\nInput 0 to cancel.")
                lookup = input("> ")
                if lookup == "0":
                    break
                else:
                    try:
                        box[int(lookup)-1].rename()
                    except ValueError:
                        print("A number, please.")
                    except IndexError:
                        print("You don't have that many monsters!")
        else:
            print()
            try:
                print(box[int(lookup)-1].fullprint())
            except ValueError:
                print("A number, please.")
            except IndexError:
                print("You don't have that many monsters!")

def checkbays(box,bays):
    print
    displaybox(box)
    for i in range(0,len(bays)):
        print("Bay %i")

box = []
bays = [[],[]]
box.append(monster(randomgene(),[0,0],[0],0,namegen(),2))
box.append(monster(randomgene(),[0,0],[0],1,namegen(),2))
box.append(monster(randomgene(),[0,0],[0],0,namegen(),2))
box.append(monster(randomgene(),[0,0],[0],1,namegen(),2))

print("""Monster Breeding Game Demo
by Nicholas Fletcher""")

while True:
    displaybox(box)
    print("""Select your action:
1: Inspect a Monster closely.
2: Send a Monster to a Breeding Bay.
3: Send a Monster to a Training Field.
4: Send a Monster to an Event.
5: Go to the Market.
6: End the Month.""")
    command = input("> ")
    if command == "1":
        inspect(box)
    if command == "2":
        checkbays(box,bays)
    if command == "5":
        box.append(monster(randomgene(),[0,0],[0],0,namegen(),2))
        print("\nYou bought a new monster.\nTheir name is %s."%(box[-1].name))

