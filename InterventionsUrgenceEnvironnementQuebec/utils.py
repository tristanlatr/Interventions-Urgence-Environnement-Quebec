import xlsxwriter
import tempfile
import re
import csv

def get_csv_file(items):
    with tempfile.NamedTemporaryFile(delete=False) as csv_file:
        headers = { key:key.title() for key in items[0].keys() }
        dict_writer = csv.DictWriter(csv_file, headers)
        dict_writer.writeheader()
        dict_writer.writerows(items)

        return csv_file

def get_xlsx_file(items, headers=None):
    """
    Argments:  
        - items: list of dict  
        - headers: dict like {'key':'Key nice title for Excel'}  

    Return excel file as tempfile.NamedTemporaryFile
    """
    with tempfile.NamedTemporaryFile(delete=False) as excel_file:
        with xlsxwriter.Workbook(excel_file.name) as workbook:
            if not headers:
                headers={ key:key.title() for key in items[0].keys() }
            worksheet = workbook.add_worksheet()
            worksheet.write_row(row=0, col=0, data=headers.values())
            header_keys = list(headers.keys())
            cell_format = workbook.add_format()
            for index, item in enumerate(items):
                row = map(lambda field_id: str(item.get(field_id, '')), header_keys)
                worksheet.write_row(row=index + 1, col=0, data=row)
                worksheet.set_row(row=index + 1, height=13, cell_format=cell_format)
            worksheet.autofilter(0, 0, len(items)-1, len(headers.keys())-1)
        return excel_file

def replace(text, conditions):
    """Multiple replacements helper method.  Stolen on the web"""
    rep = conditions
    rep = dict((re.escape(k), rep[k]) for k in rep)
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    return text
