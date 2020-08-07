# *-* coding: utf-8 *-*
import csv
import collections
import tempfile
import traceback

from django.http import HttpResponse


def import_csv_data_to_model(file_obj, model, field_header_list):
    """
    导入csv数据到模型
    :param file_obj:　文件对象
    :param model:　模型
    :param field_header_list:　字段表头部列表
    :return:
    """
    error_msg_list = []
    model_list = []

    # 写入数据到临时文件
    temp_file = tempfile.NamedTemporaryFile()
    with open(temp_file.name, "a") as f:
        for item in file_obj.chunks():
            f.write(item.decode("utf-8"))
            f.flush()
    temp_file.seek(0)

    # csv数据同步到数据库
    with open(temp_file.name, "r") as f:
        #　TODO: 这种方式不好，数量大很影响性能，根据业务情况在做决定是否优化
        model.objects.filter().delete()

        row_num = 1
        for row in csv.DictReader(f):
            row_num += 1

            try:
                data = {}
                for field_header in field_header_list:
                    for field, header in field_header.items():
                        data[field] = row.get(header)
                model_list.append(model(**data))
            except Exception as e:
                error_msg_list.append(dict(
                    row_num=row_num,
                    error=e
                ))
                traceback.print_exc()
                # 只要有错误行就终止
                break
            finally:
                temp_file.close()

        if not error_msg_list:
            model.objects.bulk_create(model_list)
            return True, error_msg_list

        return False, error_msg_list


def gen_csv_data(queryset, field_header_list):
    """
    生成csv数据
    :param queryset: 查询集
    :param field_header_list:　字段表头部列表
    :return:
    """
    data_list = []
    for qs in queryset:
        data = {}
        for field_header in field_header_list:
            for field, header in field_header.items():
                data[header] = getattr(qs, field)

        data_list.append(data)

    return data_list


def csv_response(data_list, header_dict, filename):
    """
    响应csv
    :param data_list: 数据列表
    :param header_dict:　csv头
    :param filename:　文件名
    :return:
    """
    resp = HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)

    writer = csv.DictWriter(resp, fieldnames=header_dict.values(), dialect='excel')
    writer.writeheader()
    for data in data_list:
        writer.writerow({k: v for k, v in data.items()})
    return resp


def download_csv(field_header_list, queryset, filename='result.csv'):
    """
    下载csv数据
    :param field_header_list:　头部列表（按照在csv文件中展示的顺序传入）field_header_list = [('field': 'header'),...]
    :param data_list:　数据列表
    :param filename:　文件名字
    :return:
    """
    header_dict = collections.OrderedDict()
    for field_header in field_header_list:
        for field, header in field_header.items():
            header_dict[field] = header

    data_list = gen_csv_data(queryset, field_header_list)
    return csv_response(data_list, header_dict, filename)
