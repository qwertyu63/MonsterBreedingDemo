class monster(object):
    def __init__(self, genes, name):
        self.color = None
        self.style = None
        self.genes = genes
        self.stats = [0,0,0,0]
        self.sex = None
        if name[0] == "R":
            self.name = namegen()
            self.randomize(name[1])
        else:
            self.name = name
        if name[0] == "L":
            self.loadmon(name[1])
        self.genstats()
        self.timestamp = time()
    def __str__(self):
        self.genstats()
        icons=[["M","F"],
        ["Red","Gre","Blu","Yel","Pur"],
        ["Dog", "Brd", "Fsh", "Cat"]]
        icon=icons[0][self.sex]
        cicon=icons[1][self.color]
        sicon=icons[2][self.style]
        injure = "Hurt" if self.genes[7][1]==1 else ""
        return "%s (%s %s %s) F%i S%i B%i C%i %s"%(self.name,icon,cicon,sicon,self.stats[0],self.stats[1],self.stats[2],self.stats[3],injure)
    def genstats(self):
        self.stats=[0,0,0,0]
        for i in range(0,4):
            self.stats[i]=sum(self.genes[i])-self.genes[7][1]
        if self.genes[4][0]==self.genes[4][2]:
            self.color = self.genes[4][0]
        else:
            self.color = self.genes[4][1]
        if self.genes[5][0]==self.genes[5][2]:
            self.style = self.genes[5][0]
        else:
            self.style = self.genes[5][1]
        if self.color!=self.style:
            if self.color!=5:
                self.stats[self.color]=ceil(self.stats[self.color]*0.75)
            self.stats[self.style]=ceil(self.stats[self.style]*1.25)
        self.sex = self.genes[7][0]
    def rename(self):
        print("\nWhat should %s's new name be?\nLeave blank to cancel."%(self.name))
        newname = input("> ")
        if newname != "":
            newname=newname.capitalize()
            newname=newname[:9] #Names may not exceed 9.
            self.name=newname
    def fullprint(self):
        """Prints all of the monsters stats, neatly formatted."""
        self.genstats()
        icons=[["Male","Female"],
        ["Red (-For)","Green (-Spd)",
        "Blue (-Bra)","Yellow (-Cha)","Purple"],
        ["Dog (+For)", "Bird (+Spd)", 
        "Fish (+Bra)", "Cat (+Cha)"]]
        icon=icons[0][self.sex]
        cicon=icons[1][self.color]
        sicon=icons[2][self.style]
        colorgene=colorgenes(self.genes)
        statnames=["Force","Speed","Brain","Charm"]
        block="%s: %s\n"%(self.name,icon)
        for i in range(0,4):
            block+="%s: %i (%i%i%i) [%s]\n"%(statnames[i],self.stats[i],self.genes[i][0],self.genes[i][1],self.genes[i][2],colorgene[2][i])
        block+="Color: %s (%s)\n"%(cicon,colorgene[0])
        block+="Style: %s (%s)"%(sicon,colorgene[1])
        if self.genes[7][1]==1:
            block+="\nInjured."
        return block
    def savemon(self):
        """Converts the monsters stats into a tuple for shelving."""
        save = [self.name]
        genehold=deepcopy(self.genes)
        for i in range(0,len(genehold)):
            for j in range(0,len(genehold[i])):
                genehold[i][j]=str(genehold[i][j])
        for i in range (0,len(genehold)):
            save.append(tuple(genehold[i]))
        save=tuple(save)
        return save
    def loadmon(self, save):
        """Restores a shelved monster."""
        self.genes=[[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0,0],[0,1]]
        save = list(save)
        self.name=save.pop(0)
        for i in range(0,len(save)):
            save[i]=list(save[i])
            for j in range(0,len(save[i])):
                save[i][j]=int(save[i][j])
        self.genes=deepcopy(save)
        self.genstats()
    def randomize(self,sex=None):
        """Randomly generates a monster. The sex can be specified with a 0 or 1."""
        genes=[[0,0,0],[0,0,0],[0,0,0],
        [0,0,0],[0,0,0],[0,0,0],[0,0,0,0],[0,0]]
        for i in range(0,4):
            for j in range(0,3):
                genes[i][j]=randint(1,3)
        for i in range(4,6):
            for j in range(0,2):
                genes[i][j]=randint(0,3)
            genes[i][2]=genes[i][randint(0,1)]
        for i in range(0,4):
            genes[6][i]=randint(0,35)
        if sex != None:
            genes[7][0]=sex
        else:
            genes[7][0]=randint(0,1)
        self.genes=deepcopy(genes)
    def breed(self,parent):
        """Creates the offspring of the monster calling this fuction and the one passed in."""
        if self.sex==0 and parent.sex==1:
            genes=[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0,0],[0,0]]
            limit=5
            for i in range(0,6):
                genes[i][0]=parent.genes[i][randint(0,2)]
                genes[i][1]=self.genes[i][randint(0,2)]
                potential=min(max(genes[i])+1,limit)
                genes[i][2]=randint(1,potential)
            genes[7][0]=randint(0,1)
            genes[4][2]=genes[4][randint(0,1)]
            genes[5][2]=genes[6][randint(0,1)]
            genes[6][0]=parent.genes[5][0]
            genes[6][1]=self.genes[6][1]
            genes[6][2]=self.genes[6][2]
            genes[6][3]=self.genes[6][3]
            genes[6][3]=parent.genes[6][randint(2,3)]
            inbreeding=False
            for i in range(0,4):
                if self.genes[6][i]==parent.genes[6][i]:
                    # If the parents have matching blood genes (indicating they are probably related), the offspring has one or more of their genes replaced with zeroes.
                    # The replaced gene is 50% likely to be the one they collided on, but otherwise it's random.
                    roll=randint(0,5)
                    if roll > 3:
                        roll=i
                    genes[roll][randint(0,2)]=0
                    inbreeding=True
            return (monster(deepcopy(genes),namegen()),inbreeding)
        elif self.sex==1 and parent.sex==0:
            # If the monster passed in is the female, we need to have them handle the function and return the result.
            return parent.breed(self)
        else:
            raise GayMon
    def inspection(self):
        clear()
        print(self.fullprint())
        print("\nInput R to rename %s.\nInput S to sell %s."%(self.name,self.name))
        if self.genes[7][1]==1:
            print("Input H to heal %s's injuries ($10)."%(self.name))
        print("Any other input cancels.")
        hold = input("> ")
        if hold in ("r","R"):
            self.rename()
        elif hold in ("s","S"):
            sold = self.sell()
            return sold
        elif hold in ("h","H") and self.genes[7][1]==1:
            global money
            if money >= 10:
                money-=10
                self.genes[7][1]=0
                print("%s has been healed."%(self.name))
            else:
                print("You don't have $10.")
            input()
            self.inspection()
    def sell(self):
        price=sum(self.stats)//2
        print("\nAre you sure you want to sell %s?\nYou'll get $%i for them.\nInput Y to confirm.\nAny other input cancels."%(self.name,price))
        confirm = input("> ")
        if confirm in ("y","Y"):
            global money
            money+=price
            return price
        else:
            return None
    def injure(self):
        self.genes[7][1]=1
        self.genstats()

class GayMon(Exception):
    pass

class PullFail(Exception):
    pass

class AddFail(Exception):
    pass

class bay(object):
    def __init__(self,name,size=2,unlock=None,hide=False):
        self.name=name
        self.size=size
        self.store=[]
        self.hide=hide
        self.breedOK= True if unlock=="Breed" else False
        self.stageOK= True if unlock=="Stage" else False
    def __str__(self):
        self.store.sort(key=sortmon)
        output = (self.name+":\n")
        for i in range(0,len(self.store)):
            output += str(i+1)+": "+str(self.store[i])+"\n"
        if len(self.store)==0:
            output += "None.\n"
        return output
    def addmon(self,mon,report=True):
        if len(self.store) >= self.size and self.size != -1:
            print("\nThe %s is full."%(self.name))
            input()
            raise AddFail
        else:
            self.store.append(mon)
            if report:
                print("%s enters the %s."%(mon.name,self.name))
                input()
            return True
    def removemon(self):
        clear()
        print("Remove from the %s:\n"%(self.name))
        print(self)
        print("Input the ID you want to remove.")
        target = input("> ")
        return self.pullmonster(target)
    def accessbay(self,box):
        if not self.hide: print(self)
        print(box)
        print("Input the ID you want to add to the %s. \nInput 0 to exit the %s."%(self.name,self.name))
        if len(self.store)!=0:
            print("Input R to remove monsters.")
        if len(self.store)==2 and self.breedOK:
            print("Input B to breed monsters.")
        if len(self.store)!=0 and self.stageOK:
            print("Input S to put on a show.")
        target = input("> ")
        if target in ("0",""):
            return True
        elif target in ("r","R") and len(self.store)!=0:
            try:
                box.store.append(self.removemon())
            except PullFail:
                pass
        elif target in ("b","B") and len(self.store)==2 and self.breedOK:
            box.store+=self.breedmon()
            input()
        elif target in ("s","S") and len(self.store)!=0 and self.stageOK:
            dump = self.holdshow(box)
            if dump != None:
                box.store+=dump
            input()
        else:
            try:
                transfer = box.pullmonster(target)
                self.addmon(transfer)
            except PullFail:
                pass
            except AddFail:
                box.store.append(transfer)
    def breedmon(self):
        if len(self.store)==2 and self.breedOK:
            try: 
                baby = (self.store[0].breed(self.store[1]))
                self.store.append(baby[0])
                print("%s and %s breed.\nTheir baby is named %s"%(self.store[0].name,self.store[1].name,self.store[2].name))
                if baby[1]:
                    print("The child suffers from genetic abnormalities,\n likely due to inbreeding.")
                print(self.store[2])
            except GayMon:
                print("%s and %s are the same sex.\nThey can't have offspring."%(self.store[0].name,self.store[1].name))
        hold, self.store = self.store, []
        return hold
    def holdshow(self,box):
        while True:
            clear()
            print(self)
            print("Shows:\n1: Force\n2: Speed\n3: Brain\n4: Charm\n")
            print("What kind of show do you want to put on?\nInput 0 to cancel.")
            show=input("> ")
            if show == 0:
                return None
            elif show in ("1","2","3","4"):
                show = int(show)-1
                skill = 0
                for i in range(0,len(self.store)):
                    skill+=self.store[i].stats[show]
                payout = (skill//5)*2
                print("Your show total is %i.\nYou make $%i"%(skill,payout))
                global money
                money+=payout
                hold, self.store = self.store, []
                return hold
    def inspectmon(self,buy=False):
        print(self)
        print("Input the ID you want to inspect.")
        if buy: print("Input B to buy a new monster for $10.")
        print("Input 0 to exit.")
        target = input("> ")
        if target in ("0",""):
            return True
        elif target in ("b","B"):
            global money
            if money >= 10:
                money-=10
                new=monster(None,["R",None])
                print("You bought %s for $10."%(new.name))
                print(new)
                self.addmon(new,report=False)
            else:
                print("You don't have $10.")
            input()
        else:
            try:
                hold = self.pullmonster(target)
                sold = hold.inspection()
                if not sold:
                    self.addmon(hold,report=False)
            except PullFail:
                pass
    def pullmonster(self,target):
        if target.isnumeric():
            goal = int(target)-1
            if goal in range(0,len(box.store)):
                return self.store.pop(goal)
        raise PullFail

def colorgenes(genes):
    """Converts a monsters gene numbers into letters for display"""
    letters=["","",""]
    cletter=["R","G","B","Y","P"]
    sletter=["D","B","F","C"]
    bletter=ascii_uppercase+"0123456789"
    for i in genes[4]:
        letters[0]+=cletter[i]
    for i in genes[5]:
        letters[1]+=sletter[i]
    for i in genes[6]:
        letters[2]+=bletter[i]
    return letters

def namegen():
    """Generates a random name for a monster."""
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

def sortmon(e):
    return e.timestamp

def wildhunt(box):
    while True:
        clear()
        print(box)
        print("Input the ID you want to send into the Forest. \nInput 0 to exit the Forest.")
        target = input("> ")
        if target in ("0",""):
            return True
        else:
            try:
                troop = box.pullmonster(target)
                if troop.genes[7][1]==1:
                    print("%s is injured.\nThey can't go to the Forest."%(troop.name))
                    box.addmon(troop,report=False)
                    input()
                else:
                    break
            except PullFail:
                pass
    battle = randint(0,3)
    new = monster(None,["R",None]) if battle!=0 else None
    messages=["%s found another monster, but was injured.\nThe other monster got away."%(troop.name),
    "%s found another monster and brought them back."%(troop.name),
    "%s found another monster and brought them back."%(troop.name),
    "%s found another monster and brought them back.\nThe other monster was injured in the process."%(troop.name)]
    print("\n"+messages[battle])
    if battle==0:
        troop.injure()
    else:
        if battle==3: new.injure()
        box.addmon(new,report=False)
        print("\nThe new monster is named %s."%(new.name))
        print(new)
    box.addmon(troop,report=False)
    input()

from random import randint
from time import time
from os import remove
from os.path import isfile
import shelve
from math import ceil
from os import system, name
from string import ascii_uppercase
from copy import deepcopy
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

statnames=["Force","Speed","Brain","Charm"]

box = bay("Main Storage", size=-1)
cave = bay("Breeding Cavern", unlock="Breed")
stage = bay("Performance Stage",size=3,unlock="Stage")
money = 10

newfile=True
if isfile("save.db"):
    while True:
        clear()
        print("Monster Farm:\nby Nicholas Fletcher\n")
        print("Input L to load your save file.\nInput N to start a new game.\nInput D to delete your save file.")
        select=input("> ")
        if select in ("l","L"):
            newfile=False
            with shelve.open('save') as savefile:
                money=int(savefile["money"])
                for i in range(0,int(savefile["limit"])):
                    load = savefile[str(i)]
                    gen = monster(None,["L",load])
                    box.addmon(gen,report=False)
            break
        elif select in ("n","N"):
            break
        elif select in ("d","D"):
            remove("save.db")
            break
else:
    print("Monster Farm:\nby Nicholas Fletcher\n")
    print("Press Enter to continue.")
    input()
if newfile:
    for i in range(0,4):
        gen=monster(None,["R",i%2])
        box.addmon(gen,report=False)
clear()

loop=True
while loop:
    print(box)
    print("""Where do you want to go?
    1: Main Storage
    2: Breeding Cavern
    4: The Performance Stage
    9: Records Room
You have $%i."""%(money))
    dest = input("> ")
    while True:
        clear()
        if dest == "1":
            check=box.inspectmon(buy=True)
        elif dest == "2":
            check=cave.accessbay(box)
        elif dest == "3":
            check=stage.accessbay(box)
        elif dest == "9":
            print("Do you want to save your game?\nAll monsters will return to Main Storage.")
            print("Input Y for yes.\nAny other input cancels.")
            savechoice = input("> ")
            if savechoice in ("y","Y"):
                while len(cave.store)!=0:
                    box.addmon(cave.store.pop(),report=False)
                while len(stage.store)!=0:
                    box.addmon(stage.store.pop(),report=False)
                with shelve.open('save') as savefile:
                    savefile["money"]=str(money)
                    savefile["limit"]=str(len(box.store))
                    for i in range(len(box.store)):
                        savefile[str(i)]=box.store[i].savemon()
                print("Your records have been updated.")
            print("\nInput X to quit the game.\nAny other input returns.")
            breaker = input("> ")
            if breaker in ("x","X"):
                loop=False
            break
        else:
            break
        if check:
            break
    clear()
