# Deploy to Vercel Guide

## Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FKenan3477%2FASIS&env=DATABASE_URL,NEXTAUTH_SECRET,NEXTAUTH_URL&envDescription=Environment%20variables%20needed%20for%20the%20Sales%20Form%20Portal&project-name=sales-form-portal&repository-name=sales-form-portal)

## Manual Deploy Steps

### 1. Connect Repository
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Connect your GitHub account if not connected
4. Select the `Kenan3477/ASIS` repository
5. Vercel will auto-detect this as a Next.js project

### 2. Configure Build Settings
Vercel should automatically detect:
- **Framework Preset**: Next.js
- **Build Command**: `prisma generate && next build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

### 3. Set Environment Variables
Add these environment variables in Vercel:

**Required Variables:**
- `DATABASE_URL` - Your PostgreSQL connection string
- `NEXTAUTH_SECRET` - Generate with: `openssl rand -base64 32`
- `NEXTAUTH_URL` - Will be auto-filled by Vercel

**For PostgreSQL Database:**
You can use any of these services:
- **Vercel Postgres** (recommended) - Add from Vercel dashboard
- **Neon** - Free PostgreSQL: https://neon.tech
- **PlanetScale** - Free MySQL (change schema to MySQL)
- **Supabase** - Free PostgreSQL: https://supabase.com

### 4. Database Setup Options

#### Option A: Vercel Postgres (Recommended)
1. In your Vercel project dashboard
2. Go to "Storage" tab
3. Create "Postgres" database
4. Vercel will automatically set `DATABASE_URL`

#### Option B: External Database (Neon)
1. Create account at https://neon.tech
2. Create a new project
3. Copy the connection string
4. Add as `DATABASE_URL` in Vercel environment variables

### 5. Deploy
1. Click "Deploy"
2. Vercel will build and deploy your application
3. First deployment will take 2-3 minutes
4. You'll get a live URL like: `https://your-app.vercel.app`

### 6. Run Database Migration
After first deployment:
1. Go to your Vercel project dashboard
2. Click on "Functions" tab
3. Find the latest deployment
4. The build process will automatically:
   - Generate Prisma client
   - Push database schema
   - Your app will be ready!

### 7. Seed Database (Optional)
To add default users, you can:
1. Use Prisma Studio: `npx prisma studio`
2. Or run the seed script locally: `npm run db:seed`
3. Or create users via the application

## Default Login Accounts

After deployment, create admin account via the application or use these default credentials if seeded:

**Admin Account:**
- Email: `admin@salesportal.com`
- Password: `admin123`

**Agent Account:**
- Email: `agent@salesportal.com`
- Password: `agent123`

## Features Available:
- ✅ Customer sales form submission
- ✅ Admin dashboard with sales management  
- ✅ CSV export with 158+ CRM fields
- ✅ User authentication and role management
- ✅ Sales deletion and duplicate prevention
- ✅ Responsive design for mobile/desktop

## Post-Deployment:
1. Visit your Vercel URL
2. Create admin account or login with defaults
3. Start collecting sales data!
4. Export to CSV for CRM integration

## Troubleshooting:

**Build Fails:**
- Check environment variables are set correctly
- Ensure `DATABASE_URL` is valid PostgreSQL connection

**Database Connection Issues:**
- Verify `DATABASE_URL` format: `postgresql://user:password@host:port/database`
- Check database is accessible from Vercel servers

**Authentication Issues:**
- Verify `NEXTAUTH_SECRET` is set
- Check `NEXTAUTH_URL` matches your deployment URL

## Support:
- Check Vercel deployment logs for detailed error information
- Ensure all environment variables are properly configured
- Database connection string format is correct