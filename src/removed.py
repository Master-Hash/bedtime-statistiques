if __name__ == "__main__":
    from issues import BEDTIME_NEWS
else:
    from .issues import BEDTIME_NEWS

REMOVED_ISSUES = [
    74,
    140,
    178,
    183,
    353,
    397,
    409,
    524,
    551,
    565,
    588,
    669,
    673,
]

REMOVED_ANNOTAIONS = [
    (int(i["issue"]), i["created"])
    for i in BEDTIME_NEWS
    if str.isdecimal(i["issue"])
    if int(i["issue"]) - 1 in REMOVED_ISSUES
]

if __name__ == "__main__":
    from pprint import pprint

    pprint(REMOVED_ANNOTAIONS)
