
from django.shortcuts import render
from django.views.generic import FormView
from . import forms
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
import openpyxl 
import re

# Create your views here.
class ExcelStaffView(FormView):
    form_class = forms.ImportDataForm
    template_name = 'filemanagment/excel_import.html'

    def form_valid(self, form):
        form = forms.ImportDataForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            file_to_read = openpyxl.load_workbook(self.request.FILES['file_fields'], data_only=True)     
            sheet = file_to_read['Sheet1']      # Читаем файл и лист1 книги excel
            print(f'Total Rows = {sheet.max_row} and Total Columns = {sheet.max_column}')               # получить количество строк и колонок на листе
            #print('все окей', file_to_read.active)
            # поиск ячейки с названием 'Наименование продукции' и выборка данных из данной колонки с заголовком этой ячейки            
            for row in sheet.rows:
                tyresize_list = []
                tyremodel_list = []
                tyreparametrs_list = []                       
                for cell in row:
                    if cell.value == 'Наименование продукции':
                        for row in sheet.iter_rows(min_row=cell.row+1, max_row=sheet.max_row):   
                            ### проверка если строка пустая
                            if str(row[cell.column-1].value) is not str(row[cell.column-1].value):        
                                tyresize_list.append(' ')
                            #######
                            reg_list = [
                            #'\d{3}/\d{2}[A-Za-z]\d{2}(\(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2}| \(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2})', 
                            #'\d{2}(\.|\,)(\d{2}|\d{1})(R|-)\d{2}', 
                            #'(\d{3}|\d{2})/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2}[A-Za-z]|\d{2})',  # = '(\d{3}|\d{2})/\d{2}([A-Za-z]|-)\d{2}' +  '\d{3}/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2})',    
                            '(\d{3}/\d{2}[A-Za-z]\d{2}(\(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2}| \(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2}))|(\d{2}(\.|\,)(\d{2}|\d{1})(R|-)\d{2})|((\d{3}|\d{2})/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2}[A-Za-z]|\d{2}))', #3 в одном чтобы избежать повторений двойных в ячейке наподобие #АШ 480/80R42(18.4R42)
                            '\d{2}(\.|\,)\d{1}[A-Za-z](R|-)\d{2}',
                            '(\d{4}|\d{3})[A-Za-z]\d{3}([A-Za-z]|-)\d{3}',
                            '\d{2}[A-Za-z]\d{1}([A-Za-z]|-)\d{1}',
                            '\d{2}[A-Za-z]\d{1}(\.|\,)\d{2}([A-Za-z]|-)\d{1}',
                            '\d{2}(\.|\,)\d{1}/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2})',                       
                            ' \d{1}(\.|\,)\d{2}(([A-Za-z]|-)|[A-Za-z]-)\d{2} ',
                             ' \d{1}[A-Za-z]-\d{2} ',
                            '\d{3}[A-Za-z]\d{2}[A-Za-z]',
                            '\s\d{2}([A-Za-z]|-)\d{2}(\.|\,)\d{1}', 
                            '\d{2}[A-Za-z][A-Za-z]\d{2}', 
                            ]
                            for n in reg_list:
                                result = re.search(rf'(?i){n}', str(row[cell.column-1].value))
                                if result:
                                    tyresize_list.append(result.group(0))
                                    ### удаление среза с типоразмером и всем что написано перед типоразмером
                                    left_before_size_data_index = str(row[cell.column-1].value).index(result.group(0))
                                    if left_before_size_data_index > 0:
                                        str_left_data = str(row[cell.column-1].value)[0:left_before_size_data_index-1]
                                    row[cell.column-1].value = str(row[cell.column-1].value).replace(str_left_data, '')
                                    row[cell.column-1].value = str(row[cell.column-1].value).replace(result.group(0), '')



                        for row in sheet.iter_rows(min_row=cell.row+1, max_row=sheet.max_row):    
                            ### проверка если строка пустая
                            if str(row[cell.column-1].value) is not str(row[cell.column-1].value):        
                                tyremodel_list.append(' ')
                            ####### 
                            reg_list = ['BEL-\w+',
                            '(ФБел-\d{3}-\d{1})|(Бел-\d{3}-\d{1})|ФБел-\d{3}([A-Za-z]|[А-Яа-я])|(ФБел-\d{3})|(Бел-\d{2}(\.|\,)\d{2}(\.|\,)\d{2})|(Бел-\w+)|(Бел ПТ-\w+|ПТ-\w+)|(БелОШ\w+)',
                            #'БИ-\w+',
                            #'ВИ-\w+',
                            'И-\w+|ВИ-\w+|БИ-\w+',
                            '(Ф-\d{3}-\d{1})|(Ф-\d{2}[A-Za-z][A-Za-z]-\d{1})|(Ф-\d{2}\s[A-Za-z][A-Za-z]-\d{1})|(Ф-\d{2}-\d{1})|(Ф-\w+|КФ-\w+|ВФ-\w+)',
                            'ФД-\w+',
                            'ИД-\w+',
                            '(К|K)-\d{2}[А-Яа-я][А-Яа-я]',
                            '(В-\d{2}-\d{1})|(В-\w+|ИЯВ-\w+)',
                            'ФТ-\w+',
                            'Я-\w+',]   
                            for n in reg_list:
                                result = re.search(rf'(?i){n}', str(row[cell.column-1].value))
                                if result:
                                    #print(result.group(0))
                                    tyremodel_list.append(result.group(0))
                                    ### удаление среза с моделью
                                    row[cell.column-1].value = str(row[cell.column-1].value).replace(result.group(0), '')
                                    #print(str(row[cell.column-1].value))

                        for row in sheet.iter_rows(min_row=cell.row+1, max_row=sheet.max_row):     
                            reg_list = [
                                'ЗМШ',
                                'КГШ',
                                'Сер|сер|ср',
                                'СГ',
                                'Трп|Тр|Тпр',
                                'Масс',
                                'с/х|сх',
                                'Лег|лг|легк', 
                                'Груз|груз|гр',
                                'Л/гр|Л/г|л/г',
                                'бк|б/к',
                                'Погр',
                                'кам',
                                'LS-2|LS|L-2',  
                                'Type|Typ',
                                'S|H|C',
                                '((\d{3}|\d{2})([А-Яа-я]|[A-Za-z])\d{1}((\d{3}|\d{2})[A-Za-z]))|((\d{3}|\d{2})([А-Яа-я]|[A-Za-z])\d{1}((\d{3}|\d{2}))|((\d{3}|\d{2})([А-Яа-я]|[A-Za-z])\d{1})|(\d{3}|\d{2})([А-Яа-я]|[A-Za-z]))', 
                                'Газель',
                                '(ВАЗ)',
                                'Вездеход'
                                'У-\d{1}',
                                'ошип|а/к|с выт|п/ош',
                                '(ГК|ЕР)-\d{3}',
                                'РК-5-165',
                                '\(ак23.5\)|\(ол23.5\)|\(ГК-260\)|вен.260|\(РК-5А-145\)|\(о/л\)|о/л|\(кам.14.9\)|\(кам12,5\)|ЛК-35-16.5|\(ГК-165\)|\(вен.ТК\)|\(вен.161\)|вен.260|Подз|\(Подз\)|вен.|(о/л)|\(ЛК-35-16.5\)',
                                '(кам.14.9)|(кам12,5)|вен.ЛК-35-16.5|ГК-145|РК.5-165',
                                '(\d{2}|\d{1})+$',
                            ]                
                            list_of_parametrs = []
                            for n in reg_list:
                                result = re.search(rf'(?i){n}', str(row[cell.column-1].value))
                                if result:
                                    list_of_parametrs.append(result.group(0))   
                                    #print(result)
                                    ### удаление среза с моделью                                   
                                    row[cell.column-1].value = str(row[cell.column-1].value).replace(result.group(0), '')
                                pp = str(row[cell.column-1].value)
                                print(str(row[cell.column-1].value))    
                                    ### 
                            str_of_param = ' '.join(list_of_parametrs)
                            tyreparametrs_list.append(str_of_param)


                        #print(tyreparametrs_list)
                        #print(tyresize_list)
                        #print(tyremodel_list)                          

                            #result = str(row[cell.column-1].value).find('Cер')
                            #print(str(row[cell.column-1].value))
                            #print(result)

                            #result = re.search(r'(?i)(\W|^)[сер](\W|$)', str(row[cell.column-1].value))
                            #result = re.findall(r'(?i)(\W|^).+(сер)+.(\W|$)', str(row[cell.column-1].value))
                            #result = re.findall(rf'(?i){reg_list}', str(row[cell.column-1].value))

                            #result = re.findall(rf'(?i){n}', str(row[cell.column-1].value))
                            #result = re.findall(r'(?i)сер', str(row[cell.column-1].value))

                            

                                #result = re.findall(rf'(?i){n}', str(row[cell.column-1].value))
                                #print(list_of_parametrs)


                            #(?i)(\W|^)(туфта|проклятие|убирайся|бред|черт\sвозьми|зараза)(\W|$)
                            #if .rindex:
                            #    #print(result.group(0))
                            #    print(result)
                        print('YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')


            #for row in range(2, sheet.max_row + 1): # Цикл по строкам начиная со второй (в первой заголовки)
            #    data = []
            #    for col in range(1, 16): # Цикл по столбцам от 1 до 15 ( 16 не включая)
            #        value = sheet.cell(row, col).value # value содержит значение ячейки с координатами row col
            #        data.append(value)
            #    print(data, len(data))
            #    author = directories_models.Author.objects.update_or_create(author=data[3])
            #    serie = directories_models.Serie.objects.update_or_create(serie=data[4])
            #    genre = directories_models.Genre.objects.update_or_create(genre=data[5])
            #    editor = directories_models.Editor.objects.update_or_create(editor=data[6])
            #    books_models.Book.objects.update_or_create(book_name=data[0], 
            #    price=data[1], 
            #    currency_price=data[2], 
            #    author=directories_models.Author.objects.get(author=data[3]), 
            #    serie=directories_models.Serie.objects.get(serie=data[4]), 
            #    genre=directories_models.Genre.objects.get(genre=data[5]), 
            #    editor=directories_models.Editor.objects.get(editor=data[6]), 
            #    publishing_date=data[7], 
            #    pages=data[8], 
            #    binding=data[9], 
            #    format=data[10], 
            #    isbn=data[11], 
            #    weigh=data[12], 
            #    age_restrictions=data[13], 
            #    value_available=data[14],
            #    )
            #return HttpResponseRedirect(reverse_lazy('books:book_list'))

                        from openpyxl import Workbook
                        excel_file = Workbook()
                        excel_sheet = excel_file.create_sheet(title='Holidays 2019', index=0)
                        excel_sheet['A1'] = 'Типоразмер'
                        excel_sheet['B1'] = 'Модель'
                        excel_sheet['C1'] = 'Параметры'
                        for n in range(len(tyresize_list)): 
                            excel_sheet.cell(row=n+1, column=1).value = tyresize_list[n]
                        for n in range(len(tyremodel_list)): 
                            excel_sheet.cell(row=n+1, column=2).value = tyremodel_list[n]
                        for n in range(len(tyreparametrs_list)): 
                            excel_sheet.cell(row=n+1, column=3).value = tyreparametrs_list[n]    
                        for n in range(len(pp)): 
                            excel_sheet.cell(row=n+1, column=4).value = pp[n]                         

                        excel_file.save(filename="Tyres.xlsx")
        else:
            form = forms.ImportDataForm()
        return render(self.request, 'filemanagment/excel_import.html', {'form': form})

