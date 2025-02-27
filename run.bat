cd backend 
docker-compose up -d 
cd ../frontend 
docker build -t frontend --build-arg NAME=frontend . 
docker run -d -p 5173:5173 --name URL_FE frontend
cd .. 
echo "access url shorten service at http://localhost:5173"
start http://localhost:5173