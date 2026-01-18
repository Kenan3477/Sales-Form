// Test the improved conditional regex processing
const testTemplate = `
{{#if appliances.length}}
<div class="appliance-section">
  {{#each appliances}}
  <div class="row">
    <div class="label">{{name}}</div>
  </div>
  {{/each}}
  {{#if boilerCost}}
  <div class="row">
    <div class="label">Boiler & Central Heating</div>
    <div class="value">Full system cover - {{boilerCost}}/month</div>
  </div>
  {{/if}}
</div>
{{/if}}
`;

const testData = {
  appliances: [{ name: 'Washing Machine' }],
  boilerCost: '£24.99'
};

function getNestedValue(obj, path) {
  return path.split('.').reduce((current, key) => current && current[key], obj);
}

console.log('🧪 Testing improved conditional processing...');

// First process each blocks (simulated)
let processedHtml = testTemplate.replace(/\{\{#each ([^}]+)\}\}([\s\S]*?)\{\{\/each\}\}/g, 
  (match, arrayName, blockContent) => {
    const arrayValue = getNestedValue(testData, arrayName.trim());
    if (Array.isArray(arrayValue)) {
      return arrayValue.map((item) => {
        return blockContent.replace(/\{\{([^}]+)\}\}/g, (varMatch, varKey) => {
          const value = getNestedValue(item, varKey.trim());
          return value !== undefined ? String(value) : varMatch;
        });
      }).join('');
    }
    return '';
  }
);

console.log('After {{#each}} processing:');
console.log(processedHtml);

// Now test the improved conditional processing
let attempts = 0;
const maxAttempts = 20;

while (attempts < maxAttempts) {
  const initialHtml = processedHtml;
  
  const conditionalsBefore = (processedHtml.match(/\{\{#if/g) || []).length;
  console.log(`\n🔧 Attempt ${attempts + 1}: Found ${conditionalsBefore} conditionals`);
  
  if (conditionalsBefore === 0) {
    console.log(`🔧 No more conditionals to process`);
    break;
  }
  
  // Look for simple conditionals (that don't contain nested conditionals)  
  const simpleConditionalRegex = /\{\{#if ([^}]+)\}\}([^{]*(?:\{(?!#if)[^}]*\}[^{]*)*)\{\{\/if\}\}/;
  const match = processedHtml.match(simpleConditionalRegex);
  
  if (match) {
    const [fullMatch, condition, content] = match;
    console.log(`🔧 Processing simple conditional: "${condition.trim()}"`);
    console.log(`🔧 Content preview: "${content.substring(0, 100)}..."`);
    
    const conditionValue = getNestedValue(testData, condition.trim());
    console.log(`🔧 Condition value for "${condition.trim()}":`, conditionValue, typeof conditionValue);
    
    const result = conditionValue ? content : '';
    console.log(`🔧 Will ${conditionValue ? 'INCLUDE' : 'EXCLUDE'} content`);
    
    processedHtml = processedHtml.replace(fullMatch, result);
  } else {
    console.log(`🔧 No simple conditionals found, trying fallback`);
    break;
  }
  
  attempts++;
  
  if (processedHtml === initialHtml) {
    console.log(`🔧 No changes made, stopping`);
    break;
  }
}

console.log('\n✅ Final result:');
console.log(processedHtml);