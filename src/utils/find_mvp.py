from collections import Counter


def find_mvp(List):
    try:
        counter_list = Counter(List)
        return counter_list.most_common(1)[0][0]
    except IndexError:
        return None
