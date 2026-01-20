# CSV Export Empty Fields - Troubleshooting Guide

## Current Status ✅
- **Database**: All 1,247 boiler sales have consistent data (✅ Fixed)
- **Export Logic**: Working correctly in tests (✅ Confirmed) 
- **Test Results**: William S Johnson shows Boiler: £29.99, App: £24.95

## Issue Resolution Steps

### 1. **Generate Fresh Export** 🔄
- Go to Sales Admin → Export Selected
- **Don't use old CSV files** - generate a completely new export
- The old CSV file was created before the data fix was applied

### 2. **Production API Fix** (If Still Empty)
If fresh export still shows empty fields, run this production fix:
```
POST /api/debug/fix-boiler-prices
```
- Requires admin login
- Will fix any remaining production inconsistencies
- Safe to run multiple times

### 3. **Verify Export Results** ✅
After fresh export, you should see:
- **Boiler Package Price (Internal)**: £29.99, £24.99, £19.99 (customer's selected price)
- **Single App Price (Internal)**: Sum of all appliances (e.g., £24.95)

## Data Quality Confirmation
```
Total Boiler Sales: 1,247
- Inconsistent: 0 ❌→✅
- Valid: 1,247 ✅
- Most common price: £29.99
```

## Next Steps
1. **Try fresh CSV export first** - should work now
2. If still empty → **Run production API fix** 
3. **Confirm results** show proper pricing data

The underlying data has been fixed, you just need a fresh export! 🎯