def calculate_improvement(
    before_score,
    after_score
):

    if before_score == 0:
        return 0

    return round(
        ((before_score - after_score)
        / before_score) * 100,
        2
    )