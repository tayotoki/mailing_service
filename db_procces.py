from django.db import connection

# Список стандартных таблиц Django, которые не нужно проверять
exclude_tables = [
    'auth_group',
    'auth_group_permissions',
    'auth_permission',
    'auth_user',
    'auth_user_groups',
    'auth_user_user_permissions',
    'django_admin_log',
    'django_content_type',
    'django_migrations',
    'django_session',
]

cursor = connection.cursor()
cursor.execute('SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s', ['public'])
tables_count = cursor.fetchone()

if tables_count[0] > 0:
    data_exists = False
    cursor.execute(
        'SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s', ['public']
    )
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        if table_name in exclude_tables:
            continue
        cursor.execute('SELECT COUNT(*) FROM {}'.format(table_name))
        count = cursor.fetchone()[0]
        if count > 0:
            data_exists = True
            break

    if data_exists:
        print('Data already exists. Skipping load_data step.')
    else:
        import subprocess

        subprocess.run(['poetry', 'run', 'python', 'manage.py', 'loaddata', 'data_dump.json'])
else:
    print('No tables found in the database. Skipping load_data step.')
