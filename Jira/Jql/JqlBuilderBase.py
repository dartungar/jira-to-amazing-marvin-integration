from typing import List

class JqlBuilderBase:
    _jql_string: str

    def __init__(self) -> None:
        self._jql_string = ""

    def with_status_categories(self, status_categories: List[str]) -> None:
        self._add_condition(f"statuscategory IN {self.__multiple_items(status_categories)}")

    def exclude_status_categories(self, status_categories: List[str]) -> None:
        self._add_condition(f"statuscategory NOT IN {self.__multiple_items(status_categories)}")

    def with_statuses(self, statuses: List[str]) -> None:
        self._add_condition(f"status IN {self.__multiple_items(statuses)}")

    def exclude_statuses(self, statuses: List[str]) -> None:
        self._add_condition(f"status NOT IN {self.__multiple_items(statuses)}")

    def with_projects(self, project_keys: List[str]) -> None:
        self._add_condition(f"project IN {self.__multiple_items(project_keys)}")

    def exclude_projects(self, project_keys: List[str]) -> None:
        self._add_condition(f"project NOT IN {self.__multiple_items(project_keys)}")

    def with_assignees(self, assignees: List[str]) -> None:
        self._add_condition(f"assignee IN {self.__multiple_items(assignees)}")

    def exclude_assignees(self, assignees: List[str]) -> None:
        self._add_condition(f"assignee NOT IN {self.__multiple_items(assignees)}")

    def with_assignee_not_empty(self) -> None:
        self._add_condition("assignee != EMPTY")

    def _add_condition(self, condition: str) -> None:
        if self._jql_string:
            self._jql_string += " AND "
        self._jql_string += condition

    def __multiple_items(self, items: List[str]) -> str:
        items_set = set(items)
        items_set_str = ",".join([f"\"{i}\"" for i in items_set])
        return f" ({items_set_str})"

    def __sanitize(self) -> None:
        self._jql_string.replace("@", "\\u0040")

    def __repr__(self) -> str:
        self.__sanitize()
        return self._jql_string



class JqlBuilderException(Exception):
    pass