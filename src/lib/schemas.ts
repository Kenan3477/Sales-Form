import * as z from 'zod'

export const applianceSchema = z.object({
  appliance: z.string().min(1, 'Appliance type is required'),
  otherText: z.string().optional(),
  coverLimit: z.number()
    .min(1, 'Cover limit is required')
    .refine(val => [500, 600, 700, 800].includes(val), {
      message: 'Cover limit must be 500, 600, 700, or 800'
    }),
  cost: z.number()
    .min(0.01, 'Cost per appliance is required and must be greater than 0'),
})

export const saleSchema = z.object({
  customerFirstName: z.string().min(1, 'First name is required'),
  customerLastName: z.string().min(1, 'Last name is required'),
  title: z.string().min(1, 'Title is required'),
  phoneNumber: z.string().min(1, 'Phone number is required'),
  email: z.string()
    .refine((val) => val === '' || z.string().email().safeParse(val).success, {
      message: 'Please enter a valid email address or leave empty'
    })
    .optional(),
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
  boilerPriceSelected: z.union([z.string(), z.number(), z.null()]).nullable().transform((val) => {
    if (val === null || val === undefined || val === '') return null
    const num = Number(val)
    return isNaN(num) ? null : num
  }),
  appliances: z.array(applianceSchema).max(10, 'Maximum of 10 appliances allowed'),
}).superRefine((data, ctx) => {
  // Make boiler price required when boiler cover is selected
  if (data.boilerCoverSelected && (data.boilerPriceSelected === null || data.boilerPriceSelected === 0)) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: 'Boiler price is required when boiler cover is selected',
      path: ['boilerPriceSelected']
    })
  }
  
  // Make sure at least one appliance is provided when appliance cover is selected
  if (data.applianceCoverSelected && data.appliances.length === 0) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: 'At least one appliance is required when appliance cover is selected',
      path: ['appliances']
    })
  }
})

export type ApplianceFormData = z.infer<typeof applianceSchema>
export type SaleFormData = z.infer<typeof saleSchema>

export const APPLIANCE_OPTIONS = [
  'Refrigerator',
  'Freezer', 
  'Fridge-freezer',
  'Electric cooker',
  'Gas cooker',
  'Electric hob',
  'Gas hob',
  'Induction hob',
  'Oven (electric or gas)',
  'Microwave oven',
  'Dishwasher',
  'Cooker hood / extractor fan',
  'Kettle',
  'Toaster',
  'Coffee machine',
  'Food processor',
  'Blender',
  'Slow cooker',
  'Air fryer',
  'Rice cooker',
  'Washing machine',
  'Washer-dryer',
  'Tumble dryer',
  'Condenser dryer',
  'Heat pump dryer',
  'Iron',
  'Steam generator iron',
  'Television',
  'Smart TV',
  'Soundbar',
  'Home cinema system',
  'DVD / Blu-ray player',
  'Games console',
  'Set-top box (e.g. Freeview, Sky, Virgin)',
  'Vacuum cleaner',
  'Cordless vacuum',
  'Robot vacuum',
  'Carpet cleaner',
  'Steam mop',
  'Floor polisher',
  'Electric heater',
  'Gas heater',
  'Fan heater',
  'Oil-filled radiator',
  'Air conditioner',
  'Portable fan',
  'Dehumidifier',
  'Humidifier',
  'Air purifier',
  'Electric shower',
  'Hair dryer',
  'Hair straighteners',
  'Electric shaver',
  'Electric toothbrush'
]

export const TITLE_OPTIONS = [
  'Mr',
  'Mrs', 
  'Miss',
  'Dr'
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
    currency: 'GBP',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
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