# Motion و انیمیشن — CRM تخصصی املاک

این سند قواعد حرکت، انیمیشن و transition را تعریف می‌کند. هدف، ایجاد تجربه‌ای روان و حرفه‌ای بدون ایجاد حواس‌پرتی یا کاهش عملکرد است.

---

## 1. اصول کلی

- انیمیشن‌ها باید کوتاه، ملایم و هدفمند باشند.
- هیچ انیمیشنی نباید مانع کار کاربر شود.
- انیمیشن نباید اطلاعات را پنهان یا مبهم کند.
- همه انیمیشن‌ها باید با prefers-reduced-motion سازگار باشند.
- از انیمیشن‌های پیچیده و سنگین پرهیز شود.
- Skeleton باید جایگزین Spinner برای لودهای طولانی باشد.
- Drag & Drop باید Feedback بصری فوری داشته باشد.
- انیمیشن نباید در Dark Mode رفتار متفاوتی داشته باشد.

---

## 2. توکن‌های Duration

| توکن | مقدار | کاربرد |
|---|---:|---|
| duration-instant | 0ms | بدون انیمیشن |
| duration-fast | 100ms | تغییرات بسیار سریع مانند hover |
| duration-normal | 150ms | transition استاندارد |
| duration-moderate | 200ms | Modal، Drawer |
| duration-slow | 250ms | انیمیشن‌های بزرگ‌تر |
| duration-skeleton | 1.5s | چرخه Skeleton pulse |

### قواعد Duration
- هیچ انیمیشنی نباید بیشتر از 300ms طول بکشد، مگر Skeleton.
- برای hover و focus از duration-fast استفاده شود.
- برای Modal و Drawer از duration-moderate استفاده شود.
- برای تغییر تم می‌توان از duration-normal استفاده کرد.
- برای Drag feedback از duration-instant یا duration-fast استفاده شود.

---

## 3. توکن‌های Easing

| توکن | مقدار CSS | کاربرد |
|---|---|---|
| ease-out | cubic-bezier(0, 0, 0.2, 1) | ورود عناصر به صفحه |
| ease-in | cubic-bezier(0.4, 0, 1, 1) | خروج عناصر از صفحه |
| ease-in-out | cubic-bezier(0.4, 0, 0.2, 1) | تغییرات دو طرفه |
| linear | linear | Skeleton pulse، Progress bar |

### قواعد Easing
- برای باز شدن Modal و Drawer از ease-out استفاده شود.
- برای بسته شدن Modal و Drawer از ease-in استفاده شود.
- برای hover و focus از ease-out استفاده شود.
- برای Skeleton از linear استفاده شود.
- از easingهای bounce یا elastic استفاده نشود.

---

## 4. Skeleton Loading

### رفتار
- Skeleton باید اندازه واقعی محتوا را شبیه‌سازی کند.
- Skeleton باید pulse ملایم داشته باشد.
- Skeleton نباید چشمک شدید یا سریع داشته باشد.
- Skeleton باید در Dark Mode کم‌رنگ‌تر باشد.

### مشخصات فنی
- duration: 1.5s
- easing: linear
- animation: pulse
- opacity: از 0.6 به 1 و بازگشت

### پیاده‌سازی پیشنهادی
- از Tailwind animate-pulse استفاده شود.
- رنگ Skeleton از surface-muted گرفته شود.
- در Dark Mode، رنگ Skeleton کمی تیره‌تر باشد.

### انواع Skeleton
- Text Skeleton: برای متن‌ها و عنوان‌ها
- Card Skeleton: برای کارت‌ها و KPIها
- Table Skeleton: برای جدول‌ها
- Chart Skeleton: برای نمودارها
- Avatar Skeleton: برای آواتارها
- Kanban Skeleton: برای Board و Cardها

---

## 5. Transition برای Modal

### باز شدن
- duration: 200ms
- easing: ease-out
- opacity: از 0 به 1
- transform: از scale(0.95) به scale(1)
- Overlay: از opacity 0 به مقدار نهایی

### بسته شدن
- duration: 150ms
- easing: ease-in
- opacity: از 1 به 0
- transform: از scale(1) به scale(0.95)

### قواعد
- Modal باید قبل از بسته شدن، transition کامل را تمام کند.
- اگر کاربر سریع Escape بزند، transition باید لغو شود و Modal فوراً بسته شود.
- focus trap باید در طول transition فعال بماند.
- Overlay باید همزمان با Modal تغییر کند.

---

## 6. Transition برای Drawer

### باز شدن
- duration: 200ms
- easing: ease-out
- transform: از translateX(100%) به translateX(0) برای Drawer چپ در RTL
- Overlay: از opacity 0 به مقدار نهایی

### بسته شدن
- duration: 150ms
- easing: ease-in
- transform: از translateX(0) به translateX(100%)

### قواعد
- Drawer باید از سمت مناسب باز شود.
- در RTL، Drawer جزئیات بهتر است از سمت چپ باز شود.
- Overlay باید همزمان با Drawer تغییر کند.
- در موبایل، Drawer می‌تواند از پایین باز شود؛ در این صورت از translateY استفاده شود.

---

## 7. Transition برای Dropdown و Popover

### باز شدن
- duration: 150ms
- easing: ease-out
- opacity: از 0 به 1
- transform: از translateY(-4px) به translateY(0)

### بسته شدن
- duration: 100ms
- easing: ease-in
- opacity: از 1 به 0

### قواعد
- Dropdown باید سریع باز شود.
- Dropdown نباید delay داشته باشد.
- در موبایل، Dropdown می‌تواند به‌صورت Drawer یا Modal باز شود.

---

## 8. Transition برای Toast

### ورود
- duration: 200ms
- easing: ease-out
- transform: از translateY(16px) به translateY(0)
- opacity: از 0 به 1

### خروج
- duration: 150ms
- easing: ease-in
- opacity: از 1 به 0
- transform: از translateY(0) به translateY(8px)

### قواعد
- Toast باید از پایین یا گوشه مناسب وارد شود.
- Toast نباید مانع فوکوس کیبورد شود.
- چند Toast باید به‌صورت stack نمایش داده شوند.
- Toast باید بعد از duration مشخص به‌صورت خودکار بسته شود.

---

## 9. Transition برای Tabs

### تغییر Tab
- duration: 150ms
- easing: ease-out
- فقط opacity و transform برای محتوای Tab

### قواعد
- Tab indicator باید با transition ملایم جابجا شود.
- محتوای Tab نباید انیمیشن سنگین داشته باشد.
- در موبایل، Tabها باید قابل اسکرول باشند.

---

## 10. Drag Feedback در Kanban

### شروع Drag
- duration: instant
- کارت کمی بزرگ‌تر شود: scale(1.02)
- سایه متوسط اضافه شود
- opacity کمی کاهش یابد: 0.9

### حین Drag
- duration: instant
- کارت باید با موس یا لمس حرکت کند.
- Stage مقصد باید highlight شود.
- خط نشانگر برای محل قرارگیری نمایش داده شود.

### رها کردن
- duration: 150ms
- easing: ease-out
- کارت به محل نهایی برود.
- سایه و scale به حالت عادی برگردد.

### خطا در Drag
- duration: 200ms
- easing: ease-out
- کارت به محل قبلی برگردد.
- Toast خطا نمایش داده شود.
- Undo در صورت امکان فعال شود.

### قواعد
- Drag & Drop نباید lag داشته باشد.
- در موبایل، Drag باید با long press شروع شود.
- Stage مقصد باید واضح مشخص باشد.
- از ghost image یا clone برای Drag استفاده شود.

---

## 11. Hover و Focus Effects

### Hover
- duration: 100ms
- easing: ease-out
- تغییر رنگ ملایم
- تغییر سایه در صورت نیاز
- تغییر opacity در صورت نیاز

### Focus
- duration: instant
- focus ring باید فوراً نمایش داده شود.
- هیچ delay برای focus مجاز نیست.

### Active
- duration: instant
- تغییر رنگ یا scale بسیار کوچک
- feedback فوری برای کلیک

---

## 12. Page Transitions

### تغییر صفحه
- duration: 150ms
- easing: ease-out
- فقط opacity برای محتوای صفحه
- از slide یا zoom برای صفحات استفاده نشود.

### قواعد
- Router transition باید ساده باشد.
- Skeleton باید قبل از لود داده نمایش داده شود.
- از انیمیشن‌های سنگین برای تغییر صفحه پرهیز شود.
- در موبایل، transition می‌تواند کمی ساده‌تر باشد.

---

## 13. Progress Bar و Loading

### Progress Bar
- duration: linear
- animation: indeterminate یا determinate
- رنگ: primary
- ارتفاع: 2px یا 4px

### Spinner
- duration: 0.8s
- animation: rotate
- رنگ: primary
- اندازه: 16px، 24px، 32px

### قواعد
- برای لودهای کوتاه از Spinner استفاده شود.
- برای لودهای طولانی از Skeleton استفاده شود.
- Progress Bar باید در بالای صفحه یا داخل دکمه باشد.
- Spinner نباید بزرگ‌تر از 32px باشد.

---

## 14. prefers-reduced-motion

### رفتار
- اگر کاربر prefers-reduced-motion را فعال کرده باشد:
  - همه transitionها باید duration-instant شوند.
  - Skeleton pulse باید غیرفعال شود.
  - Drag feedback باید بدون scale و shadow باشد.
  - فقط تغییر رنگ بدون انیمیشن مجاز است.

### پیاده‌سازی
- از media query استفاده شود:
  @media (prefers-reduced-motion: reduce)
- در Tailwind از motion-reduce: استفاده شود.
- باید همه انیمیشن‌ها را override کند.

---

## 15. بایدها و نبایدها

### بایدها
- استفاده از duration کوتاه
- استفاده از ease-out برای ورود
- استفاده از Skeleton برای لودهای طولانی
- Drag feedback فوری
- پشتیبانی از prefers-reduced-motion
- تست انیمیشن‌ها در Dark Mode

### نبایدها
- انیمیشن بیشتر از 300ms
- bounce یا elastic
- انیمیشن‌های پیچیده و سنگین
- حذف focus ring با انیمیشن
- Skeleton با چشمک شدید
- Drag بدون feedback
- انیمیشن که مانع کار کاربر شود

---

## 16. چک‌لیست Motion

- [ ] همه transitionها بین 100ms تا 250ms هستند.
- [ ] Modal با ease-out باز و با ease-in بسته می‌شود.
- [ ] Drawer با ease-out باز و با ease-in بسته می‌شود.
- [ ] Skeleton pulse ملایم دارد.
- [ ] Drag feedback فوری و واضح است.
- [ ] Toast با transition مناسب وارد و خارج می‌شود.
- [ ] prefers-reduced-motion پشتیبانی می‌شود.
- [ ] هیچ انیمیشنی بیشتر از 300ms نیست.
- [ ] Dark Mode رفتار انیمیشن را تغییر نمی‌دهد.
- [ ] focus ring بدون delay نمایش داده می‌شود.

---

## 17. جمع‌بندی

| عنصر | Duration | Easing | رفتار |
|---|---:|---|---|
| Hover | 100ms | ease-out | تغییر رنگ ملایم |
| Focus | instant | - | focus ring فوری |
| Modal باز | 200ms | ease-out | opacity + scale |
| Modal بسته | 150ms | ease-in | opacity + scale |
| Drawer باز | 200ms | ease-out | translateX |
| Drawer بسته | 150ms | ease-in | translateX |
| Dropdown | 150ms | ease-out | opacity + translateY |
| Toast | 200ms | ease-out | opacity + translateY |
| Tabs | 150ms | ease-out | opacity |
| Page | 150ms | ease-out | opacity |
| Skeleton | 1.5s | linear | pulse |
| Drag | instant | - | scale + shadow |
