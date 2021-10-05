#!/usr/bin/env python3

from Application import Application
import sys

if __name__ == "__main__":
    app = Application()

    if sys.argv[1]:
        if sys.argv[1] == '--sync':
            app.sync()

        if sys.argv[1] == '--update':
            app.get_jira_issues_for_existing_marvin_projects()

        else:
            app.get_jira_issues_by_string_and_add_projects_to_marvin(
                sys.argv[1])
    else:
        app.sync()
