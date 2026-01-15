# Sales Form Portal

A comprehensive web application for sales agents to submit customer sales and for admins to manage submissions with configurable mandatory fields and CSV export capabilities.

## Features

### Core Functionality
- **Role-based Authentication**: Agent and Admin roles with different permissions
- **Dynamic Sales Form**: Configurable form with conditional sections for appliances and boiler cover
- **Live Cost Calculation**: Real-time total plan cost updates based on selected options
- **Admin Management Panel**: Complete sales management with filtering, editing, and CSV export
- **Field Configuration**: Admin can configure which fields are mandatory vs optional

### Sales Form Features
- Customer information capture (name, phone, email)
- Direct debit details with validation
- Appliance cover with dynamic appliance list builder
- Boiler cover with multiple pricing options
- Form validation (client and server-side)
- Mobile-responsive design

### Admin Features
- View all sales with filtering by agent, date range, customer name
- Export sales data to CSV format
- Configure mandatory/optional field settings for all form fields
- Edit and delete sales (optional feature included)
- Sales detail view with complete information

## Tech Stack

- **Frontend**: Next.js 14 with App Router, TypeScript, Tailwind CSS
- **Backend**: Next.js API Routes with Prisma ORM
- **Database**: PostgreSQL
- **Authentication**: NextAuth.js with credentials provider
- **Forms**: React Hook Form with Zod validation
- **UI Components**: Custom components with Lucide icons

## Prerequisites

- Node.js 18+ and npm
- PostgreSQL database
- Git

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sales-form-portal
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your database and authentication settings:
   ```env
   DATABASE_URL="postgresql://username:password@localhost:5432/sales_form_portal"
   NEXTAUTH_SECRET="your-super-secret-nextauth-secret-key-here"
   NEXTAUTH_URL="http://localhost:3000"
   ```

4. **Set up the database**
   ```bash
   # Push the schema to the database
   npm run db:push
   
   # Seed the database with default users and settings
   npm run db:seed
   ```

5. **Generate Prisma client**
   ```bash
   npm run db:generate
   ```

## Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Default Users

After seeding the database, you can use these accounts:

- **Admin**: admin@salesportal.com / admin123
- **Agent**: agent@salesportal.com / agent123

## Database Management

- **View database**: `npm run db:studio` (opens Prisma Studio)
- **Reset database**: `npm run db:push` (resets and applies schema)
- **Re-seed data**: `npm run db:seed`

## Production Deployment

1. **Build the application**
   ```bash
   npm run build
   ```

2. **Start production server**
   ```bash
   npm start
   ```

3. **Environment Setup**
   - Set `NEXTAUTH_URL` to your production domain
   - Ensure PostgreSQL is accessible
   - Use a secure `NEXTAUTH_SECRET`

## Project Structure

```
src/
├── app/                 # Next.js App Router pages
│   ├── api/            # API routes
│   ├── auth/           # Authentication pages
│   ├── sales/          # Sales-related pages
│   ├── admin/          # Admin panel pages
│   └── dashboard/      # Dashboard page
├── components/         # Reusable React components
├── lib/               # Utility functions and configurations
│   ├── auth.ts        # NextAuth configuration
│   ├── prisma.ts      # Prisma client
│   └── schemas.ts     # Zod validation schemas
└── types/             # TypeScript type definitions

prisma/
├── schema.prisma      # Database schema
└── seed.ts           # Database seeding script
```

## Key Features Implementation

### Form Validation
- Client-side validation with React Hook Form and Zod
- Server-side validation for security
- Dynamic validation based on admin field configuration

### Role-based Access Control
- Middleware-based route protection
- Session-based authentication
- Different UI and permissions for agents vs admins

### Dynamic Form Sections
- Conditional appliance section with repeatable rows
- Boiler cover section with radio button options
- Live total cost calculation

### CSV Export
- Filtered data export capability
- Consistent column structure
- Appliance data serialization

## API Endpoints

- `GET/POST /api/sales` - Sales CRUD operations
- `GET/PUT /api/field-configurations` - Field configuration management
- `/api/auth/[...nextauth]` - Authentication endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please contact the development team or create an issue in the repository.