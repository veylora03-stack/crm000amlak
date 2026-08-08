# سیستم رنگ — CRM تخصصی املاک

این سند سیستم رنگی محصول را برای حالت روشن، حالت تاریک، کامپوننت‌ها، پیام‌های وضعیت و نمودارها تعریف می‌کند. تمام رنگ‌ها باید از توکن‌های معنایی استفاده کنند و مستقیماً در کامپوننت‌ها hardcode نشوند.

---

## 1. اصول کلی

- رنگ‌ها باید معنایی باشند، نه تزئینی.
- هر رنگ باید در هر دو حالت Light و Dark قابل استفاده باشد.
- کنتراست متن و پس‌زمینه باید حداقل AA باشد.
- از رنگ‌های خیلی اشباع‌شده در پس‌زمینه‌های بزرگ استفاده نشود.
- در Dark Mode از مشکی خالص استفاده نشود.
- در Light Mode از سفید خالص برای سطح‌ها استفاده شود، اما پس‌زمینه صفحه کمی خاکستری باشد.
- رنگ نباید تنها وسیله انتقال معنا باشد؛ باید با آیکون یا متن همراه شود.
- رنگ‌های وضعیت در کل محصول یکسان باشند.

---

## 2. توکن‌های اصلی رنگ

| توکن | نقش | کاربرد |
|---|---|---|
| `primary` | رنگ اصلی | دکمه اصلی، لینک، فوکوس، انتخاب فعال |
| `secondary` | رنگ ثانویه | دکمه ثانویه، عناصر کم‌اهمیت‌تر، Tagها |
| `success` | موفقیت | Toast موفقیت، وضعیت‌های مثبت، Done |
| `warning` | هشدار | وضعیت‌های نیازمند توجه، Overdue نزدیک |
| `danger` | خطر | خطا، حذف، پیام‌های ناموفق |
| `info` | اطلاع | پیام اطلاعاتی، وضعیت خنثی مهم |
| `neutral` | خنثی | متن، border، آیکون، پس‌زمینه‌های کم‌رنگ |
| `background` | پس‌زمینه صفحه | بدنه اصلی صفحه |
| `surface` | سطح | کارت، Modal، Drawer، جدول |
| `border` | خط جداکننده | Input، جدول، Separator |

---

## 3. پالت روشن — Light Mode

### رنگ‌های پایه

| توکن | مقدار پیشنهادی | کاربرد |
|---|---|---|
| `background` | `#f8fafc` | پس‌زمینه اصلی صفحه |
| `surface` | `#ffffff` | کارت، Modal، جدول |
| `surface-muted` | `#f1f5f9` | پس‌زمینه کم‌رنگ برای Empty State یا Skeleton |
| `border` | `#e2e8f0` | Border استاندارد |
| `border-strong` | `#cbd5e1` | Separator قوی |
| `text-primary` | `#0f172a` | متن اصلی |
| `text-secondary` | `#475569` | متن ثانویه |
| `text-muted` | `#94a3b8` | Placeholder، متن کم‌اهمیت |
| `text-disabled` | `#cbd5e1` | متن غیرفعال |

### Primary

| توکن | مقدار پیشنهادی | کاربرد |
|---|---|---|
| `primary-50` | `#eff6ff` | پس‌زمینه ملایم primary |
| `primary-100` | `#dbeafe` | Hover ملایم |
| `primary-500` | `#3b82f6` | رنگ اصلی روشن‌تر |
| `primary-600` | `#2563eb` | دکمه اصلی، لینک |
| `primary-700` | `#1d4ed8` | Hover دکمه اصلی |
| `primary-900` | `#1e3a8a` | متن روی پس‌زمینه روشن primary |

### Secondary

| توکن | مقدار پیشنهادی | کاربرد |
|---|---|---|
| `secondary-50` | `#f8fafc` | پس‌زمینه کم‌رنگ |
| `secondary-100` | `#f1f5f9` | پس‌زمینه Tag |
| `secondary-500` | `#64748b` | دکمه ثانویه، آیکون |
| `secondary-700` | `#334155` | متن دکمه ثانویه |

### Success

| توکن | مقدار پیشنهادی | کاربرد |
|---|---|---|
| `success-50` | `#f0fdf4` | پس‌زمینه موفقیت |
| `success-500` | `#22c55e` | آیکون موفقیت |
| `success-600` | `#16a34a` | متن موفقیت |
| `success-700` | `#15803d` | متن قوی موفقیت |

### Warning

| توکن | مقدار پیشنهادی | کاربرد |
|---|---|---|
| `warning-50` | `#fffbeb` | پس‌زمینه هشدار |
| `warning-500` | `#f59e0b` | آیکون هشدار |
| `warning-600` | `#d97706` | متن هشدار |
| `warning-700` | `#b45309` | متن قوی هشدار |

### Danger

| توکن | مقدار پیشنهادی | کاربرد |
|---|---|---|
| `danger-50` | `#fef2f2` | پس‌زمینه خطا |
| `danger-500` | `#ef4444` | آیکون خطا |
| `danger-600` | `#dc2626` | دکمه خطرناک، متن خطا |
| `danger-700` | `#b91c1c` | Hover دکمه خطرناک |

### Info

| توکن | مقدار پیشنهادی | کاربرد |
|---|---|---|
| `info-50` | `#eff6ff` | پس‌زمینه اطلاعات |
| `info-500` | `#3b82f6` | آیکون اطلاعات |
| `info-600` | `#2563eb` | متن اطلاعات |
| `info-700` | `#1d4ed8` | متن قوی اطلاعات |

---

## 4. پالت تاریک — Dark Mode

### رنگ‌های پایه

| توکن | مقدار پیشنهادی | کاربرد |
|---|---|---|
| `background` | `#0f172a` | پس‌زمینه اصلی صفحه |
| `surface` | `#1e293b` | کارت، Modal، جدول |
| `surface-muted` | `#273449` | Skeleton، Empty State |
| `border` | `#334155` | Border استاندارد |
| `border-strong` | `#475569` | Separator قوی |
| `text-primary` | `#e2e8f0` | متن اصلی |
| `text-secondary` | `#94a3b8` | متن ثانویه |
| `text-muted` | `#64748b` | Placeholder |
| `text-disabled` | `#475569` | متن غیرفعال |

### Primary در Dark Mode

| توکن | مقدار پیشنهادی | کاربرد |
|---|---|---|
| `primary-500` | `#3b82f6` | دکمه اصلی |
| `primary-400` | `#60a5fa` | Hover دکمه اصلی |
| `primary-300` | `#93c5fd` | لینک یا متن روی سطح تیره |
| `primary-900` | `#1e3a8a` | پس‌زمینه ملایم انتخاب‌شده |

### Secondary در Dark Mode

| توکن | مقدار پیشنهادی | کاربرد |
|---|---|---|
| `secondary-500` | `#64748b` | آیکون و متن کم‌رنگ |
| `secondary-400` | `#94a3b8` | متن ثانویه |
| `secondary-800` | `#1e293b` | سطح |
| `secondary-900` | `#0f172a` | پس‌زمینه |

### Success در Dark Mode

| توکن | مقدار پیشنهادی | کاربرد |
|---|---|---|
| `success-500` | `#22c55e` | آیکون موفقیت |
| `success-400` | `#4ade80` | متن موفقیت |
| `success-900` | `#14532d` | پس‌زمینه ملایم موفقیت |

### Warning در Dark Mode

| توکن | مقدار پیشنهادی | کاربرد |
|---|---|---|
| `warning-500` | `#f59e0b` | آیکون هشدار |
| `warning-400` | `#fbbf24` | متن هشدار |
| `warning-900` | `#78350f` | پس‌زمینه ملایم هشدار |

### Danger در Dark Mode

| توکن | مقدار پیشنهادی | کاربرد |
|---|---|---|
| `danger-500` | `#ef4444` | آیکون خطا |
| `danger-400` | `#f87171` | متن خطا |
| `danger-900` | `#7f1d1d` | پس‌زمینه ملایم خطا |

### Info در Dark Mode

| توکن | مقدار پیشنهادی | کاربرد |
|---|---|---|
| `info-500` | `#3b82f6` | آیکون اطلاعات |
| `info-400` | `#60a5fa` | متن اطلاعات |
| `info-900` | `#1e3a8a` | پس‌زمینه ملایم اطلاعات |

---

## 5. رنگ‌های وضعیت در جدول‌ها و Badgeها

| وضعیت | نوع | رنگ پیشنهادی |
|---|---|---|
| New / جدید | info | `info-50` / `info-600` در Light، `info-900` / `info-400` در Dark |
| Contacted / تماس گرفته شد | info | `info-50` / `info-600` |
| Qualified / واجد شرایط | success | `success-50` / `success-600` |
| Unqualified / فاقد شرایط | neutral | `secondary-100` / `secondary-700` |
| Negotiating / در حال مذاکره | warning | `warning-50` / `warning-600` |
| Won / برنده | success | `success-50` / `success-600` |
| Lost / بازنده | danger | `danger-50` / `danger-600` |
| Archived / آرشیو | neutral | `secondary-100` / `secondary-700` |
| Published / منتشرشده | success | `success-50` / `success-600` |
| Draft / پیش‌نویس | neutral | `secondary-100` / `secondary-700` |
| Reserved / رزروشده | warning | `warning-50` / `warning-600` |
| Sold / فروخته‌شده | success | `success-50` / `success-600` |
| Rented / اجاره‌داده‌شده | info | `info-50` / `info-600` |
| Expired / منقضی | danger | `danger-50` / `danger-600` |
| Todo | neutral | `secondary-100` / `secondary-700` |
| In Progress | info | `info-50` / `info-600` |
| Done | success | `success-50` / `success-600` |
| Cancelled | danger | `danger-50` / `danger-600` |

---

## 6. رنگ در کامپوننت‌ها

### Button

| نوع | پس‌زمینه | متن | Border |
|---|---|---|---|
| Primary | `primary-600` | سفید | بدون Border |
| Secondary | `surface` | `text-primary` | `border` |
| Ghost | شفاف | `text-secondary` | بدون Border |
| Danger | `danger-600` | سفید | بدون Border |
| Disabled | `surface-muted` | `text-disabled` | بدون Border |

### Input

| حالت | Border | پس‌زمینه | متن |
|---|---|---|---|
| Normal | `border` | `surface` | `text-primary` |
| Focus | `primary-500` | `surface` | `text-primary` |
| Error | `danger-500` | `surface` | `text-primary` |
| Disabled | `border` | `surface-muted` | `text-disabled` |

### Alert / Toast

| نوع | پس‌زمینه | متن | آیکون |
|---|---|---|---|
| Success | `success-50` | `success-700` | `success-600` |
| Warning | `warning-50` | `warning-700` | `warning-600` |
| Danger | `danger-50` | `danger-700` | `danger-600` |
| Info | `info-50` | `info-700` | `info-600` |

در Dark Mode، پس‌زمینه Alert باید از نسخه تیره مانند `success-900` یا `danger-900` استفاده کند و متن با رنگ روشن‌تر نمایش داده شود.

### Modal / Drawer

| عنصر | Light | Dark |
|---|---|---|
| Overlay | `rgba(15, 23, 42, 0.4)` | `rgba(0, 0, 0, 0.6)` |
| Surface | `#ffffff` | `#1e293b` |
| Border | `#e2e8f0` | `#334155` |
| Title | `#0f172a` | `#e2e8f0` |
| Body | `#475569` | `#94a3b8` |

### Sidebar

| عنصر | Light | Dark |
|---|---|---|
| Background | `#ffffff` | `#0f172a` |
| Item Text | `#475569` | `#94a3b8` |
| Active Background | `primary-50` | `#1e3a8a` با شفافیت ملایم |
| Active Text | `primary-700` | `#93c5fd` |
| Hover Background | `#f1f5f9` | `#1e293b` |

### Topbar

| عنصر | Light | Dark |
|---|---|---|
| Background | `#ffffff` | `#0f172a` |
| Border Bottom | `#e2e8f0` | `#334155` |
| Search Placeholder | `#94a3b8` | `#64748b` |
| Icon | `#64748b` | `#94a3b8` |

### Table

| عنصر | Light | Dark |
|---|---|---|
| Header Background | `#f8fafc` | `#0f172a` |
| Header Text | `#475569` | `#94a3b8` |
| Row Background | `#ffffff` | `#1e293b` |
| Row Hover | `#f8fafc` | `#273449` |
| Border | `#e2e8f0` | `#334155` |

---

## 7. رنگ در نمودارها

### پالت پیشنهادی نمودارها

| ترتیب | Light | Dark |
|---|---|---|
| 1 | `#2563eb` | `#60a5fa` |
| 2 | `#16a34a` | `#4ade80` |
| 3 | `#f59e0b` | `#fbbf24` |
| 4 | `#dc2626` | `#f87171` |
| 5 | `#7c3aed` | `#a78bfa` |
| 6 | `#0891b2` | `#22d3ee` |
| 7 | `#db2777` | `#f472b6` |

### قواعد نمودارها
- رنگ Funnel باید از طیف primary استفاده کند.
- وضعیت‌های Won/Lost باید با success/danger مشخص شوند.
- محورهای نمودار باید کم‌رنگ باشند.
- Tooltip باید از سطح `surface` و متن `text-primary` استفاده کند.
- رنگ نمودارها نباید با رنگ‌های وضعیت اشتباه گرفته شود.

---

## 8. رنگ در Pipeline و Kanban

| عنصر | Light | Dark |
|---|---|---|
| Board Background | `#f8fafc` | `#0f172a` |
| Column Background | `#f1f5f9` | `#1e293b` |
| Card Background | `#ffffff` | `#273449` |
| Card Border | `#e2e8f0` | `#334155` |
| Drag Shadow | `shadow-md` | `shadow-md` |
| Stage Indicator | رنگ Stage | همان رنگ Stage با کنتراست مناسب |

### رنگ Stageها
- هر Stage یک رنگ کم‌رنگ برای پس‌زمینه و یک رنگ قوی برای نقطه نشانگر دارد.
- Stage برنده از success استفاده کند.
- Stage بازنده از danger استفاده کند.
- Stageهای میانی از طیف info، warning یا neutral استفاده کنند.

---

## 9. رنگ فوکوس و دسترسی‌پذیری

| حالت | رنگ |
|---|---|
| Focus Ring | `primary-500` |
| Focus Shadow | `0 0 0 2px` با شفافیت primary |
| Danger Focus | `danger-500` |
| Success Focus | `success-500` |

### قواعد
- همه عناصر تعاملی باید focus visible داشته باشند.
- فوکوس نباید فقط با تغییر رنگ ظریف باشد.
- کنتراست متن دکمه Primary روی `primary-600` باید AA باشد.
- متن لینک باید از متن معمولی متمایز باشد.
- رنگ خطا باید با آیکون یا متن همراه باشد.

---

## 10. قواعد Tailwind

این رنگ‌ها باید در `tailwind.config.js` به‌صورت semantic تعریف شوند.

### نمونه ساختار پیشنهادی
- `colors.background`
- `colors.surface`
- `colors.surface-muted`
- `colors.border`
- `colors.border-strong`
- `colors.text-primary`
- `colors.text-secondary`
- `colors.text-muted`
- `colors.primary`
- `colors.secondary`
- `colors.success`
- `colors.warning`
- `colors.danger`
- `colors.info`

### قواعد
- در کامپوننت‌ها از کلاس‌هایی مانند `bg-primary-600` فقط از طریق توکن‌های semantic استفاده شود.
- برای Dark Mode از `dark:` استفاده شود.
- رنگ‌های خام فقط در config تعریف شوند.
- در صفحات از رنگ raw مانند `bg-[#123456]` استفاده نشود.

---

## 11. بایدها و نبایدها

### بایدها
- استفاده از توکن‌های معنایی
- حفظ کنتراست AA
- استفاده از رنگ ملایم برای پس‌زمینه Alert
- استفاده از آیکون در کنار رنگ وضعیت
- استفاده از Dark Mode جداگانه برای surface و border

### نبایدها
- استفاده از مشکی خالص `#000000` برای پس‌زمینه
- استفاده از سفید خالص برای متن روی رنگ‌های روشن
- استفاده از رنگ‌های متعدد برای دکمه‌های اصلی
- تغییر رنگ وضعیت در صفحات مختلف
- استفاده از opacity زیاد برای متن اصلی
- استفاده از رنگ بدون متن یا آیکون برای انتقال خطا

---

## 12. جمع‌بندی

| بخش | Light | Dark |
|---|---|---|
| Page Background | `#f8fafc` | `#0f172a` |
| Surface | `#ffffff` | `#1e293b` |
| Border | `#e2e8f0` | `#334155` |
| Text Primary | `#0f172a` | `#e2e8f0` |
| Text Secondary | `#475569` | `#94a3b8` |
| Primary | `#2563eb` | `#3b82f6` |
| Success | `#16a34a` | `#4ade80` |
| Warning | `#d97706` | `#fbbf24` |
| Danger | `#dc2626` | `#f87171` |
| Info | `#2563eb` | `#60a5fa` |
