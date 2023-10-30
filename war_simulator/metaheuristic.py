import random
from goal_function import get_army_fitness
from metawars_api import Unit, Weapon, Armour, army_cost


def generate_init_population(number_of_individuals):
    population = []
    for i in range(number_of_individuals):
        individual = generate_init_individual()
        population.append(individual)
    return population


def generate_army_by_amounts(peasants_avg, swordmen_avg, spearmen_avg, archers_avg, defenders_avg, horsemen_avg, snipers_avg, knights_avg, elefants_avg):
    army = []
    weapon_types = [Weapon.diamond, Weapon.wood, Weapon.steel]
    armour_types = [Armour.diamond, Armour.wood, Armour.steel]

    peasants = [Unit(Unit.peasant, weapon_types[random.randrange(
        3)], armour_types[random.randrange(3)], random.randrange(1, 15)) for i in range(peasants_avg)]
    if army_cost(army + peasants) <= 100000:
        army = army + peasants

    swordmen = [Unit(Unit.swordman, weapon_types[random.randrange(
        3)], armour_types[random.randrange(3)], random.randrange(1, 15)) for i in range(swordmen_avg)]
    if army_cost(army + swordmen) <= 100000:
        army = army + swordmen

    spearmen = [Unit(Unit.spearman, weapon_types[random.randrange(
        3)], armour_types[random.randrange(3)], random.randrange(1, 15)) for i in range(spearmen_avg)]
    if army_cost(army + spearmen) <= 100000:
        army = army + spearmen

    archers = [Unit(Unit.archer, weapon_types[random.randrange(3)], armour_types[random.randrange(
        3)], random.randrange(1, 15)) for i in range(archers_avg)]
    if army_cost(army + archers) <= 100000:
        army = army + archers

    defenders = [Unit(Unit.defender, weapon_types[random.randrange(
        3)], armour_types[random.randrange(3)], random.randrange(1, 15)) for i in range(defenders_avg)]
    if army_cost(army + defenders) <= 100000:
        army = army + defenders

    horsemen = [Unit(Unit.horseman, weapon_types[random.randrange(
        3)], armour_types[random.randrange(3)], random.randrange(1, 15)) for i in range(horsemen_avg)]
    if army_cost(army + horsemen) <= 100000:
        army = army + horsemen

    knights = [Unit(Unit.knight, weapon_types[random.randrange(3)], armour_types[random.randrange(
        3)], random.randrange(1, 15)) for i in range(knights_avg)]
    if army_cost(army + knights) <= 100000:
        army = army + knights

    snipers = [Unit(Unit.sniper, weapon_types[random.randrange(3)], armour_types[random.randrange(
        3)], random.randrange(1, 15)) for i in range(snipers_avg)]
    if army_cost(army + snipers) <= 100000:
        army = army + snipers

    elefants = [Unit(Unit.elefant, weapon_types[random.randrange(
        3)], armour_types[random.randrange(3)], random.randrange(1, 15)) for i in range(elefants_avg)]
    if army_cost(army + elefants) <= 100000:
        army = army + elefants

    return army


def generate_init_individual():
    individual = []
    while True:
        unit_types = [Unit.archer, Unit.defender, Unit.elefant, Unit.horseman,
                      Unit.knight, Unit.peasant, Unit.sniper, Unit.swordman, Unit.spearman]
        unit_type = unit_types[random.randrange(9)]
        weapon_types = [Weapon.diamond, Weapon.wood, Weapon.steel]
        weapon_type = weapon_types[random.randrange(3)]
        armour_types = [Armour.diamond, Armour.wood, Armour.steel]
        armour_type = armour_types[random.randrange(3)]
        level = random.randrange(1, 15)
        if army_cost(individual + [Unit(unit_type, weapon_type, armour_type, level)]) > 100000:
            break
        individual = individual + [Unit(unit_type, weapon_type, armour_type, level)]
    return individual


def generate_best_army(number_of_iterations, number_of_init_individuals, alpha=0.3):
    population = generate_init_population(number_of_init_individuals)
    while number_of_iterations > 0:
        number_of_iterations -= 1
        for i in range(len(population)):
            x = population[random.randrange(number_of_init_individuals)]
            y = population[random.randrange(number_of_init_individuals)]
            if x != y:
                child = reproduce(x, y)
                if random.random() < alpha:
                    child = mutate(child)
                if army_cost(child) <= 100000:
                    population.append(child)
        population.sort(key=get_army_fitness, reverse=True)
        population = population[:number_of_init_individuals]
    return population[0]


def reproduce(x, y):
    peasants_avg = (len([y for y in x if y.unit_type == Unit.peasant]) +
                    len([x for x in y if x.unit_type == Unit.peasant]))//2
    swordmen_avg = (len([y for y in x if y.unit_type == Unit.swordman]) +
                    len([x for x in y if x.unit_type == Unit.swordman]))//2
    spearmen_avg = (len([y for y in x if y.unit_type == Unit.spearman]) +
                    len([x for x in y if x.unit_type == Unit.spearman]))//2
    archers_avg = (len([y for y in x if y.unit_type == Unit.archer]) +
                   len([x for x in y if x.unit_type == Unit.archer]))//2
    defenders_avg = (len([y for y in x if y.unit_type == Unit.defender]) +
                     len([x for x in y if x.unit_type == Unit.defender]))//2
    horsemen_avg = (len([y for y in x if y.unit_type == Unit.horseman]) +
                    len([x for x in y if x.unit_type == Unit.horseman]))//2
    snipers_avg = (len([y for y in x if y.unit_type == Unit.sniper]) +
                   len([x for x in y if x.unit_type == Unit.sniper]))//2
    knights_avg = (len([y for y in x if y.unit_type == Unit.knight]) +
                   len([x for x in y if x.unit_type == Unit.knight]))//2
    elefants_avg = (len([y for y in x if y.unit_type == Unit.elefant]) +
                    len([x for x in y if x.unit_type == Unit.elefant]))//2
    child = generate_army_by_amounts(peasants_avg, swordmen_avg, spearmen_avg, archers_avg,
                                     defenders_avg, horsemen_avg, snipers_avg, knights_avg, elefants_avg)
    return child


def mutate(x):
    return x + [x[random.randrange(len(x))]]
