1. All the security related and private info should be exported and kept into an .env file, normally located in the manage.py dir
2. No spaces inside .env file
3. From os.environ.get('SECRET_KEY', None)
4. .ENV files should be different for production, development, etc...
5. can use pip install django-environ, then
import environ
env = environ.Env()
env.read_env(env_file='.env')
SECRET_KEY = env('SECRET_KEY)
6. 