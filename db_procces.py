from django.db import connection

cursor = connection.cursor()
cursor.execute('SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s', ['public'])
tables_count = cursor.fetchone()

if tables_count[0] > 0:
    print('Data already exists. Skipping load_data step.')
else:
    import subprocess
    subprocess.run(['poetry', 'run', 'python', 'manage.py', 'loaddata', 'data_dump.json'])
