import math
import json
import urllib.request

## Constants & Maps

# Keys to keep for assignment transfer
player_keys = ['firstName',
               'lastName',
               'born',
               'college',
               'face',
               'imgURL',
               'tid',
               'ratings',
               'hgt',
               'weight',
               'pos']

# Names for all T1 CAPs
CAP_NAMES = ['Rodney Okafor']

# GBBL -> GGBBLL tid mapping
assignment_map = {
    '0': 31,
    '1': 12,
    '2': 11,
    '3': 8,
    '4': 25,
    '5': 2,
    '6': 23,
    '7': 30,
    '8': 7,
    '9': 19,
    '10': 17,
    '11': 6,
    '12': 0,
    '13': 21,
    '14': 13,
    '15': 20,
    '16': 26,
    '17': 9,
    '18': 5,
    '19': 24,
    '20': 15,
    '21': 10,
    '22': 4,
    '23': 14,
    '24': 29,
    '25': 22,
    '26': 1,
    '27': 16,
    '28': 18,
    '29': 3,
    '30': 27,
    '31': 28
}

# GGBBLL -> GBBL tid mapping
points_map = {v: k for (k, v) in assignment_map.items()}

## Functions
def main_to_g_league(player):
    return assignment_map[str(player['tid'])]


def g_league_to_main(player):
    return int(points_map[player['tid']])


def cap_check(player):
    return(player['firstName'].strip() + " " + player['lastName'].strip()) in CAP_NAMES


def playoff_check(stat, season):
    return bool(stat["playoffs"] is True and stat["season"] == season)


def print_points(points, player, teamDict):
    pp = f"{find_player(player)} (@{teamDict[g_league_to_main(player)]}): {points} TP"
    print(pp)


def print_cap_points(points, player, teamDict):
    pcp = f"{find_player(player)} (CAP) (@{teamDict[g_league_to_main(player)]}): {points} TP"
    print(pcp)


def find_player(player):
    if len(player['lastName']) == 0:
        return player['firstName'].strip()
    if len(player['firstName']) == 0:
        return player['lastName'].strip()
    return player['firstName'].strip() + " " + player['lastName'].strip()


def awardCount(player, season):
    count = 0
    for award in player['awards']:
        if award["season"] == season:
            count += 1
    return count


def assign_points(stat, player, season):
    awards = awardCount(player, season)
    points = (math.ceil((0.01*stat['pts'])) + math.ceil((0.025*(stat['drb']+stat['orb']))) +
              math.ceil((0.12*stat['blk'])) + math.ceil((0.15*stat['stl'])) +
              math.ceil((0.035*stat['ast'])) + (4 * awards))
    base = math.ceil((0.4*stat['gp'])+(0.2*stat['gs']))
    points = max(points, base)
    return points


def cap_points(stat, player, season):
    points_min = 30
    awards = awardCount(player, season)
    points = (math.ceil((0.015*stat['pts'])) + math.ceil((0.09*(stat['drb']+stat['orb']))) +
              math.ceil((0.3*stat['blk'])) + math.ceil((0.25*stat['stl'])) +
              math.ceil((0.1*stat['ast'])) + (7 * awards))
    base = math.ceil((0.5*stat['gp'])+(0.5*stat['gs']))
    if (points < base) and (base >= 30):
        return base
    if (points < base < 30):
        return points_min
    return points

def fetch_export(filename):

    if filename.lower().startswith('http'):
        req = urllib.request.Request(filename)
    else:
        raise ValueError from None
    pass

    with urllib.request.urlopen(req) as f:
        return json.loads(f.read().decode('utf-8-sig'))

