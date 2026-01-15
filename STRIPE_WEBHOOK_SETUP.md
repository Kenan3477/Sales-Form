# ASIS Stripe Webhook Setup Guide

## 🎯 Overview
Your ASIS Research Platform now has a complete Stripe webhook integration to handle:
- ✅ **Payment confirmations** (checkout.session.completed)  
- ✅ **Subscription payments** (invoice.payment_succeeded)
- ✅ **Payment failures** (invoice.payment_failed)
- ✅ **Academic discount tracking** (50% off for .edu emails)
- ✅ **Signature verification** for security

## 🚀 Railway Environment Setup

### 1. Add Stripe Webhook Secret to Railway
```bash
# In Railway Dashboard > Variables, add:
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

### 2. Your Webhook Endpoint
```
https://web-production-e42ae.up.railway.app/stripe/webhook
```

## 🔧 Stripe Dashboard Configuration

### 1. Create Webhook in Stripe Dashboard
1. Go to **Stripe Dashboard** → **Developers** → **Webhooks**
2. Click **"Add endpoint"**
3. Set endpoint URL: `https://web-production-e42ae.up.railway.app/stripe/webhook`

### 2. Select Events to Listen For
Enable these events:
- ✅ `checkout.session.completed` - One-time payments
- ✅ `invoice.payment_succeeded` - Subscription payments  
- ✅ `invoice.payment_failed` - Failed payments

### 3. Copy Webhook Secret
1. After creating the webhook, click on it
2. In the **"Signing secret"** section, click **"Reveal"**
3. Copy the secret (starts with `whsec_`)
4. Add it to Railway as `STRIPE_WEBHOOK_SECRET`

## 💰 ASIS Pricing Tiers Integration

### Academic Pricing (50% Discount)
- **Academic Basic**: $49.50/month (50% off $99)
- **Academic Professional**: $149.50/month (50% off $299)  
- **Academic Enterprise**: $499.50/month (50% off $999)

### Standard Pricing
- **Professional**: $299/month
- **Enterprise**: $999/month

### Revenue Tracking
The webhook will automatically:
1. **Log all successful payments** with customer email
2. **Track academic discounts** (.edu email detection)
3. **Monitor subscription renewals** 
4. **Alert on payment failures**

## 🧪 Testing the Webhook

### Test Registration Endpoint
```bash
curl -X POST https://web-production-e42ae.up.railway.app/register \
  -H "Content-Type: application/json" \
  -d '{"email":"student@university.edu"}'
```

Expected response:
```json
{
  "message": "Registration successful",
  "email": "student@university.edu", 
  "is_academic": true,
  "discount": 50
}
```

### Test Webhook (Use Stripe CLI)
```bash
stripe listen --forward-to https://web-production-e42ae.up.railway.app/stripe/webhook
stripe trigger checkout.session.completed
```

## 📊 Revenue Projection

### Target: $100K in 60 Days
- **Academic customers** (50% discount): ~85% of revenue
- **Corporate customers** (full price): ~15% of revenue
- **Average monthly revenue**: $84,650
- **Required customers**: 
  - Academic: ~1,200 customers at $49.50/month
  - Corporate: ~85 customers at $299/month

## 🔒 Security Features

### Webhook Signature Verification
- ✅ **HMAC SHA256** signature verification
- ✅ **Timestamp validation** to prevent replay attacks
- ✅ **Secret key validation** from environment variables
- ✅ **Error logging** for failed requests

### CORS and Headers
- ✅ **CORS enabled** for web integration
- ✅ **JSON content-type** enforcement
- ✅ **Proper HTTP status codes**

## 🎯 Next Steps

1. **Configure Stripe Products/Prices** in Dashboard
2. **Set up Stripe Checkout Sessions** with academic discount logic  
3. **Add webhook secret** to Railway environment variables
4. **Test payment flows** with Stripe test cards
5. **Monitor webhook logs** in Railway deployment logs

## 🚨 Important Notes

- **Webhook endpoint**: `/stripe/webhook` 
- **Environment variable**: `STRIPE_WEBHOOK_SECRET`
- **Academic detection**: Automatic for `.edu` domains
- **Revenue logging**: All payments logged to console (extend to database as needed)

Your ASIS Research Platform is now ready for production billing! 🚀
