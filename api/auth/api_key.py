from typing import List, Dict, Any, Tuple

from asyncio import get_running_loop

from passlib.hash import sha256_crypt
import secrets

from database.connection import db
from database.models.api_key import api_keys


def get_random_string(
    length,
    allowed_chars=(
        'abcdefghijklmnopqrstuvwxyz'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    )
):
    return ''.join(secrets.choice(allowed_chars) for i in range(length))


def concatenate(left: str, right: str) -> str:
    return "{}.{}".format(left, right)


def split(concatenated: str):
    left, _, right = concatenated.partition(".")
    return left, right


class KeyGenerator(object):
    def __init__(self, prefix_length=8, secret_key_length=32):
        self.prefix_length = prefix_length
        self.secret_key_length = secret_key_length

    def get_prefix(self):
        return get_random_string(self.prefix_length)

    def get_secret_key(self):
        return get_random_string(self.secret_key_length)

    def hash(self, value):
        return sha256_crypt.using(rounds=50000).hash(value)

    def generate(self):
        prefix = self.get_prefix()
        secret_key = self.get_secret_key()
        key = concatenate(prefix, secret_key)
        hashed_key = self.hash(key)
        return key, prefix, hashed_key

    def verify(self, key, hashed_key):
        return sha256_crypt.verify(key, hashed_key)


async def generate_api_key(
    name: str, permissions: List[str]
) -> Tuple[Dict[str, Any], str]:
    loop = get_running_loop()
    key_generator = KeyGenerator()

    # Since the sha256 algorithms are CPU bound, it is
    # necessary to run the generation in a separate thread
    key, prefix, hashed_key = await loop.run_in_executor(
        None,
        key_generator.generate,
    )

    api_key_data = {
        "name": name,
        "prefix": prefix,
        "hashed_key": hashed_key,
        "permissions": permissions,
        "is_active": True
    }

    query = api_keys.insert().values(api_key_data)
    await db.execute(query)
    return api_key_data, key


async def validate_key(key: str) -> Dict[str, Any] | None:
    loop = get_running_loop()
    key_generator = KeyGenerator()

    prefix, _, _ = key.partition(".")

    query = api_keys.select().where(api_keys.c.prefix == prefix)

    api_key = await db.fetch_one(query)

    if api_key is None:
        return None

    # Since the sha256 algorithms are CPU bound, it is
    # necessary to run the validation in a separate thread
    key_valid = await loop.run_in_executor(
        None, key_generator.verify, key, api_key["hashed_key"]
    )

    if not key_valid:
        return None

    return api_key


async def has_permission(key: str, permission: str):
    api_key = await validate_key(key)

    if api_key is None:
        return False

    return permission in api_key["permissions"]
