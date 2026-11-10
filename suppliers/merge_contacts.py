"""Добавляет компании с собранными контактами в Поставщики_Караганда_2GIS.xlsx.

Вход: CSV (разделитель «;», UTF-8) с колонками
  Название;Телефон;E-mail;WhatsApp;Рубрика;Адрес;Ссылка;Примечание[;Раздел]
Телефоны — в формате «+7 701 122 60 10», несколько через «; » (такое поле берётся в кавычки: "+7 701 ...; +7 777 ...").
Если «Раздел» пуст, он определяется по рубрике 2GIS (RULES ниже).

Что делает: пропускает дубли (по ссылке 2GIS), добавляет строки в лист раздела и в
«Все поставщики», сортирует по названию, пересчитывает «№» и «Сводку», копирует
оформление существующих строк, обновляет автофильтр. Сохраняет каждые N компаний.

Запуск:  python suppliers/merge_contacts.py контакты.csv [--every 50]
"""
import copy, csv, re, sys
from pathlib import Path
import openpyxl

XLSX = Path(__file__).with_name("Поставщики_Караганда_2GIS.xlsx")
ALL = "Все поставщики"
RULES = [  # (раздел, шаблон рубрики/категории)
    ("Строительные материалы", r"металлопрокат|пило|лесоматериал|цемент|стройматериал|строительн|лаки|краск|смес|фасад|бетон|раствор|кирпич|кровел|крепёж|крепеж|изоляц|гипсокартон|плитк"),
    ("Электрика и электротовары", r"светотехн|кабел|провод|электротех|электротовар|освещен"),
    ("Сантехника и отопление", r"сантехн|отоплен|водоснабж|канализац|насос|трубопровод|арматур"),
    ("Компьютеры и оргтехника", r"компьютер|оргтехн|картридж|ноутбук|принтер"),
    ("Канцелярские товары", r"канц|офисная бумага|полиграф|бумаг"),
    ("Мебель", r"мебел"),
    ("Хозяйственные товары", r"бытовая химия|хозтовар|хозяйствен|посуд|упаковк|моющ"),
    ("Продукты питания", r"продукт|питани|бакале|напитк|мясо|молоч"),
    ("Спецодежда и СИЗ", r"спецодежд|спецобув|сиз|средства защиты|униформ"),
    ("Инструменты и оборудование", r"инструмент|промышленного оборудования|оборудован"),
    ("Автозапчасти", r"автозапчаст|запчасти для|шины|диски|автохими|автотовар|аккумулятор"),
]
OTHER = "Другие поставщики"


def section_for(text: str) -> str:
    t = (text or "").lower()
    for name, rx in RULES:
        if re.search(rx, t):
            return name
    return OTHER


def sheet_of(wb, section):
    for ws in wb.worksheets:
        if re.sub(r"^\d+\.\s*", "", ws.title) == section:
            return ws
    raise KeyError(f"Нет листа раздела «{section}»")


def rows_of(ws):
    hdr = [c.value for c in ws[1]]
    return hdr, [list(r) for r in ws.iter_rows(min_row=2, values_only=True) if any(v not in (None, "") for v in r)]


SECTION_ORDER = [n for n, _ in RULES] + [OTHER]


def rewrite(ws, hdr, rows, name_col, by_section=False):
    """Перезаписывает данные листа с сортировкой и нумерацией, копируя стиль 2-й строки."""
    style = [copy.copy(c._style) for c in ws[2]] if ws.max_row >= 2 else None
    height = ws.row_dimensions[2].height
    sec = lambda r: SECTION_ORDER.index(r[1]) if by_section and r[1] in SECTION_ORDER else 0
    rows.sort(key=lambda r: (sec(r), str(r[name_col] or "").lower()))
    if ws.max_row > 1:
        ws.delete_rows(2, ws.max_row - 1)
    for i, r in enumerate(rows, 1):
        r[0] = i
        for j, v in enumerate(r, 1):
            c = ws.cell(row=i + 1, column=j, value=v)
            if style:
                c._style = copy.copy(style[j - 1])
        if height:
            ws.row_dimensions[i + 1].height = height
    if ws.auto_filter.ref:
        ws.auto_filter.ref = f"A1:{openpyxl.utils.get_column_letter(len(hdr))}{len(rows) + 1}"


def update_summary(wb):
    ws = wb["Сводка"]
    total = 0
    for r in range(2, ws.max_row + 1):
        title = ws.cell(r, 1).value
        if title == "ИТОГО":
            ws.cell(r, 2).value = total
            break
        if title and title in wb.sheetnames:
            n = len(rows_of(wb[title])[1])
            ws.cell(r, 2).value = n
            total += n


def main():
    src = Path(sys.argv[1])
    every = int(sys.argv[sys.argv.index("--every") + 1]) if "--every" in sys.argv else 50
    wb = openpyxl.load_workbook(XLSX)
    all_ws = wb[ALL]
    all_hdr, all_rows = rows_of(all_ws)
    link_col = all_hdr.index("Ссылка 2GIS")
    known = {str(r[link_col]).rstrip("/") for r in all_rows}
    pending: dict[str, list] = {}
    added = skipped = 0

    def flush():
        for sec, items in pending.items():
            ws = sheet_of(wb, sec)
            hdr, rows = rows_of(ws)
            rewrite(ws, hdr, rows + items, hdr.index("Название компании"))
        pending.clear()
        rewrite(all_ws, all_hdr, all_rows, all_hdr.index("Название компании"), by_section=True)
        update_summary(wb)
        wb.save(XLSX)

    with src.open(encoding="utf-8-sig", newline="") as f:
        for rec in csv.DictReader(f, delimiter=";"):
            link = (rec.get("Ссылка") or "").strip().rstrip("/")
            if not link or link in known or not (rec.get("Телефон") or "").strip():
                skipped += 1
                continue
            sec = (rec.get("Раздел") or "").strip() or section_for(f"{rec.get('Рубрика','')} {rec.get('Название','')}")
            vals = [None, rec["Название"].strip(), rec["Телефон"].strip(), (rec.get("Адрес") or "").strip(), link,
                    (rec.get("Рубрика") or "").strip(), (rec.get("E-mail") or "").strip() or None,
                    (rec.get("WhatsApp") or "").strip() or None, (rec.get("Примечание") or "").strip() or None]
            pending.setdefault(sec, []).append(vals)
            all_rows.append([None, sec] + vals[1:])
            known.add(link)
            added += 1
            if added % every == 0:
                flush()
                print(f"сохранено: {added}")
    flush()
    print(f"Добавлено: {added}, пропущено (дубли/без телефона): {skipped}. Файл: {XLSX}")


if __name__ == "__main__":
    main()
