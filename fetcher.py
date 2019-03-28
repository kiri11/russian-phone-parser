import asyncio
import aiohttp
import async_timeout
import re


url_list = [
    'https://www.tinkoff.ru',
    'https://www.dns-shop.ru',
    'https://hands.ru/company/about',
    'https://repetitors.info',
    'https://www.ruki-iz-plech.ru'
]


def normalize(phone):
    """Normalize phone numbers to 8KKKNNNNNNN format."""
    if phone.startswith('+'):
        phone = phone[1:]
    return '8' + phone[1:]


def parse_phone(txt):
    """Find set of phones in text."""
    phone_regexp = r"\D((\+7|7|8)+([0-9]){10})\D"
    return {normalize(phone) for phone, _, _ in re.findall(phone_regexp, txt)}


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return url, parse_phone(await response.text())


async def main():
    async with aiohttp.ClientSession() as session:
        htmls = await asyncio.gather(*[fetch(session, url) for url in url_list], return_exceptions=True)

        for url, phones in htmls:
            print(url, phones)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
