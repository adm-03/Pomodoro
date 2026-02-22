

import asyncio
import sys


pytest_plugins = [
    "tests.fixtures.auth.auth_service",
    "tests.fixtures.auth.clients",
    "tests.fixtures.users.user_repository",
    "tests.fixtures.infrastructure",
    "tests.fixtures.users.user_model"
]

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())