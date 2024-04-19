1. Prepare for deployment -> have .env file and requirements.txt
2. Install gunicor
3. Package application in docker image -> 'docker build -t image_name .'
3.0 Configure docker-compose WEB part
3.1 Check if running normally
3.2 Replace .env file in the docker-compose with the production .env file
3.3 Run with gunicorn, create new compose file for production with more workers
3.4 Static files -> must be run using nginx
3.5 CSRF_TRUSTED_ORIGINS must be set
4. Push docker image to Docker Hub
5. Pull image to server
6. start application on the server
