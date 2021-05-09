def compute_count_sorted_dict(list_):
    count_dict = dict((i, list_.count(i)) for i in list_)
    return {k: v for k, v in sorted(count_dict.items(), key=lambda item: item[1], reverse=True)}
