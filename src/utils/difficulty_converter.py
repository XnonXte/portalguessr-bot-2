def diff_expanded_to_acronym(difficulty):
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


def diff_acronym_to_expanded(difficulty):
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
