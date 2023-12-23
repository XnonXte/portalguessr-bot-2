def get_color_by_status(status):
    match (status):
        case "pending":
            return "#99aab5"
        case "accepted":
            return "#57f287"
        case "rejected":
            return "#ed4245"
