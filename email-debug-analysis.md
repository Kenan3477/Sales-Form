🔍 EMAIL VALIDATION ISSUE ANALYSIS
===================================

📊 Current Status: DEBUGGING IN PROGRESS

🎯 Root Cause Identified:
- ✅ Email validation logic is WORKING CORRECTLY
- ✅ One successful sale was created (Morfydd Kill) - proves validation works
- ❌ Someone is submitting INVALID EMAIL FORMATS (not empty emails)
- 🔍 Need to identify what invalid format is being submitted

📧 What Works:
- ✅ Empty email: "" → SUCCESS
- ✅ Valid email: "user@domain.com" → SUCCESS  
- ✅ Undefined email: undefined → SUCCESS (for optional fields)

📧 What Fails:
- ❌ Invalid format: "invalid-email" → ERROR (as expected)
- ❌ Invalid format: "user@" → ERROR (as expected)
- ❌ Invalid format: "@domain.com" → ERROR (as expected)

🔧 Current Validation Logic:
```javascript
// For optional email fields (most common):
email: z.string()
  .refine((val) => val === '' || z.string().email().safeParse(val).success, {
    message: 'Please enter a valid email address or leave empty'
  })
  .optional()

// For required email fields:
email: z.string()
  .refine((val) => val === '' || z.string().email().safeParse(val).success, {
    message: 'Please enter a valid email address'
  })
```

🚨 Error Pattern:
- Error Message: "Please enter a valid email address or leave empty"
- This indicates: Email field is OPTIONAL but invalid format submitted
- ZodError Path: ["email"] 

🔍 Debug Information Added:
- ✅ Frontend: Logs exact email value being sent
- ✅ Backend: Logs email value received and validation details
- ✅ Enhanced logging: Shows invalid formats when caught

📈 Expected Next Steps:
1. 🔍 Debug logs will show EXACT invalid email being submitted
2. 🎯 Identify if it's:
   - User error (typing invalid email)
   - Frontend processing issue
   - Data corruption during transmission
3. 🛠️ Apply appropriate fix based on root cause

🎉 Success Indicators:
- One sale DID succeed (Morfydd Kill) 
- Validation is working as designed
- Issue is with specific invalid input, not validation logic

⏰ Status: Enhanced debug version deployed
📍 Next: Wait for debug logs or test submission to see exact problematic email value