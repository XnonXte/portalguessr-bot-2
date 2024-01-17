from const import (
    EASY_COLOR,
    MEDIUM_COLOR,
    HARD_COLOR,
    VERY_HARD_COLOR,
)


def diff_to_acronym(difficulty_expanded):
    difficulty_acronyms = {"Easy": "e", "Medium": "m", "Hard": "h", "Very Hard": "vh"}

    return difficulty_acronyms.get(difficulty_expanded, "e")


def diff_to_expanded(difficulty_acronym):
    difficulty_expands = {"e": "Easy", "m": "Medium", "h": "Hard", "vh": "Very Hard"}

    return difficulty_expands.get(difficulty_acronym, "Easy")


def find_mvp(array):
    count_dict = {}

    for item in array:
        if item not in count_dict:
            count_dict[item] = 0
        count_dict[item] += 1

    most_common_item = None
    max_count = 0

    for item, count in count_dict.items():
        if count > max_count:
            most_common_item = item
            max_count = count

    return most_common_item


def get_color(difficulty_expanded):
    difficulty_colors = {
        "Easy": EASY_COLOR,
        "Medium": MEDIUM_COLOR,
        "Hard": HARD_COLOR,
        "Very Hard": VERY_HARD_COLOR,
    }

    return difficulty_colors.get(difficulty_expanded, EASY_COLOR)


def get_timeout(difficulty_expanded):
    difficulty_timeouts = {"Easy": 15, "Medium": 20, "Hard": 25, "Very Hard": 30}

    return difficulty_timeouts.get(difficulty_expanded, 15)
