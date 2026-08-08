import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const results = {
  timestamp: new Date().toISOString(),
  pages: [],
  components: [],
  stores: [],
  utils: [],
  issues: [],
  recommendations: []
};

function findFiles(dir, extension) {
  const files = [];
  if (!fs.existsSync(dir)) return files;
  
  const items = fs.readdirSync(dir, { withFileTypes: true });
  
  for (const item of items) {
    const fullPath = path.join(dir, item.name);
    if (item.isDirectory()) {
      files.push(...findFiles(fullPath, extension));
    } else if (item.name.endsWith(extension)) {
      files.push(fullPath);
    }
  }
  
  return files;
}

function extractImports(content, pattern) {
  const imports = [];
  const regex = new RegExp(pattern, 'g');
  let match;
  
  while ((match = regex.exec(content)) !== null) {
    imports.push(match[1]);
  }
  
  return imports;
}

function fileExists(filePath) {
  return fs.existsSync(filePath);
}

console.log('🔍 Starting comprehensive analysis...\n');

// 1. Analyze pages
console.log('[1/5] Analyzing pages...');
const pages = findFiles('src/pages', '.vue');
results.pages = pages.map(p => path.relative('src/pages', p));
console.log(`  ✓ Found ${pages.length} pages\n`);

// 2. Analyze components
console.log('[2/5] Analyzing components...');
const components = findFiles('src/components', '.vue');
results.components = components.map(c => path.relative('src/components', c));
console.log(`  ✓ Found ${components.length} components\n`);

// 3. Check imports in all Vue files
console.log('[3/5] Checking imports...');
const allVueFiles = [...pages, ...components];
let missingComponents = 0;
let missingStores = 0;
let missingUtils = 0;

allVueFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  const fileName = path.relative('src', file);
  
  const componentImports = extractImports(content, /from\s+['"]@\/components\/([^'"]+)['"]/);
  componentImports.forEach(imp => {
    const fullPath = path.join('src/components', imp + '.vue');
    if (!fileExists(fullPath)) {
      missingComponents++;
      results.issues.push({
        type: 'missing_component',
        file: fileName,
        missing: imp,
        severity: 'error'
      });
    }
  });
  
  const storeImports = extractImports(content, /from\s+['"]@\/stores\/([^'"]+)['"]/);
  storeImports.forEach(imp => {
    const fullPath = path.join('src/stores', imp + '.js');
    if (!fileExists(fullPath)) {
      missingStores++;
      results.issues.push({
        type: 'missing_store',
        file: fileName,
        missing: imp,
        severity: 'error'
      });
    }
  });
  
  const utilImports = extractImports(content, /from\s+['"]@\/utils\/([^'"]+)['"]/);
  utilImports.forEach(imp => {
    const fullPath = path.join('src/utils', imp + '.js');
    if (!fileExists(fullPath)) {
      missingUtils++;
      results.issues.push({
        type: 'missing_util',
        file: fileName,
        missing: imp,
        severity: 'error'
      });
    }
  });
});

console.log(`  ✗ Missing components: ${missingComponents}`);
console.log(`  ✗ Missing stores: ${missingStores}`);
console.log(`  ✗ Missing utils: ${missingUtils}\n`);

// 4. Check for common issues
console.log('[4/5] Checking for common issues...');
let hardcodedColors = 0;
let inlineStyles = 0;
let oldClasses = 0;

allVueFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  const fileName = path.relative('src', file);
  
  const colors = content.match(/#[0-9a-fA-F]{6}/g) || [];
  if (colors.length > 5) {
    hardcodedColors += colors.length;
    results.issues.push({
      type: 'hardcoded_colors',
      file: fileName,
      count: colors.length,
      severity: 'warning'
    });
  }
  
  const styles = content.match(/style=['"][^'"]+['"]/g) || [];
  if (styles.length > 3) {
    inlineStyles += styles.length;
    results.issues.push({
      type: 'inline_styles',
      file: fileName,
      count: styles.length,
      severity: 'info'
    });
  }
  
  const oldClassPatterns = ['card-old', 'btn-old', 'input-old'];
  oldClassPatterns.forEach(pattern => {
    if (content.includes(pattern)) {
      oldClasses++;
      results.issues.push({
        type: 'old_class',
        file: fileName,
        class: pattern,
        severity: 'warning'
      });
    }
  });
});

console.log(`  ⚠ Hardcoded colors: ${hardcodedColors}`);
console.log(`  ⚠ Inline styles: ${inlineStyles}`);
console.log(`  ⚠ Old classes: ${oldClasses}\n`);

// 5. Generate recommendations
console.log('[5/5] Generating recommendations...');

if (missingComponents > 0) {
  results.recommendations.push(`Fix ${missingComponents} missing component imports`);
}
if (missingStores > 0) {
  results.recommendations.push(`Fix ${missingStores} missing store imports`);
}
if (missingUtils > 0) {
  results.recommendations.push(`Fix ${missingUtils} missing utility imports`);
}
if (hardcodedColors > 10) {
  results.recommendations.push(`Refactor ${hardcodedColors} hardcoded colors to use design tokens`);
}
if (inlineStyles > 10) {
  results.recommendations.push(`Convert ${inlineStyles} inline styles to CSS classes`);
}
if (oldClasses > 0) {
  results.recommendations.push(`Update ${oldClasses} old class names to new design system`);
}

results.recommendations.push('Add error boundaries to catch runtime errors');
results.recommendations.push('Implement proper error handling in API calls');
results.recommendations.push('Add loading states to all async operations');
results.recommendations.push('Consider code splitting for large components');

console.log(`  ✓ Generated ${results.recommendations.length} recommendations\n`);

// Save results
const reportPath = '../test-results/detailed-report.json';
fs.writeFileSync(reportPath, JSON.stringify(results, null, 2));

console.log('=====================================');
console.log('         Analysis Complete           ');
console.log('=====================================\n');
console.log('📊 Summary:');
console.log(`  Pages: ${results.pages.length}`);
console.log(`  Components: ${results.components.length}`);
console.log(`  Issues: ${results.issues.length}`);
console.log(`  Recommendations: ${results.recommendations.length}\n`);

if (results.issues.length > 0) {
  console.log('🚨 Critical Issues:');
  results.issues
    .filter(i => i.severity === 'error')
    .slice(0, 10)
    .forEach(issue => {
      console.log(`  ❌ ${issue.file}: ${issue.type} - ${issue.missing}`);
    });
  console.log('');
}

if (results.issues.filter(i => i.severity === 'warning').length > 0) {
  console.log('⚠️  Warnings:');
  results.issues
    .filter(i => i.severity === 'warning')
    .slice(0, 10)
    .forEach(issue => {
      console.log(`  ⚠️  ${issue.file}: ${issue.type}`);
    });
  console.log('');
}

console.log('💡 Top Recommendations:');
results.recommendations.slice(0, 5).forEach(rec => {
  console.log(`  • ${rec}`);
});
console.log('');

console.log(`📄 Full report: ${reportPath}`);
