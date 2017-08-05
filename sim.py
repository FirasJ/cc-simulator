
def ceil(value, interval):
    return value + (interval - value) % interval

celebrate = [1., 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55]
arrow = [0, 10, 15, 20, 25, 30, 35, 40, 45, 55, 65]
celebrateDuration = 8000
zerk = [1., 1.1, 1.15, 1.2, 1.25, 1.3]
revit = [0,20, 40, 60, 80, 100]

class Hero(object):
    def __init__(self, name, atkSpeed, skillLevel, zerkLevel, revitLevel, procCD):
        self.name = name
        self.atkSpeed = atkSpeed
        self.skillLevel = skillLevel
        self.hasAttacked = False
        self.celebrateStacks = []
        self.zerkLevel = zerkLevel
        self.lastAttack = 0
        self.lastProc = -100000
        self.energy = revit[revitLevel]
        self.procCD = procCD
        self.procCount = 0
    
    def hasAttacked(self):
        return self.hasAttacked
    
    def setAttack(self, time):
        self.lastAttack = time
    
    def getAttack(self):
        return self.lastAttack
    
    def getAtkSpeed(self):
        if len(self.celebrateStacks)>0:
            tempSpeed = self.atkSpeed
            for stack in self.celebrateStacks:
                tempSpeed = tempSpeed / celebrate[stack[0]]
            return ceil(tempSpeed/zerk[self.zerkLevel],200)
        else:
            return ceil(self.atkSpeed/zerk[self.zerkLevel], 200)
    
    def addCelebrate(self, celebrateLevel, time):
        self.celebrateStacks.append([celebrateLevel, time])
    
    def addEnergy(self, energy):
        self.energy += energy
        
    def update(self, time):
        if self.hasAttacked == True:
            if self.lastAttack + self.getAtkSpeed() <= time:
                self.hasAttacked = False
        
        # Expire celebrate
        if len(self.celebrateStacks)>0:
            if self.celebrateStacks[0][1]<= time-8000:
                self.celebrateStacks.pop(0)
        
        if self.hasAttacked == False:
            self.hasAttacked = True
            self.lastAttack = time
            if self.energy >= 100 and self.lastProc + self.procCD <= time:
                self.proc(time)
            print(self.name, "swing", self.energy, self.getAtkSpeed(), len(self.celebrateStacks))
            if self.name[:5] == "Aries":
                self.energy += 12
            else:
                self.energy += 15
    
    def proc(self, time):
        self.energy = 0
        self.procCount += 1
        self.lastProc = time
        print(self.name, "proccing")
        if self.name[:2] == "PD":
            for hero in heroArray:
                hero.addCelebrate(self.skillLevel,time)
        if self.name[:5] == "Cupid":
            for hero in heroArray:
                if hero.name[:5] != "Cupid":
                    hero.addEnergy(arrow[self.skillLevel])
                
   
# Create your heroes here, folloing the format:
# Hero("HeroName", AtkSpeed, SkillLevel, ZerkLevel, ReviteLevel, Skill CD)
# Pumpkin Duke must have a name that starts with "PD" and Cupid must have a
# name that starts with "Cupid".
PD = Hero("PD", 1000, 1, 0, 4, 0)
#Cupid = Hero("Cupid", 1200, 9, 0, 5, 6000)

# After you create your heroes, add the variable names to this array, then hit
# the "run" button above
heroArray = [PD]

# Output shows the time in 100ms incriments, it shows the energy *before* the
# action taken (i.e. PD1 swwing 0 800.0 0) means it had 0 energy before that 
# swing (and will now have 15, internally). It then lists the calculated atk
# speed at the time of the swing, and the number of stacks of celebrate.
# ex. "Cupid swing 120 600.0 3" means cupid attacked, has 120 energy (i.e. 
# 'Arrow', his skill, is still on CD), swings every 600 ms, and has 3 stacks
# of celebrate (though we don't know what level haste those stacks give).

for i in range(0, 30000, 100):
    print(i)
    for hero in heroArray:
        hero.update(i)

print("Total procs per hero:")
for hero in heroArray:
    print(hero.name, hero.procCount)
        
