def ceil(value, interval):
    return value + (interval - value) % interval


# PD's skill
celebrate = [1., 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55]
celebrateDuration = 8000

# Cupid's Skill
arrow = [0, 10, 15, 20, 25, 30, 35, 40, 45, 55, 65]

# Mike's Skill
divinity = [1., 1.18, 1.22, 1.26, 1.3, 1.34, 1.38, 1.43, 1.48, 1.54, 1.6]
divinityDuration = 8000

# Valentina's Skill
cyclone = [0., 24., 32., 40., 50., 60., 70., 84., 96., 108., 126.]
cycloneDuration = [1., 2000, 2000, 2000, 2500, 2500, 2500, 3000, 3000, 3000, 3500]
cyclonePerTick = [100 * cyclone[i] / cycloneDuration[i] for i in range(0, 10)]

# Talents and Crests
zerk = [1., 1.1, 1.15, 1.2, 1.25, 1.3, 1.4, 1.5, 1.7]
revit = [0, 20, 40, 60, 80, 100]

# Artifacts
blitz = [1., 1.1, 1.15, 1.20, 1.25, 1.3]

# Enchantments
fury = [1., 1.1, 1.14, 1.19, 1.24, 1.3]


class Hero(object):
    def __init__(self, name, atkSpeed, skillLevel):
        self.name = name
        self.atkSpeed = atkSpeed
        self.skillLevel = skillLevel
        self.hasAttacked = False
        self.celebrateStacks = []
        self.divinityStacks = []
        self.cycloneStacks = []
        self.zerkLevel = 0
        self.lastAttack = 0
        self.lastProc = -100000
        self.energy = 0
        self.procCD = 0
        self.procCount = 0
        self.energyInc = 15
        self.blitzLevel = 0
        self.furyLevel = 0

    def setZerkLevel(self, zerkLevel):
        self.zerkLevel = zerkLevel

    def setRevitLevel(self, revitLevel):
        self.energy = revit[revitLevel]

    def setProcCD(self, procCD):
        self.procCD = procCD

    def setEnergyInc(self, energyInc):
        self.energyInc = energyInc

    def setBlitzLevel(self, blitzLevel):
        self.blitzLevel = blitzLevel

    def setFuryLevel(self, furyLevel):
        self.furyLevel = furyLevel

    def hasAttacked(self):
        return self.hasAttacked

    def setAttack(self, time):
        self.lastAttack = time

    def getAttack(self):
        return self.lastAttack

    def getAtkSpeed(self):
        tempSpeed = self.atkSpeed

        # PD's celebrate
        for stack in self.celebrateStacks:
            tempSpeed = tempSpeed / celebrate[stack[0]]

        # Mike's divinity
        for stack in self.divinityStacks:
            tempSpeed = tempSpeed / divinity[stack[0]]

        totalBuff = zerk[self.zerkLevel] * blitz[self.blitzLevel] * fury[self.furyLevel]
        return ceil(tempSpeed / totalBuff, 200)

    def getProcCount(self):
        return self.procCount

    def addCelebrate(self, celebrateLevel, time):
        self.celebrateStacks.append([celebrateLevel, time])

    def addDivinity(self, skillLevel, time):
        self.divinityStacks.append([skillLevel, time])

    def addCyclone(self, skillLevel, time, duration):
        self.cycloneStacks.append([skillLevel, time, duration])

    def addEnergy(self, energy):
        self.energy = min(100, round(self.energy + energy, 2))

    def update(self, time):
        if self.hasAttacked == True:
            if self.lastAttack + self.getAtkSpeed() <= time:
                self.hasAttacked = False

        # Apply Love Cyclone
        if time % 100 == 0:
            for stack in self.cycloneStacks:
                self.addEnergy(cyclonePerTick[stack[0]])

        # Expire buffs
        self.celebrateStacks = list(filter(lambda x: x[1] > time - celebrateDuration, self.celebrateStacks))
        self.divinityStacks = list(filter(lambda x: x[1] > time - divinityDuration, self.divinityStacks))
        self.cycloneStacks = list(filter(lambda x: x[1] > time - x[2], self.cycloneStacks))

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
                hero.addCelebrate(self.skillLevel, time)
        if self.name[:5] == "Cupid":
            for hero in heroArray:
                if hero.name[:5] != "Cupid":
                    hero.addEnergy(arrow[self.skillLevel])
        if self.name[:3] == "Mike":
            for hero in heroArray:
                hero.addDivinity(self.skillLevel, time)
        if self.name[:3] == "Val":
            for hero in heroArray:
                hero.addCyclone(self.skillLevel, time, cycloneDuration[self.skillLevel])


# Create your heroes here, following the format:
#   hero = Hero("HeroName", AtkSpeed, SkillLevel)
# After creating a hero, you can specify any of the following:
#   hero.setZerkLevel(zerk level)
#   hero.setRevitLevel(revit level)
#   hero.setProcCD(proc CD in ms)
#   hero.setEnergyInc(energy increment per hit) - default=15
#   hero.setBlitzLevel(blitz level)
#   hero.setFuryLevel(fury level)
#
#  A few heroes must have a name that starts with a specific prefix:
#   Pumpkin Duke must start with "PD".
#   Cupid must start with "Cupid".
#   Michael must start with "Mike".
#   Valentina must start with "Val".

pd = Hero("PD", 1000, 10)
pd.setZerkLevel(8)
pd.setRevitLevel(5)
# pd.setBlitzLevel(5)
# pd.setFuryLevel(5)

cupid = Hero("Cupid", 1200, 10)
cupid.setProcCD(6000)
cupid.setRevitLevel(5)

val = Hero("Val", 1200, 7)
val.setProcCD(6000)
# val.setRevitLevel(4)

mike = Hero("Mike", 1500, 9)
mike.setProcCD(8000)
# mike.setRevitLevel(5)

# After you create your heroes, add the variable names to this array, then run the program
heroArray = [pd, val]

# Output shows the time in 100ms increments, it shows the energy *before* the
# action taken (i.e. PD1 swing 0 800.0 0) means it had 0 energy before that
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
    print(hero.name, hero.getProcCount())
