# نقشه سایت — CRM تخصصی املاک

این سند ساختار صفحات، مسیرهای اصلی و سطح دسترسی هر صفحه را تعریف می‌کند. تمام صفحات داخلی باید با Layout اصلی شامل Sidebar راست، Topbar ثابت و محتوای قابل اسکرول نمایش داده شوند.

---

## 1. ساختار کلی مسیرها

### مسیرهای عمومی
- `/login` — ورود به سیستم
- `/forgot-password` — فراموشی رمز عبور
- `/reset-password` — بازنشانی رمز عبور به‌صورت Mock

### مسیرهای اصلی بعد از ورود
- `/` — Redirect به `/dashboard`
- `/dashboard` — داشبورد
- `/clients` — لیست مشتریان
- `/clients/:id` — جزئیات مشتری
- `/properties` — لیست املاک
- `/properties/:id` — جزئیات ملک
- `/pipeline` — پایپ‌لاین فروش به‌صورت Kanban
- `/deals` — لیست معاملات
- `/tasks` — وظایف و یادآورها
- `/reports` — گزارش‌گیری
- `/notifications` — نوتیفیکیشن‌ها
- `/settings` — تنظیمات
- `/profile` — پروفایل کاربری
- `/users` — مدیریت کاربران

---

## 2. جدول صفحات

| صفحه | مسیر | عنوان فارسی | نقش‌های دارای دسترسی | هدف اصلی |
|---|---|---|---|---|
| Login | `/login` | ورود | همه | احراز هویت |
| Forgot Password | `/forgot-password` | فراموشی رمز عبور | همه | شروع فرآیند بازیابی رمز به‌صورت Mock |
| Reset Password | `/reset-password` | بازنشانی رمز عبور | همه | بازنشانی رمز به‌صورت Mock |
| Dashboard | `/dashboard` | داشبورد | Admin، Manager، Agent | مشاهده KPIها، نمودارها و فعالیت‌های اخیر |
| Clients | `/clients` | مشتریان | Admin، Manager، Agent | لیست، جستجو، فیلتر و مدیریت مشتریان |
| Client Detail | `/clients/:id` | جزئیات مشتری | Admin، Manager، Agent | مشاهده اطلاعات مشتری، Timeline، Dealها و تعامل‌ها |
| Properties | `/properties` | املاک | Admin، Manager، Agent | لیست، جستجو، فیلتر و مدیریت املاک |
| Property Detail | `/properties/:id` | جزئیات ملک | Admin، Manager، Agent | مشاهده ملک، تصاویر، نقشه و Smart Match |
| Pipeline | `/pipeline` | پایپ‌لاین فروش | Admin، Manager، Agent | مدیریت Dealها به‌صورت Kanban |
| Deals | `/deals` | معاملات | Admin، Manager، Agent | لیست و مدیریت معاملات در نمای جدولی |
| Tasks | `/tasks` | وظایف | Admin، Manager، Agent | مدیریت وظایف، یادآورها و کارهای روزانه |
| Reports | `/reports` | گزارش‌ها | Admin، Manager | گزارش‌گیری و خروجی Excel/CSV |
| Notifications | `/notifications` | نوتیفیکیشن‌ها | همه کاربران وارد شده | مشاهده و مدیریت نوتیفیکیشن‌ها |
| Settings | `/settings` | تنظیمات | Admin | تنظیمات سیستم، Pipelineها، Stageها و مقادیر پایه |
| Profile | `/profile` | پروفایل | همه کاربران وارد شده | مشاهده و ویرایش پروفایل شخصی |
| Users | `/users` | کاربران | Admin | مدیریت کاربران و نقش‌ها |

---

## 3. صفحه Login

### هدف
ورود کاربر به سیستم با ایمیل/نام کاربری و رمز عبور.

### ساختار
- فرم ورود
- پیام خطای سراسری
- لینک فراموشی رمز عبور

### حالت‌ها
- Loading
- Validation Error
- خطای سرور
- خطای کاربر غیرفعال

---

## 4. صفحه Forgot Password / Reset Password

### هدف
بازیابی رمز عبور در حالت محلی و Mock؛ بدون ایمیل واقعی.

### ساختار
- فرم دریافت ایمیل یا نام کاربری
- پیام تأیید Mock
- فرم بازنشانی رمز در حالت Mock

### حالت‌ها
- Loading
- Success
- Error
- Validation Error

---

## 5. صفحه Dashboard

### هدف
نمایش خلاصه وضعیت فروش، مشتریان، معاملات، وظایف و فعالیت‌های اخیر.

### ساختار
- KPI Cards
- Chart Cards
- Recent Activities
- Tasks Widget
- Date Range Selector
- فیلتر Agent یا Pipeline در صورت نیاز

### حالت‌ها
- Skeleton Loading
- Empty State
- Error State
- No Permission در صورت محدودیت نقش

---

## 6. صفحه Clients

### هدف
مدیریت مشتریان/لیدها.

### ساختار
- PageHeader با دکمه افزودن مشتری
- فیلترها
- جستجو
- جدول مشتریان
- Pagination
- Modal/Drawer ایجاد یا ویرایش مشتری

### حالت‌ها
- Loading
- Empty State
- Error State
- Validation Error
- Success Toast

---

## 7. صفحه Client Detail

### هدف
مشاهده جزئیات کامل یک مشتری.

### ساختار
- اطلاعات اصلی مشتری
- Tabs یا بخش‌ها:
  - Timeline تعامل‌ها
  - Dealها
  - یادداشت‌ها
  - تعامل‌ها
- اقدامات سریع:
  - ثبت تعامل
  - ایجاد Deal
  - تخصیص Agent
  - افزودن یادداشت

### حالت‌ها
- Loading
- Not Found
- No Permission
- Empty Timeline
- Error State

---

## 8. صفحه Properties

### هدف
مدیریت لیست املاک.

### ساختار
- PageHeader با دکمه افزودن ملک
- فیلتر پیشرفته
- جستجوی سریع
- جدول املاک
- Pagination
- Modal/Drawer ایجاد یا ویرایش ملک

### حالت‌ها
- Loading
- Empty State
- Error State
- Validation Error
- Success Toast

---

## 9. صفحه Property Detail

### هدف
مشاهده جزئیات کامل ملک.

### ساختار
- اطلاعات اصلی ملک
- گالری تصاویر
- نقشه
- Smart Match با مشتریان
- وضعیت ملک
- اقدامات:
  - ویرایش
  - آرشیو
  - انتشار
  - کپی کد ملک

### حالت‌ها
- Loading
- Not Found
- No Permission
- Empty Gallery
- Error State

---

## 10. صفحه Pipeline

### هدف
مدیریت Dealها به‌صورت Kanban.

### ساختار
- PipelineSelector
- Kanban Board
- Stage Columns
- Deal Cards
- Quick Add Deal
- Deal Drawer
- Stage Settings

### حالت‌ها
- Loading
- Empty Pipeline
- Empty Stage
- Drag Feedback
- Error State
- No Permission

---

## 11. صفحه Deals

### هدف
مدیریت معاملات در نمای لیستی/جدولی.

### ساختار
- فیلترها
- جستجو
- جدول Dealها
- Pagination
- فرم ایجاد/ویرایش Deal

### حالت‌ها
- Loading
- Empty State
- Error State
- Validation Error
- Success Toast

---

## 12. صفحه Tasks

### هدف
مدیریت وظایف و یادآورها.

### ساختار
- نمای امروز
- نمای هفته
- نمای ماه
- لیست وظایف
- فیلترها
- فرم ایجاد وظیفه سریع

### حالت‌ها
- Loading
- Empty State
- Overdue Highlight
- Error State
- Success Toast

---

## 13. صفحه Reports

### هدف
گزارش‌گیری و خروجی‌گیری.

### ساختار
- انتخاب نوع گزارش
- فیلترها
- جدول گزارش
- نمودار گزارش در صورت نیاز
- دکمه Export CSV
- دکمه Export Excel

### حالت‌ها
- Loading
- Empty State
- Error State
- Export Success
- Export Error

---

## 14. صفحه Notifications

### هدف
مشاهده و مدیریت نوتیفیکیشن‌های داخلی.

### ساختار
- لیست نوتیفیکیشن‌ها
- فیلتر خوانده‌شده/نخوانده
- علامت‌گذاری به‌عنوان خوانده‌شده
- علامت‌گذاری همه به‌عنوان خوانده‌شده

### حالت‌ها
- Loading
- Empty State
- Error State

---

## 15. صفحه Settings

### هدف
مدیریت تنظیمات سیستم توسط Admin.

### ساختار
- تنظیمات عمومی
- مدیریت Pipelineها
- مدیریت Stageها
- مدیریت منابع لید
- مدیریت دلایل برد/باخت
- مدیریت انواع ملک
- مدیریت وضعیت‌های ملک
- مدیریت امکانات رفاهی

### حالت‌ها
- Loading
- No Permission
- Validation Error
- Success Toast
- Error State

---

## 16. صفحه Profile

### هدف
مشاهده و ویرایش پروفایل کاربری.

### ساختار
- اطلاعات شخصی
- تغییر رمز عبور
- آواتار
- آخرین ورود

### حالت‌ها
- Loading
- Validation Error
- Success Toast
- Error State

---

## 17. صفحه Users

### هدف
مدیریت کاربران توسط Admin.

### ساختار
- جدول کاربران
- جستجو
- فیلتر نقش
- فیلتر وضعیت فعال/غیرفعال
- فرم ایجاد کاربر
- فرم ویرایش کاربر
- تغییر نقش
- فعال/غیرفعال کردن کاربر
- ریست رمز عبور

### حالت‌ها
- Loading
- Empty State
- Validation Error
- No Permission
- Success Toast
- Error State

---

## 18. قاعده دسترسی کلی

| نقش | دسترسی |
|---|---|
| Admin | همه صفحات |
| Manager | Dashboard، Clients، Client Detail، Properties، Property Detail، Pipeline، Deals، Tasks، Reports، Notifications، Profile |
| Agent | Dashboard، Clients، Client Detail، Properties، Property Detail، Pipeline، Deals، Tasks، Notifications، Profile |
| Client | فقط صفحات محدود مرتبط با داده‌های خودش؛ در این نسخه به‌عنوان نقش محدود در سطح API و UI |

---

## 19. قاعده طراحی مسیرها

- تمام صفحات داخلی باید دارای PageHeader باشند.
- breadcrumb باید در صفحات Detail نمایش داده شود.
- Sidebar باید در تمام صفحات داخلی ثابت باشد.
- در موبایل، Sidebar به‌صورت کشویی نمایش داده شود.
- Topbar باید شامل جستجوی سریع، نوتیفیکیشن و منوی کاربر باشد.
- صفحات عمومی فقط شامل Layout ساده بدون Sidebar باشند.
- دسترسی‌ها باید هم در Router Guard و هم در API کنترل شوند.
