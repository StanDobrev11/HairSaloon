1. All the security related and private info should be exported and kept into an .env file, normally located in the manage.py dir
2. No spaces inside .env file
3. From os.environ.get('SECRET_KEY', None)