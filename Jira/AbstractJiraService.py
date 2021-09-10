from abc import ABC, abstractmethod


class AbstractJiraService(ABC):
    BASE_API_URL: str
    GET_ISSUE_ENDPOINT: str
    GET_MULTIPLE_ISSUES_ENDPOINT: str

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_single_issue_data(self) -> str:
        pass

    @abstractmethod
    def get_multiple_issues_data(self) -> str:
        pass
