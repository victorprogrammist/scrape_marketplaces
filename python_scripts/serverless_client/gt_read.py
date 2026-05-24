import aiohttp
import tools.ozy_tools

async def read_text_from_github() -> str:

    username = 'victorprogrammist'
    repo = 'do_not_look_here_never_ever_again'
    filename ='temporary_address.txt'

    url = f"https://api.github.com/repos/{username}/{repo}/contents/{filename}"

    headers = {
        "Accept": "application/vnd.github.raw",
        "X-GitHub-Api-Version": "2026-03-10",
    }

    try:

        connector = aiohttp.TCPConnector(ssl=False)

        async with aiohttp.ClientSession(headers=headers, connector=connector) as session:

            async with session.get(url, timeout=10.0) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    raise Exception(f"Не удалось прочитать github. HTTP Статус: {response.status}")

    except Exception as e:
        tools.ozy_tools.logmsg(tools.ozy_tools.format_error(e))
        raise Exception(f"Произошла ошибка при обращении к github: {e}")

