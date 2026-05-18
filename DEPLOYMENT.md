# DEPLOYMENT.md - Railway Deployment Guide

## 🚀 Deploying to Railway

This guide walks you through deploying the full-stack application to Railway.

## Prerequisites

- Railway account (https://railway.app)
- Railway CLI installed: `npm i -g @railway/cli`
- GitHub repository with the project code
- GitHub Actions secrets configured

## Step 1: Set Up Railway Account

1. Go to https://railway.app and sign up
2. Click "New Project"
3. Select "Blank Project"

## Step 2: Create PostgreSQL Database

1. In your Railway project, click "New"
2. Select "Database" → "PostgreSQL"
3. Once created, go to the database settings
4. Find and copy the `DATABASE_URL` from the "Connect" tab

## Step 3: Deploy Backend Service

### Option A: Using Railway CLI (Recommended)

1. **Login to Railway CLI:**
   ```bash
   railway login
   ```

2. **Initialize Railway project in backend:**
   ```bash
   cd backend
   railway init
   ```

3. **Link to your Railway project:**
   ```bash
   railway link
   ```

4. **Set environment variables:**
   ```bash
   railway variable add DATABASE_URL="<your-database-url>"
   railway variable add FLASK_ENV=production
   ```

5. **Deploy:**
   ```bash
   railway up
   ```

6. **Get the deployment URL:**
   ```bash
   railway logs
   ```
   Look for the URL in the logs (e.g., `https://backend-production.railway.app`)

### Option B: Connect GitHub Repository

1. In Railway dashboard, click "New" → "GitHub Repo"
2. Select your repository
3. Choose the `backend` folder as the root directory
4. Railway will automatically detect `Dockerfile` and deploy

## Step 4: Deploy Frontend Service

1. In Railway, click "New" → "GitHub Repo"
2. Select your repository again
3. Choose the `frontend` folder as the root directory
4. Add environment variable:
   ```
   REACT_APP_API_URL=https://<backend-url>/api
   ```
   Replace `<backend-url>` with your actual backend URL from Step 3

5. Deploy - Railway will automatically detect `Dockerfile`

## Step 5: Configure GitHub Actions for Auto-Deployment

### Add Railway Token to GitHub Secrets

1. In Railway dashboard, go to Account Settings
2. Find "API Tokens" or "CLI Tokens"
3. Create a new token and copy it
4. Go to your GitHub repository → Settings → Secrets and variables → Actions
5. Add a new secret:
   - Name: `RAILWAY_TOKEN`
   - Value: Paste your Railway token

### Enable CD Workflow

The `.github/workflows/cd.yml` is already configured to:
- Run tests automatically (via CI)
- Deploy to Railway on successful push to main branch
- Deploy both backend and frontend services

## Step 6: Verify Deployment

### Check Backend

```bash
curl https://<backend-url>/health
```

Should return:
```json
{
  "status": "healthy"
}
```

### Check API Endpoints

```bash
# Get students
curl https://<backend-url>/api/data

# Add student
curl -X POST https://<backend-url>/api/data \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","course":"CS"}'
```

### Check Frontend

Open `https://<frontend-url>` in your browser

## Environment Variables Reference

### Backend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `FLASK_ENV` | Flask environment | `production` |
| `PORT` | Server port | `5000` |

### Frontend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API URL | `https://backend-url/api` |
| `PORT` | Server port | `3000` |

## Troubleshooting

### Application won't start

1. **Check logs:**
   ```bash
   railway logs
   ```

2. **Verify environment variables:**
   ```bash
   railway variable ls
   ```

3. **Rebuild deployment:**
   - Go to Railway dashboard
   - Find the service
   - Click "Deploy" → "Redeploy"

### Database connection error

1. Verify `DATABASE_URL` is correctly set
2. Check PostgreSQL database is running
3. Ensure network access is allowed

### Frontend not connecting to backend

1. Check `REACT_APP_API_URL` is set correctly
2. Verify backend service is running (check logs)
3. Check CORS is enabled in backend (should be by default)
4. Check browser console for exact error message

### Performance issues

1. Check container logs for errors
2. Monitor database queries
3. Consider upgrading Railway plan

## Monitoring

### View Logs

```bash
# All logs
railway logs

# Follow in real-time
railway logs --follow

# Specific service
railway logs --service backend
```

### Monitoring Dashboard

1. Go to Railway dashboard
2. Select your project
3. View metrics for each service:
   - CPU usage
   - Memory usage
   - Network I/O
   - Status

## Scaling

### Increase Resources

1. Go to service settings in Railway
2. Select instance type
3. Choose higher tier for more CPU/RAM

### Database Scaling

1. Go to PostgreSQL database settings
2. Select larger instance type
3. Railway handles migration automatically

## Continuous Deployment

The CD workflow in `.github/workflows/cd.yml` automatically:

1. Runs all tests (from CI workflow)
2. Builds Docker images
3. Deploys to Railway on push to `main` branch
4. Sends notifications

To trigger a deployment:
```bash
git push origin main
```

## Rollback

### Using Railway Dashboard

1. Go to your service
2. Click "Deployments"
3. Select previous deployment
4. Click "Redeploy"

### Using CLI

```bash
railway rollback
```

## Custom Domain

1. Go to service settings in Railway
2. Find "Domain" section
3. Add your custom domain
4. Update DNS records as instructed

## SSL/HTTPS

Railway automatically provides HTTPS for all deployments using Let's Encrypt.

## Cost Optimization

1. Use Railway's free tier for small projects
2. Monitor usage in Railway dashboard
3. Set up billing alerts
4. Consider using Railway's reserved instances for production

## Support

- Railway Documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub Issues: Create an issue in your repository

---

**Happy deploying!** 🎉
