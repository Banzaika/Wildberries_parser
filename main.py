import openpyxl
import sys, os
import requests
from parser import get_photos

excel_file_name = input("Введите название вашего Excel файла(вместе с раширением): ")
#loading excel file
wb = openpyxl.load_workbook(excel_file_name)
first_sheet = wb.sheetnames[0]
sheet1 = wb[first_sheet]

#collecting to url-artikul pairs
link_artikul = []
row_number = 1
while True:
    url = sheet1['A' + str(row_number)].value
    artikul = sheet1['B' + str(row_number)].value
    if url and artikul:
        link_artikul.append([url, artikul])
        row_number += 1
    else:
        if not url and not artikul:
            break
        else:
            print('Количество ссылок и артикулов отличаются, либо один из ячеек пуст.')
            input('Введите что-нибудь, чтобы выйти.')
            sys.exit()


def install_img(file_name, link):
    p = requests.get(link)
    with open(file_name, "wb") as out:
        out.write(p.content)


# change dir and work with dirs
current_abs_dir = os.getcwd()
previous_dir, current_dir = os.path.split(current_abs_dir)
os.chdir(previous_dir)
wildber = 'Wildberries'
os.mkdir(wildber)
os.chdir(wildber)
common_dir = os.getcwd()


def mk_and_chdir(dirname):
    os.mkdir(dirname)
    os.chdir(dirname)


def main():
    print("Скачивание фотографий...")
    for product in link_artikul:
        url, artikul = product
        photo_links = get_photos(url)
        mk_and_chdir(str(artikul))
        for index, photo_url in enumerate(photo_links):
            install_img(str(index + 1) + '.jpg', photo_url)
        os.chdir(common_dir)
    print('Скачивание успешно завершено')


if __name__=="__main__":
    main()
