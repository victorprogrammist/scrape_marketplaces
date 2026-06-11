
from datetime import datetime
import os
import sys
from pathlib import Path
import traceback
import asyncio
import re


global_function_for_logging = None
global_filename_for_logging = None


COLLAPSE_WHITESPACE = re.compile(r'\s+')

def stripped(raw_text):
    return COLLAPSE_WHITESPACE.sub(' ', raw_text).strip()

def remove_all_spaces(raw_text):
    return COLLAPSE_WHITESPACE.sub('', raw_text)

async def locator_get_tagname(locator):
    # результат всегда в верхнем регистре
    tag_name = await locator.evaluate("element => element.tagName")
    return tag_name


async def wait_with_timeout(
        event: asyncio.Event,
        timeout_sec: float,
        event_fail = None
        ) -> bool:

    if event_fail is not None:
        return await wait_with_timeout_0(event, timeout_sec, event_fail)

    try:
        await asyncio.wait_for(event.wait(), timeout=timeout_sec)
        return True

    except TimeoutError:
        return False



async def wait_with_timeout_0(
        event: asyncio.Event,
        timeout_sec: float,
        event_fail: asyncio.Event
        ) -> bool:

    if event_fail.is_set():
        return False

    if event.is_set():
        return True

    main_task = asyncio.create_task(event.wait())
    fail_task = asyncio.create_task(event_fail.wait())

    try:

        done, pending = await asyncio.wait(
            {main_task, fail_task},
            timeout=timeout_sec,
            return_when=asyncio.FIRST_COMPLETED,
        )

        if main_task in done and not fail_task in done:
            return True

        return False

    finally:
        main_task.cancel()
        fail_task.cancel()
        await asyncio.gather(main_task, fail_task, return_exceptions=True)


def format_error(e):

    msg = str(e)
    if not msg:
        exc_type = type(e).__name__
        exc_args = e.args
        msg = f'{exc_type}, {exc_args}'

    tb = traceback.format_exc()

    return f'=== Ошибка: {msg}\n{tb}'


def assign_logger(fn_for_logging):
    global global_function_for_logging
    global_function_for_logging = fn_for_logging


def filename_for_log():
    global global_filename_for_logging

    if global_filename_for_logging is None:
        global_filename_for_logging = get_filename_for_store('logmsg.log')

    return global_filename_for_logging


def appendLog(s):

    fn = filename_for_log()

    with open(fn, 'at') as f:
        f.write(f'{date_time_str()}: {s}\n')


def logmsg(msg):
    if global_function_for_logging is None:
        print(msg)
        appendLog(msg)
    else:
        global_function_for_logging(msg)


def only_numbers(src, can_be_point = True):

    if isinstance(src, int):
        return src

    if isinstance(src, float):
        if can_be_point:
            return src
        return int(src)

    if not isinstance(src, str):
        return 0

    abc = '0123456789'

    was_point = False
    res = []
    for sy in src:
        if sy in abc:
            res.append(sy)
        elif (sy == '.' or sy == ',') and not was_point and can_be_point:
            res.append('.')
            was_point = True

    if not res:
        return 0

    res = ''.join(res)

    if not was_point:
        return int(res)

    return float(res)


def date_time_str():
    return datetime.now().strftime("%Y-%m-%d--%H-%M-%S")

def check_make_path(pa):
    Path(pa).mkdir(parents=True, exist_ok=True)
    return pa

def check_make_path_for_file(filename):
    check_make_path(os.path.split(filename)[0])
    return filename

def make_absolute(file_path, base_dir):
    if os.path.isabs(file_path):
        return os.path.normpath(file_path)
    else:
        combined = os.path.join(base_dir, file_path)
        return os.path.abspath(combined)

#*******************************************************************


def base_path(subpath = None, filename = None):

    script_path = os.path.abspath(sys.argv[0])
    source_dir = os.path.dirname(script_path)

    as_m = script_path.endswith('__main__.py')

    if as_m:
        source_dir = os.path.join(source_dir, '..')

    if subpath:
        source_dir = os.path.join(source_dir, subpath)

    if not filename:
        return source_dir

    return make_absolute(filename, source_dir)


def get_filename_for_read(filename):
    return base_path('results', filename)


def get_filename_for_store(filename):

    res = get_filename_for_read(filename)

    return check_make_path_for_file(res)


#*******************************************************************


