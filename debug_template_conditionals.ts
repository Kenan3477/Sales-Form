import { EnhancedTemplateService } from './src/lib/paperwork/enhanced-template-service';

const templateService = new EnhancedTemplateService();

const testData = {
  customer: { firstName: 'John', lastName: 'Doe' },
  agreement: {
    planCost: 31.48,
    hasBoilerCover: true,
    boilerCost: 15.00,
    totalPlanCost: 46.48
  },
  boilerCover: {
    enabled: true,
    cost: 15.00
  },
  appliances: [
    {
      appliance: 'Washing Machine',
      cover_limit: '£500',
      cost_per_appliance: '£8.50'
    }
  ]
};

const testTemplate = `
<h2>Customer: {{customer.firstName}} {{customer.lastName}}</h2>
<p>Plan Cost: £{{agreement.planCost}}</p>

{{#if agreement.hasBoilerCover}}
<div class="boiler-section">
  <h3>Boiler Cover</h3>
  <p>Monthly Cost: £{{agreement.boilerCost}}</p>
  <p>Coverage included!</p>
</div>
{{/if}}

{{#if appliances.length}}
<div class="appliances-section">
  <h3>Appliances</h3>
  {{#each appliances}}
  <div class="appliance">
    <p>{{appliance}}: {{cover_limit}} ({{cost_per_appliance}}/month)</p>
    {{#if ../agreement.hasBoilerCover}}
    <p>Boiler cover is also included</p>
    {{/if}}
  </div>
  {{/each}}
</div>
{{/if}}
`;

console.log('🧪 Testing template processing...');
console.log('📊 Test data:', JSON.stringify(testData, null, 2));
console.log('\n📝 Template:');
console.log(testTemplate);
console.log('\n🔄 Processing...\n');

const result = templateService.processTemplate(testTemplate, testData);

console.log('\n✅ Final result:');
console.log(result);