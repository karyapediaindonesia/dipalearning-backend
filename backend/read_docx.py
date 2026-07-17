import docx
import sys

def extract_text(filename):
    try:
        doc = docx.Document(filename)
        fullText = []
        for para in doc.paragraphs:
            if para.text.strip():
                fullText.append(para.text)
        return '\n'.join(fullText)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    text = extract_text(r'C:\dipalearning\SRS_Sistem_Informasi_Manajemen_DIPA_Learning_Center_v2.0.docx')
    with open(r'C:\dipalearning\SRS_text.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Extraction done.')