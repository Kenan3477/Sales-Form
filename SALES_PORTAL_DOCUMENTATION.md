# Sales Form Portal - Comprehensive Feature Documentation

**Version:** 1.1.3  
**Last Updated:** January 19, 2026  
**Production URL:** https://sales-form-chi.vercel.app  
**Repository:** https://github.com/Kenan3477/Sales-Form  

---

## 🚀 Overview

The Sales Form Portal is a comprehensive web application designed for sales teams to efficiently manage customer sales submissions, appliance and boiler cover plans, and administrative operations. The system features role-based access control, real-time duplicate detection, advanced filtering, and CRM-ready data export capabilities.

---

## 👥 User Roles & Authentication

### **Agent Role**
- **Primary Function**: Submit customer sales and manage their own submissions
- **Access Level**: Limited to own sales data
- **Key Features**: 
  - Create new sales with dynamic form validation
  - View and edit own sales
  - Real-time duplicate customer detection
  - Live cost calculation

### **Admin Role**
- **Primary Function**: Manage all sales, users, and system configuration
- **Access Level**: Full system access
- **Key Features**:
  - Complete sales management across all agents
  - User management (create, edit, delete users)
  - Field configuration settings
  - Advanced filtering and reporting
  - CSV export with deduplication
  - SMS messaging capabilities
  - Sales import functionality

### **Authentication System**
- **Technology**: NextAuth.js with credential-based authentication
- **Security Features**:
  - bcrypt password hashing
  - Session-based authentication
  - Middleware route protection
  - Rate limiting (Redis in production)
  - Security event logging

---

## 💼 Sales Management Features

### **Dynamic Sales Form**
The core sales form adapts based on user selections and admin field configuration:

#### **Customer Information Section**
- **First Name** *(configurable requirement)*
- **Last Name** *(configurable requirement)*
- **Title** *(Mr, Mrs, Miss, Ms, Dr - optional)*
- **Phone Number** *(configurable requirement)*
- **Email Address** *(configurable requirement with dynamic validation)*
- **Mailing Address** *(street, city, province, postal code - all configurable)*
- **Notes** *(large text area for comprehensive details - configurable)*

#### **Direct Debit Information**
- **Account Name** *(configurable requirement)*
- **Sort Code** *(6 digits with smart formatting - configurable)*
- **Account Number** *(8 digits with enhanced paste handling - configurable)*
- **Direct Debit Date** *(configurable requirement)*

#### **Coverage Selection**
**Appliance Cover Section:**
- Dynamic appliance builder with unlimited appliances
- Predefined appliance types: Washing Machine, Tumble Dryer, Dishwasher, Fridge Freezer, Electric Cooker, Gas Cooker, Electric Hob, Gas Hob, Microwave, Other
- Custom "Other" text field for unlisted appliances
- Cover limit options: £500, £600, £700, £800
- Individual cost per appliance
- Real-time total calculation

**Boiler Cover Section:**
- Multiple pricing tiers available
- Integrated with appliance total for complete plan cost
- Conditional display based on user selection

### **Smart Input Handling** *(New Feature)*
- **Enhanced Paste Support**: Automatically handles 8-digit account numbers and 6-digit sort codes
- **Auto-Formatting**: Removes spaces, hyphens, and non-digit characters automatically
- **Real-time Validation**: Input cleaning as users type
- **Format Flexibility**: Accepts various input formats for banking details

### **Real-time Duplicate Detection**
Advanced customer deduplication system with multiple confidence levels:

#### **Detection Methods**
- **Phone Number Matching**: Primary detection method
- **Email Address Matching**: Secondary validation
- **Name Combination**: Tertiary check for completeness
- **Confidence Scoring**: HIGH/MEDIUM/LOW risk assessment

#### **User Experience**
- **Live Checking**: Detects duplicates as users type
- **Visual Feedback**: Color-coded warnings with existing customer details
- **Override System**: Allow proceeding with duplicates when necessary
- **Detailed Information**: Shows existing customer data for verification

---

## 🛠 Admin Management Panel

### **Sales Management Interface**
Comprehensive dashboard for managing all sales submissions:

#### **Advanced Filtering System**
- **Agent Filter**: Filter by specific agent email *(New Feature)*
- **Date Range**: From/To date filtering for sales creation
- **Direct Debit Dates**: From/To filtering for payment dates
- **Plan Type**: Appliance-only, Boiler-only, Both
- **Appliance Count**: 1, 2-3, 4-5, 6+ appliances
- **Boiler Cover**: Yes/No filtering
- **Customer Search**: Name and email search functionality
- **Status Filter**: Active, Cancelled, Failed Payment, etc.

#### **Bulk Operations**
- **Multi-Selection**: Checkbox selection for multiple sales
- **Bulk Delete**: Remove multiple sales simultaneously
- **Bulk Export**: Export selected sales only
- **Safety Confirmations**: Prevent accidental bulk operations

### **CSV Export System**
Enterprise-grade data export with CRM integration:

#### **Export Features**
- **160+ Field Headers**: Comprehensive data mapping for CRM systems
- **Deduplication Integration**: Export with duplicate exclusion
- **Custom Filtering**: Export filtered subsets of data
- **Selected Sales Export**: Export only chosen sales
- **Standardized Format**: Consistent column structure across exports

#### **CRM-Ready Data Fields**
```
Customer Information:
- Customer Title, First Name, Last Name, Full Name
- Customer Premium, Customer Package (Appliance/Boiler/Both)
- Email, Phone, Mobile (normalized)
- Full Address components

Financial Information:
- Sort Code, Account Number, Account Name
- Direct Debit Date, Total Plan Cost
- Individual appliance costs and limits

Technical Fields:
- Lead Source (FE3), Payment Method (DD)
- Processor (DD), Customer Reference
- Creation timestamps and agent information

Appliance Details:
- Up to 10 appliances with full specifications
- Appliance types, costs, cover limits
- Boiler cover details and pricing
```

### **User Management System**
Complete administrative control over system users:

#### **User Operations**
- **Create Users**: Add new agents and admins
- **Edit Users**: Update email addresses, passwords, roles
- **Role Management**: Switch between AGENT and ADMIN roles
- **Security Protection**: Cannot delete users with sales or self-delete
- **User Listing**: View all system users with their details

#### **Security Features**
- **Password Management**: Secure password updates
- **Role Validation**: Proper authorization checks
- **Data Protection**: Prevents deletion of users with associated data

### **Field Configuration System**
Dynamic form validation management:

#### **Configurable Fields**
All form fields can be set as mandatory or optional:
- Customer information fields
- Contact details
- Address components
- Direct debit information
- Notes and additional fields

#### **Dynamic Validation**
- **Client-side**: React Hook Form with Zod schemas
- **Server-side**: API validation based on current settings
- **Real-time Updates**: Changes apply immediately to forms

---

## 📤 Import/Export Capabilities

### **Sales Import System**
Bulk data import with multiple format support:

#### **Supported Formats**
- **CSV**: Standard comma-separated values
- **JSON**: Structured data format
- **Firebase Export**: Special handling for Firebase data structures

#### **Import Features**
- **Data Validation**: All uploaded data validated against required fields
- **Automatic Processing**: Coverage type detection and cost calculations
- **Appliance Parsing**: Handles up to 10 appliances per sale
- **Error Reporting**: Detailed validation error messages
- **Format Flexibility**: Multiple ways to structure appliance data

#### **Sample Data Formats**
**CSV Structure:**
```csv
customerFirstName,customerLastName,phoneNumber,email,accountName,sortCode,accountNumber,directDebitDate,totalPlanCost,appliance1,appliance1Cost,appliance1CoverLimit,appliance2,appliance2Cost,appliance2CoverLimit
John,Doe,01234567890,john@email.com,John Doe,12-34-56,12345678,2026-02-01,45.98,Washing Machine,15.99,500,Dishwasher,4.00,600
```

**JSON Structure:**
```json
[
  {
    "customerFirstName": "John",
    "customerLastName": "Doe",
    "phoneNumber": "01234567890",
    "email": "john@email.com",
    "accountName": "John Doe",
    "sortCode": "12-34-56",
    "accountNumber": "12345678",
    "directDebitDate": "2026-02-01",
    "totalPlanCost": 45.98,
    "appliances": [
      {
        "appliance": "Washing Machine",
        "cost": 15.99,
        "coverLimit": 500
      }
    ]
  }
]
```

### **Export System**
- **Filtered Exports**: Export based on current filter settings
- **Deduplication**: Remove duplicates before export
- **CRM Integration**: 160+ fields for external system compatibility
- **Date Stamped Files**: Automatic filename generation with dates

---

## 📱 Communication Features

### **SMS Messaging System**
Integrated customer communication capabilities:

#### **SMS Features**
- **Bulk SMS**: Send messages to multiple customers
- **Template System**: Predefined message templates
- **Delivery Tracking**: SMS status monitoring
- **Error Handling**: Failed message tracking and retry capabilities
- **Agent Grouping**: SMS organization by sales agent

#### **SMS Status Tracking**
- NOT_SENT: Queued for delivery
- SENDING: In progress
- SENT: Successfully delivered
- FAILED: Delivery failed
- SKIPPED: Intentionally not sent

---

## 🗄 Document Management

### **Document Generation System**
Automated document creation and management:

#### **Document Templates**
- **HTML Templates**: Customizable document layouts
- **Version Control**: Multiple template versions
- **Active Status**: Enable/disable templates
- **Template Types**: Different document categories

#### **Generated Documents**
- **PDF Generation**: Convert templates to PDF format
- **File Management**: Secure file storage and retrieval
- **Download Tracking**: Monitor document access
- **Metadata Storage**: Additional document information

---

## 🔧 Technical Architecture

### **Frontend Technology**
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript for type safety
- **Styling**: Tailwind CSS for responsive design
- **Forms**: React Hook Form with Zod validation
- **Icons**: Lucide React icon library

### **Backend Technology**
- **API**: Next.js API Routes
- **Database**: PostgreSQL with Prisma ORM
- **Authentication**: NextAuth.js with session management
- **Validation**: Zod schemas for data validation

### **Database Schema**
**Core Tables:**
- **Users**: Authentication and role management
- **Sales**: Main sales data with relationships
- **Appliances**: Individual appliance details
- **FieldConfigurations**: Dynamic form settings
- **SMSLogs**: Communication tracking
- **DocumentTemplates**: Template management
- **GeneratedDocuments**: Document tracking

### **Security Features**
- **Rate Limiting**: Redis-based production rate limiting
- **Input Validation**: Comprehensive data validation
- **CSRF Protection**: Cross-site request forgery prevention
- **Content Security Policy**: XSS attack prevention
- **Audit Logging**: Security event tracking

---

## 🚀 Deployment & Infrastructure

### **Production Environment**
- **Platform**: Vercel for hosting and deployment
- **Database**: PostgreSQL (production)
- **Performance**: Optimized with edge caching
- **SSL**: Automatic HTTPS certification
- **Monitoring**: Built-in performance monitoring

### **Development Environment**
- **Local Database**: PostgreSQL or SQLite
- **Hot Reloading**: Real-time development updates
- **Database Studio**: Prisma Studio for data management
- **Seeding**: Automated test data generation

---

## 📊 Reporting & Analytics

### **Sales Analytics**
- **Sales Volume**: Track sales by agent and date range
- **Revenue Tracking**: Monitor total plan costs and trends
- **Customer Patterns**: Analyze customer data and preferences
- **Appliance Trends**: Popular appliance types and coverage levels

### **Export Analytics**
- **CRM Integration**: 160+ field comprehensive data export
- **Deduplication Statistics**: Track duplicate customer detection
- **Filter Usage**: Monitor most used filter combinations
- **Download Tracking**: Document access patterns

---

## 🔒 Security & Compliance

### **Data Protection**
- **Password Security**: bcrypt hashing with salt rounds
- **Session Management**: Secure session handling
- **Input Sanitization**: Prevent injection attacks
- **Rate Limiting**: API abuse prevention

### **Audit Trail**
- **Security Events**: Comprehensive logging of security-related actions
- **User Activity**: Track user actions and data access
- **Change History**: Monitor data modifications
- **Export Tracking**: Log data export activities

---

## 🆕 Recent Feature Updates

### **Version 1.1.3 Enhancements**
- **Enhanced Account Number Handling**: Smart paste functionality for banking details
- **Agent Filtering**: Complete filtering by agent in admin panel
- **User Management**: Full CRUD operations for user accounts
- **Deduplication System**: Real-time duplicate customer detection
- **Enhanced Security**: Comprehensive rate limiting and audit logging
- **Import System**: Multiple format support for bulk data import
- **SMS Integration**: Customer communication capabilities
- **Document Generation**: Automated PDF creation and management

---

## 📞 Support & Usage

### **Default Admin Credentials**
- **Username**: admin@salesportal.com
- **Password**: admin123

### **Default Agent Credentials**
- **Username**: agent@salesportal.com
- **Password**: agent123

### **Key URLs**
- **Production**: https://sales-form-chi.vercel.app
- **Admin Panel**: /admin/sales
- **User Management**: /admin/users
- **Settings**: /admin/settings
- **Import**: /admin/sales/import
- **SMS**: /admin/sales/sms

---

## 🔄 API Endpoints

### **Core API Routes**
- `GET/POST /api/sales` - Sales CRUD operations
- `GET/PUT /api/field-configurations` - Field configuration management
- `POST /api/sales/import` - Bulk sales import
- `GET/POST /api/sales/export` - Data export with filtering
- `POST /api/sales/bulk-delete` - Bulk deletion operations
- `GET/POST /api/admin/users` - User management operations
- `POST /api/admin/sales/sms` - SMS messaging
- `/api/auth/[...nextauth]` - Authentication endpoints

### **Advanced Features**
- **Real-time Filtering**: Dynamic query parameter support
- **Deduplication API**: Customer duplicate detection
- **Template Management**: Document template operations
- **File Upload**: Import file handling
- **Export Processing**: Large dataset export handling

---

This comprehensive Sales Form Portal provides a complete solution for sales team management, customer data handling, and administrative operations with enterprise-grade security and scalability features.