import json
from collections import defaultdict

from excel_parser.re_utils import get_cab


def default_to_regular(d):
    if isinstance(d, defaultdict):
        d = {k: default_to_regular(v) for k, v in d.items()}
    return d


def get_all_cabs(cab_time_json):
    cabs = set()
    for wday in cab_time_json.keys():
        for num_den in cab_time_json[wday].keys():
            for cls_t in cab_time_json[wday][num_den].keys():
                for cls in cab_time_json[wday][num_den][cls_t]:
                    cabs.add(get_cab(cls))
    return sorted(cabs)


def get_curr_time_cabs(clss):
    cabs = set()
    for c in clss:
        cabs.add(get_cab(c))
    return cabs


def rebuild_json(cab_time_json, cabs):
    rebuilt_cab_time = defaultdict(lambda: defaultdict(dict))
    for wday in cab_time_json.keys():
        for num_den in cab_time_json[wday].keys():
            for cls_t in cab_time_json[wday][num_den].keys():
                rebuilt_cab_time[wday][cls_t][num_den] = []
                curr_time_cabs = get_curr_time_cabs(cab_time_json[wday][num_den][cls_t])
                for cab in cabs:
                    rebuilt_cab_time[wday][cls_t][num_den].append(cab in curr_time_cabs)
    return default_to_regular(rebuilt_cab_time)


def get_rebuilt_json(cab_time_json):
    all_cabs = get_all_cabs(cab_time_json)
    return rebuild_json(cab_time_json, all_cabs)


def main():
    with open("data.json", "r", encoding="windows-1251") as f:
        cab_time_json = json.load(f)
    all_cabs = get_all_cabs(cab_time_json)
    rebuild_cab_time_json = rebuild_json(cab_time_json, all_cabs)
    print()


if __name__ == '__main__':
    main()
