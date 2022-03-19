import json

from excel_parser.cab_time_matcher import get_all_cabs, rebuild_json
from excel_parser.table_parser import parse_t


def excel_parse(path, idx):
    cab_time_json = json.loads(parse_t(path, idx))
    all_cabs = get_all_cabs(cab_time_json)
    rebuild_cab_time_json = rebuild_json(cab_time_json, all_cabs)
    return rebuild_cab_time_json, all_cabs