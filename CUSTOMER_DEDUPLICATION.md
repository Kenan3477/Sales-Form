# Customer Deduplication System

## Overview

The Sales Form Portal now includes a comprehensive customer deduplication system that prevents duplicate customer entries both during sales form creation and bulk import operations.

## 🎯 Key Features

### **Real-time Duplicate Detection**
- **Instant checking** as users type customer information
- **Confidence-based scoring**: HIGH, MEDIUM, LOW
- **Visual warnings** with existing customer details
- **Intelligent matching** across multiple criteria

### **Multi-level Protection**
1. **Email Address**: Exact match (HIGH confidence)
2. **Phone Number**: Normalized matching including UK format variations (HIGH confidence)
3. **Full Name**: Case-insensitive exact match (MEDIUM confidence)
4. **Similar Names**: Partial matching for typos (LOW confidence)

### **Smart Override System**
- **HIGH confidence duplicates**: Require explicit confirmation to proceed
- **MEDIUM/LOW confidence**: Can be acknowledged or dismissed
- **Complete customer details** shown for review

## 🛡️ Implementation Details

### **1. Sales Form Protection (`/sales/new`)**

#### **Real-time Checking**
```typescript
// Automatic duplicate check after 1 second of no typing
useEffect(() => {
  const timeoutId = setTimeout(() => {
    checkCustomerDuplicate()
  }, 1000)
  return () => clearTimeout(timeoutId)
}, [customerFirstName, customerLastName, customerEmail, customerPhone])
```

#### **Visual Feedback**
- **Red warning**: HIGH confidence duplicate (blocks submission)
- **Yellow warning**: MEDIUM confidence duplicate (requires acknowledgment)  
- **Blue info**: LOW confidence duplicate (informational)
- **Existing customer card** with full details and previous sale information

#### **Form Submission Protection**
```typescript
// Prevents submission for HIGH confidence duplicates
if (duplicateCheck?.isDuplicate && duplicateCheck.confidence === 'HIGH' && !showDuplicateForm) {
  setError(`Cannot create sale: ${duplicateCheck.message}`)
  return
}
```

### **2. API Endpoint (`/api/customers/check-duplicate`)**

#### **Request Format**
```json
{
  "customerFirstName": "John",
  "customerLastName": "Smith", 
  "email": "john.smith@email.com",
  "phoneNumber": "07123456789"
}
```

#### **Response Format**
```json
{
  "isDuplicate": true,
  "customer": {
    "id": "customer-id",
    "customerFirstName": "John",
    "customerLastName": "Smith",
    "email": "john.smith@email.com",
    "phoneNumber": "07123456789",
    "totalPlanCost": 150.00,
    "createdAt": "2024-01-15T10:30:00Z",
    "createdBy": {
      "email": "agent@company.com"
    }
  },
  "reason": "Email address already exists in the system",
  "confidence": "HIGH",
  "message": "Strong match: This email address is already registered"
}
```

### **3. Enhanced Sales API (`/api/sales`)**

#### **Duplicate Prevention**
- **Automatic checking** before sale creation
- **409 Conflict response** for duplicates
- **Override flag support** (`ignoreDuplicateWarning`)
- **Comprehensive logging** of all duplicate attempts

#### **Security Integration**
```typescript
// Enhanced duplicate checking with security logging
const duplicateCheck = await checkForSaleDuplicate({
  customerFirstName, customerLastName, email, phoneNumber,
  accountNumber, totalPlanCost
})

if (duplicateCheck.isDuplicate) {
  logSecurityEvent('SALE_DUPLICATE_BLOCKED', securityContext, {
    userId: session.user.id,
    duplicateReason: duplicateCheck.duplicateReason,
    confidence: duplicateCheck.confidence
  })
}
```

### **4. Import System Protection**

#### **Existing Features** (Already Implemented)
- **Bulk duplicate detection** during CSV/JSON imports
- **Detailed duplicate reports** with skip summaries
- **Conservative approach**: Skips any potential duplicates
- **Comprehensive logging** of skipped records

#### **Import Response**
```json
{
  "success": true,
  "imported": 45,
  "total": 50,
  "skipped": 5,
  "duplicates": [
    {
      "customer": "John Smith",
      "email": "john@email.com", 
      "phone": "07123456789",
      "reason": "Email address already exists",
      "existingCustomer": { "..." }
    }
  ]
}
```

## 🧠 Duplicate Detection Logic

### **Email Matching**
```typescript
// Case-insensitive exact email matching
const emailMatch = await prisma.sale.findFirst({
  where: {
    email: { equals: email, mode: 'insensitive' }
  }
})
```

### **Phone Number Matching**
```typescript
// Multi-format phone number checking
const normalizedPhone = phoneNumber.replace(/[\s\-\(\)\+]/g, '')
const phoneQueries = [
  { phoneNumber: normalizedPhone },
  { phoneNumber: phoneNumber },
  { phoneNumber: { endsWith: normalizedPhone.slice(-10) } } // UK format
]
```

### **Name Matching**
```typescript
// Exact name matching (case-insensitive)
const nameMatch = await prisma.sale.findFirst({
  where: {
    AND: [
      { customerFirstName: { equals: firstName, mode: 'insensitive' } },
      { customerLastName: { equals: lastName, mode: 'insensitive' } }
    ]
  }
})
```

### **Similar Name Detection**
```typescript
// Partial name matching for typos
const similarMatch = await prisma.sale.findFirst({
  where: {
    OR: [
      { customerFirstName: { contains: firstName, mode: 'insensitive' } },
      { customerLastName: { contains: lastName, mode: 'insensitive' } }
    ]
  }
})
```

## 📋 User Experience

### **Sales Form Workflow**
1. **User types** customer information
2. **System checks** for duplicates after 1-second delay
3. **Warning appears** if duplicate found
4. **User reviews** existing customer details
5. **Decision required**: Continue anyway or start over
6. **Form submission** respects confidence level

### **Import Workflow**  
1. **File uploaded** (CSV or JSON)
2. **Each record checked** for duplicates
3. **Duplicates skipped** automatically
4. **Summary report** shows results
5. **Detailed list** of skipped duplicates provided

## 🔒 Security Features

### **Rate Limiting**
- **Customer lookup**: 100 requests per hour
- **Sales creation**: Standard rate limits apply
- **Import operations**: 10 imports per hour

### **Input Sanitization**
- **All inputs sanitized** before database queries
- **SQL injection protection** via Prisma
- **XSS prevention** on all outputs

### **Audit Logging**
```typescript
logSecurityEvent('CUSTOMER_DUPLICATE_CHECK', securityContext, {
  userId: user.id,
  customerData: { firstName, lastName, email: "***" } // Privacy protection
})
```

## 🚀 Deployment Status

- ✅ **Development**: Implemented and tested
- ✅ **Production**: Deployed to Vercel
- ✅ **Security**: Enterprise-level protection
- ✅ **Performance**: Optimized database queries

## 📊 Benefits

### **Data Quality**
- **Prevents duplicates** at point of entry
- **Maintains clean database** integrity
- **Reduces customer confusion** from multiple records
- **Improves reporting accuracy**

### **User Experience**
- **Real-time feedback** prevents mistakes
- **Clear visual indicators** of duplicate status
- **Informed decisions** with existing customer details
- **Flexible override** system for edge cases

### **Business Value**
- **Reduces data cleanup** effort
- **Prevents duplicate payments** and confusion
- **Maintains customer relationship** integrity
- **Supports compliance** requirements

## 🔧 Configuration

### **Confidence Thresholds**
```typescript
const CONFIDENCE_LEVELS = {
  HIGH: ['email_match', 'phone_match', 'identical_sale'],
  MEDIUM: ['name_match', 'similar_email'],  
  LOW: ['similar_name', 'partial_match']
}
```

### **Timing Settings**
```typescript
const DEBOUNCE_DELAY = 1000; // 1 second delay before checking
const MIN_FIELD_LENGTHS = {
  firstName: 2,
  lastName: 2, 
  email: 5,
  phone: 8
}
```

This comprehensive deduplication system ensures data integrity while providing flexibility for legitimate edge cases! 🎉