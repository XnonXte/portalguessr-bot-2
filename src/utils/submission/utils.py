from discord import Color


def get_color_by_status(status):
    if status == "pending":
        return Color.from_str("#99aab5")
    elif status == "accepted":
        return Color.from_str("#57f287")
    elif status == "rejected":
        return Color.from_str("#ed4245")
    else:
        raise Exception("Unknown status.")
