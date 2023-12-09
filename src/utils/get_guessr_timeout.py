def get_guessr_timeout(difficulty):
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
