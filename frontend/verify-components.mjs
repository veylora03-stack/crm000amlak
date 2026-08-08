import fs from 'fs';
import path from 'path';

const reportPath = '../test-results/detailed-report.json';
const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));

const missingComponents = report.issues.filter(i => i.type === 'missing_component');

console.log(`\n🔍 Checking ${missingComponents.length} reported missing components...\n`);

let falsePositives = 0;
let actualMissing = 0;
const actualMissingList = [];

missingComponents.forEach(issue => {
    const relativePath = issue.missing.replace(/[\\/]/g, path.sep);
    const fullPath = path.join('src', 'components', relativePath);
    
    if (fs.existsSync(fullPath)) {
        falsePositives++;
    } else {
        actualMissing++;
        actualMissingList.push({
            file: issue.file,
            missing: issue.missing
        });
    }
});

console.log(`✅ False positives (already exist): ${falsePositives}`);
console.log(`❌ Actually missing: ${actualMissing}`);

if (actualMissing > 0) {
    console.log('\n⚠️  Actually missing components:');
    actualMissingList.forEach(item => {
        console.log(`  - ${item.file}: ${item.missing}`);
    });
} else {
    console.log('\n✨ All components exist! The 76 "missing" reports were all false positives.');
}
