from datetime import timedelta

import mysql.connector
import pyodbc
from faker import Faker

fake = Faker("zh_CN")

conn_sqlserver = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=test_inventory;UID=sa;PWD=xA123456')
cursor_sqlserver = conn_sqlserver.cursor()

conn_mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="test_0311_2"
)
cursor_mysql = conn_mysql.cursor()


def generate_supplier_customer_table():
    insert_query_inventory = "INSERT INTO supplier_customer (supplier_customer_name, contact_person, contact_phone_number, contact_person_position, address," \
                             " supplier_customer_type_id, FGC_Creator, FGC_CreateDate, FGC_LastModifier, FGC_LastModifyDate) " \
                             "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    cursor_mysql.execute("SELECT 全名 FROM test_0311_2.省市区表")
    results = cursor_mysql.fetchall()
    address_full_paths = [result[0] for result in results]

    for i in range(60, 1000001):
        random_number = fake.random_int(0, 4289)
        address_full_path = address_full_paths[random_number]
        people = \
            fake.random_elements(elements=('采购员1', '销售员1', '采购主管1', '销售主管1', '仓库主管1', '库存管理员1'),
                                 length=1)[0]

        time = fake.date_time()
        cursor_sqlserver.execute(insert_query_inventory,
                                 (fake.company(), fake.name(), fake.phone_number(), fake.job(),
                                  address_full_path + fake.street_address(),
                                  fake.random_int(2, 3), people, time, people, time))

    # 提交更改
    conn_sqlserver.commit()

    # 关闭连接
    cursor_mysql.close()
    conn_mysql.close()
    cursor_sqlserver.close()
    conn_sqlserver.close()


def generate_sales_order_table():
    insert_query_sales_order = "INSERT INTO sales_order (order_id, sales_date, customer_id, contact_person, contact_phone_number, delivery_date, project_id," \
                               "seller, sales_department, outstock_status, total_amount, audit_status, FGC_Creator, " \
                               "FGC_CreateDate, FGC_LastModifier, FGC_LastModifyDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    insert_query_sales_order_detail = "INSERT INTO sales_order_detail (sales_order_id, item_id, sales_volume, unit_price, FGC_Creator, FGC_CreateDate," \
                                      " FGC_LastModifier, FGC_LastModifyDate) " \
                                      "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

    cursor_sqlserver.execute("SELECT ID, contact_person, contact_phone_number FROM test_inventory.dbo.supplier_customer WHERE supplier_customer_type_id = 3")
    results = cursor_sqlserver.fetchall()
    customer_length = len(results)
    customer_ids = [result[0] for result in results]
    customer_persons = [result[1] for result in results]
    customer_phone_numbers = [result[2] for result in results]

    cursor_sqlserver.execute("SELECT ID, sales_price FROM test_inventory.dbo.item")
    results2 = cursor_sqlserver.fetchall()
    item_length = len(results2)
    item_ids = [result[0] for result in results2]
    item_sales_prices = [result[1] for result in results2]

    for i in range(79, 1000001):
        random_number = fake.random_int(0, customer_length - 1)
        customer_id = customer_ids[random_number]
        customer_person = customer_persons[random_number]
        customer_phone_number = customer_phone_numbers[random_number]

        people = fake.random_elements(elements=('销售员1', '销售主管1'), length=1)[0]

        sales_date = fake.date_time()
        # 生成开始日期
        delivery_date = fake.date_time_between(start_date=sales_date, end_date=sales_date + timedelta(
            days=fake.random_int(1, 20)))

        total_amount = 0
        for j in range(fake.random_int(1, 3)):
            random_number2 = fake.random_int(0, item_length - 1)
            item_id = item_ids[random_number2]
            item_sales_price = item_sales_prices[random_number2]
            item_number = fake.random_int(1, 20)
            cursor_sqlserver.execute(insert_query_sales_order_detail,
                                     (i, item_id, item_number, item_sales_price, people, sales_date, people,
                                      sales_date))
            total_amount += item_sales_price * item_number

        cursor_sqlserver.execute(insert_query_sales_order,
                                 ("XS-20240319-" + str(i), sales_date, customer_id, customer_person, customer_phone_number,
                                  delivery_date,
                                  fake.random_int(1, 16), people, "销售部", 8, total_amount, 1, people, sales_date,
                                  people, sales_date))

    # 提交更改
    conn_sqlserver.commit()

    # 关闭连接
    cursor_sqlserver.close()
    conn_sqlserver.close()


def update_sales_order_table():
    conn_update = pyodbc.connect('DRIVER={SQL Server};SERVER=xa-dd3-forguncy1;DATABASE=test_inventory;UID=sa;PWD=xA123456')
    cursor_update = conn_update.cursor()
    cursor_update.execute("SELECT ID, seller FROM test_inventory.dbo.sales_order")
    results = cursor_update.fetchall()
    sales_ids = [result[0] for result in results]
    seller_names = [result[1] for result in results]
    i: int = 0
    for sales_id in sales_ids:
        cursor_update.execute("UPDATE sales_order SET FGC_Creator = ? WHERE ID = ?;", (seller_names[i], sales_id))
        i = i + 1

    conn_update.commit()
    conn_update.close()

def generate_purchase_table():
    insert_query_purchase_order = "INSERT INTO purchase_order (purchase_order_id, purchase_date, supplier_customer_id, contact_person, telephone, pay_date, project_id," \
                                  "purchase_person, purchase_department, in_state, total_number, paid_number, ticket_number, " \
                                  "pay_address, approval_state, FGC_Creator, " \
                                  "FGC_CreateDate, FGC_LastModifier, FGC_LastModifyDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    insert_query_purchase_order_details = "INSERT INTO purchase_order_details (purchase_order_id, goods_id, purchase_count, price, FGC_Creator, FGC_CreateDate," \
                                      " FGC_LastModifier, FGC_LastModifyDate) " \
                                      "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

    cursor_sqlserver.execute("SELECT ID, contact_person, contact_phone_number FROM test_inventory.dbo.supplier_customer WHERE supplier_customer_type_id = 2")
    results = cursor_sqlserver.fetchall()
    purchase_length = len(results)
    purchase_ids = [result[0] for result in results]
    purchase_persons = [result[1] for result in results]
    purchase_phone_numbers = [result[2] for result in results]

    cursor_sqlserver.execute("SELECT ID, sales_price FROM test_inventory.dbo.item")
    results2 = cursor_sqlserver.fetchall()
    item_length = len(results2)
    item_ids = [result[0] for result in results2]
    item_sales_prices = [result[1] for result in results2]

    for i in range(73, 1000001):
        random_number = fake.random_int(0, purchase_length - 1)
        purchase_id = purchase_ids[random_number]
        purchase_person = purchase_persons[random_number]
        purchase_phone_number = purchase_phone_numbers[random_number]

        people = fake.random_elements(elements=('采购员1', '采购主管1'), length=1)[0]

        purchase_date = fake.date_time()
        # 生成开始日期
        pay_date = fake.date_time_between(start_date=purchase_date, end_date=purchase_date + timedelta(
            days=fake.random_int(1, 20)))

        total_number = 0
        for j in range(fake.random_int(1, 3)):
            random_number2 = fake.random_int(0, item_length - 1)
            item_id = item_ids[random_number2]
            item_sales_price = item_sales_prices[random_number2]
            item_number = fake.random_int(1, 20)
            cursor_sqlserver.execute(insert_query_purchase_order_details,
                                     (i, item_id, item_number, item_sales_price, people, purchase_date, people,
                                      purchase_date))
            total_number += item_sales_price * item_number
        paid_number = fake.random_int(0, total_number)

        cursor_sqlserver.execute(insert_query_purchase_order,
                                 ("CG-20240319-" + str(i), purchase_date, purchase_id, purchase_person, purchase_phone_number,
                                  pay_date,
                                  fake.random_int(1, 16), people, "采购部", 5, total_number, paid_number, paid_number, fake.address(), 1, people, purchase_date,
                                  people, purchase_date))

    # 提交更改
    conn_sqlserver.commit()

    # 关闭连接
    cursor_sqlserver.close()
    conn_sqlserver.close()


if __name__ == '__main__':
    update_sales_order_table()
