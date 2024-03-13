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
url = "http://xa-dd3-shaysong/%E5%8E%8B%E6%B5%8B0311/ServerCommand/AddUser"
cookies = {
    "ForguncyUserService": "kg4IPeWFUiy8Z0oxEHPKuK2p8k89bvLvr6HczUOb1jHikEhLL3g2euYTyjlA5FfHxyLUw_jmr4-9hwmOCOAXlBiccE-5GBW44JB_-qIpKBxZvBPqphhcEE6K24L1gdcbgWgvyZVlWB951JUCo8eg87YliMN3OSofIP6ywDJibQ4pmIFOU8i1ADHukz_1mSk78_94FkfYsZHWLk1I9UVC0vBWSoeRrWnHUFi6wRmiONf0VoI8l8KWVXRlydEGk8n19dlTcnjlSRFUMWXBaSLkFM3tb7Io2de9_95O6l0NpY4tkUOz8JjIRofCrKo2OFhDF-u_etLg-yvO7dtmU7JNyEd45WkQOMPqqMKT5doRhCzbcF4OJpYv3gt6v14nh7tH5oIW2SKhpbKyBQGR7WipfPlb2CM_MB4OYjbABfPNXxBnWkH35nSM7K0mb4BEzODAQBj8hiURAsua6HhkCCrlHtIiyOUc438uyd81puODYcJD6uzjjiZW83lMi0073QSaC5xZviEer-WYOVNeteisHNih5vuWVnd1aUYceSqDnVtQ2dWQ0NaSmdHMzRLG82LSmdhnDmE8zMPlNlexEAbpsnUe_OkXgqb1KMbAyey57r4NWJD1nvJMkSF-NHV6O7AYww0J2q38Pe3esfJKEdIXh7Lnbzzhut_RlznL38iFuCioi_oc7dHfr8BMfH8ohBBBvJkT1WiaZYHUm3ApKoCAT7hNS8LqQwZf6tK2c_6osizdomBLRb3qX8wVdkQJ2kQtATONto_-m57TAu5oTViw1SiQ-qh4BpxbQE-6tVQFFMpid6NBWrEFgZTjXRrojZMlg-J_zVEt2gOLLcf2qDKqrkiZONklUxTS9De4wzMrg8LpgyY5PPk2feMh1W71beLkw9bjXFOdo4H0XbTy8MxrW8lCfeBOcwaqV3TESiVQ7Ro8n0Ap_0Vqanj2BrC4MtCkbVPWIyOKf-deBlWzBuPCPjhUDMQVYES-D7qCcuYMEOHm0IRf8nNwwEp5rw2NBJO0Us7AexQXM34MffrmyoGoder8Dc9S5SPybfmQ3vZA0f7U5CMxkdv262wHAounlm48fTt8cfmDRHiQHp2mcFDIf5VI7iJ6d-pGWth5Yii4lkEVBPQ9ku9Jw5kO22eKiN6cu7odF1O14EXC5rG8rQAMRhw-_RIARMf0o6yA49OMMMI3_onG6_KkvoMJ3O09fAeLe2ugnzJVs8Lc9wLRbGnkg209JDMmexkBzuv1VqxanuQNQRyDfWUnNBaaLVtn4XNi9bSu3jmmgVdu9T2LosG7DmYHgekXeaUyD3n2Jmo_RCU",
    "ForguncyServer": "MkxsVqPIKawOnyC8P6gWRXNVDG2Su5Poh9KUOULmu9lu5lMS7VJKlHXbpFUQgu0Fs18tw_QjpXu5IeOGbV7jVXJTBoR4D99Nr9wU0-6_EBPJEnwdOy10sZqaSh0YPVLatpfIoGP7JqdXNu7SkNbGdffF8b_7qLVG2UoskC-FVJZZc-h5sS5gNhSZI3epOxJg4oBkNGx08UtlN6iU3OfCAb0DUltwMUOcvzhrMaKslvY0JZZVh6TVTmJ0mumKByZJr6fK3evC0D1xRacuMMwEdmauoTJJcTUz_8pzPgf23rQs6Ggym24sWtFtM6i6JBAP8W7PNjvjX4Pdc410sgy8n507TosZ4L1qvE6GsKACFH2FmClNofkybiP3dVARUtXjOpv-t-3JNFdZ1UENOUtftCUvwyinWsQ1gWhrSl46LJhUvGyRVaMjrW8i6_9jx4H2"}


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
    generate_business_trip_table()
