import re


def fix_links():
    with open('data/links.txt', 'r') as links:
        links = links.readlines()

    fixed_links = []

    for link in links:
        link = re.sub(r'\w*://[w\d*.]*', '', link)  # remove protocol
        link = re.sub(r'/.*', '', link)  # remove path and path params

        fixed_links.append(link)

    with open('data/links.txt', 'w') as links:
        links.writelines(map(str, fixed_links))


def fix_paths():
    with open('data/paths.txt', 'r') as paths:
        source_lines = paths.readlines()
        lines = []
        for i in range(len(source_lines)):
            if 'http' in source_lines[i]:
                continue

            lines.append(source_lines[i])

    with open('data/paths.txt', 'w') as paths:
        paths.writelines(map(str, lines))


def fix_links_and_paths():
    fix_links()
    fix_paths()
