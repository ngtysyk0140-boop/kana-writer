"""ひらがな・カタカナの書き順データを KanjiVG から取り出して data/kana_strokes.js を作る。
入力: ../kanji-reader/tools/src/kanjivg.xml（漢検アプリと共用）"""
import xml.etree.ElementTree as ET, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '..', 'kanji-reader', 'tools', 'src', 'kanjivg.xml')
OUT = os.path.join(HERE, '..', 'data')
os.makedirs(OUT, exist_ok=True)
root = ET.parse(SRC).getroot()
S = {}
for kj in root.iter('kanji'):
    kid = kj.get('id')
    if '-' in kid: continue
    cp = int(kid.split('_')[1], 16)
    if 0x3041 <= cp <= 0x30FF:
        S[chr(cp)] = [p.get('d') for p in kj.iter('path')]
with open(os.path.join(OUT, 'kana_strokes.js'), 'w', encoding='utf-8') as f:
    f.write('// ひらがな・カタカナの書き順: KanjiVG (Ulrich Apel, CC BY-SA 3.0) 109x109 座標\n')
    f.write('window.KANA_STROKES = ' + json.dumps(S, ensure_ascii=False, separators=(',', ':')) + ';\n')
print(len(S), 'kana', os.path.getsize(os.path.join(OUT, 'kana_strokes.js')), 'bytes')
