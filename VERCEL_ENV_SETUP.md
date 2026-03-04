# Vercel Environment Variables Setup Guide

## Required Environment Variables for Vercel

Add these environment variables in your Vercel Dashboard → Project Settings → Environment Variables:

### Database
```
DATABASE_URL=prisma+postgres://accelerate.prisma-data.net/?api_key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqd3RfaWQiOjEsInNlY3VyZV9rZXkiOiJza19xVW5Dd0dBbmd6alNSdjdrbnhaU0UiLCJhcGlfa2V5IjoiMDFLRjBUWEdaMUVCUkVKWThEUkdWRUZGUzUiLCJ0ZW5hbnRfaWQiOiIxMDk0ZDJkMWI3MWFkODk5YTFmNjYyOWQ3YzdhYTk0NDM1ODY4ZjI2MzY5MWZkNTEwMWZjZmFiOGFmMWUzZjIzIiwiaW50ZXJuYWxfc2VjcmV0IjoiOTIxZmY2ZmYtODI2YS00NzE0LTk2NGItMTBiYmE5MTI2NDFhIn0.CwFEOQ3_dDNsriK3e6nddtPd3DT4pZqyezN2w-Hi5mw

DIRECT_URL=postgresql://1094d2d1b71ad899a1f6629d7c7aa94435868f263691fd5101fcfab8af1e3f23:sk_qUnCwGAngzjSRv7knxZSE@db.prisma.io:5432/postgres?sslmode=require
```

### Authentication  
```
NEXTAUTH_SECRET=SSmzc72+dkcsCzIEJcxdd2ByPlPZXuolrZdPqWct1NA=
NEXTAUTH_URL=https://your-vercel-app-url.vercel.app
```

### Email Configuration
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=hello@theflashteam.co.uk
EMAIL_PASSWORD=cemblaszaclxrqgc
```

### SMS Configuration  
```
VOODOO_API_KEY=TLc4xzZQcknVVXS3k21A32GwOqPk9QATbcNPSogvOJHjhZ
VOODOO_FROM=Flash
```

## Instructions:

1. Go to Vercel Dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add each variable above
5. Set Environment to "Production, Preview, and Development"
6. Click Add for each variable
7. Deploy your app again

## Common Issues:

1. **NEXTAUTH_URL must match your actual Vercel domain**
2. **Email might fail in serverless - consider using Resend instead**
3. **Database URL must be the Prisma Accelerate URL for serverless**

## Alternative Email Setup for Vercel:

If Gmail SMTP continues to fail on Vercel (common in serverless), set up Resend:

1. Get API key from https://resend.com
2. Add to Vercel: `RESEND_API_KEY=your_resend_api_key`
3. Verify your domain `theflashteam.co.uk` in Resend
4. Update sender email to use verified domain