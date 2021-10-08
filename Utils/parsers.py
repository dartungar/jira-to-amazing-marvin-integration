import re
from typing import Set


def get_single_issue_key_from_string(string: str) -> str:
    key_regex = re.compile(r'[A-Z]{2,6}-[1-9][0-9]{0,4}')
    keys_found = key_regex.findall(string)
    return keys_found[0] if keys_found else None


def get_issues_keys_from_string(string: str) -> Set[str]:
    '''get a set of issue keys by parsing string'''
    key_regex = re.compile(r'[A-Z]{2,6}-[1-9][0-9]{0,4}')
    return set(key_regex.findall(string))
