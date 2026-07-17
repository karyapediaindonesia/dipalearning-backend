import sys
import zipfile
import xml.etree.ElementTree as ET

def extract_text_from_docx(docx_path):
    text = ""
    try:
        with zipfile.ZipFile(docx_path) as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.XML(xml_content)
            
            # The namespace for WordprocessingML
            WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
            PARA = WORD_NAMESPACE + 'p'
            TEXT = WORD_NAMESPACE + 't'
            
            for paragraph in tree.iter(PARA):
                texts = [node.text for node in paragraph.iter(TEXT) if node.text]
                if texts:
                    text += "".join(texts) + "\n"
    except Exception as e:
        print(f"Error: {e}")
    return text

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        out_path = path + ".txt"
        text = extract_text_from_docx(path)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Extraction complete. Output written to {out_path}")
