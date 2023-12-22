from utils.guessr.lb import (
    get_score,
    add_score,
    update_score,
)


async def update_user_stats(user_id, difficulty):
    user_data = await get_score(user_id)

    if not user_data:
        initial_scores = {"Easy": 0, "Medium": 0, "Hard": 0, "Very Hard": 0}
        initial_scores[difficulty] += 1

        await add_score(user_id, {"scores": initial_scores})
    else:
        user_data["scores"][difficulty] += 1

        await update_score(user_id, user_data)
