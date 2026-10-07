#!/usr/bin/env python3
"""
Converte um projeto em Markdown simples para .docx, sem dependências externas.

Uso:
    python3 gerar_docx.py projeto.md projeto.docx

Suporta: # / ## / ### títulos, parágrafos, listas (- * + e 1.),
**negrito**, *itálico*, tabelas Markdown simples e linha horizontal (---)
como quebra de página.
"""

import re
import sys
import zipfile
from xml.sax.saxutils import escape

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
</Types>"""

ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>"""

STYLES = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{W_NS}">
<w:docDefaults>
<w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri" w:eastAsia="Calibri"/><w:sz w:val="22"/><w:szCs w:val="22"/><w:lang w:val="pt-BR"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:pPrDefault>
</w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/><w:jc w:val="left"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:color w:val="1F4E3D"/><w:sz w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:keepNext/><w:spacing w:before="200" w:after="80"/><w:jc w:val="left"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:color w:val="2E6B4F"/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="60"/><w:ind w:left="720"/></w:pPr></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders>
<w:top w:val="single" w:sz="4" w:space="0" w:color="808080"/><w:left w:val="single" w:sz="4" w:space="0" w:color="808080"/>
<w:bottom w:val="single" w:sz="4" w:space="0" w:color="808080"/><w:right w:val="single" w:sz="4" w:space="0" w:color="808080"/>
<w:insideH w:val="single" w:sz="4" w:space="0" w:color="808080"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="808080"/>
</w:tblBorders><w:tblCellMar><w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>
</w:styles>"""

NUMBERING = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="{W_NS}">
<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
</w:numbering>"""


def runs(texto: str) -> str:
    """Converte **negrito** e *itálico* em runs do Word."""
    partes = re.split(r"(\*\*.+?\*\*|__.+?__|(?<!\w)\*[^*\s][^*]*?\*(?!\w))", texto)
    xml = []
    for p in partes:
        if not p:
            continue
        rpr = ""
        if (p.startswith("**") and p.endswith("**")) or (p.startswith("__") and p.endswith("__")):
            p, rpr = p[2:-2], "<w:rPr><w:b/></w:rPr>"
        elif p.startswith("*") and p.endswith("*") and len(p) > 2:
            p, rpr = p[1:-1], "<w:rPr><w:i/></w:rPr>"
        xml.append(f'<w:r>{rpr}<w:t xml:space="preserve">{escape(p)}</w:t></w:r>')
    return "".join(xml)


def paragrafo(texto: str, estilo: str | None = None, num: tuple[int, int] | None = None) -> str:
    ppr = ""
    if estilo or num:
        ppr = "<w:pPr>"
        if estilo:
            ppr += f'<w:pStyle w:val="{estilo}"/>'
        if num:
            ppr += f'<w:numPr><w:ilvl w:val="{num[1]}"/><w:numId w:val="{num[0]}"/></w:numPr>'
        ppr += "</w:pPr>"
    return f"<w:p>{ppr}{runs(texto)}</w:p>"


def celulas(linha: str) -> list[str]:
    linha = linha.strip()
    if linha.startswith("|"):
        linha = linha[1:]
    if linha.endswith("|"):
        linha = linha[:-1]
    return [c.strip() for c in linha.split("|")]


def tabela(linhas: list[str]) -> str:
    dados = [celulas(l) for l in linhas if not re.match(r"^\s*\|?\s*:?-{3,}", l)]
    if not dados:
        return ""
    ncols = max(len(r) for r in dados)
    largura = 9000 // ncols
    grid = "".join(f'<w:gridCol w:w="{largura}"/>' for _ in range(ncols))
    xml = [f'<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="5000" w:type="pct"/></w:tblPr><w:tblGrid>{grid}</w:tblGrid>']
    for i, row in enumerate(dados):
        row = row + [""] * (ncols - len(row))
        xml.append("<w:tr>" + ("<w:trPr><w:tblHeader/></w:trPr>" if i == 0 else ""))
        for c in row:
            texto = f"**{c}**" if i == 0 and c and not c.startswith("**") else c
            shade = '<w:shd w:val="clear" w:color="auto" w:fill="D9EAD3"/>' if i == 0 else ""
            xml.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{largura}" w:type="dxa"/>{shade}</w:tcPr>'
                f'<w:p><w:pPr><w:spacing w:after="0"/><w:jc w:val="left"/></w:pPr>{runs(texto)}</w:p></w:tc>'
            )
        xml.append("</w:tr>")
    xml.append("</w:tbl><w:p/>")
    return "".join(xml)


def converter(md: str) -> str:
    corpo: list[str] = []
    linhas = md.splitlines()
    i = 0
    paragrafo_buf: list[str] = []

    def flush():
        if paragrafo_buf:
            corpo.append(paragrafo(" ".join(s.strip() for s in paragrafo_buf)))
            paragrafo_buf.clear()

    while i < len(linhas):
        linha = linhas[i]
        s = linha.strip()

        if not s:
            flush()
            i += 1
            continue

        if s.startswith("|"):
            flush()
            bloco = []
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                bloco.append(linhas[i])
                i += 1
            corpo.append(tabela(bloco))
            continue

        m = re.match(r"^(#{1,6})\s+(.+)$", s)
        if m:
            flush()
            nivel = len(m.group(1))
            estilo = {1: "Title", 2: "Heading1", 3: "Heading2"}.get(nivel, "Heading2")
            corpo.append(paragrafo(m.group(2), estilo))
            i += 1
            continue

        if re.match(r"^(-{3,}|\*{3,})$", s):
            flush()
            corpo.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
            i += 1
            continue

        # Listas têm um nível só: sublistas viram itens do mesmo nível (simples e compatível)
        m = re.match(r"^[-*+]\s+(.+)$", s)
        if m:
            flush()
            corpo.append(paragrafo(m.group(1), "ListParagraph", (1, 0)))
            i += 1
            continue

        # Listas numeradas: o número vai no próprio texto, assim aparece igual em qualquer leitor
        m = re.match(r"^(\d+[.)])\s+(.+)$", s)
        if m:
            flush()
            corpo.append(
                '<w:p><w:pPr><w:pStyle w:val="ListParagraph"/><w:ind w:left="720" w:hanging="360"/></w:pPr>'
                f'<w:r><w:t>{m.group(1)}</w:t><w:tab/></w:r>{runs(m.group(2))}</w:p>'
            )
            i += 1
            continue

        paragrafo_buf.append(s)
        i += 1

    flush()
    sect = '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1417" w:right="1134" w:bottom="1134" w:left="1701" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>'
    doc = (
        f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        f'<w:document xmlns:w="{W_NS}"><w:body>{"".join(corpo)}{sect}</w:body></w:document>'
    )
    return doc


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    origem, destino = sys.argv[1], sys.argv[2]
    with open(origem, encoding="utf-8") as f:
        doc = converter(f.read())

    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/numbering.xml", NUMBERING)
        z.writestr("word/document.xml", doc)

    print(f"Gerado: {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
