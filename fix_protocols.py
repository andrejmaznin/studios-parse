with open('links.txt', 'r+') as links:
    lines = links.readlines()

    for i in range(len(lines)):
        if 'https' not in lines[i]:
            lines[i] = lines[i].replace('http', 'https')

with open('links.txt', 'w') as links:
    links.writelines(map(str, lines))
