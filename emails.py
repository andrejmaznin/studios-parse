import asyncio
import re
import ssl
from asyncio import gather
from typing import Optional, List

from httpx import AsyncClient
from bs4 import BeautifulSoup
import httpx._exceptions as exc

CONTACT_PATHS = ['/contact', '/contacts']
EMAIL_TEMPLATE = re.compile(
    '''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])''')  # noqa

with open('links.txt') as file:
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
) -> List[str]:
    if source := await get_html(url, client=client):
        bs = BeautifulSoup(
            source,
            features="html.parser"
        )

        emails = bs.find_all(
            'a',
            attrs={
                'href': EMAIL_TEMPLATE
            }
        )

        return [email.text for email in emails]


async def emails_by_url(
    base_url: str,
    client: AsyncClient
) -> List:
    emails = []

    for path in CONTACT_PATHS:
        if emails_on_path := await find_email(url=base_url + path, client=client):
            emails += emails_on_path

    return [re.sub('\n\t', '', email) for email in emails]


async def main():
    async with AsyncClient() as client:
        emails = await gather(*[emails_by_url(link, client) for link in links])

    results = []

    for i in list(filter(lambda a: a, emails)):
        results += i

    return list(set(filter(EMAIL_TEMPLATE.match, results)))


with open('emails.txt', 'w') as file:
    file.writelines(i + '\n' for i in asyncio.run(main()))
