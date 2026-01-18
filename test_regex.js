const html = `Test {{#if boilerCost}}Boiler content here{{/if}} end`;
const data = { boilerCost: '£24.99' };

console.log('Original:', html);

// Test the current regex pattern 
const result = html.replace(/\{\{#if ([^}]+)\}\}((?:[^{]|\{(?!{))*?)\{\{\/if\}\}/g,
  (match, condition, content) => {
    console.log('Match found:', { match, condition, content });
    const value = data[condition.trim()];
    console.log('Condition value:', value);
    return value ? content : '';
  }
);

console.log('Result:', result);

// Test simpler regex
const result2 = html.replace(/\{\{#if ([^}]+)\}\}(.*?)\{\{\/if\}\}/g,
  (match, condition, content) => {
    console.log('Simple match found:', { match, condition, content });
    const value = data[condition.trim()];
    return value ? content : '';
  }
);

console.log('Simple result:', result2);