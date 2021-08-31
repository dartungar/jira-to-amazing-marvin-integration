from JiraTask import JiraTask
from MarvinService import MarvinService
from JiraService import JiraService
from MarvinProject import MarvinProject
import sys

if __name__ == "__main__":
    jira = JiraService()
    tasks = []
    if sys.argv[1]:
        tasks = jira.get_task_keys_from_string(sys.argv[1])
    for key in tasks:
        raw_task_data = jira.get_raw_task_data(key)
        task = JiraTask.from_raw_jira_task_data(raw_task_data)
        project = MarvinProject.from_jira_task(task)
        marvin = MarvinService()
        marvin.create_project(project)
        print(f'Added project: {project.title}')
