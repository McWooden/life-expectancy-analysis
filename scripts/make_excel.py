import csv
import zipfile
import io

def csv_to_xlsx(csv_path, xlsx_path):
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))
    
    # Generate sheet1.xml
    sheet_xml_lines = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
        '<sheetData>'
    ]
    
    col_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    
    for row_idx, row in enumerate(reader, start=1):
        sheet_xml_lines.append(f'<row r="{row_idx}">')
        for col_idx, val in enumerate(row):
            col_letter = col_letters[col_idx]
            cell_ref = f"{col_letter}{row_idx}"
            
            # Check if numeric (not header row)
            if row_idx > 1:
                try:
                    num_val = float(val)
                    if num_val.is_integer():
                        val_str = str(int(num_val))
                    else:
                        val_str = str(num_val)
                    sheet_xml_lines.append(f'<c r="{cell_ref}"><v>{val_str}</v></c>')
                    continue
                except ValueError:
                    pass
            
            # Escaping XML special chars
            val_escaped = (val.replace("&", "&amp;")
                              .replace("<", "&lt;")
                              .replace(">", "&gt;")
                              .replace('"', "&quot;")
                              .replace("'", "&apos;"))
            sheet_xml_lines.append(f'<c r="{cell_ref}" t="inlineStr"><is><t>{val_escaped}</t></is></c>')
        sheet_xml_lines.append('</row>')
        
    sheet_xml_lines.append('</sheetData>')
    sheet_xml_lines.append('</worksheet>')
    sheet1_xml = "\n".join(sheet_xml_lines)
    
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
        '  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n'
        '  <Default Extension="xml" ContentType="application/xml"/>\n'
        '  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>\n'
        '  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>\n'
        '  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>\n'
        '</Types>'
    )
    
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
        '  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>\n'
        '</Relationships>'
    )
    
    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">\n'
        '  <sheets>\n'
        '    <sheet name="LifeExpectancyData" sheetId="1" r:id="rId1"/>\n'
        '  </sheets>\n'
        '</workbook>'
    )
    
    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
        '  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>\n'
        '  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>\n'
        '</Relationships>'
    )
    
    styles_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">\n'
        '  <fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>\n'
        '  <fills count="1"><fill><patternFill patternType="none"/></fill></fills>\n'
        '  <borders count="1"><border><left/><right/><top/><bottom/></border></borders>\n'
        '  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>\n'
        '  <cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>\n'
        '</styleSheet>'
    )
    
    with zipfile.ZipFile(xlsx_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('_rels/.rels', rels)
        z.writestr('xl/workbook.xml', workbook_xml)
        z.writestr('xl/_rels/workbook.xml.rels', workbook_rels)
        z.writestr('xl/worksheets/sheet1.xml', sheet1_xml)
        z.writestr('xl/styles.xml', styles_xml)

csv_to_xlsx('/mnt/alterra/repo/life-expectancy-analysis/data/life_expectancy_data.csv', '/mnt/alterra/repo/life-expectancy-analysis/data/life_expectancy_data.xlsx')
print("Successfully generated /mnt/alterra/repo/life-expectancy-analysis/data/life_expectancy_data.xlsx")
