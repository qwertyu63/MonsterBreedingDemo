class monster(object):
    def __init__(self, genes, sex, name,age=0):
        self.color = None
        self.age = age
        self.genes = genes
        self.stats = [0,0,0,0]
        self.skills = [0,0,0,0]
        self.sex = sex
        self.name = name
        if genes[4][0]==genes[4][2]:
            self.color = genes[4][0]
        else:
            self.color = genes[4][1]
        self.genstats()
        self.timestamp = time()
    def __str__(self):
        if self.sex==0:
            icon = "M"
        elif self.sex==1:
            icon = "F"
        else:
            icon = "I"
        if self.color==0:
            cicon = "r"
        elif self.color==1:
            cicon = "g"
        elif self.color==1:
            cicon = "b"
        else:
            cicon = "y"
        return "%s (%s%s) F%i S%i B%i C%i"%(self.name,cicon,icon,self.stats[0],self.stats[1],self.stats[2],self.stats[3])
    def passtime(self):
        self.genstats()
        self.age += 1
    def genstats(self):
        self.stats=[0,0,0,0]
        for i in range(0,4):
            self.stats[i]=sum(self.genes[i])+self.skills[i]
        self.stats[self.color]+=1
    def rename(self):
        print("\nWhat should %s's new name be?\nLeave blank to cancel."%(self.name))
        newname = input("> ")
        if newname != "":
            self.name=newname.capitalize()
    def train(self,boost):
        for i in range(0,4):
            self.skills[i]+=boost[i]
            limit = 4 if self.color==i else 3
            if self.skills[i]>limit:
                self.skills=limit
    def fullprint(self):
        if self.sex==0:
            icon = "Male"
        elif self.sex==1:
            icon = "Female"
        else:
            icon = "Intersex"
        if self.color==0:
            cicon = "Red; +1 Force"
        elif self.color==1:
            cicon = "Green; +1 Speed"
        elif self.color==1:
            cicon = "Blue; +1 Brain"
        else:
            cicon = "Yellow; +1 Charm"
        colormark=[0,0,0,0]
        colormark[self.color]=1
        colorgene=colorgenes(self.genes[4])
        return """%s:
%s (%s months)
Force: %i (%i%i%i)
Speed: %i (%i%i%i)
Brain: %i (%i%i%i)
Charm: %i (%i%i%i)
Color: %s (%s)
Core Genes: %s-%s-%s-%s
        """%(self.name,icon,self.age,self.stats[0],self.genes[0][0],self.genes[0][1],self.genes[0][2],self.stats[1],self.genes[1][0],self.genes[1][1],self.genes[1][2],self.stats[2],self.genes[2][0],self.genes[2][1],self.genes[2][2],self.stats[3],self.genes[3][0],self.genes[3][1],self.genes[3][2],cicon,colorgene,self.genes[5][0],self.genes[5][1],self.genes[5][2],self.genes[5][3])
    def savebuild(self):
        save = self.genes[0]
        save += self.genes[1]
        save += self.genes[2]
        save += self.genes[3]
        save += self.genes[4]
        save += self.genes[5]
        save += self.skills
        save.append(self.age)
        save.append(self.sex)
        save.append(self.name)
        for i in range(0,len(save)):
            save[i]=str(save[i])
        save=tuple(save)
        return save
    def saveload(self, save):
        save = list(save)
        for i in range(0,len(save)):
            if i != 25:
                save[i]=int(save[i])
        self.genes[0]=save[0:3]
        self.genes[1]=save[3:6]
        self.genes[2]=save[6:9]
        self.genes[3]=save[9:12]
        self.genes[4]=save[12:15]
        self.genes[4]=save[19:19]
        self.skills=save[19:23]
        self.age=save[23]
        self.sex=save[24]
        self.name=save[25]
        self.genstats()

from random import randint, shuffle
from time import time
from os.path import isfile
import shelve

def colorgenes(genes):
    letters=""
    for i in genes:
        if i == 0:
            letters+="R"
        if i == 1:
            letters+="G"
        if i == 2:
            letters+="B"
        if i == 3:
            letters+="Y"
    return letters

def sortmon(e):
    return e.timestamp

def breed(mom, dad, sex=None):
    print("\n%s and %s are trying to breed."%(mom.name,dad.name))
    penalty = bloodcheck(mom,dad)
    testpass = alert(mom,dad,penalty)
    if not testpass:
        genes=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0,0]]
        for i in range(0,5):
            genes[i][0]=mom.genes[i][randint(0,2)]
            genes[i][1]=dad.genes[i][randint(0,2)]
            genes[i][2]=randint(1,4)
        genes[4][2]=genes[4][randint(0,1)]
        genes[5][0]=mom.genes[5][0]
        genes[5][1]=dad.genes[5][0]
        genes[5][2]=mom.genes[5][randint(1,3)]
        genes[5][3]=dad.genes[5][randint(1,3)]
        shuffle(genes[5])
        while penalty != 0:
            genes[randint(0,3)][randint(0,2)]=0
            penalty -= 1
        if sex == None:
            sex = randint(0,1)
        newname = namegen()
        print("Their offspring is named %s."%(newname))
        return monster(genes,sex,newname)
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
    if penalty>1 and alert==False:
        print("%s and %s are closely related.\nTheir offspring will be much weaker than normal."%(mom.name,dad.name))
    if penalty==1 and alert==False:
        print("%s and %s are related.\nTheir offspring will be weaker than normal."%(mom.name,dad.name))
    return alert

def bloodcheck(mom, dad):
    penalty = 0
    for i in range(0,4):
        if mom.genes[5][i] in dad.genes[5]:
            penalty += 1
    return penalty

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
    genes=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0,0]]
    for i in range(0,4):
        for j in range(0,3):
            genes[i][j]=randint(1,3)
    genes[4][0]=randint(0,3)
    genes[4][1]=genes[4][0]
    genes[4][2]=genes[4][0]
    for i in range(0,4):
        genes[5][i]=randint(100,999)
    return genes

def inspect(box):
    while True:
        lookup = getmonster(box,"Which monster do you want to inspect?\nInput 0 to exit.",rename=True)
        print()
        if lookup == None:
            break
        elif lookup == "Drop":
            while True:
                displaybox(box)
                lookup = getmonster(box,"Which monster do you want to rename?\nInput 0 to cancel.")
                if lookup == None:
                    break
                else:
                    lookup.rename()
                    box.append(lookup)
        else:
            print(lookup.fullprint())
            box.append(lookup)

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
        if targetbay in ("0",""):
            break
        else:
            print()
            try:
                bayedit(bays[int(targetbay)-1],box)
            except ValueError:
                print("A number, please.")
            except IndexError:
                print("You don't have that many bays!")

def bayedit(bay,box,name="bay"):
    while True:
        flag = False
        if name == "stage":
            phrase = "on the stage"
            label = "On Stage"
        else:
            phrase = "in the bay"
            label = "In Bay"
        if len(bay) == 2:
            bay, eject = fullbay(bay,name)
            if eject != None:
                box.append(eject)
            else:
                flag = True
        else:
            if len(bay) == 1:
                print("\n"+label+": "+str(bay[0]))
                output = getmonster(box,"Which monster do you want to put %s?\nInput 0 to cancel."%(phrase),bay[0])
            else:
                output = getmonster(box,"Which monster do you want to put %s?\nInput 0 to cancel."%(phrase))
            if output == "Drop":
                print("\n%s has been removed from the %s."%(bay[0].name,name))
                box.append(bay.pop(0))
            elif output != None:
                bay.append(output)
            elif output == None:
                flag = True
        if name == "stage":
            return flag

def getmonster(box,message="Which monster do you want?\nInput 0 to cancel.",drop=False,rename=False):
    displaybox(box)
    print(message)
    if drop != False:
        print("Input R to remove %s."%(drop.name))
    if rename != False:
        print("Input R to enter rename mode.")
    target = input("> ")
    if target in ("0",""):
        return None
    if target in ("R","r"):
        return "Drop"
    else:
        try:
            hold = box.pop(int(target)-1)
            return hold
        except ValueError:
            print("A number, please.")
        except IndexError:
            print("There's not that many monsters to choose from.")

def fullbay(bay,name="bay"):
        print("\n"+name.capitalize()+":",end="")
        displaybox(bay)
        print("That %s is already full.\nInput 1 or 2 to remove that monster.\nAny other input cancels."%(name))
        remove = None
        target = input("> ")
        if target == "1":
            print("\n%s has been removed from the %s."%(bay[0].name,name))
            remove = bay.pop(0)
        elif target == "2":
            print("\n%s has been removed from the %s."%(bay[1].name,name))
            remove = bay.pop(1)
        return (bay,remove)

def exhibit(box,stage,stagetarget):
    while True:
        print("\nThis month's show is about %s."%(statname[stagetarget]))
        flag = bayedit(stage,box,name="stage")
        if flag:
            break

def runexhibit(stage, stagetarget):
    if len(stage) != 0:
        showtotal = 0
        showtotal += stage[0].stats[stagetarget]
        if len(stage)==2:
            showtotal += stage[1].stats[stagetarget]
            bonus = bloodcheck(stage[0],stage[1])
            showtotal += (bonus*2)
            print("\n%s and %s put on an exhibition of %s."%(stage[0].name,stage[1].name,statname[stagetarget]))
            if bonus != 0:
                print("As they are related, they work together well.")
        else:
            print("\n%s puts on an exhibition of %s."%(stage[0].name,statname[stagetarget]))
    print("Your exhibition score is %i."%(showtotal))
    tickets=int(showtotal/2)
    print("Ticket sales made you $%i."%(tickets))
    global money
    money+=tickets

box = []
bays = [[],[]]
train = [None,None,None,None]
stage = []
stagetarget = randint(0,3)
unlock = False
statname=["Force","Speed","Brain","Charm"]
money = 10
save = False

print("""Monster Breeding Game Demo
by Nicholas Fletcher""")

if isfile("box.db"):
    while True:
        print("\nThere is a save file.\nDo you want to [L]oad it or [S]tart a new name?")
        option = input("> ")
        if option in ("S","s"):
            box.append(monster(randomgene(),0,namegen(),age=2))
            box.append(monster(randomgene(),1,namegen(),age=2))
            box.append(monster(randomgene(),0,namegen(),age=2))
            box.append(monster(randomgene(),1,namegen(),age=2))
            break
        elif option in ("L","l"):
            with shelve.open('box') as savefile:
                money=int(savefile["money"])
                bays=[]
                count = int(savefile["bays"])
                while count != 0:
                    bays.append([])
                    count-=1
                count = int(savefile["limit"])
                for i in range(0,count):
                    load=savefile[str(i)]
                    null=monster(randomgene(),2,"Null")
                    null.saveload(load)
                    box.append(null)
            break
else:
    box.append(monster(randomgene(),0,namegen(),age=2))
    box.append(monster(randomgene(),1,namegen(),age=2))
    box.append(monster(randomgene(),0,namegen(),age=2))
    box.append(monster(randomgene(),1,namegen(),age=2))

while True:
    displaybox(box)
    print("""Money: $%i
    
Select your action:
1: Visit your Monster Storage.
2: Visit the Breeding Bays.
3: Visit the Exhibition Stage (%s).
5: Visit the Market. [WIP]
6: End the Month."""%(money,statname[stagetarget]))
    if save == True:
        print("R: Record your progress. [WIP]")
    command = input("> ")
    if command == "1":
        inspect(box)
    elif command == "2":
        save = False
        checkbays(box,bays)
    elif command == "3":
        save = False
        exhibit(box,stage,stagetarget)
    elif command in ("6","0"):
        print()
        save = True
        for i in range(0,len(bays)):
            baby = None
            if len(bays[i])==2:
                baby = breed(bays[i][0],bays[i][1])
            while len(bays[i]) != 0:
                box.append(bays[i].pop(0))
            if baby != None:
                    box.append(baby)
        if len(stage) != 0:
            runexhibit(stage,stagetarget)
            box+=stage
            stage=[]
        for i in range(0,len(box)):
            box[i].passtime()
        stagetarget = randint(0,3)
    elif command == "9":
        money+=99
    elif command in ("R","r") and save == True: #WIP
        with shelve.open('box') as savefile:
            for i in range(0,len(box)):
                savefile[str(i)]=box[i].savebuild()
            savefile["bays"]=str(len(bays))
            savefile["limit"]=str(len(box))
            savefile["money"]=str(money)
        break