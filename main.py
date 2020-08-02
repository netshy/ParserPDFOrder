import os
import shutil
import sys
import time
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFSyntaxError

BASE_DIR = os.path.dirname(__file__)
LOAD_DIR = os.path.join(BASE_DIR, "load")
RESULT_DIR = os.path.join(BASE_DIR, "result")
TRASH_DIR = os.path.join(BASE_DIR, "trash")


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,
                                  caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    return text


def take_order_number(pdf_text):
    for number in pdf_text.splitlines():
        if number.startswith('ПЛАТЕЖНОЕ'):
            return number


def validate_file():
    file_name = take_name_file()
    if file_name is not None:
        pdf_text = convert_pdf_to_txt(LOAD_DIR + '/' + file_name)
        result = take_order_number(pdf_text)
        if result is not None:
            if result.startswith('ПЛАТЕЖНОЕ'):
                return True
        shutil.move(LOAD_DIR + '/' + file_name, TRASH_DIR + '/' + file_name)
        print(f'{time.asctime()}: Файл "{file_name}" не имеет номера платежного поручения. '
              f'Файл перенесен в папку trash.')


def take_name_file():
    file_name = os.listdir("load")
    for item in file_name:
        return item


def make_folders():
    if not os.path.isdir("load"):
        os.mkdir("load")
    if not os.path.isdir("result"):
        os.mkdir("result")
    if not os.path.isdir("trash"):
        os.mkdir("trash")


def main():
    make_folders()
    while True:
        file_name = take_name_file()
        try:
            if validate_file() is True:
                pdf_text = convert_pdf_to_txt(LOAD_DIR + '/' + file_name)
                result = take_order_number(pdf_text)
                old_file = os.path.join(LOAD_DIR, file_name)
                new_file = os.path.join(RESULT_DIR, result + '.pdf')
                os.rename(old_file, new_file)
                print(f'{time.asctime()}: "{file_name}" переименован')
            if not take_name_file():
                return print(f'{time.asctime()}: В папке нет файлов. '
                             f'\nЗагрузи в папку load платежные поручения в формате PDF.')

        except KeyboardInterrupt:
            print('Прерывание с клавиатуры')
            sys.exit()
        except FileExistsError:
            return print(f'{time.asctime()}: Скрипт выключен.'
                         f' Ошибка уникальности названия "{file_name}".'
                         f'\nВозможно в папке result уже есть такой же файл.')
        except PDFSyntaxError:
            return print(f'{time.asctime()}: Скрипт выключен. Ошибка типа файла.'
                         f'Вы уверены, что у файла "{file_name}" верный тип?')
        except Exception as e:
            return print(f'{time.asctime()}: Скрипт выключен. Ошибка во время выполнения задания: {e}')


if __name__ == '__main__':
    main()
