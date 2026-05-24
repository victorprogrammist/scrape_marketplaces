
import sys
import json

import use_cli.params
import tools.ozy_tools

import serverless_client.slc

import asyncio


def final_error(dest_file, msg):

    tools.ozy_tools.logmsg(msg)

    s = json.dumps( {"ошибка": msg}, indent=4, ensure_ascii=False, sort_keys=False)

    with open(dest_file, 'w', encoding='utf-8') as f:
        f.write(s)

    sys.exit(1)


async def main() -> None:

    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    params = use_cli.params.read_params_from_file()

    dest_file = params.get('dest_filename')

    if not params:
        final_error(dest_file, 'входные параметры не определены')
        sys.exit(1)
        return

    query = json.dumps(params, indent=4, ensure_ascii=False, sort_keys=False)

    try:
        answer = await serverless_client.slc.serverless_request(query)
    except Exception as e:
        final_error(dest_file, tools.ozy_tools.format_error(e))
        sys.exit(1)
        return

    with open(dest_file, 'w', encoding='utf-8') as f:
        f.write(answer)



