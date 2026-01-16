import * as z from 'zod'

export const applianceSchema = z.object({
  appliance: z.string().min(1, 'Appliance type is required'),
  otherText: z.string().optional(),
  coverLimit: z.number().min(0, 'Cover limit must be positive'),
  cost: z.number().min(0, 'Cost must be positive'),
})

export const saleSchema = z.object({
  customerFirstName: z.string().min(1, 'First name is required'),
  customerLastName: z.string().min(1, 'Last name is required'),
  title: z.string().optional(),
  phoneNumber: z.string().min(1, 'Phone number is required'),
  email: z.string().email('Valid email is required'),
  notes: z.string().optional(),
  mailingStreet: z.string().optional(),
  mailingCity: z.string().min(1, 'City is required'),
  mailingProvince: z.string().optional(),
  mailingPostalCode: z.string().optional(),
  accountName: z.string().min(1, 'Account name is required'),
  sortCode: z.string().regex(/^\d{6}$/, 'Sort code must be 6 digits'),
  accountNumber: z.string().regex(/^\d{8}$/, 'Account number must be 8 digits'),
  directDebitDate: z.string().min(1, 'Direct debit date is required'),
  applianceCoverSelected: z.boolean(),
  boilerCoverSelected: z.boolean(),
  boilerPriceSelected: z.union([z.string(), z.number()]).nullable().transform((val) => val ? Number(val) : null),
  appliances: z.array(applianceSchema),
})

export type ApplianceFormData = z.infer<typeof applianceSchema>
export type SaleFormData = z.infer<typeof saleSchema>

export const APPLIANCE_OPTIONS = [
  'Washing machine',
  'Tumble dryer', 
  'Dishwasher',
  'Fridge',
  'Freezer',
  'Oven/Cooker',
  'Hob',
  'Microwave',
  'TV',
  'Laptop',
  'Other'
]

export const BOILER_OPTIONS = [
  { value: 14.99, label: '£14.99/month' },
  { value: 19.99, label: '£19.99/month' },
  { value: 24.99, label: '£24.99/month' },
  { value: 29.99, label: '£29.99/month' },
]

export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP'
  }).format(amount)
}

export function formatPhoneNumber(phone: string): string {
  // Basic UK phone number formatting
  const cleaned = phone.replace(/\D/g, '')
  
  if (cleaned.length === 11 && cleaned.startsWith('0')) {
    return cleaned.replace(/(\d{4})(\d{3})(\d{4})/, '$1 $2 $3')
  }
  
  if (cleaned.length === 10) {
    return '0' + cleaned.replace(/(\d{3})(\d{3})(\d{4})/, '$1 $2 $3')
  }
  
  return phone
}