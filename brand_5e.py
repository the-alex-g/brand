from math import floor

ABILITIES_SPELLOUT = {
    "str":"Strength",
    "dex":"Dexterity",
    "con":"Constitution",
    "int":"Intelligence",
    "wis":"Wisdom",
    "cha":"Charisma"
}
SKILL_ABILITY = {
    "athletics":"str",
    "acrobatics":"dex",
    "sleight of hand":"dex",
    "stealth":"dex",
    "arcana":"int",
    "history":"int",
    "investigation":"int",
    "nature":"int",
    "religion":"int",
    "animal handling":"wis",
    "insight":"wis",
    "medicine":"wis",
    "perception":"wis",
    "survival":"wis",
    "deception":"cha",
    "intimidation":"cha",
    "performance":"cha",
    "persuasion":"cha"
}
SKILL_PRETTYNAME = {
    "athletics":"Athletics",
    "acrobatics":"Acrobatics",
    "sleight of hand":"Sleight of Hand",
    "stealth":"Stealth",
    "arcana":"Arcana",
    "history":"History",
    "investigation":"Investigation",
    "nature":"Nature",
    "religion":"Religion",
    "animal handling":"Animal Handling",
    "insight":"Insight",
    "medicine":"Medicine",
    "perception":"Perception",
    "survival":"Survival",
    "deception":"Deception",
    "intimidation":"Intimidation",
    "performance":"Performance",
    "persuasion":"Persuasion"
}
CR_TO_XP = {
    0:"10",
    "1/8":"25",
    "1/4":"50",
    "1/2":"100",
    1:"200",
    2:"450",
    3:"700",
    4:"1,100",
    5:"1,800",
    6:"2,300",
    7:"2,900",
    8:"3,900",
    9:"5,000",
    10:"5,900",
    11:"7,200",
    12:"8,400",
    13:"10,000",
    14:"11,500",
    15:"13,000",
    16:"15,000",
    17:"18,000",
    18:"20,000",
    19:"22,000",
    20:"25,000",
    21:"33,000",
    22:"41,000",
    23:"50,000",
    24:"62,000",
    25:"75,000",
    26:"90,000",
    27:"105,000",
    28:"120,000",
    29:"135,000",
    30:"155,000",
}


# calculates proficiency bonus from cr
def cr_to_prof(cr):
    if type(cr) == str:
        return 2
    else:
        return max(2, floor((cr - 1) / 4) + 2)


# returns decimal form of given cr
def cr_to_digit(cr):
    if type(cr) == int:
        return cr
    else:
        return 1 / int(cr[-1])


# returns fractional from of given cr
def cr_to_string(cr):
    if type(cr) == int:
        return str(cr)
    elif type(cr) == float:
        return {0.125:"1/8", 0.25:"1/4", 0.5:"1/2"}[cr]
    else:
        return cr


# calculates bonus from ability score
def score_to_bonus(score):
    return floor(score / 2) - 5


# returns dictionary with bonuses mapped to abilities
def ability_scores_to_bonuses(stats):
    bonusdict = {}
    for ability in stats:
        bonusdict[ability] = score_to_bonus(stats[ability])
    return bonusdict


# returns a spell description in an indented quote block
def makespell(name, level, school, casting_time, spell_range, components, duration, classes, effect, higher_levels):
    spell = "\\begin{quote}" + bold(name) + NEWLINE + italics(format_index(int(level)) + "-level " + school.lower()) + NEWLINE
    spell += bold("Casting Time: ") + casting_time + NEWLINE
    spell += bold("Range: ") + spell_range + NEWLINE
    spell += bold("Components: ") + components + NEWLINE
    spell += bold("Duration: ") + duration + NEWLINE
    spell += bold("Classes: ") + classes + NEWLINE
    spell += effect + NEWLINE
    spell += bolditalics("At Higher Levels: ") + higher_levels
    return spell + "\\end{quote}"


# returns CR with XP value
def cr(cr):
    return str(cr) + " (" + CR_TO_XP[cr] + " XP)"


# returns in the form of "DC challenge Ability (Skill) check"
def check(dc, *skill):
    skill = separate(skill)
    return "DC " + str(dc) + " " + ABILITIES_SPELLOUT[SKILL_ABILITY[skill]] + " (" + SKILL_PRETTYNAME[skill] + ") check"


# similar to the save function, but with a skill
def opposedcheck(ability, abilitybonus, profbonus):
    dc = 8 + abilitybonus + profbonus
    ability_name = ""
    if ability != "w/none":
        ability_name = ABILITIES_SPELLOUT[ability[2:]] + " "
    return "DC " + str(dc) + " " + ability_name + "check"


# returns in the form of "DC challenge Ability saving throw"
def save(ability, abilitybonus, profbonus):
    dc = 8 + abilitybonus + profbonus
    ability_name = ""
    if ability != "w/none":
        ability_name = ABILITIES_SPELLOUT[ability[2:]] + " "
    return "DC " + str(dc) + " " + ability_name + "saving throw"


# returns in the form of "DC challenge Ability saving throw"
def basicsave(ability, difficulty):
    ability_name = ""
    if ability != "w/none":
        ability_name = ABILITIES_SPELLOUT[ability[2:]] + " "
    return "DC " + str(difficulty) + " " + ability_name + "saving throw"


# returns in the form of "score (bonus)"
def stat(score):
    return str(score) + " (" + format_bonus(score_to_bonus(score)) + ")"