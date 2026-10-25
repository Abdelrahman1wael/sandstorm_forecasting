import docx
import zipfile

path = 'Documentation/final for Saudi Arabia and especially in Riyadh city.docx'
doc = docx.Document(path)
print('Total paragraphs:', len(doc.paragraphs))
print('Total tables:', len(doc.tables))
for i, t in enumerate(doc.tables):
    print(f'  Table {i+1}: rows={len(t.rows)}, cols={len(t.columns)}')

with zipfile.ZipFile(path) as z:
    media = [f for f in z.namelist() if f.startswith('word/media/')]
    print(f'Total embedded images: {len(media)}')
    for m in media:
        print('  ', m, z.getinfo(m).file_size, 'bytes')

full_text = ' '.join([p.text for p in doc.paragraphs]).lower()
for forbidden in ['china', 'beijing', 'hebei', 'gobi', 'cma', 'mongolian']:
    count = full_text.count(forbidden)
    print(f'Count of forbidden word "{forbidden}": {count}')
