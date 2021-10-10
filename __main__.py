#!/usr/bin/env python3

from Application.Application import Application
import sys

if __name__ == "__main__":
    app = Application()

    if sys.argv[1]:
        if sys.argv[1] == '--sync':
            app.sync()

        if sys.argv[1] == '--update':
            app.check_assignees()

        else:
            print(sys.argv[1])
    else:
        app.sync()
