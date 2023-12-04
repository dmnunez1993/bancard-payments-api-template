#!/usr/bin/env python3
from typing import List

import argparse
import asyncio

from auth.api_key import generate_api_key
from database.connection import db


async def _connect_and_create_api_key(name: str, permissions: List[str]):
    await db.connect()
    await generate_api_key(name, permissions)
    await db.disconnect()


def main():
    parser = argparse.ArgumentParser(description="Creates an Api Key")
    parser.add_argument(
        '-n',
        '--name',
        help="Name",
        type=str,
        required=True,
        dest='name',
    )
    parser.add_argument(
        '-p',
        '--permission',
        help="Permission",
        type=str,
        required=True,
        action='append',
        dest='permissions',
    )

    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    print(
        f"Creating Api key with name: {args.name}, permissions: {args.permissions}"
    )
    loop.run_until_complete(
        _connect_and_create_api_key(args.name, args.permissions)
    )


if __name__ == '__main__':
    main()
