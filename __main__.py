#!/usr/bin/env python3

from Application.Application import Application
import sys
import asyncio

if __name__ == "__main__":
    app = Application()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    if sys.argv[1]:
        if sys.argv[1] == '--sync':
            asyncio.run(app.sync())

        if sys.argv[1] == '--update':
            asyncio.run(app.update_projects())

        else:
            print(sys.argv[1])
    else:
        app.sync()
