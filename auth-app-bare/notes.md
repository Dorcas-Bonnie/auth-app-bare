# DevOps Learning Notes - Auth App Project

## Phase 1: Git & GitHub ✅ DONE
- Extracted auth-app-bare.zip into WSL
- Configured Git with name and email
- Created GitHub repository (auth-app)
- Initialised Git in project folder
- Pushed frontend and backend code to GitHub
- Learned: git add, git commit, git push
- Learned: what a branch is and why you never work on main directly

## Phase 2: Run App Locally ✅ DONE
- Installed Python 3.12 using deadsnakes PPA
- Created virtual environment (.venv) using python3.12
- Activated virtual environment (source .venv/bin/activate)
- Installed all backend dependencies (pip install -r requirements.txt)
- Fixed bcrypt version conflict (pip install bcrypt==4.0.1)
- Created .env file from .env.example
- Generated a secure SECRET_KEY using python3 secrets module
- Started backend server (uvicorn main:app --reload --port 8000)
- Tested API on Swagger UI (localhost:8000/docs)
- Successfully registered a user (201 response)
- Successfully logged in and received JWT token (200 response)
- Started frontend (python3 -m http.server 3000)
- Saw full login page and dashboard at localhost:3000

## Phase 3: Docker ✅ MOSTLY DONE
- Learned what Docker is and why it exists
- Learned difference between image and container
- Learned what a Dockerfile is
- Wrote backend Dockerfile from scratch
- Learned what each Dockerfile instruction does:
  FROM        → base image to start from
  WORKDIR     → working directory inside container
  COPY        → copy files into container
  RUN         → execute command during build
  EXPOSE      → document which port app uses
  CMD         → command to run when container starts
- Built backend image (docker build -t auth-backend .)
- Fixed JSONArgsRecommended warning in CMD
- Ran backend container (docker run -d -p 8000:8000 --name backend auth-backend)
- Confirmed app works inside container at localhost:8000/docs
- Successfully registered and logged in through container
- Learned docker ps, docker stop, docker rm, docker images
- TODO: Write frontend Dockerfile ← NEXT STEP

## Key Concepts Learned

### Docker
- Image = blueprint (recipe). Built from Dockerfile. Not running.
- Container = running instance of an image (meal cooked from recipe)
- Dockerfile = instructions for building an image
- docker build -t name . → builds image from Dockerfile in current folder
- docker run -d -p 8000:8000 --name backend auth-backend → runs container
- docker ps → shows running containers
- docker stop name → stops container
- docker rm name → removes container
- docker images → shows all images

### Port mapping
- -p 8000:8000 means your machine port 8000 maps to container port 8000
- Left side = your machine
- Right side = inside container
- Without this your browser cannot reach the app

### Virtual environment
- Isolates Python libraries for one project
- python3.12 -m venv .venv → creates it
- source .venv/bin/activate → activates it
- (.venv) in prompt confirms it is active
- Not needed once app is in Docker

### .env files
- Never commit to GitHub
- Contains real secrets like SECRET_KEY
- .env.example is the safe template that goes on GitHub
- Docker reads them as environment variables at runtime

### Error codes
- 200 → success
- 201 → created successfully
- 401 → not authenticated
- 403 → forbidden
- 404 → not found
- 422 → wrong data format sent
- 500 → something crashed on the backend, check terminal logs

### Reading error messages
- Always read bottom to top
- First line tells you error TYPE (AttributeError, TypeError etc)
- File and line number tells you WHERE it broke
- Message after colon tells you WHY it broke

### Ports
- 8000 → FastAPI/Django convention
- 3000 → Frontend dev server convention
- 5432 → PostgreSQL always
- 3306 → MySQL always
- 80   → HTTP
- 443  → HTTPS

## Tools Installed
- WSL / Ubuntu
- Python 3.12
- Git
- Docker Desktop
- VS Code

## Current Project Structure
auth-app-bare/
├── backend/
│   ├── main.py          API routes (register, login, /me, /health)
│   ├── auth.py          JWT token creation and password hashing
│   ├── database.py      SQLite database setup
│   ├── models.py        Pydantic request/response models
│   ├── test_main.py     Automated tests
│   ├── requirements.txt Python libraries needed
│   ├── Dockerfile       ✅ Written - containerises the backend
│   ├── .env.example     Safe template for secrets
│   └── .env             Real secrets - never on GitHub
├── frontend/
│   ├── index.html       Login and register page
│   ├── dashboard.html   Protected page after login
│   ├── style.css        All styling
│   └── app.js           Talks to backend API
└── notes.md             This file

## Next Steps
Phase 3 remaining:
- Write frontend Dockerfile
- Build frontend image
- Run frontend container
- Confirm login page works from container

Phase 4 - Docker Compose:
- Write docker-compose.yml
- Connect frontend and backend containers
- Add environment variables
- Run everything with one command
- Add Docker volumes for database persistence

Phase 5 - GitHub Actions:
- Create .github/workflows/ci.yml
- Run tests automatically on every push
- Build Docker images in pipeline
- Add GitHub Secrets

Phase 6 - DevSecOps:
- Add Gitleaks (secret scanning)
- Add Trivy (container vulnerability scanning)
- Add Bandit (Python code security)
- Build security gates into pipeline

Phase 7 - Deploy to AWS:
- Set up EC2 instance
- Deploy containers to real server
- Add domain name
- Configure HTTPS
- Full dev, staging, prod setup

## Session: Phase 3 Complete - Docker
Date: Monday 7 July

### What I did today:
- Wrote frontend Dockerfile from scratch
- Learned what nginx is and why we use it
- Built frontend image (auth-frontend)
- Ran frontend container on port 3000
- Saw full login page served from Docker container
- Confirmed frontend image is 92MB vs backend 456MB
- Understood why frontend cannot reach backend yet

### Frontend Dockerfile explained:
FROM nginx:alpine
  → use nginx web server, alpine = tiny version

COPY . /usr/share/nginx/html
  → copy all frontend files into the folder
    nginx serves files from

EXPOSE 80
  → nginx listens on port 80 inside container

CMD ["nginx", "-g", "daemon off;"]
  → start nginx in foreground
  → daemon off keeps it running inside container

### Key concepts learned:

nginx
  - web server that serves static files
  - used by 400 million+ websites
  - perfect for HTML, CSS, JS files
  - handles SSL termination in production
  - sits in front of your app in production

alpine
  - minimal Linux distribution
  - designed to be as small as possible
  - nginx:alpine = only 92MB
  - python:3.12-slim = 456MB (has Python + libraries)

Why frontend image is smaller than backend:
  - Frontend: nginx + 4 static files = 92MB
  - Backend: Python + FastAPI + JWT + bcrypt
             + all dependencies = 456MB

Why frontend cannot reach backend:
  - Each container runs on its own isolated network
  - They cannot see each other by default
  - Docker Compose puts them on the same network
  - Then they can communicate

### Commands learned today:
docker build -t auth-frontend .  
  → build frontend image from Dockerfile

docker run -d -p 3000:80 --name frontend auth-frontend
  → run frontend container
  → map machine port 3000 to container port 80
  → nginx inside container listens on 80

docker images
  → list all images on your machine

mv dockerfile Dockerfile
  → rename file (Linux is case sensitive)

cat > Dockerfile << 'EOF'
...content...
EOF
  → write content directly into a file from terminal

cat Dockerfile
  → print file contents to confirm it saved

### Important lesson:
Docker is case sensitive on Linux
  → Dockerfile with capital D
  → not dockerfile with lowercase d

### Port mapping for this project:
Frontend: -p 3000:80
  → your machine 3000 → container 80 (nginx default)
Backend:  -p 8000:8000
  → your machine 8000 → container 8000 (uvicorn)

### Phase 3 complete:
✅ Backend Dockerfile written
✅ Backend image built (auth-backend:latest, 456MB)
✅ Backend container tested, API works
✅ Frontend Dockerfile written
✅ Frontend image built (auth-frontend:latest, 92MB)
✅ Frontend container running, login page visible

### Next session - Phase 4: Docker Compose
- Write docker-compose.yml from scratch
- Connect frontend and backend on same network
- Add environment variables
- Add Docker volumes (database persistence)
- Run everything with: docker compose up --build
- Actually log in through the real UI
- One command starts everything

### Score on recap questions: 3.5/5
Still need to remember:
- nginx = web server that serves static files
- COPY . /usr/share/nginx/html = copies files 
  into folder nginx serves from
- docker build -t name .  (not docker -build)
- docker ps = shows running containers

## Session 4 - Phase 4: Docker Compose
Date: 

### What I did today:
- Created docker-compose.yml from scratch
- Learned YAML indentation rules
- Created .env file at project root
- Confirmed .env is in .gitignore
- Learned what each line in docker-compose.yml does

### docker-compose.yml explained:

services:
  → top level key, everything underneath is a service
  → a service = one container

backend:
  → name of the service
  → also the hostname inside Docker network
  → frontend reaches backend at http://backend:8000

build: ./backend
  → build image using Dockerfile in ./backend folder
  → Docker Compose handles the build automatically

ports: "8000:8000"
  → same as -p 8000:8000 in docker run
  → left side = your machine, right side = container

environment:
  → passes environment variables into container
  → ${SECRET_KEY} reads value from .env file automatically

healthcheck:
  → Docker checks http://localhost:8000/health every 10s
  → if it fails 3 times, container marked unhealthy
  → frontend waits for backend to be healthy before starting

depends_on: condition: service_healthy
  → frontend only starts after backend passes health check
  → prevents frontend starting before backend is ready

### .env file:
- Lives at project root
- Contains SECRET_KEY and other config values
- Never pushed to GitHub (.gitignore protects it)
- Docker Compose reads it automatically
- Different values on each server (dev, staging, prod)

### Why SECRET_KEY is in .env and not in code:
BAD  → hardcoded in main.py, visible to anyone
GOOD → in .env file, never on GitHub
       different value on each environment
       dev = simple string
       prod = long random string

### YAML rules learned:
- Indentation is everything in YAML
- Use spaces not tabs
- Everything under backend: must be indented
- Wrong indentation = broken file
- VS Code shows YAML errors with red underlines

### Commands learned:
docker compose up --build
  → build images and start all services

docker compose down
  → stop and remove all containers cleanly

docker compose up --build -d
  → run in background

docker compose logs -f
  → see logs from all containers

### Next session - Finish Phase 4:
- Run docker compose up --build
- Watch both containers start
- Open http://localhost:3000
- Actually log in through the real UI
- Frontend talking to backend through Docker network
- See full app working end to end

### Score on recap questions: 4/5
Port mapping still needs work:
-p 3000:80
  left side  = your machine port
  right side = inside container port
  different because nginx listens on 80 inside
  but we access it on 3000 outside