from datetime import timedelta
import mysql.connector
from faker import Faker
import requests

fake = Faker("zh_CN")

db = mysql.connector.connect(
    host="xa-dd3-forguncy1",
    user="shaysong",
    password="xA123456",
    database="test_0311_2"
)
cursor = db.cursor()


def generate_qianke_table():
    insert_query_qianke = "INSERT INTO 潜客表 (ID, 姓名, 公司, 职位, 手机, 电子邮箱, 潜客来源ID, 行业ID, 客户类型ID," \
                          "地址编号, 详细地址, 负责人, 跟进阶段, 感兴趣产品, 状态ID, FGC_Creator, FGC_CreateDate) " \
                          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    insert_query_qiankejilucaozuo = "INSERT INTO 潜客记录操作表 (ID, 潜客ID, 操作类型, FGC_Creator, " \
                                    "FGC_CreateDate) VALUES (%s, %s, %s, %s, %s)"

    cursor.execute("SELECT 编号, 全名 FROM test_0311_2.省市区表")
    results = cursor.fetchall()
    address_numbers = [result[0] for result in results]
    address_full_paths = [result[1] for result in results]

    for i in range(28, 1000001):
        random_number = fake.random_int(0, 4289)
        address_number = address_numbers[random_number]
        address_full_path = address_full_paths[random_number]
        people = fake.random_elements(elements=('市场人员1', '市场人员2', '市场人员3'), length=1)[0]
        principal = fake.random_elements(elements=(None, '销售人员1', '销售人员2', '销售人员3'), length=1)[0]
        products = fake.random_elements(elements=('1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                                                  '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                                                  '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                                                  '31', '32', '33', '34', '35', '36', '37', '38'), unique=True)

        time = fake.date_time()
        cursor.execute(insert_query_qianke,
                       (i, fake.name(), fake.company(), fake.job(), fake.phone_number(), fake.company_email(),
                        fake.random_int(1, 8), fake.random_int(1, 24), fake.random_int(1, 5), address_number,
                        address_full_path + fake.street_address(), principal, fake.random_int(1, 5),
                        ','.join(products), fake.random_int(1, 4), people, time))
        cursor.execute(insert_query_qiankejilucaozuo,
                       (18+i, i, "创建", people, time))

    # 提交更改
    db.commit()

    # 关闭连接
    cursor.close()
    db.close()


def generate_lianxiren_table():
    insert_query_kehu = "INSERT INTO 客户表 (ID, 名称, 电话, 行业ID, 员工数, 地址编号, 详细地址, 客户类型ID, FGC_Creator, " \
                        "FGC_CreateDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    insert_query_lianxiren = "INSERT INTO 联系人表 (ID, 姓名, 职位, 手机, 电子邮箱, 客户ID, FGC_Creator, FGC_CreateDate) " \
                             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    cursor.execute("SELECT 编号, 全名 FROM test_0311_2.省市区表")
    results = cursor.fetchall()
    address_numbers = [result[0] for result in results]
    address_full_paths = [result[1] for result in results]

    for i in range(17, 1000001):
        random_number = fake.random_int(0, 4289)
        address_number = address_numbers[random_number]
        address_full_path = address_full_paths[random_number]
        people = fake.random_elements(elements=('销售人员1', '销售人员2', '销售人员3'), length=1)[0]

        time = fake.date_time()
        cursor.execute(insert_query_kehu,
                       (i, fake.company(), fake.phone_number(), fake.random_int(1, 24), fake.random_int(50, 20000),
                        address_number, address_full_path + fake.street_address(), fake.random_int(1, 5), people, time))
        cursor.execute(insert_query_lianxiren,
                       (i-3, fake.name(), fake.job(), fake.phone_number(), fake.company_email(), i, people, time))

    # 提交更改
    db.commit()

    # 关闭连接
    cursor.close()
    db.close()



def update_kehu_table():
    update_query_kehu = "UPDATE 客户表 SET FGC_Creator = %s WHERE ID = %s"

    cursor.execute("SELECT ID FROM test_0311_2.客户表")
    results = cursor.fetchall()
    kehu_ids = [result[0] for result in results]

    for kehu_id in kehu_ids:
        user_name = "role2_user" + str(fake.random_int(1, 1000))
        print(str(kehu_id) + " " + user_name)
        cursor.execute(update_query_kehu, (user_name, kehu_id))

    # 提交更改
    db.commit()

    # 关闭连接
    cursor.close()
    db.close()


def update_lianxiren_table():
    update_query_lianxiren = "UPDATE 联系人表 SET FGC_Creator = %s WHERE ID = %s"

    cursor.execute("SELECT ID, 客户ID FROM test_0311_2.联系人表")
    results = cursor.fetchall()
    lianxiren_ids = [result[0] for result in results]
    kehu_ids = [result[1] for result in results]
    i = 0
    for lianxiren_id in lianxiren_ids:
        cursor.execute("SELECT FGC_Creator FROM test_0311_2.客户表 WHERE ID = %s", (kehu_ids[i],))
        user_name = cursor.fetchall()[0][0]
        print(str(lianxiren_id) + " " + user_name)
        cursor.execute(update_query_lianxiren, (user_name, lianxiren_id))
        i = i + 1

    # 提交更改
    db.commit()

    # 关闭连接
    cursor.close()
    db.close()


if __name__ == '__main__':
    update_lianxiren_table()
