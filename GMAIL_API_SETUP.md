## 🎯 Gmail API Setup for Hello@theflashteam.co.uk

### **Step 1: Enable Gmail API**
1. Go to **Google Cloud Console**: https://console.cloud.google.com
2. Select your project (or create one)
3. Go to **APIs & Services** → **Library**
4. Search for "Gmail API" and **Enable** it

### **Step 2: Create OAuth2 Credentials**
1. Go to **APIs & Services** → **Credentials**
2. Click **"+ Create Credentials"** → **OAuth client ID**
3. Choose **"Web application"**
4. **Name**: Sales Form Gmail API
5. **Authorized redirect URIs**: Add `urn:ietf:wg:oauth:2.0:oob`
6. **Download** the JSON file (client_secret.json)

### **Step 3: Get Refresh Token**
Run this one-time script to get your refresh token:

```javascript
// gmail-setup.js
const { google } = require('googleapis');
const readline = require('readline');

const oauth2Client = new google.auth.OAuth2(
  'YOUR_CLIENT_ID',
  'YOUR_CLIENT_SECRET', 
  'urn:ietf:wg:oauth:2.0:oob'
);

const scopes = [
  'https://www.googleapis.com/auth/gmail.send'
];

const authUrl = oauth2Client.generateAuthUrl({
  access_type: 'offline',
  scope: scopes,
});

console.log('Authorize this app by visiting this url:', authUrl);

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

rl.question('Enter the code from that page here: ', (code) => {
  rl.close();
  oauth2Client.getToken(code, (err, token) => {
    if (err) return console.error('Error retrieving access token', err);
    console.log('Your refresh token is:', token.refresh_token);
    console.log('Add this to your environment variables!');
  });
});
```

### **Step 4: Add Environment Variables**
Add these to your `.env` file and Vercel:

```bash
# Gmail API Configuration  
GMAIL_CLIENT_ID=your_client_id_here
GMAIL_CLIENT_SECRET=your_client_secret_here
GMAIL_REFRESH_TOKEN=your_refresh_token_here

# Keep your existing email config for fallback
EMAIL_USER=Hello@theflashteam.co.uk
EMAIL_PASSWORD=your_app_password
```

### **Step 5: Add to Vercel**
```bash
vercel env add GMAIL_CLIENT_ID
vercel env add GMAIL_CLIENT_SECRET  
vercel env add GMAIL_REFRESH_TOKEN
```

### **Step 6: Deploy**
```bash
npm run build
git add .
git commit -m "Add Gmail API integration"
git push
```

## ✅ **What This Achieves:**
- ✅ Emails sent from **Hello@theflashteam.co.uk** (your Gmail)
- ✅ **No SMTP port blocking** issues in Vercel
- ✅ **Higher reliability** than SMTP in serverless
- ✅ **Same professional appearance**
- ✅ **SMTP fallback** if Gmail API fails
- ✅ **Same email templates** and PDF attachments

## 🚀 **Priority Order:**
1. **Gmail API** (Hello@theflashteam.co.uk) - Primary method
2. **SMTP fallback** - If Gmail API fails 
3. **Resend/Web service** - Last resort

This keeps your existing Gmail account while solving the serverless port blocking issue!