import asyncio
import re
import ssl
from asyncio import gather
from parser.consts import CONTACT_PATHS, EMAIL_TEMPLATE
from typing import List, Optional

import httpx._exceptions as exc
from bs4 import BeautifulSoup
from httpx import AsyncClient

with open('../data/links.txt') as file:
    links = [line.rstrip('\n') for line in file.readlines()]


async def get_html(
    url: str,
    client: AsyncClient,
    **kwargs
) -> Optional[str]:
    try:
        response = await client.get(url, **kwargs)
        return response.text

    except (exc.ConnectError, ssl.SSLError, exc.ConnectTimeout):
        return None


async def find_email(
    url: str,
    client: AsyncClient
) -> Optional[List[str]]:
    if source := await get_html(url, client=client):
        bs = BeautifulSoup(
            source,
            features='html.parser'
        )

        emails = bs.find_all(
            'a',
            attrs={
                'href': EMAIL_TEMPLATE
            }
        )

        return [email.text for email in emails]

    return None


async def emails_by_url(
    base_url: str,
    client: AsyncClient
) -> List:
    emails = []

    for path in CONTACT_PATHS:
        if emails_on_path := await find_email(
            url=base_url + path,
            client=client
        ):
            emails += emails_on_path

    return [re.sub('\n\t', '', email) for email in emails]


async def main():
    async with AsyncClient() as client:
        emails = await gather(*[emails_by_url(link, client) for link in links])

    results = []

    for i in list(filter(lambda a: a, emails)):
        results += i

    return list(set(filter(EMAIL_TEMPLATE.match, results)))


with open('../data/emails.txt', 'w') as file:
    file.writelines(i + '\n' for i in asyncio.run(main()))
