import os
import sys
import time
import shutil
from io import StringIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
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
        print(f'Файл {file_name} не имеет номера платежного поручения. Файл перенесен в папку trash.')


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
        try:
            if validate_file() is True:
                file_name = take_name_file()
                pdf_text = convert_pdf_to_txt(LOAD_DIR + '/' + file_name)
                result = take_order_number(pdf_text)
                old_file = os.path.join(LOAD_DIR, file_name)
                new_file = os.path.join(RESULT_DIR, result + '.pdf')
                os.rename(old_file, new_file)
            if not take_name_file():
                return print('В папке нет файлов. Загрузи в папку load платежные поручения в формате PDF.')

        except KeyboardInterrupt:
            print('Прерывание с клавиатуры')
            sys.exit()
        except PDFSyntaxError:
            return print('Ошибка типа файла. Вы уверены, что в папке верный тип файла?')
        except Exception as e:
            print(f'Ошибка во время выполнения задания: {e}')
            time.sleep(30)


if __name__ == '__main__':
    main()
