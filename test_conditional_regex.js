// Test the conditional regex processing
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

console.log('🧪 Original template:');
console.log(testTemplate);

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

console.log('\n🔧 After processing {{#each}}:');
console.log(processedHtml);

// Then process conditionals
console.log('\n🔧 Looking for conditionals...');
const conditionalMatches = processedHtml.match(/\{\{#if ([^}]+)\}\}/g) || [];
console.log('Found conditionals:', conditionalMatches);

processedHtml = processedHtml.replace(/\{\{#if ([^}]+)\}\}([\s\S]*?)\{\{\/if\}\}/g,
  (match, condition, content) => {
    console.log(`\n🔧 Processing conditional: "${condition.trim()}"`);
    console.log(`🔧 Full match: "${match}"`);
    console.log(`🔧 Content: "${content}"`);
    const conditionValue = getNestedValue(testData, condition.trim());
    console.log(`🔧 Condition value:`, conditionValue);
    const result = conditionValue ? content : '';
    console.log(`🔧 Result:`, result ? 'INCLUDE' : 'EXCLUDE');
    return result;
  }
);

console.log('\n✅ Final result:');
console.log(processedHtml);