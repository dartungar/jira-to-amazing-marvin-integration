#!/usr/bin/env python3

from Application import Application
import sys

if __name__ == "__main__":
    app = Application()

    if sys.argv[1]:
        if sys.argv[1] == '--sync':
            app.sync()

        else:
            app.get_jira_issues_by_string_and_add_projects_to_marvin(
                sys.argv[1])
    else:
        app.sync()
