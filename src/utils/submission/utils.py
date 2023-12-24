def get_color_by_status(status):
    if status == "pending":
        return "#99aab5"
    elif status == "accepted":
        return "#57f287"
    elif status == "rejected":
        return "#ed4245"
    else:
        raise Exception("Unknown status.")
