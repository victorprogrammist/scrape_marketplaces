import asyncio
import sys
import aiohttp
import time
import json

import tools.ozy_tools
import tools.content_packer
import client_tools.get_from_github


async def __start_messaging(url: str, request):

    tools.ozy_tools.logmsg(f'подключение к {url}')

    TIMEOUT_FOR_AIOHTTP = 60 * 5

    time_start = time.perf_counter()

    req_unpacked = len(request)

    request = tools.content_packer.pack_message(request, 'gzip')

    req_packed = len(request)

    ans_unpacked = 0
    ans_packed = 0

    headers = {
        "Bypass-Tunnel-Reminder": "true",
        "Content-Type": "application/octet-stream",
        "Content-Transfer-Encoding": "binary",
        "Content-Length": str(len(request))
    }

    try:
        async with aiohttp.ClientSession(headers=headers) as session:

            async with session.post(url, data=request, timeout=TIMEOUT_FOR_AIOHTTP) as response:

                if response.status == 200:

                    answer = await response.read()

                    ans_packed = len(answer)

                    _, answer = tools.content_packer.decompress_message(answer)

                    ans_unpacked = len(answer)

                    return answer

                else:

                    error_body = await response.text()
                    short_error_body = error_body[:500] if error_body else "Empty body"

                    raise Exception(f'aiohttp error, status: {response.status}, {short_error_body}')


    except aiohttp.ClientConnectorError:
        raise Exception("Ошибка подключения.")

    except Exception as e:
        tools.ozy_tools.logmsg(tools.ozy_tools.format_error(e))
        raise Exception(f"Произошла ошибка: {e}")

    finally:

        time_passed = time.perf_counter() - time_start

        tools.ozy_tools.logmsg(
            f'Размеры, запрос: {req_packed}/{req_unpacked}, ответ: {ans_packed}/{ans_unpacked}, время: {time_passed:.3f}')


async def make_request(request):

    try:

        if isinstance(request, dict):
            request = json.dumps(request, indent=4, ensure_ascii=False, sort_keys=False)

        url = await client_tools.get_from_github.get_from_github()
        if url is None:
            raise Exception("Что-то не так")

        return await __start_messaging(url, request)

    except Exception as e:

        return tools.ozy_tools.format_error(e)



