import { PrismaClient } from '@prisma/client'
import { EnhancedTemplateService } from './src/lib/paperwork/enhanced-template-service'

const prisma = new PrismaClient()

async function testFixedDocumentGeneration() {
  try {
    console.log("🧪 Testing fixed document generation...")

    const sale = await prisma.sale.findFirst({
      include: {
        appliances: true,
        createdBy: { select: { email: true } }
      }
    })

    if (!sale) {
      console.error("No sale found!")
      return
    }

    const templateData = {
      customerName: `${sale.customerFirstName} ${sale.customerLastName}`,
      email: sale.email,
      phone: sale.phoneNumber,
      address: `${sale.mailingStreet}, ${sale.mailingCity}, ${sale.mailingProvince}, ${sale.mailingPostalCode}`,
      coverageStartDate: new Date().toLocaleDateString("en-GB"),
      policyNumber: `TFT${String(Math.floor(Math.random() * 10000)).padStart(4, "0")}`,
      totalCost: (sale.totalPlanCost * 12).toFixed(2),
      monthlyCost: sale.totalPlanCost.toFixed(2),
      hasApplianceCover: sale.applianceCoverSelected,
      hasBoilerCover: sale.boilerCoverSelected,
      appliances: sale.appliances.map(appliance => ({
        name: appliance.appliance + (appliance.otherText ? ` (${appliance.otherText})` : ""),
        coverLimit: `£${appliance.coverLimit.toFixed(2)}`,
        monthlyCost: `£${appliance.cost.toFixed(2)}`
      })),
      boilerCost: sale.boilerPriceSelected ? `£${sale.boilerPriceSelected.toFixed(2)}` : null,
      currentDate: new Date().toLocaleDateString("en-GB", { 
        day: "numeric", month: "long", year: "numeric"
      }),
      agreement: {
        coverage: {
          hasBoilerCover: sale.boilerCoverSelected,
          boilerPriceFormatted: sale.boilerPriceSelected ? `£${sale.boilerPriceSelected.toFixed(2)}/month` : null
        }
      },
      metadata: {
        agentName: sale.agentName || sale.createdBy?.email || "Flash Team Support"
      }
    }

    console.log("📝 Appliances:", templateData.appliances)
    console.log("📝 Agreement coverage:", templateData.agreement.coverage)

    const enhancedTemplateService = new EnhancedTemplateService()
    const result = await enhancedTemplateService.generateDocument("welcome-letter", templateData)

    const hasRawConditionals = result.includes("{{#if") || result.includes("{{/if}}")
    console.log("❌ Has unprocessed conditionals:", hasRawConditionals)
    
    const hasBoilerContent = result.includes("Boiler Coverage")
    console.log("✅ Has boiler content:", hasBoilerContent)
    
    if (hasRawConditionals) {
      const matches = result.match(/\{\{#if[^}]*\}\}|\{\{\/if\}\}/g)
      console.log("Raw conditionals found:", matches)
    }

  } catch (error) {
    console.error("❌ Error:", error)
  } finally {
    await prisma.$disconnect()
  }
}

testFixedDocumentGeneration()
