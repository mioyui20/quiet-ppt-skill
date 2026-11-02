"""Write native fade/Morph transitions to a new PPTX. Python standard library only."""
import argparse
from pathlib import Path
from zipfile import ZipFile
from xml.dom import minidom

P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
MC = 'http://schemas.openxmlformats.org/markup-compatibility/2006'
P14 = 'http://schemas.microsoft.com/office/powerpoint/2010/main'
P159 = 'http://schemas.microsoft.com/office/powerpoint/2015/09/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

def pairs(doc):
    names = [n.getAttribute('name') for n in doc.getElementsByTagNameNS(P, 'cNvPr')
             if n.getAttribute('name').startswith('!!')]
    if len(set(names)) != len(names):
        raise ValueError('Duplicate forced Morph object name on one slide')
    return set(names)

def transition(morph, duration):
    attrs = (f'xmlns:p="{P}" xmlns:p14="{P14}" xmlns:mc="{MC}" '
             f'mc:Ignorable="p14" spd="slow" p14:dur="{round(duration*1000)}" '
             'advClick="1"')
    if morph:
        xml = (f'<mc:AlternateContent xmlns:mc="{MC}">'
               f'<mc:Choice xmlns:p159="{P159}" Requires="p159">'
               f'<p:transition {attrs}><p159:morph option="byObject"/>'
               '</p:transition></mc:Choice><mc:Fallback>'
               f'<p:transition xmlns:p="{P}" spd="slow" advClick="1">'
               '<p:fade/></p:transition></mc:Fallback></mc:AlternateContent>')
    else:
        xml = f'<p:transition {attrs}><p:fade/></p:transition>'
    return minidom.parseString(xml).documentElement

def apply(source, target, morph_slides, duration):
    source, target = Path(source).resolve(), Path(target).resolve()
    if source == target or target.exists():
        raise ValueError('Output must be a new file, distinct from source')
    if not 0.1 <= duration <= 5:
        raise ValueError('Duration must be 0.1 to 5 seconds')
    with ZipFile(source) as archive:
        pres = minidom.parseString(archive.read('ppt/presentation.xml'))
        rels = minidom.parseString(archive.read('ppt/_rels/presentation.xml.rels'))
        lookup = {n.getAttribute('Id'): n.getAttribute('Target')
                  for n in rels.documentElement.childNodes if n.nodeType == n.ELEMENT_NODE}
        paths = []
        for n in pres.getElementsByTagNameNS(P, 'sldId'):
            path = lookup[n.getAttributeNS(R, 'id')]
            paths.append(path.lstrip('/') if path.startswith('/') else 'ppt/' + path)
        docs = {path: minidom.parseString(archive.read(path)) for path in paths}
        for number in morph_slides:
            if number < 2 or number > len(paths):
                raise ValueError(f'Invalid destination slide: {number}')
            if not (pairs(docs[paths[number-2]]) & pairs(docs[paths[number-1]])):
                raise ValueError(f'No forced Morph pair for slide {number}')
        for number, path in enumerate(paths, 1):
            doc = docs[path]
            root = doc.documentElement
            for node in list(root.childNodes):
                if node.nodeType != node.ELEMENT_NODE:
                    continue
                is_transition = node.namespaceURI == P and node.localName == 'transition'
                is_alternate = (node.namespaceURI == MC and node.localName == 'AlternateContent'
                                and node.getElementsByTagNameNS(P, 'transition'))
                if is_transition or is_alternate:
                    root.removeChild(node)
            before = next((n for n in root.childNodes if n.nodeType == n.ELEMENT_NODE
                           and n.namespaceURI == P and n.localName in ('timing', 'extLst')), None)
            node = doc.importNode(transition(number in morph_slides,
                                 duration if number in morph_slides else 0.3), True)
            root.insertBefore(node, before)
        with ZipFile(target, 'x') as output:
            for info in archive.infolist():
                data = docs[info.filename].toxml(encoding='utf-8') if info.filename in docs else archive.read(info)
                output.writestr(info, data)
    print(f'Saved {len(paths)} slides; Morph destinations: {sorted(morph_slides)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source')
    parser.add_argument('output')
    parser.add_argument('--morph-slides', type=int, nargs='*', default=[])
    parser.add_argument('--duration', type=float, default=0.85)
    args = parser.parse_args()
    apply(args.source, args.output, set(args.morph_slides), args.duration)
