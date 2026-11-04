import re, zipfile, html, sys
def esc(t): return html.escape(t, quote=False)
def runs(t):
    out = ""
    for part in re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", t):
        if not part: continue
        if part.startswith("**"): out += f'<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{esc(part[2:-2])}</w:t></w:r>'
        elif part.startswith("`"): out += f'<w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="19"/></w:rPr><w:t xml:space="preserve">{esc(part[1:-1])}</w:t></w:r>'
        else: out += f'<w:r><w:t xml:space="preserve">{esc(part)}</w:t></w:r>'
    return out
def para(t, style=None, bullet=False):
    pp = f'<w:pStyle w:val="{style}"/>' if style else ""
    if bullet: t = "• " + t; pp += '<w:ind w:left="360" w:hanging="220"/>'
    return f"<w:p><w:pPr>{pp}</w:pPr>{runs(t)}</w:p>"
def table(rows):
    b = '<w:tcBorders>' + ''.join(f'<w:{s} w:val="single" w:sz="4" w:color="999999"/>' for s in ("top","left","bottom","right")) + '</w:tcBorders>'
    x = '<w:tbl><w:tblPr><w:tblW w:w="5000" w:type="pct"/></w:tblPr>'
    for i, r in enumerate(rows):
        x += "<w:tr>"
        for c in r:
            shade = '<w:shd w:val="clear" w:fill="E7EEF7"/>' if i == 0 else ""
            txt = runs(f"**{c}**" if i == 0 and not c.startswith("**") else c)
            x += f'<w:tc><w:tcPr>{b}{shade}</w:tcPr><w:p><w:pPr><w:spacing w:after="0"/></w:pPr>{txt}</w:p></w:tc>'
        x += "</w:tr>"
    return x + "</w:tbl><w:p/>"
def convert(md):
    body, tbl, code = "", [], False
    def flush():
        nonlocal body, tbl
        if tbl: body += table(tbl); tbl = []
    for l in md.split("\n"):
        if l.startswith("```"): flush(); code = not code; continue
        if code: body += f'<w:p><w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/></w:rPr><w:t xml:space="preserve">{esc(l)}</w:t></w:r></w:p>'; continue
        if l.startswith("|"):
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if not all(re.fullmatch(r":?-+:?", c) for c in cells): tbl.append(cells)
            continue
        flush()
        m = re.match(r"(#+) (.*)", l)
        if m: body += para(m.group(2), f"Heading{min(len(m.group(1)),3)}")
        elif re.match(r"\s*[-*] ", l): body += para(re.sub(r"^\s*[-*] ", "", l), bullet=True)
        elif re.match(r"\d+\. ", l): body += para(l, bullet=False)
        elif l.strip(): body += para(l)
    flush(); return body
def build(files, out):
    body = ""
    for i, f in enumerate(files):
        if i: body += '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
        body += convert(open(f, encoding="utf-8").read())
    doc = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>{body}<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080"/></w:sectPr></w:body></w:document>'
    sty = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="21"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="100"/></w:pPr></w:pPrDefault></w:docDefaults>' + "".join(f'<w:style w:type="paragraph" w:styleId="Heading{n}"><w:name w:val="heading {n}"/><w:pPr><w:keepNext/><w:spacing w:before="240" w:after="100"/></w:pPr><w:rPr><w:b/><w:color w:val="1F3864"/><w:sz w:val="{s}"/></w:rPr></w:style>' for n, s in ((1,36),(2,28),(3,24))) + '</w:styles>'
    ct = '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>'
    rels = '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
    drels = '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct); z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", doc); z.writestr("word/styles.xml", sty); z.writestr("word/_rels/document.xml.rels", drels)
build(["FINAL_TEST_REPORT.md","simulation/SIMULATION_REPORT.md","project_inspection.md","prerequisite_report.md","msa_validation_report.md","build_report.md","iqtree_report.md","treeqmc_report.md"], "TREE-QMC_Test_Report.docx")
