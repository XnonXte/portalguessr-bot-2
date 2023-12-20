from utils.guessr_scores_req import (
    guessr_get_score,
    guessr_add_score,
    guessr_update_score,
)


async def update_user_score(user_id, difficulty):
    user_data = await guessr_get_score(user_id)

    if not user_data:
        initial_scores = {"Easy": 0, "Medium": 0, "Hard": 0, "Very Hard": 0}
        initial_scores[difficulty] += 1

        await guessr_add_score(user_id, {"scores": initial_scores})
    else:
        user_data["scores"][difficulty] += 1

        await guessr_update_score(user_id, user_data)
