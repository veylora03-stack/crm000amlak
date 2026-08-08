<template>
  <AppLayout>
    <PageHeader title="مدیریت کاربران" description="ایجاد، ویرایش و مدیریت کاربران سیستم" />
    <UsersManagement />
  </AppLayout>
</template>

<script setup>
import AppLayout from '@/layouts/AppLayout.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import UsersManagement from '@/components/settings/UsersManagement.vue'
</script>
