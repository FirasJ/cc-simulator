
def ceil(value, interval):
    return value + (interval - value) % interval

# PD's skill
celebrate = [1., 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55]
celebrateDuration = 8000

# Cupid's Skill
arrow = [0, 10, 15, 20, 25, 30, 35, 40, 45, 55, 65]

# Talents and Crests
zerk = [1., 1.1, 1.15, 1.2, 1.25, 1.3, 1.4, 1.5, 1.7]
revit = [0, 20, 40, 60, 80, 100]

class Hero(object):
    def __init__(self, name, atkSpeed, skillLevel):
        self.name = name
        self.atkSpeed = atkSpeed
        self.skillLevel = skillLevel
        self.hasAttacked = False
        self.celebrateStacks = []
        self.zerkLevel = 0
        self.lastAttack = 0
        self.lastProc = -100000
        self.energy = 0
        self.procCD = 0
        self.procCount = 0
        self.energyInc = 15

    def setZerkLevel(self, zerkLevel):
        self.zerkLevel = zerkLevel

    def setRevitLevel(self, revitLevel):
        self.energy = revit[revitLevel]

    def setProcCD(self, procCD):
        self.procCD = procCD

    def setEnergyInc(self, energyInc):
        self.energyInc = energyInc

    def hasAttacked(self):
        return self.hasAttacked

    def setAttack(self, time):
        self.lastAttack = time

    def getAttack(self):
        return self.lastAttack

    def getAtkSpeed(self):
        tempSpeed = self.atkSpeed

        # Celebrate
        for stack in self.celebrateStacks:
            tempSpeed = tempSpeed / celebrate[stack[0]]

        totalBuff = zerk[self.zerkLevel]
        return ceil(tempSpeed / totalBuff, 200)

    def addCelebrate(self, celebrateLevel, time):
        self.celebrateStacks.append([celebrateLevel, time])

    def addEnergy(self, energy):
        self.energy = min(100, round(self.energy + energy, 2))

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
            self.addEnergy(self.energyInc)

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


# Create your heroes here, following the format:
#   hero = Hero("HeroName", AtkSpeed, SkillLevel)
# After creating a hero, you can specify any of the following:
#   hero.setZerkLevel(zerk level)
#   hero.setRevitLevel(revit level)
#   hero.setProcCD(proc CD in ms)
#   hero.setEnergyInc(energy increment per hit) - default=15
#
#  A few heroes must have a name that starts with a specific prefix:
#   Pumpkin Duke must start with "PD".
#   Cupid must start with "Cupid".

pd = Hero("PD", 1000, 10)
pd.setZerkLevel(8)
pd.setRevitLevel(5)

# After you create your heroes, add the variable names to this array, then hit
# the "run" button above
heroArray = [pd]

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
