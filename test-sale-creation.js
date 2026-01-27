const https = require('https')
const http = require('http')

function makeAuthenticatedRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url)
    const client = urlObj.protocol === 'https:' ? https : http
    
    const req = client.request({
      hostname: urlObj.hostname,
      port: urlObj.port || (urlObj.protocol === 'https:' ? 443 : 80),
      path: urlObj.pathname,
      method: options.method || 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    }, (res) => {
      let data = ''
      res.on('data', chunk => data += chunk)
      res.on('end', () => {
        console.log(`Response Status: ${res.statusCode}`)
        console.log(`Response Headers:`, res.headers)
        console.log(`Response Body:`, data)
        
        try {
          const jsonData = JSON.parse(data)
          resolve({ status: res.statusCode, data: jsonData, text: data })
        } catch {
          resolve({ status: res.statusCode, text: data })
        }
      })
    })
    
    req.on('error', (error) => {
      console.error('Request error:', error)
      reject(error)
    })
    
    if (options.body) {
      req.write(options.body)
    }
    
    req.end()
  })
}

async function testSaleCreation() {
  console.log('🔄 Testing sale creation to reproduce error...')
  
  try {
    // Test sale data
    const testSale = {
      customerFirstName: "Test",
      customerLastName: "Customer",
      title: "Mr",
      phoneNumber: "07999888777", // Use a unique number to avoid duplicates
      email: "test.customer@example.com",
      notes: "Test sale for error debugging",
      mailingStreet: "123 Test Street",
      mailingCity: "Test City",
      mailingProvince: "Test County", 
      mailingPostalCode: "TS1 1TS",
      accountName: "Test Account",
      sortCode: "123456",
      accountNumber: "12345678",
      directDebitDate: new Date().toISOString(),
      applianceCoverSelected: true,
      boilerCoverSelected: false,
      appliances: [
        {
          type: "Washing Machine",
          cost: 12.99
        }
      ],
      agentId: "test-agent-id",
      agentName: "Test Agent"
    }
    
    console.log('📝 Attempting to create test sale...')
    
    const response = await makeAuthenticatedRequest('http://localhost:3000/api/sales', {
      method: 'POST',
      body: JSON.stringify(testSale)
    })
    
    if (response.status === 401) {
      console.log('⚠️ Authentication required - this is expected without session')
      console.log('The error likely occurs after authentication')
    } else if (response.status >= 400) {
      console.log(`❌ Error ${response.status}:`, response.text)
    } else {
      console.log('✅ Sale created successfully')
    }
    
  } catch (error) {
    console.error('❌ Test failed:', error.message)
  }
}

testSaleCreation()