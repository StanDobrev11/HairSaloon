1. Prepare for deployment -> have .env file and requirements.txt
2. Install gunicor
3. Package application in docker image -> 'docker build -t image_name .'
3.0 Configure docker-compose WEB part
3.1 Check if running normally
4. Push docker image to Docker Hub
5. Pull image to server
6. start application on the server