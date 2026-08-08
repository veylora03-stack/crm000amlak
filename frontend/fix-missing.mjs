import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load the report
const reportPath = '../test-results/detailed-report.json';
const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));

// Filter only missing_component errors
const missingComponents = report.issues.filter(i => i.type === 'missing_component');

console.log(`🔍 Found ${missingComponents.length} missing component reports\n`);

// Normalize path for current OS
function normalizePath(p) {
  return p.replace(/[\\/]/g, path.sep);
}

// Track what we need to create
const toCreate = [];
const falsePositives = [];

// Check each missing component
missingComponents.forEach(issue => {
  const relativePath = normalizePath(issue.missing);
  const fullPath = path.join('src', 'components', relativePath);
  
  if (!fs.existsSync(fullPath)) {
    toCreate.push({
      file: issue.file,
      component: relativePath,
      fullPath: fullPath
    });
  } else {
    falsePositives.push({
      file: issue.file,
      component: relativePath
    });
  }
});

console.log(`✅ False positives (already exist): ${falsePositives.length}`);
console.log(`❌ Actually missing: ${toCreate.length}\n`);

if (falsePositives.length > 0) {
  console.log('📋 False positives (no action needed):');
  falsePositives.slice(0, 10).forEach(fp => {
    console.log(`  ✓ ${fp.component}`);
  });
  if (falsePositives.length > 10) {
    console.log(`  ... and ${falsePositives.length - 10} more`);
  }
  console.log('');
}

// Create missing components with proper templates
if (toCreate.length > 0) {
  console.log(`🏗️  Creating ${toCreate.length} missing components...\n`);
  
  toCreate.forEach(item => {
    const dir = path.dirname(item.fullPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    // Generate appropriate template based on component name
    let template = '';
    const componentName = path.basename(item.component, '.vue');
    
    if (componentName.includes('Modal')) {
      template = `<template>
  <Modal :open="open" :title="title" size="md" @close="$emit('close')">
    <slot />
    <template #footer>
      <slot name="footer">
        <button class="btn-secondary" @click="$emit('close')">بستن</button>
      </slot>
    </template>
  </Modal>
</template>

<script setup>
import Modal from '@/components/ui/Modal.vue'

defineProps({
  open: { type: Boolean, default: false },
  title: { type: String, default: '' }
})

defineEmits(['close'])
</script>
`;
    } else if (componentName.includes('Drawer')) {
      template = `<template>
  <Drawer :open="open" :title="title" @close="$emit('close')">
    <slot />
    <template #footer>
      <slot name="footer">
        <button class="btn-secondary" @click="$emit('close')">بستن</button>
      </slot>
    </template>
  </Drawer>
</template>

<script setup>
import Drawer from '@/components/ui/Drawer.vue'

defineProps({
  open: { type: Boolean, default: false },
  title: { type: String, default: '' }
})

defineEmits(['close'])
</script>
`;
    } else if (componentName.includes('Filters') || componentName.includes('Selector')) {
      template = `<template>
  <div class="card p-4">
    <slot />
  </div>
</template>

<script setup>
defineProps({
  modelValue: { type: Object, default: () => ({}) }
})

defineEmits(['update:modelValue'])
</script>
`;
    } else if (componentName.includes('Table') || componentName.includes('List')) {
      template = `<template>
  <div class="card overflow-hidden">
    <slot />
  </div>
</template>

<script setup>
defineProps({
  items: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false }
})

defineEmits(['click'])
</script>
`;
    } else if (componentName.includes('Gallery') || componentName.includes('Images')) {
      template = `<template>
  <div class="grid gap-4 md:grid-cols-3">
    <slot />
  </div>
</template>

<script setup>
defineProps({
  images: { type: Array, default: () => [] }
})

defineEmits(['click'])
</script>
`;
    } else if (componentName.includes('Map')) {
      template = `<template>
  <div class="card overflow-hidden" style="height: 400px;">
    <slot />
  </div>
</template>

<script setup>
defineProps({
  latitude: { type: Number, default: null },
  longitude: { type: Number, default: null }
})
</script>
`;
    } else if (componentName.includes('Timeline') || componentName.includes('Deals') || componentName.includes('Notes')) {
      template = `<template>
  <div class="space-y-3">
    <slot />
  </div>
</template>

<script setup>
defineProps({
  items: { type: Array, default: () => [] }
})

defineEmits(['click'])
</script>
`;
    } else if (componentName.includes('Export')) {
      template = `<template>
  <button class="btn-secondary" @click="$emit('export')">
    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
    </svg>
    خروجی
  </button>
</template>

<script setup>
defineEmits(['export'])
</script>
`;
    } else {
      template = `<template>
  <div class="card p-4">
    <slot />
  </div>
</template>

<script setup>
defineProps({
  loading: { type: Boolean, default: false }
})
</script>
`;
    }
    
    fs.writeFileSync(item.fullPath, template);
    console.log(`  ✓ Created: ${item.component}`);
  });
  
  console.log(`\n✅ Created ${toCreate.length} missing components`);
} else {
  console.log('✨ All components exist! No creation needed.');
}

// Save updated report
report.fixed = {
  falsePositives: falsePositives.length,
  created: toCreate.length,
  createdList: toCreate.map(c => c.component)
};

fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));

console.log(`\n📄 Updated report saved to: ${reportPath}`);
console.log('\n🚀 Run "npm run dev" to see the fixes!');
