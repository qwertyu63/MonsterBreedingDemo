class monster(object):
    def __init__(self, genes, parents, line, sex, name, sprite=None, age=0):
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
        self.sprite=sprite
        if self.sprite == None:
            self.sprite = [randint(1,3),randint(1,3)]
        self.timestamp = time()
    def __str__(self):
        if self.sex==0:
            icon = "M"
        elif self.sex==1:
            icon = "F"
        else:
            icon = "I"
        return "%s (%s %i) F%i S%i B%i C%i"%(self.name,icon,self.age,self.stats[0],self.stats[1],self.stats[2],self.stats[3])
    def fullprint(self):
        if self.sex==0:
            icon = "Male"
        elif self.sex==1:
            icon = "Female"
        else:
            icon = "Intersex"
        return """%s (%s, %i months)
Force: %i (%i, %i, %i, +%i)
Speed: %i (%i, %i, %i, +%i)
Brain: %i (%i, %i, %i, +%i)
Charm: %i (%i, %i, %i, +%i)"""%(self.name,icon,self.age,self.stats[0],self.genes[0][0],self.genes[0][1],self.genes[0][2],self.skills[0],self.stats[1],self.genes[1][0],self.genes[1][1],self.genes[1][2],self.skills[1],self.stats[2],self.genes[2][0],self.genes[2][1],self.genes[2][2],self.skills[2],self.stats[3],self.genes[3][0],self.genes[3][1],self.genes[3][2],self.skills[3])
    def passtime(self):
        self.genstats()
        self.age += 1
    def genstats(self):
        self.stats=[0,0,0,0]
        for i in range(0,4):
            self.stats[i]=sum(self.genes[i])+self.skills[i]
    def rename(self):
        print("\nWhat should %s's new name be?\nLeave blank to cancel."%(self.name))
        newname = input("> ")
        if newname != "":
            self.name=newname.capitalize()
    def train(self,boost):
        for i in range(0,4):
            self.skills[i]+=boost[i]
            if self.skills[i]>3:
                self.skills=3

from random import randint
from time import time

def sortmon(e):
    return e.timestamp

def breed(mom, dad, sex=None):
    print("\n%s and %s are trying to make a new monster."%(mom.name,dad.name))
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
        newname = namegen()
        print("Their offspring is named %s."%(newname))
        return monster(genes,parents,line,sex,newname)
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
    if penalty==2 and alert==False:
        print("%s and %s are closely related.\nTheir offspring will be much weaker than normal."%(mom.name,dad.name))
    if penalty==1 and alert==False:
        print("%s and %s are related.\nTheir offspring will be weaker than normal."%(mom.name,dad.name))
    return alert

def inbreeding(mom, dad):
    penalty = 0
    line = mom.parents+dad.parents
    line = list(set(line))
    try:
        line.remove(0)
    except ValueError:
        pass
    line.sort()
    print(line)
    if mom.parents[0] in dad.parents:
        if mom.parents[0] != 0:
            penalty = 2
    if mom.parents[1] in dad.parents:
        if mom.parents[1] != 0:
            penalty = 2
    if mom.id in dad.parents:
        penalty=2
    if dad.id in mom.parents:
        penalty=2
    if penalty==0:
        oldline = mom.line+dad.line+line
        cleanline = []
        for i in range(0,len(oldline)):
            if oldline[i] in cleanline:
                penalty=1
                break
            else:
                cleanline.append(oldline[i])
    return (penalty, line)

def displaybox(box):
    box.sort(key=sortmon)
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

def inspect(box):
    while True:
        displaybox(box)
        print("Which monster do you want to inspect?\nInput 0 to exit or N to enter rename mode.")
        lookup = input("> ")
        print(lookup)
        if lookup == "0" or lookup == "":
            break
        elif lookup == "N" or lookup == "n":
            while True:
                displaybox(box)
                print("Which monster do you want to rename?\nInput 0 to cancel.")
                lookup = input("> ")
                if lookup == "0" or lookup == "":
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
    while True:
        displaybox(box)
        for i in range(0,len(bays)):
            bayid=i+1
            print("Bay %i: "%(bayid),end="")
            if len(bays[i]) == 0:
                print("Empty.")
            elif len(bays[i]) == 1:
                print(bays[i][0].name)
            else:
                print(bays[i][0].name+", "+bays[i][1].name)
        print("\nWhich bay do you want to use?\nInput 0 to exit.")
        targetbay = input("> ")
        if targetbay == "0" or targetbay == "":
            break
        else:
            print()
            try:
                bayedit(bays[int(targetbay)-1],box)
            except ValueError:
                print("A number, please.")
            except IndexError:
                print("You don't have that many bays!")

def bayedit(bay,box):
    while True:
        if len(bay) == 2:
            print("\nIn Bay:",end="")
            displaybox(bay)
            print("That bay is already full.\nInput 1 or 2 to remove that monster.\nAny other input cancels.")
            target = input("> ")
            if target == "1":
                print("\n%s has been removed from the bay."%(bay[0].name))
                box.append(bay.pop(0))
            elif target == "2":
                print("\n%s has been removed from the bay."%(bay[1].name))
                box.append(bay.pop(1))
            else:
                return
        else:
            if len(bay) == 1:
                print("In Bay: "+str(bay[0]))
            print("In Box:",end="")
            displaybox(box)
            print("Which monster do you want to add to the bay?\nInput 0 to cancel.")
            if len(bay)==1:
                print("Input R to remove %s from the bay."%(bay[0].name))
            target = input("> ")
            if target == "0" or target == "":
                return
            elif (target == "R" or target == "r") and len(bay) == 1:
                print("\n%s has been removed from the bay."%(bay[0].name))
                box.append(bay.pop(0))
            else:
                try:
                    bay.append(box.pop(int(target)-1))
                    print("\n%s is now in the bay."%(bay[-1].name))
                except ValueError:
                    print("A number, please.")
                except IndexError:
                    print("You don't have that many monsters!")

def trainbays(box,train):
    while True:
        names = ["Empty","Empty","Empty","Empty"]
        for i in range(0,4):
            if train[i] != None:
                names[i]=train[i].name
        print("""
Training Bays:
Force (1): %s
Speed (2): %s
Brain (3): %s
Charm (4): %s"""%(names[0],names[1],names[2],names[3]))
        displaybox(box)
        print("Which bay do you want to use?\nInput 0 to exit.")
        target = input("> ")
        valid = ["1","2","3","4"]
        if target in ("0",""):
            break
        elif target in valid:
            num = int(target)-1
            if train[num]==None:
                hold = getmonster(box)
                if hold != None:
                    train[num] = hold
                    print("%s is ready to train."%(train[num].name))
            else:
                box.append(train[num])
                print("%s has been returned to the box."%(train[num].name))
                train[num] = None

def getmonster(box):
    displaybox(box)
    print("Which monster do you want to put in?\nInput 0 to cancel.")
    target = input("> ")
    if target == "0" or target == "":
        return None
    else:
        try:
            hold = box.pop(int(target)-1)
            return hold
        except ValueError:
            print("A number, please.")
        except IndexError:
            print("You don't have that many monsters!")

def exhibit(box,stage,stagetarget):
    while True:
        if len(stage) == 2:
            print("\nOn Stage:",end="")
            displaybox(stage)
            print("The stage is already full.\nInput 1 or 2 to remove that monster.\nAny other input cancels.")
            target = input("> ")
            if target == "1":
                print("\n%s has been removed from the stage."%(stage[0].name))
                box.append(stage.pop(0))
            elif target == "2":
                print("\n%s has been removed from the stage."%(stage[1].name))
                box.append(stage.pop(1))
            else:
                return
        else:
            if len(stage) == 1:
                print("\nOn Stage: "+str(stage[0]))
            print("\nIn Box:",end="")
            displaybox(box)
            print("Which monster do you want to add to the stage?\nInput 0 to cancel.")
            if len(stage)==1:
                print("Input R to remove %s from the stage."%(stage[0].name))
            target = input("> ")
            if target == "0" or target == "":
                return
            elif (target == "R" or target == "r") and len(stage) == 1:
                print("\n%s has been removed from the stage."%(stage[0].name))
                box.append(stage.pop(0))
            else:
                try:
                    stage.append(box.pop(int(target)-1))
                    print("\n%s is now on the stage."%(stage[-1].name))
                except ValueError:
                    print("A number, please.")
                except IndexError:
                    print("You don't have that many monsters!")

box = []
bays = [[],[]]
train = [None,None,None,None]
stage = []
stagetarget = [randint(0,3)]
box.append(monster(randomgene(),[0,0],[],0,namegen(),age=2))
box.append(monster(randomgene(),[0,0],[],1,namegen(),age=2))
box.append(monster(randomgene(),[0,0],[],0,namegen(),age=2))
box.append(monster(randomgene(),[0,0],[],1,namegen(),age=2))
statname=["Force","Speed","Brain","Charm"]

print("""Monster Breeding Game Demo
by Nicholas Fletcher""")

while True:
    displaybox(box)
    print("""Select your action:
1: Inspect a Monster.
2: Visit the Breeding Bays.
3: Visit the Training Bays.
4: Visit the Exhibition Stage.
5: Go to the Market.
6: End the Month.""")
    command = input("> ")
    if command == "1":
        inspect(box)
    elif command == "2":
        checkbays(box,bays)
    elif command == "3":
        trainbays(box,train)
    elif command == "4":
        exhibit(box,stage,stagetarget)
    elif command == "5":
        box.append(monster(randomgene(),[0,0],[],0,namegen(),2))
        print("\nYou bought a new monster.\nTheir name is %s."%(box[-1].name))
    elif command in ("6","0"):
        print()
        for i in range(0,len(bays)):
            baby = None
            if len(bays[i])==2:
                baby = breed(bays[i][0],bays[i][1])
            while len(bays[i]) != 0:
                box.append(bays[i].pop(0))
            if baby != None:
                    box.append(baby)
        for i in range(0,len(train)):
            bonus=[0,0,0,0]
            bonus[i]=1
            if train[i]!=None:
                train[i].train(bonus)
                print("%s's %s improved."%(train[i].name,statname[i]))
                box.append(train[i])
                train[i]=None
        for i in range(0,len(stage)):
            box.append(stage.pop())
        for i in range(0,len(box)):
            box[i].passtime()
        stagetarget = [randint(0,3)]
