Container Hardening.

Look at any Dockerfile and immediately spot:
- Is it running as root? (security risk)
- Is it using a bloated base image? (attack surface)
- Is it missing a .dockerignore? (data leak risk)
- Is it missing health checks? (reliability risk)
- Are layers optimised? (size issue)
- Should this be distroless? (production hardening)


Scripts I'll write
deploy.sh          → automate deployment steps
setup.sh           → set up environment on a new server
healthcheck.sh     → check if all services are running
backup.sh          → backup the database
rollback.sh        → roll back to previous version

git checkout main
git pull origin main
git merge feature/github-actions
git push origin main