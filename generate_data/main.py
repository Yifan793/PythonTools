from datetime import timedelta

import mysql.connector
from faker import Faker
import random
from faker.providers import person
import requests

fake = Faker("zh_CN")
fake.add_provider(person)
# 创建数据库连接
db_user = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="userservicedb_0311"
)
cursor_user = db_user.cursor()
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="formula"
)
cursor = db.cursor()
url = "http://xa-dd3-shaysong/test_0311_2/ServerCommand/AddUser"
cookies = {
    "ForguncyUserService": "TxumQYr9kL0cDRx7GaxJCffy3LD9pcTWKmF9DSO6NRZ--pQe2_E8t9MGaZ7adCcgwxIlR-OpRDm_I793_zABKOgcnHxe--tX3a4JQ6XkqVh1D8ugOhoL9DNMWJbbiIT7aFsm69p_wACym4YiabsIld0clVabUX1S6ag0V9ZMK-UDMjFNNNez8_Szt0DIrQbNEdy2gkxPboq52NhN7xyNMX-9b6oFpN4KpMEpweVJrzHFGNWfK3Iw4MTx69OudnxcKBikq1mOunQtA2c1nimepm081Z6XSL-Ch0NCP7lnLaoEfMxv_c3WSAtZaw2u2Ppyhz8uBbVp0-WzqsLNzJv0XEb0RaZEH08bd99KWN1gPH48ZQUFlDYwGbwBSP_hOiF62-ndCk1FPpOR9Lul-OhCKhZaKSubKgZE9AGsQ2AzaMxlOtWsWI_zAtwKmlxbt-iHWucI0HFmSkrow46hvTmlIt26PjjoSdic-BC-o9DQ6ZrYASRJPHb2c2roYeEQAogsQ-f6Aje_gr_n29A7Ctpb-ybJI905DTJ4LaUm7suWXgveG2UVmKCLrlpDdVSRbDZeuRR6Q0jBUwS7HbVqKhXvsapfXWD0QmIXnf9SubF6ggm11gqziUOMfFJHapdZnZ4g938XMDhcuPEvOhss8eOlKghvjXkg-X0fOFnGkE7IOv0uQImWRNJrPvTfN-pMeQOoj77zLzd3BadY-wHyp7T8bCUsvQu2DRgFcdM4ef0qlZJFk-F80zdoleP2PNDSGC4bEDd6l5bl2BawsjDd1kS4oKlPMBTc3BJgR-JFBEr3oMau3qbz7CvqiV-d-HQbXTFFx9HNMk0FXE3vcNZ1iHgCN9F8bhXRvHoHxvqCzdifGdALIvbPy6MvS924S9g-2G-RDqjfwhiiu2DWNfYzC1JFj53cm8Dp_gXo4rtKkb9MDPrvHhehg0tLdMPizG1uN0fHCkVk5e7wukikM4Iifh7WGa0s384Qo1Gpwq5asDfSbReh4LrK5H2Li4EC6ekKJJuT1pzRLKLUOsXfVBrZJLaEFuCNRcHQZo9cr4D1SGba61_NUmkFhTfCwg3uUPfr1mUanF0FumJ6aBgQ_C_0tWBraEaREnCl4Oa4RteScbJnDfm2vMgTDBhhktUgsuNbl0iSHabTgBkf70yaiWHdWKEFnjg9oDJ6oygo3kJ2SAqywQ7JEci3mq76tg4jBFDVz55bQRiNgveh-fPrINpsGFa4CT3ejaKxhJzk1oui7WoULvmficlaXvIFETparEcF6dVeI30ffSXZbFOOZkouhgyvUYj9wCZ5eVeS5uBJDdrqN9_C3zJZGD2nyisBc_-XQ5Xu",
    "ForguncyServer": "MkxsVqPIKawOnyC8P6gWRXNVDG2Su5Poh9KUOULmu9kgTXfNMNMHr_pR2UkMxzq8vabgsfXet6u24pBR2s9xN0ldEXlAOK8u1RT2irv3Ufy47U_ekea1t9GaXmthBEpWsQ9LSnJcdTEdd2q96Ctv7r2aozmUEFtjCiBaKB-4md4NdoFD0hAHEQFrn-jKzX5gC_eWRBjteL1TfbID6093KuANsID_j10pxKPwhe9h9klEPQcVXmNbKiuvFvf9z0nnQgTv28mZT-FOcFwGNmz6KcLEG0Ii4v-n6PVhwCt2K9ssY2XbyNVcUhDc9lq_dLJDk7GfnyGyAFP5exY_0S5O5SRqCwa-HdHVUVutaa4gv73xp7sVoYN1YJqxDoRM2jA1BbVWDznIsYDhaVZ4VV0SFmCnn-28dUeT2vtJph6ISCmUc1pMGeVDDZYuHyYpgOiw"}


def generate_specific_users():
    for i in range(2, 1001):
        username = "role2_user" + str(i)
        email = fake.email()

        requests.post(url, data={"用户名": username, "全名": username, "电子邮箱": email, "密码": "123456"},
                      cookies=cookies)


def generate_userprofile():
    insert_query = "INSERT INTO userprofile (UserId, UserName, FullName, Email, Picture, SignaturePad) VALUES (%s, %s, %s, %s, %s, %s)"
    used_usernames = set()

    for i in range(2, 50001):
        user_id = i

        username = fake.name()
        if username in used_usernames:
            suffix = 1
            while f"{username}({suffix})" in used_usernames:
                suffix += 1
            username = f"{username}({suffix})"
        used_usernames.add(username)

        full_name = f"{username}{user_id}"
        email = fake.email()
        picture_url = fake.image_url()

        requests.post(url, data={"用户名": username, "全名": full_name, "电子邮箱": email, "密码": "123456"},
                      cookies=cookies)
        # 执行插入操作
        # cursor_user.execute(insert_query, (user_id, username, full_name, email, picture_url, ""))

    # # 提交更改
    # db_user.commit()
    #
    # # 关闭连接
    # cursor_user.close()
    # db_user.close()


def generate_webpages_membership():
    insert_query = "INSERT INTO webpages_membership (UserId, CreateDate, ConfirmationToken, IsConfirmed, LastPasswordFailureDate, PasswordFailuresSinceLastSuccess," \
                   "Password, PasswordChangedDate, PasswordSalt, PasswordVerificationToken, PasswordVerificationTokenExpirationDate," \
                   "IsEnabled, IsMFAEnabled, MFASecret) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    for i in range(1, 50002):
        user_id = i
        cursor_user.execute(insert_query, (user_id, None, None, fake.boolean(), None, 0,
                                           "ADw+hMxj20IktDN+mIYyjxJT0EVBtfsspLf1kadWVDBMH6cy61MSBxOAeI4U+85CeA==",
                                           None, "", None, None, fake.boolean(), fake.boolean(), None))

    # 提交更改
    db_user.commit()

    # 关闭连接
    cursor_user.close()
    db_user.close()


def generate_webpages_roles():
    insert_query = "INSERT INTO webpages_roles (RoleId, RoleName, Permissions, Type, Description) VALUES (%s, %s, %s, %s, %s)"

    used_role_names = set()

    for i in range(2, 10000):
        role_id = i

        role_name = fake.job()
        if role_name in used_role_names:
            suffix = 1
            while f"{role_name}({suffix})" in used_role_names:
                suffix += 1
            role_name = f"{role_name}({suffix})"
        used_role_names.add(role_name)

        cursor_user.execute(insert_query, (role_id, role_name, "", 1, ""))

    # 提交更改
    db_user.commit()

    # 关闭连接
    cursor_user.close()
    db_user.close()


def generate_city_name():
    insert_query = "INSERT INTO 出差地点 (ID, 地点) VALUES (%s, %s)"

    city_names = set()

    for i in range(1, 51):
        city_id = i

        while True:
            city_name = fake.city_name()
            if city_name not in city_names:
                city_names.add(city_name)
                break

        cursor.execute(insert_query, (city_id, city_name))

    # 提交更改
    db.commit()

    # 关闭连接
    cursor.close()
    db.close()


def generate_business_trip_table():
    insert_query_出差信息表 = "INSERT INTO 出差信息表 (ID, 出差人, 出差人数, 部门, 出差类型, 出差地点, 分机号, 申请日期, 出差事由, 成本中心, 开始时间," \
                              "结束时间, 出差天数, 其他事项, 是否申请签证, 签证种类, 是否需要借款, 需要管理部预定, 流程实例ID, 状态," \
                              "FGC_Creator, FGC_CreateDate) VALUES (%s, %s, %s, %s, %s, %s," \
                              "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    insert_query_出差借款额度表 = "INSERT INTO 出差借款额度表 (ID, 出差ID, CNY, USD, JPY," \
                                  "FGC_Creator, FGC_CreateDate, FGC_LastModifier, FGC_LastModifyDate) VALUES (%s, %s)"
    insert_query_出差结算汇率表 = "INSERT INTO 出差结算汇率表 (ID, 出差ID, 美元汇率, 日元汇率," \
                                  "FGC_Creator, FGC_CreateDate, FGC_LastModifier, FGC_LastModifyDate) VALUES (%s, %s)"
    insert_query_出差行程表 = "INSERT INTO 出差行程表 (ID, 出差ID, 日期, 交通工具, 起点, 到达, 票价," \
                              "FGC_Creator, FGC_CreateDate, FGC_LastModifier, FGC_LastModifyDate) VALUES (%s, %s)"
    insert_query_出差费用借支表 = "INSERT INTO 出差费用借支表 (ID, 出差ID, 项目, CNY, USD, JPY, 出纳签字/日期," \
                                  "FGC_Creator, FGC_CreateDate, FGC_LastModifier, FGC_LastModifyDate) VALUES (%s, %s)"
    insert_query_出差预定表 = "INSERT INTO 出差预定表 (ID, 出差ID, 子项目ID, 日期, 起点, 终点, `费用（CNY）`, 图片, 说明, 是否付款," \
                              "FGC_Creator, FGC_CreateDate, FGC_LastModifier, FGC_LastModifyDate) VALUES (%s, %s)"
    insert_query_出差预算表 = "INSERT INTO 出差预算表 (ID, 出差ID, 子项目ID, 人次, 次数, CNY人均标准, CNY标准, CNY, USD人均标准, USD标准, USD," \
                              "JPY人均标准, JPY标准, JPY, 说明" \
                              "FGC_Creator, FGC_CreateDate, FGC_LastModifier, FGC_LastModifyDate) VALUES (%s, %s)"
    insert_query_票据报销清单表 = "INSERT INTO 票据报销清单表 (ID, 出差ID, 主项目ID, 日期, 地点或起点, 其它或终点, 事由或交通工具, CNY, USD, JPY, 票据数," \
                                  "备注," \
                                  "FGC_Creator, FGC_CreateDate, FGC_LastModifier, FGC_LastModifyDate) VALUES (%s, %s)"

    cursor_user.execute("SELECT UserName FROM userservicedb_0311.userprofile")
    usernames = [row[0] for row in cursor_user.fetchall()]
    cursor.execute("SELECT 出差类型 FROM 出差类型")
    business_trip_type = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT 地点 FROM 出差地点")
    business_trip_location = [row[0] for row in cursor.fetchall()]

    for i in range(100001, 1000001):
        people_number = fake.random_int(1, 7)
        user_name = fake.random_elements(elements=usernames, length=people_number, unique=True)
        department = fake.random_choices(elements=('人事部', '财务部', '部门1', '部门2'), length=1)[0]
        apply_for_visa = fake.boolean()
        visa_type = "身份证" if apply_for_visa else None
        borrow_money = fake.boolean()
        state = fake.random_choices(elements=('申请中', '办公室预定', '财务部预算', '经理审批', '总经理审批', '财务部借支',
                                              '票据报销', '财务部结算', '完成'), length=1)[0]
        # 生成申请日期
        application_date = fake.date_time()
        # 生成开始日期
        start_date = fake.date_time_between(start_date=application_date, end_date=application_date + timedelta(
                                          days=fake.random_int(1, 60)))
        # 生成结束日期
        end_date = fake.date_time_between(start_date=start_date, end_date=start_date + timedelta(
                                          days=fake.random_int(1, 30)))
        # 计算天数
        days_difference = (end_date - start_date).days
        cursor.execute(insert_query_出差信息表,
                       (i, ",".join(user_name), people_number,
                        department, fake.random_choices(elements=business_trip_type, length=1)[0],
                        fake.random_choices(elements=business_trip_location, length=1)[0], None, application_date, None,
                        department, start_date, end_date, days_difference, None, apply_for_visa, visa_type,
                        borrow_money, ",".join(fake.random_choices(elements=('机票', '酒店'))), None, state,
                        fake.random_choices(elements=user_name, length=1)[0], application_date))

    # 提交更改
    db.commit()

    # 关闭连接
    cursor.close()
    db.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    generate_specific_users()
