def get_status(improvement):

    if improvement >= 80:
        return "Resolved"

    elif improvement >= 40:
        return "Partially Resolved"

    return "Not Resolved"