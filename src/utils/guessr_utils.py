from const import (
    GUESSR_EASY_COLOR,
    GUESSR_MEDIUM_COLOR,
    GUESSR_HARD_COLOR,
    GUESSR_VERY_HARD_COLOR,
)


def guessr_diff_to_acronym(difficulty):
    match difficulty:
        case "Easy":
            return "e"
        case "Medium":
            return "m"
        case "Hard":
            return "h"
        case "Very Hard":
            return "vh"
        case _:
            raise Exception("Unknown identifier.")


def guessr_diff_to_expanded(difficulty):
    match difficulty:
        case "e":
            return "Easy"
        case "m":
            return "Medium"
        case "h":
            return "Hard"
        case "vh":
            return "Very Hard"
        case _:
            raise Exception("Unknown identifier.")


def guessr_find_mvp(array):
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


def guessr_get_color(difficulty):
    match difficulty:
        case "Easy":
            return GUESSR_EASY_COLOR
        case "Medium":
            return GUESSR_MEDIUM_COLOR
        case "Hard":
            return GUESSR_HARD_COLOR
        case "Very Hard":
            return GUESSR_VERY_HARD_COLOR
        case _:
            raise Exception("Unknown identifier.")


def guessr_get_timeout(difficulty):
    match difficulty:
        case "Easy":
            return 10
        case "Medium":
            return 15
        case "Hard":
            return 20
        case "Very Hard":
            return 25
        case _:
            raise Exception("Unknown identifier.")
