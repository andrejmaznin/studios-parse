import asyncio
from parser.emails import parse_and_write_emails
from parser.links import parse_studios_links
from parser.paths import parse_studios_paths

from service.fix_links_and_paths import fix_links, fix_paths

print('parsing paths...')
parse_studios_paths(10)
print('fixing paths...')
fix_paths()
print('parsing links...')
parse_studios_links()
print('fixing links...')
fix_links()
asyncio.run(parse_and_write_emails())
