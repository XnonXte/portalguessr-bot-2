from const import (
    EASY_COLOR,
    MEDIUM_COLOR,
    HARD_COLOR,
    VERY_HARD_COLOR,
)


def diff_to_acronym(difficulty):
    if difficulty == "Easy":
        return "e"
    elif difficulty == "Medium":
        return "m"
    elif difficulty == "Hard":
        return "h"
    elif difficulty == "Very Hard":
        return "vh"
    else:
        raise Exception("Unknown identifier.")


def diff_to_expanded(difficulty):
    if difficulty == "e":
        return "Easy"
    elif difficulty == "m":
        return "Medium"
    elif difficulty == "h":
        return "Hard"
    elif difficulty == "vh":
        return "Very Hard"
    else:
        raise Exception("Unknown identifier.")


def find_mvp(array):
    count_dict = {}

    for item in array:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    most_common_item = None
    max_count = 0

    for item, count in count_dict.items():
        if count > max_count:
            most_common_item = item
            max_count = count

    return most_common_item


def get_color(difficulty):
    if difficulty == "Easy":
        return EASY_COLOR
    elif difficulty == "Medium":
        return MEDIUM_COLOR
    elif difficulty == "Hard":
        return HARD_COLOR
    elif difficulty == "Very Hard":
        return VERY_HARD_COLOR
    else:
        raise Exception("Unknown identifier.")


def get_timeout(difficulty):
    if difficulty == "Easy":
        return 10
    elif difficulty == "Medium":
        return 15
    elif difficulty == "Hard":
        return 20
    elif difficulty == "Very Hard":
        return 25
    else:
        raise Exception("Unknown identifier.")
