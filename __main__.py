import json
from JiraTask import JiraTask
from MarvinService import MarvinService
from JiraService import JiraService
from MarvinProject import MarvinProject
import sys

if __name__ == "__main__":
    jira = JiraService()
    marvin = MarvinService()

    tasks_keys = []

    if sys.argv[1]:
        if sys.argv[1] == '--sync':
            marvin.populate_repository_from_API()
            jira_tasks_raw = jira.get_raw_tasks_data()['issues']
            tasks = []
            for jt in jira_tasks_raw:
                if not marvin.projects_repository.exists(jt['key']):
                    tasks.append(JiraTask.from_raw_jira_task_data(jt))
            print(json.dumps(len(tasks)))
            for task in tasks:
                project = MarvinProject.from_jira_task(task)
                marvin.create_project_with_API(project)

        else:
            tasks_keys = jira.get_task_keys_from_string(sys.argv[1])
            for key in tasks_keys:
                raw_task_data = jira.get_raw_task_data(key)
                task = JiraTask.from_raw_jira_task_data(raw_task_data)
                project = MarvinProject.from_jira_task(task)
                marvin.create_project_with_API(project)
                print(f'Added project: {project.title}')
