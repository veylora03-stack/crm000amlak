<template>
  <div class="relative flex min-h-screen items-center justify-center overflow-hidden bg-app-bg-light px-4 py-10 dark:bg-app-bg-dark">
    <!-- Subtle gradient orbs -->
    <div class="pointer-events-none absolute top-0 left-1/2 -z-10 h-[500px] w-[800px] -translate-x-1/2 rounded-full bg-gradient-to-br from-brand-500/10 via-accent-500/5 to-transparent blur-3xl" aria-hidden="true"></div>
    <div class="pointer-events-none absolute bottom-0 right-0 -z-10 h-[400px] w-[600px] rounded-full bg-gradient-to-tl from-brand-400/8 to-transparent blur-3xl" aria-hidden="true"></div>

    <div class="relative w-full max-w-sm animate-fade-in">
      <!-- Logo -->
      <div class="mb-8 text-center">
        <div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 shadow-glow">
          <svg class="h-6 w-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
            <polyline points="9 22 9 12 15 12 15 22"></polyline>
          </svg>
        </div>
        <h1 class="text-2xl font-bold tracking-tight">
          <slot name="title">ورود به حساب</slot>
        </h1>
        <p class="mt-1.5 text-sm text-base-500 dark:text-base-400">
          <slot name="subtitle">برای ادامه وارد حساب خود شوید</slot>
        </p>
      </div>

      <!-- Card -->
      <div class="card p-6">
        <slot />
      </div>

      <p class="mt-6 text-center text-[11px] text-base-400">
        © ۱۴۰۵ — تمامی حقوق محفوظ است
      </p>
    </div>
  </div>
</template>
