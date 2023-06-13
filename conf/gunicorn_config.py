import multiprocessing

# Gunicorn config variables
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2

# Django specific settings
pythonpath = 'D:/Documents/SOFTWARE PROJECTS/LeetCode Friends'
module = 'website:application'

# PostgreSQL database settings
database_host = 'db.xsqouwxwkxlryycnvoac.supabase.co'
database_port = '5432'
database_name = 'postgres'
database_user = 'postgres'
database_password = 'lWAlQIjqUfLL1osB'

# Construct the PostgreSQL connection string
database_url = f'postgresql://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}'

# Environment variables for Django and PostgreSQL
raw_env = [
    f'DJANGO_SETTINGS_MODULE=your_django_project.settings',
    f'DATABASE_URL={database_url}'
]