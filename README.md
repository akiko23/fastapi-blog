# FastAPI-blog
The sample backend API for blog that was developed using FastAPI.
## Installation
1. Clone the repository and go to the project folder
   ```
   git clone https://github.com/akiko23/fastapi-blog && cd fastapi-blog
   ```
2. Rename .env_dists and provide your own variables (optional)
   ```
   mv .envs/app.env_dist .envs/app.env
   mv .envs/db.env_dist .envs/db.env
   mv .envs/test.env_dist .envs/test.env
   ```
3. Start app in docker
   ```
   docker-compose up -d
   ```
4. Check it up in your browser: <a href="http://localhost:8000/docs">click</a>
