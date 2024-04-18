settings.py must include following settings to user SMTP server MAILJET:

EMAIL_HOST = 'in-v3.mailjet.com'
EMAIL_PORT = 587

We need to create new API key -> HairSaloonAPI

in settings.py:

EMAIL_HOST_USER = 'api key'
EMAIL_HOST_PASSWORD = 'secret key'

It is best to use the key and secret as .env files. This is done by:

1. install django-environ
2. set-up django-environ to manage .env files in settings.py

    import environ
    
    env = environ.Env()
    environ.Env.read_env()
    
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD)

3. Create .env file in the manage.py directory and set the vars
4. Add .env to gitignore

5. EMAIL_USE_SSL = True

To test this, go to main url and use send_email() and for the recipient list create temp email 