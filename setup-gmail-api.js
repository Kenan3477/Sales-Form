const { google } = require('googleapis');
const readline = require('readline');

console.log('🚀 Gmail API Setup for Hello@theflashteam.co.uk\n');

// You'll get these from Google Cloud Console
const CLIENT_ID = process.env.GMAIL_CLIENT_ID || 'YOUR_CLIENT_ID_HERE';
const CLIENT_SECRET = process.env.GMAIL_CLIENT_SECRET || 'YOUR_CLIENT_SECRET_HERE';

if (CLIENT_ID === 'YOUR_CLIENT_ID_HERE' || CLIENT_SECRET === 'YOUR_CLIENT_SECRET_HERE') {
  console.log('❌ Please set up your OAuth2 credentials first:');
  console.log('1. Go to: https://console.cloud.google.com');
  console.log('2. Enable Gmail API');
  console.log('3. Create OAuth2 credentials');
  console.log('4. Set environment variables: GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET');
  console.log('5. Run this script again');
  process.exit(1);
}

const oauth2Client = new google.auth.OAuth2(
  CLIENT_ID,
  CLIENT_SECRET,
  'urn:ietf:wg:oauth:2.0:oob'
);

const scopes = [
  'https://www.googleapis.com/auth/gmail.send'
];

const authUrl = oauth2Client.generateAuthUrl({
  access_type: 'offline',
  scope: scopes,
});

console.log('📧 Setting up Gmail API for Hello@theflashteam.co.uk');
console.log('==================================================');
console.log('\n🔗 Visit this URL to authorize the app:');
console.log(authUrl);
console.log('\n📋 Steps:');
console.log('1. Click the link above');
console.log('2. Sign in with Hello@theflashteam.co.uk');
console.log('3. Grant permissions');
console.log('4. Copy the authorization code');
console.log('5. Paste it below');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

rl.question('\n🔑 Enter the authorization code: ', (code) => {
  rl.close();
  
  oauth2Client.getToken(code, (err, token) => {
    if (err) {
      console.error('❌ Error retrieving access token:', err);
      return;
    }
    
    console.log('\n✅ Success! Here are your environment variables:');
    console.log('===============================================');
    console.log(`GMAIL_CLIENT_ID=${CLIENT_ID}`);
    console.log(`GMAIL_CLIENT_SECRET=${CLIENT_SECRET}`);
    console.log(`GMAIL_REFRESH_TOKEN=${token.refresh_token}`);
    console.log('\n📝 Add these to:');
    console.log('1. Your .env file for local development');
    console.log('2. Vercel environment variables for production');
    console.log('\n🚀 Then deploy and test!');
  });
});