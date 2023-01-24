# import psycopg2

# conn = psycopg2.connect("""
#     host=rc1b-ljcqb8gimrseyebe.mdb.yandexcloud.net
#     port=6432
#     sslmode=verify-full
#     dbname=db1
#     user=Psy_user
#     password=WeWillWin2022
#     target_session_attrs=read-write
# """)

# q = conn.cursor()
# q.execute('SELECT version()')
# temp = q.fetchone()

# print(temp)

# conn.close()

# mkdir - -parents ~/.postgresql & & \
#     wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \
#     - -output-document ~/.postgresql/root.crt & & \
#     chmod 0600 ~/.postgresql/root.crt

import sqlite3

con = sqlite3.connect(
    "/Users/sunshine/Dev/_Leave2Live_Hackathon/Admin/Admin_part/db.sqlite3")
q = con.cursor()
patient = ['Maria', 'Maria', 'Мария', 'Иванова', '2000-10-20',
           'English', '@test', '+79991111111', 'test@example.com',
           'Relationships', '', '10', '', '', '', '']
# q.execute(
#     """INSERT INTO Web_admin_patient VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
#     ?, ?, ?, ?);""", patient)
q.execute("""
    INSERT INTO "Web_admin_user" ("last_login", "is_superuser", "is_staff",
     "is_active", "date_joined", "password", "username", "first_name", "last_name",
      "date_of_birth", "language", "telegram_nickname", "phone", "email")
       VALUES('None', 'False', 'False', 'True', '''2022-12-18 18:59:09.401307''',
        '''pbkdf2_sha256$260000$r87pIYVSOuioetlNUJg6Kv$QWLlsAQNgI+FrkWd+l+5DEbeo4bOSZEmL/rHuxqdt9c=''',
         '''Maria''', '''Мария''', '''Иванова''', '''2022-12-18''', '''RUS''', '''''', '''''',
          '''''')
""")
q.commit()
# temp = q.fetchone()
 
# print(temp)
# con.commit()
con.close()


# patient = ['password': 'Maria',
#            'username': 'Maria',
#            'first_name': 'Мария',
#            'last_name': 'Иванова',
#            'date_of_birth': '2000-10-20',
#            'language': 'English',
#            'telegram': '@test',
#            'telephone_number': '+79991111111',
#            'email': 'test@example.com',
#            'problem': 'Relationships',
#            'assigned_id': '',
#            'priority': '10',
#            'processed':'',
#            '',
#            '',
#            '',
           ]
