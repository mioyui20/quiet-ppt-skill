"""Contract tests for non-destructive PPTX transition edits (no Office needed)."""
import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as ET

SCRIPT = Path(__file__).resolve().parents[1] / 'quiet-ppt/scripts/set_transitions.py'
spec = importlib.util.spec_from_file_location('quiet_ppt_transitions', SCRIPT)
motion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(motion)
P, MC, P159, P14, R = motion.P, motion.MC, motion.P159, motion.P14, motion.R


def fixture(path, first=('!!shared',), second=('!!shared',), reverse=False):
    def slide(names):
        shapes = ''.join(f'<p:sp><p:nvSpPr><p:cNvPr id="{i+2}" name="{name}"/></p:nvSpPr></p:sp>'
                         for i, name in enumerate(names))
        return (f'<p:sld xmlns:p="{P}"><p:cSld><p:spTree>{shapes}</p:spTree></p:cSld>'
                '<p:clrMapOvr/><p:transition><p:push dir="l"/></p:transition><p:timing/></p:sld>')
    order = ['r2', 'r1'] if reverse else ['r1', 'r2']
    pres = f'<p:presentation xmlns:p="{P}" xmlns:r="{R}"><p:sldIdLst>'
    pres += ''.join(f'<p:sldId id="{256+i}" r:id="{rid}"/>' for i, rid in enumerate(order))
    pres += '</p:sldIdLst></p:presentation>'
    rels = ('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="r1" Target="slides/slide1.xml"/>'
            '<Relationship Id="r2" Target="slides/slide2.xml"/></Relationships>')
    with ZipFile(path, 'w', ZIP_DEFLATED) as z:
        z.writestr('ppt/presentation.xml', pres)
        z.writestr('ppt/_rels/presentation.xml.rels', rels)
        z.writestr('ppt/slides/slide1.xml', slide(first))
        z.writestr('ppt/slides/slide2.xml', slide(second))
        z.writestr('ppt/notesSlides/notesSlide1.xml', b'<notes>preserve this</notes>')
        z.writestr('ppt/media/example.bin', b'\x00\xffuntouched image data')


class TransitionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name) / 'input.pptx'
        self.output = Path(self.temp.name) / 'output.pptx'
        fixture(self.source)

    def test_native_morph_fallback_duration_order_and_preserved_parts(self):
        original = self.source.read_bytes()
        motion.apply(self.source, self.output, {2}, 0.85)
        self.assertEqual(self.source.read_bytes(), original)
        with ZipFile(self.source) as before, ZipFile(self.output) as after:
            self.assertEqual(set(before.namelist()), set(after.namelist()))
            for name in before.namelist():
                if not name.startswith('ppt/slides/'):
                    self.assertEqual(before.read(name), after.read(name))
            d = ET.fromstring(after.read('ppt/slides/slide2.xml'))
            choice = d.find(f'{{{MC}}}AlternateContent/{{{MC}}}Choice')
            trans = choice.find(f'{{{P}}}transition')
            self.assertEqual(trans.get(f'{{{P14}}}dur'), '850')
            self.assertEqual(trans.get('advClick'), '1')
            self.assertIsNone(trans.get('advTm'))
            self.assertEqual(trans.find(f'{{{P159}}}morph').get('option'), 'byObject')
            self.assertIsNotNone(d.find(f'{{{MC}}}AlternateContent/{{{MC}}}Fallback/{{{P}}}transition/{{{P}}}fade'))
            self.assertLess(list(d).index(d.find(f'{{{MC}}}AlternateContent')), list(d).index(d.find(f'{{{P}}}timing')))
            first = ET.fromstring(after.read('ppt/slides/slide1.xml'))
            self.assertIsNotNone(first.find(f'{{{P}}}transition/{{{P}}}fade'))
            self.assertIsNone(d.find(f'{{{P}}}transition'))

    def test_slide_order_comes_from_presentation_relationships(self):
        fixture(self.source, reverse=True)
        motion.apply(self.source, self.output, {2}, 0.7)
        with ZipFile(self.output) as z:
            d = ET.fromstring(z.read('ppt/slides/slide1.xml'))
            self.assertIsNotNone(d.find(f'.//{{{P159}}}morph'))
            other = ET.fromstring(z.read('ppt/slides/slide2.xml'))
            self.assertIsNone(other.find(f'.//{{{P159}}}morph'))

    def test_same_path_and_existing_output_are_rejected_without_changes(self):
        original = self.source.read_bytes()
        with self.assertRaises(ValueError):motion.apply(self.source, self.source, {2}, 0.8)
        self.assertEqual(self.source.read_bytes(), original)
        self.output.write_bytes(b'keep existing output')
        with self.assertRaises(ValueError):motion.apply(self.source, self.output, {2}, 0.8)
        self.assertEqual(self.output.read_bytes(), b'keep existing output')

    def test_invalid_targets_do_not_create_output(self):
        for targets in [{0}, {1}, {3}]:
            with self.subTest(targets=targets), self.assertRaises(ValueError):
                motion.apply(self.source, self.output, targets, 0.8)
            self.assertFalse(self.output.exists())

    def test_missing_pair_and_duplicate_forced_names_are_rejected(self):
        for first, second in [(('!!one',), ('!!two',)), (('!!shared','!!shared'), ('!!shared',))]:
            fixture(self.source, first=first, second=second)
            with self.assertRaises(ValueError):motion.apply(self.source, self.output, {2}, 0.8)
            self.assertFalse(self.output.exists())

    def test_invalid_duration_does_not_create_output(self):
        for duration in [0, -1, 5.1, float('nan')]:
            with self.subTest(duration=duration), self.assertRaises(ValueError):
                motion.apply(self.source, self.output, {2}, duration)
            self.assertFalse(self.output.exists())

    def test_reapplying_to_a_copy_does_not_stack_transitions(self):
        motion.apply(self.source, self.output, {2}, 0.8)
        final = self.output.with_name('third.pptx')
        motion.apply(self.output, final, {2}, 1.0)
        with ZipFile(final) as z:
            d = ET.fromstring(z.read('ppt/slides/slide2.xml'))
            self.assertEqual(len(d.findall(f'{{{MC}}}AlternateContent')), 1)
            self.assertEqual(len(d.findall(f'.//{{{P159}}}morph')), 1)


if __name__ == '__main__':
    unittest.main()
