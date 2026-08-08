# توکن‌های طراحی — CRM تخصصی املاک

این سند توکن‌های پایه طراحی را تعریف می‌کند. این توکن‌ها باید مبنای Tailwind CSS، کامپوننت‌ها و استایل‌های سراسری باشند. هدف، ایجاد ظاهر یکپارچه، قابل نگهداری و سازگار با Dark Mode است.

---

## 1. اصول نام‌گذاری توکن‌ها

- نام‌ها باید معنایی باشند، نه صرفاً مقدار.
- توکن‌های رنگی در فایل جداگانه Color System کامل می‌شوند.
- توکن‌های فاصله، گوشه، سایه، عرض و breakpoint در همه صفحات یکسان استفاده شوند.
- از مقادیر hardcoded در کامپوننت‌ها پرهیز شود.
- همه توکن‌ها باید با Tailwind CSS قابل استفاده باشند.

### الگوی نام‌گذاری
- `--space-*` برای فاصله‌ها
- `--radius-*` برای گوشه‌ها
- `--shadow-*` برای سایه‌ها
- `--width-*` برای عرض‌ها
- `--z-*` برای لایه‌ها
- `--color-*` برای رنگ‌ها

---

## 2. توکن‌های فاصله — Spacing

| توکن | مقدار | کاربرد |
|---|---:|---|
| `space-0` | 0px | بدون فاصله |
| `space-1` | 4px | فاصله بسیار کوچک |
| `space-2` | 8px | فاصله بین آیکون و متن |
| `space-3` | 12px | فاصله داخلی کوچک |
| `space-4` | 16px | Padding استاندارد کارت‌ها |
| `space-5` | 20px | فاصله بین بخش‌های کوچک |
| `space-6` | 24px | Padding استاندارد صفحات |
| `space-8` | 32px | فاصله بین بخش‌های اصلی |
| `space-10` | 40px | فاصله بزرگ |
| `space-12` | 48px | فاصله خیلی بزرگ |
| `space-16` | 64px | فاصله بین بلوک‌های بزرگ |
| `space-20` | 80px | فاصله ویژه صفحات Auth |
| `space-24` | 96px | فاصله خیلی بزرگ برای صفحات خالی |

### قواعد استفاده
- Padding پیش‌فرض کارت: `space-4` در موبایل و `space-6` در دسکتاپ.
- Padding پیش‌فرض محتوای صفحه: `space-4` در موبایل و `space-6` در دسکتاپ.
- فاصله بین فیلدهای فرم: `space-4`.
- فاصله بین دکمه‌ها: `space-2` یا `space-3`.
- فاصله بین ردیف‌های جدول: حداقل `space-3`.

---

## 3. توکن‌های گوشه — Border Radius

| توکن | مقدار | کاربرد |
|---|---:|---|
| `radius-none` | 0px | بدون گوشه گرد |
| `radius-sm` | 4px | Badge، Tag کوچک |
| `radius-md` | 8px | Input، Button، Select |
| `radius-lg` | 12px | Card، Modal، Drawer |
| `radius-xl` | 16px | Auth Card، Dashboard Card |
| `radius-2xl` | 24px | Empty State، بلوک‌های بزرگ |
| `radius-full` | 9999px | Avatar، Pill Badge |

### قواعد استفاده
- Inputها و Buttonها از `radius-md` استفاده کنند.
- Cardها از `radius-lg` استفاده کنند.
- Modal و Drawer از `radius-lg` یا `radius-xl` استفاده کنند.
- آواتار همیشه `radius-full` باشد.
- در Dark Mode مقدار radius تغییر نکند.

---

## 4. توکن‌های سایه — Shadows

| توکن | کاربرد |
|---|---|
| `shadow-none` | بدون سایه |
| `shadow-sm` | کارت‌های ساده و سطوح کم‌اهمیت |
| `shadow-md` | Card، Dropdown، Popover |
| `shadow-lg` | Modal، Drawer |
| `shadow-xl` | Command Palette، Overlayهای مهم |
| `shadow-focus` | حالت فوکوس قابل دسترس |
| `shadow-topbar` | سایه ظریف Topbar هنگام اسکرول |
| `shadow-sidebar` | سایه Sidebar کشویی در موبایل |

### قواعد استفاده
- سایه‌ها نباید در Dark Mode شدید باشند.
- برای فوکوس کیبورد از `shadow-focus` استفاده شود.
- Modal باید سایه واضح‌تری نسبت به Dropdown داشته باشد.
- در حالت Drag در Kanban از سایه متوسط استفاده شود.

---

## 5. توکن‌های عرض — Widths

| توکن | مقدار | کاربرد |
|---|---:|---|
| `width-sidebar` | 264px | عرض Sidebar دسکتاپ |
| `width-topbar` | 64px | ارتفاع Topbar |
| `width-content-max` | 1440px | حداکثر عرض محتوا |
| `width-form-max` | 768px | حداکثر عرض فرم‌ها |
| `width-auth-card` | 420px | کارت Login و Reset Password |
| `width-modal-sm` | 400px | Modal کوچک |
| `width-modal-md` | 560px | Modal متوسط |
| `width-modal-lg` | 720px | Modal بزرگ |
| `width-modal-xl` | 960px | Modal خیلی بزرگ |
| `width-drawer` | 480px | Drawer استاندارد |
| `width-drawer-lg` | 640px | Drawer بزرگ برای جزئیات |
| `width-command-palette` | 640px | عرض Command Palette |
| `width-kanban-column` | 320px | عرض ستون Kanban |
| `width-kanban-column-min` | 280px | حداقل عرض ستون Kanban در موبایل |

### قواعد استفاده
- Sidebar در دسکتاپ ثابت و 264px است.
- Topbar ارتفاع 64px دارد.
- فرم‌های طولانی نباید از 768px عریض‌تر شوند.
- Modalها باید روی موبایل تقریباً تمام‌عرض شوند.
- Drawer در موبایل می‌تواند تمام‌عرض یا نزدیک به تمام‌عرض باشد.

---

## 6. توکن‌های Breakpoint

| توکن | محدوده | کاربرد |
|---|---:|---|
| `mobile` | کمتر از 640px | موبایل |
| `tablet` | 640px تا 1024px | تبلت |
| `desktop` | بیشتر از 1024px | لپتاپ و دسکتاپ |
| `wide` | بیشتر از 1440px | نمایشگرهای بزرگ |

### قواعد استفاده
- طراحی باید Mobile-first باشد.
- Sidebar زیر 1024px کشویی شود.
- جداول در موبایل به کارت یا Scroll افقی تبدیل شوند.
- Kanban در موبایل و تبلت Scroll افقی داشته باشد.
- فرم‌ها زیر 640px تک‌ستونه شوند.
- Dashboard در موبایل KPIها را به‌صورت کارت‌های تک‌ستونه یا دوستونه نمایش دهد.

---

## 7. توکن‌های Z-Index

| توکن | مقدار | کاربرد |
|---|---:|---|
| `z-base` | 0 | محتوای عادی |
| `z-dropdown` | 1000 | Dropdown، Select، Popover |
| `z-sticky` | 1020 | Sticky Header جدول‌ها |
| `z-sidebar` | 1030 | Sidebar ثابت دسکتاپ |
| `z-sidebar-mobile` | 1040 | Sidebar کشویی موبایل |
| `z-drawer` | 1050 | Drawer |
| `z-modal` | 1060 | Modal |
| `z-command-palette` | 1070 | Command Palette |
| `z-toast` | 1080 | Toast |
| `z-tooltip` | 1090 | Tooltip |

### قواعد استفاده
- Toast باید بالاتر از Modal باشد.
- Command Palette باید بالاتر از Drawer و Modal باشد.
- Tooltip باید بالاترین لایه باشد.
- Overlay باید زیر محتوای Modal و بالای محتوای اصلی باشد.

---

## 8. توکن‌های Border

| توکن | مقدار | کاربرد |
|---|---|---|
| `border-width-1` | 1px | Border استاندارد Input، Card |
| `border-width-2` | 2px | فوکوس، انتخاب فعال |
| `border-color-default` | رنگ خاکستری ملایم | Border پیش‌فرض |
| `border-color-strong` | رنگ خاکستری تیره‌تر | Separator قوی |
| `border-color-focus` | رنگ Primary | فوکوس |
| `border-color-danger` | رنگ Danger | خطا |
| `border-color-success` | رنگ Success | موفقیت |

### قواعد استفاده
- Inputها در حالت عادی border ظریف داشته باشند.
- در حالت خطا، border قرمز و پیام فارسی زیر فیلد نمایش داده شود.
- فوکوس باید همیشه قابل مشاهده باشد.
- در Dark Mode borderها باید کم‌رنگ‌تر اما قابل تشخیص باشند.

---

## 9. توکن‌های Opacity و Overlay

| توکن | مقدار | کاربرد |
|---|---:|---|
| `opacity-disabled` | 50% | دکمه یا فیلد غیرفعال |
| `opacity-hover` | 80% | حالت hover ملایم |
| `overlay-light` | rgba(15, 23, 42, 0.4) | Overlay در حالت روشن |
| `overlay-dark` | rgba(0, 0, 0, 0.6) | Overlay در حالت تاریک |

### قواعد استفاده
- Overlay باید خوانایی Modal را حفظ کند.
- Overlay نباید در Dark Mode کاملاً سیاه مطلق باشد.
- دکمه‌های غیرفعال باید واضح غیرفعال به نظر برسند.

---

## 10. توکن‌های چگالی — Density

| توکن | مقدار | کاربرد |
|---|---|---|
| `density-compact` | 8px - 12px | جداول فشرده |
| `density-normal` | 12px - 16px | حالت پیش‌فرض |
| `density-comfortable` | 16px - 24px | کارت‌ها و فرم‌ها |

### قواعد استفاده
- جداول مدیریتی می‌توانند حالت compact داشته باشند.
- فرم‌ها باید comfortable باشند.
- در موبایل از density comfortable استفاده شود.

---

## 11. توکن‌های پیشنهادی برای Tailwind

این توکن‌ها باید در `tailwind.config.js` تعریف شوند:

- spacing بر اساس پیکسل‌های بالا
- borderRadius بر اساس `radius-*`
- boxShadow بر اساس `shadow-*`
- maxWidth بر اساس `width-*`
- zIndex بر اساس `z-*`
- breakpoints بر اساس 640px، 1024px و 1440px

### نمونه mapping مفهومی
- `p-4` معادل 16px
- `rounded-md` معادل 8px
- `rounded-lg` معادل 12px
- `shadow-md` برای Card
- `shadow-lg` برای Modal
- `max-w-3xl` برای فرم‌ها
- `max-w-screen-2xl` برای محتوای اصلی

---

## 12. قواعد نهایی توکن‌ها

- هیچ صفحه‌ای نباید خارج از این توکن‌ها فاصله، سایه یا radius سفارشی داشته باشد.
- تغییر توکن‌ها باید فقط از طریق Config یا فایل استایل مرکزی انجام شود.
- Dark Mode باید فقط توکن‌های رنگی را تغییر دهد، نه فاصله‌ها و radiusها را.
- کامپوننت‌ها باید در هر دو حالت روشن و تاریک با همین توکن‌ها کار کنند.
- همه مقادیر باید در RTL نیز درست نمایش داده شوند.
