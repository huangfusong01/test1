import xlrd
from configs.settings import *
path_finance = r'C:\Users\cat\Desktop\finance.xlsx'
path_d = r'D:\PycharmProjects\test\config\test.xlsx'
path_service = r'C:\Users\cat\Desktop\service.xlsx'
path_operation = r'C:\Users\cat\Desktop\operation.xlsx'
path_customer = r'C:\Users\cat\Desktop\customer.xlsx'
path_customerB = r'C:\Users\cat\Desktop\test1.xls'
local_path1 = r'D:\PyProjects\test\config\test.xlsx'
local_path = TESTCASE_EXCLE_PATH

def read_excles():
    try:
        workbook = xlrd.open_workbook(local_path)
	
    except:
        print("文件路径有误")

    '''获取表格的所有sheet'''
    sheets_list = workbook.sheet_names()

    '''存放表格所有sheet返回的数据'''
    sheets_date = []
    # print(sheets_list)

    for sheet in sheets_list:

        sheet_table = workbook.sheet_by_name(sheet)  # 通过sheet索引获取工作表内容

        # print(table.row_values(1))
        '''获取工作表第一行内容作为key'''
        first_row = sheet_table.row_values(0)
        row_length = sheet_table.nrows

        # 定义两个列表，来存放循环表格row的内容
        all_rows = []
        rows_dic = []

        # 循环逐行打印
        for i in range(row_length):
            if i == 0:  # 跳过第一行，第一行是列名
                continue
            all_rows.append(sheet_table.row_values(i))
        # print(all_rows)

        for rows in all_rows:
            # print(rows)
            list = dict(zip(first_row, rows))
            # print(list)
            rows_dic.append(list)

        sheet_data = {"sheet": sheet_table.name, "data": rows_dic}
        sheets_date.append(sheet_data)

    # print(rows_dic)
    print(sheets_date)
    return sheets_date

    '''
    table1 = data.sheet_by_index(0)
    print(table1.row_values(1))
    table2=data.sheet_names()[1]
    print(table2)
    table3 = data.sheet_by_name("sheet1")
    print(table3.row(1))
    print(table3.row_values(1))
    print('table3名称：{}\table3行数：{}\table3列数：{}'.format(table3.name,table3.nrows,table3.ncols))

    '''


if __name__ == "__main__":
    read_excles()

