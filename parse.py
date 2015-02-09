import sys
import re
import os
import yaml


all_links = set()

def get_metadata(wiki):
    cat_re = re.compile(r'\[\[Category:([^|]*)(?:|[^\]]*)?\]\]')
    remaining_lines = []
    metadata = {}
    for line in wiki.split('\n'):
        mo = cat_re.match(line)
        if mo:
            if ':' in mo.group(1):
                typ, name = mo.group(1).split(':', 1)
                metadata.setdefault(typ.lower(), []).append(name)
        else:
            remaining_lines.append(line)
    return '\n'.join(remaining_lines), metadata


def images(wiki):
    img_re = re.compile(r'\[\[Image:([^|\]]*)(?:|[^\]]*)?\]\]')
    return img_re.sub(r'![](/img/\1)', wiki)


def links(wiki):
    interlink_re = re.compile(r'\[\[([^|\]]*)(|[^\]]*)\]\]')

    def interlink_repl(mo):
        name = mo.group(2) if mo.group(2) else mo.group(1)
        if name.startswith('Recipe:'):
            name = name[7:]
        linkname = mo.group(1)
        if linkname.startswith('Recipe:'):
            linkname = linkname[7:]
        if linkname.startswith(':Category:Cookbook:'):
            linkname = linkname[len(':Category:Cookbook:'):]
        if linkname == 'Cornbread':
            linkname = 'Corn Muffins'
        all_links.add(slugify(linkname))
        return '[{}]({}.html)'.format(name, slugify(linkname))
    wiki = interlink_re.sub(interlink_repl, wiki)

    ext_re = re.compile('\[(http(?:s)?:[^ \]]*)( [^\]]*)?]')

    def ext_repl(mo):
        if mo.group(2):
            return '[{}]({})'.format(mo.group(2).strip(), mo.group(1))
        else:
            return '[{}]({})'.format(mo.group(1), mo.group(1))
    wiki = ext_re.sub(ext_repl, wiki)

    http_re = re.compile('(?<![\[(])(http(s)?:[^ ]*)')
    wiki = http_re.sub(r'[\0](\0)', wiki)

    return wiki


def lists(wiki):
    list_re = re.compile('^#+', re.M)

    def list_repl(mo):
        return ' ' + ' ' * (len(mo.group(0)) - 1) + '1.'
    return list_re.sub(list_repl, wiki)


def headers(wiki):
    header_re = re.compile('^(=+)(.*)(=+)$', re.M)

    def header_repl(mo):
        depth = max(len(mo.group(1)), len(mo.group(3)))
        return '#' * depth + ' ' + mo.group(2) + '\n'
    return header_re.sub(header_repl, wiki)


def notoc(wiki):
    notoc_re = re.compile('__NOTOC__')
    return notoc_re.sub('', wiki)

def slugify(title):
    slug_re = re.compile(r'[^a-zA-Z0-9]')
    return slug_re.sub('-', title.lower())[:30]


def process(filename):
    title = os.path.basename(filename)[:-4].replace('_', ' ')
    with open(filename) as f:
        wiki = f.read()
        wiki, metadata = get_metadata(wiki)
        metadata['title'] = title
        wiki = images(wiki)
        wiki = links(wiki)
        wiki = lists(wiki)
        wiki = headers(wiki)
        wiki = notoc(wiki)
        dest_filename = slugify(title) + '.md'
        with open('_recipes/' + dest_filename, 'w') as d:
            print >>d, '---'
            print >>d, yaml.dump(metadata)
            print >>d, '---'
            print >>d, wiki

def main():
    for f in sys.argv[1:]:
        process(f)

if __name__ == "__main__":
    main()
