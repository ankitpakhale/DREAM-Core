from app.framework import Request
import inspect
from app.utils import logger
from typing import Any, Callable
import diskcache as dc
from functools import wraps
import hashlib
import json


class CacheManager:
    """
    CacheManager handles caching operations using a dictionary for now.
    """

    # diskcache configurations
    cache_store = dc.Cache(".dream_cache")

    @staticmethod
    def get(key: str) -> Any:
        """
        get value from cache by key
        """
        return CacheManager.cache_store.get(key)

    @staticmethod
    def set(key: str, value: Any) -> None:
        """
        set value in cache by key
        """
        CacheManager.cache_store[key] = value

    @staticmethod
    def has(key: str) -> bool:
        """
        check if key exists in cache
        """
        return key in CacheManager.cache_store

    @staticmethod
    def delete(key: str) -> None:
        """
        Delete a specific cache entry by key.
        """
        if CacheManager.has(key):
            del CacheManager.cache_store[key]

    @staticmethod
    def clear() -> None:
        """
        Clear all cache entries.
        """
        CacheManager.cache_store.clear()

    @staticmethod
    def generate_cache_key(func: Callable, args: tuple, kwargs: dict) -> str:
        """
        Generates a unique cache key based on function name, args, and kwargs.
        This improved version handles complex nested structures and string representations.
        """
        # start with the function name
        func_name = func.__name__

        # process args
        processed_args = []
        for arg in args:
            if isinstance(arg, dict):
                # for dictionaries, sort keys and convert to JSON for consistent representation
                processed_args.append(json.dumps(arg, sort_keys=True))
            elif isinstance(arg, str):
                # special handling for strings that might contain serialized data
                # check if it looks like a list or dict representation
                if (arg.startswith("[") and arg.endswith("]")) or (
                    arg.startswith("{") and arg.endswith("}")
                ):
                    try:
                        # try to parse it as JSON first
                        parsed = json.loads(arg.replace("'", '"'))
                        processed_args.append(json.dumps(parsed, sort_keys=True))
                    except json.JSONDecodeError:
                        # if it's not valid JSON, use the string as is
                        processed_args.append(arg)
                else:
                    processed_args.append(arg)
            else:
                processed_args.append(str(arg))

        # process kwargs
        processed_kwargs = []
        for k, v in sorted(kwargs.items()):
            if isinstance(v, dict):
                # for dictionaries, sort keys and convert to JSON
                processed_kwargs.append(f"{k}={json.dumps(v, sort_keys=True)}")
            elif isinstance(v, str):
                # special handling for strings that might contain serialized data
                if (v.startswith("[") and v.endswith("]")) or (
                    v.startswith("{") and v.endswith("}")
                ):
                    try:
                        # try to parse it as JSON first
                        parsed = json.loads(v.replace("'", '"'))
                        processed_kwargs.append(
                            f"{k}={json.dumps(parsed, sort_keys=True)}"
                        )
                    except json.JSONDecodeError:
                        # if it's not valid JSON, use the string as is
                        processed_kwargs.append(f"{k}={v}")
                else:
                    processed_kwargs.append(f"{k}={v}")
            else:
                processed_kwargs.append(f"{k}={str(v)}")

        # combine everything into a single string
        key_data = (
            f"{func_name}-{'-'.join(processed_args)}-{'-'.join(processed_kwargs)}"
        )

        # log the key data for debugging
        logger.debug(f"Cache key data before hashing: {key_data}")

        # generate a hash for consistent and unique key
        cache_key = hashlib.sha256(key_data.encode("utf-8")).hexdigest()
        return cache_key


# object of cache_manager
cache_manager = CacheManager()


def cache(func):
    """
    Custom decorator to cache the result using CacheManager.
    Supports both synchronous and asynchronous functions.
    """

    is_coroutine = inspect.iscoroutinefunction(func)

    def generate_cache_key_from_form_data():
        try:
            form_data = {}
            if hasattr(Request, "forms") and Request.forms:
                possible_fields = [
                    "difficulty_level",
                    "programming_language",
                    "topics",
                    "user_code",
                    "rating",
                    "comments",
                    "full_name",
                    "email",
                    "cache_key",
                ]

                for field in possible_fields:
                    value = Request.forms.get(field)
                    if value is not None:
                        form_data[field] = value

                if form_data:
                    logger.info(f"Extracted form data: {form_data}")
                    form_str = json.dumps(form_data, sort_keys=True)
                    return hashlib.sha256(form_str.encode("utf-8")).hexdigest()
        except Exception as e:
            logger.error(f"Error extracting form data: {e}")
        return None

    if is_coroutine:

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            cache_key = generate_cache_key_from_form_data()
            if not cache_key:
                cache_key = cache_manager.generate_cache_key(func, args, kwargs)
                logger.warning("Fallback cache key generation used (async)")

            logger.info(f"Cache_key: {cache_key}")

            cached_result = cache_manager.get(cache_key)
            if cached_result:
                logger.info(f"Cache hit for key: {cache_key}")
                return cached_result

            result = await func(*args, **kwargs)
            cache_manager.set(cache_key, result)
            logger.warning(f"Cache miss for key: {cache_key}")
            logger.warning("Result successfully cached for future use.")
            return result

        return async_wrapper

    else:

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            cache_key = generate_cache_key_from_form_data()
            if not cache_key:
                cache_key = cache_manager.generate_cache_key(func, args, kwargs)
                logger.warning("Fallback cache key generation used (sync)")

            logger.info(f"Cache_key: {cache_key}")

            cached_result = cache_manager.get(cache_key)
            if cached_result:
                logger.info(f"Cache hit for key: {cache_key}")
                return cached_result

            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result)
            logger.warning(f"Cache miss for key: {cache_key}")
            logger.warning("Result successfully cached for future use.")
            return result

        return sync_wrapper


async def delete_cache(_key):
    await cache_manager.delete(_key)


async def clear_cache():
    await cache_manager.clear()
