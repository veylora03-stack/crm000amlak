# Kanban — CRM تخصصی املاک

این سند رفتار استاندارد Kanban برای ماژول پایپ‌لاین فروش و معاملات را تعریف می‌کند. Kanban باید در دسکتاپ، تبلت و موبایل قابل استفاده باشد.

---

## 1. اصول کلی Kanban

- Kanban باید Drag & Drop داشته باشد.
- Drag & Drop باید با Optimistic Update همراه باشد.
- در صورت خطا، باید Undo Move انجام شود.
- هر Stage باید رنگ مشخص داشته باشد.
- هر Stage باید جمع مبلغ Dealها را نشان دهد.
- Quick Add Deal باید در هر Stage در دسترس باشد.
- Deal Card باید اطلاعات کلیدی را نمایش دهد.
- Kanban باید در موبایل Scroll افقی داشته باشد.
- Kanban باید Skeleton Loading داشته باشد.
- Kanban باید Empty State داشته باشد.

---

## 2. ساختار Kanban Board

### بخش‌های اصلی
- PageHeader با عنوان «پایپ‌لاین فروش»
- PipelineSelector برای انتخاب Pipeline
- Kanban Board تمام‌عرض
- Stage Columns
- Deal Cards
- Quick Add Deal

### چیدمان
- دسکتاپ: Board تمام‌عرض با Scroll افقی در صورت نیاز
- تبلت: Board با Scroll افقی
- موبایل: Board با Scroll افقی، ستون‌ها حداقل 85% عرض صفحه

### فاصله‌ها
- فاصله بین ستون‌ها: 16px
- فاصله بین Deal Cards: 8px
- Padding داخلی ستون: 12px
- Padding داخلی Deal Card: 12px

---

## 3. Pipeline Selector

### رفتار
- باید در بالای Kanban Board قرار گیرد.
- باید Dropdown یا Select باشد.
- باید Pipeline فعال را نشان دهد.
- تغییر Pipeline باید Board را به‌روزرسانی کند.
- باید Skeleton هنگام تغییر Pipeline نمایش داده شود.

### قواعد
- اگر فقط یک Pipeline وجود دارد، Selector ساده باشد.
- اگر Pipeline فعال حذف شده است، به اولین Pipeline فعال برگردد.
- Pipeline غیرفعال نباید در Selector نمایش داده شود.

---

## 4. Stage Columns

### ساختار هر Stage
- عنوان Stage
- رنگ Stage
- تعداد Dealها
- جمع مبلغ Dealها
- Deal Cards
- Quick Add Deal

### رفتار
- Stage باید Header مشخص داشته باشد.
- Stage باید رنگ ملایم در پس‌زمینه داشته باشد.
- Stage باید رنگ قوی در نقطه نشانگر داشته باشد.
- Stage باید Drop Target باشد.
- Stage باید با Drag Over highlight شود.

### قواعد
- Stageهای برنده باید رنگ success داشته باشند.
- Stageهای بازنده باید رنگ danger داشته باشند.
- Stageهای میانی باید رنگ‌های info، warning یا neutral داشته باشند.
- Stage غیرفعال نباید نمایش داده شود.
- Stage خالی باید پیام مناسب داشته باشد.

### جمع مبلغ Stage
- باید در Header Stage نمایش داده شود.
- باید با فرمت فارسی و جداکننده هزارگان باشد.
- باید با تغییر Dealها به‌روزرسانی شود.
- در Optimistic Update باید فوری به‌روزرسانی شود.

---

## 5. Deal Card

### اطلاعات Deal Card
- عنوان معامله
- نام مشتری
- مبلغ معامله
- Agent مسئول
- وضعیت برد/باخت
- تاریخ تخمینی بسته شدن

### ساختار Deal Card
- عنوان در بالا
- مشتری با آیکون یا Avatar
- مبلغ با فرمت فارسی
- Agent با Avatar کوچک
- وضعیت با Badge یا رنگ
- تاریخ با فرمت شمسی

### رفتار
- Deal Card باید قابل کلیک باشد.
- کلیک باید Deal Drawer را باز کند.
- Deal Card باید Draggable باشد.
- Deal Card باید Hover State داشته باشد.
- Deal Card باید Focus State داشته باشد.

### قواعد
- Deal Card نباید اطلاعات زیاد و شلوغ نمایش دهد.
- Deal Card باید در موبایل فشرده‌تر باشد.
- Deal Card باید در Dark Mode خوانا باشد.
- Deal Card باید با کیبورد قابل دسترسی باشد.

### اندازه Deal Card
- دسکتاپ: عرض کامل ستون، ارتفاع خودکار
- تبلت: عرض کامل ستون، ارتفاع خودکار
- موبایل: عرض کامل ستون، ارتفاع فشرده

---

## 6. Drag & Drop

### شروع Drag
- با Long Press در موبایل شروع شود.
- با Mouse Down در دسکتاپ شروع شود.
- Deal Card کمی بزرگ‌تر شود: scale(1.02)
- سایه متوسط اضافه شود.
- opacity کمی کاهش یابد: 0.9

### حین Drag
- Deal Card باید با موس یا لمس حرکت کند.
- Stage مقصد باید highlight شود.
- خط نشانگر برای محل قرارگیری نمایش داده شود.
- Board باید Scroll خودکار در صورت نیاز داشته باشد.

### رها کردن
- Deal Card به محل نهایی برود.
- سایه و scale به حالت عادی برگردد.
- Optimistic Update اعمال شود.
- درخواست API ارسال شود.

### قواعد
- Drag & Drop نباید lag داشته باشد.
- Drag & Drop باید با Touch کار کند.
- Drag & Drop باید با کیبورد جایگزین داشته باشد.
- Stage مقصد باید واضح مشخص باشد.
- از ghost image یا clone برای Drag استفاده شود.

---

## 7. Optimistic Update

### رفتار
- با رها کردن Deal، Stage فوری تغییر کند.
- جمع مبلغ Stage فوری به‌روزرسانی شود.
- تعداد Dealها فوری به‌روزرسانی شود.
- درخواست API در پس‌زمینه ارسال شود.
- در صورت موفقیت، وضعیت نهایی اعمال شود.

### قواعد
- Optimistic Update باید فوری باشد.
- Optimistic Update نباید منتظر پاسخ سرور بماند.
- Optimistic Update باید با Toast کوتاه تأیید شود.
- Optimistic Update نباید باعث پرش UI شود.

---

## 8. Undo Move

### رفتار
- اگر درخواست API ناموفق بود، Deal به Stage قبلی برگردد.
- Toast خطا نمایش داده شود.
- دکمه Undo در Toast در صورت امکان نمایش داده شود.
- جمع مبلغ Stage به حالت قبل برگردد.

### قواعد
- Undo باید فوری انجام شود.
- Undo باید با انیمیشن ملایم باشد.
- Undo نباید باعث از دست رفتن داده شود.
- اگر خطای دسترسی بود، پیام مناسب نمایش داده شود.

---

## 9. Quick Add Deal

### رفتار
- باید در پایین هر Stage یا در Header Stage باشد.
- کلیک باید DealForm را باز کند.
- Stage باید به‌صورت پیش‌فرض انتخاب شده باشد.
- Pipeline باید به‌صورت پیش‌فرض انتخاب شده باشد.
- بعد از ایجاد، Deal باید در همان Stage نمایش داده شود.

### قواعد
- Quick Add باید ساده و سریع باشد.
- Quick Add نباید فرم طولانی داشته باشد.
- Quick Add باید با کیبورد قابل دسترس باشد.
- Quick Add باید در موبایل قابل استفاده باشد.

---

## 10. Deal Drawer

### رفتار
- کلیک روی Deal Card باید Deal Drawer را باز کند.
- Deal Drawer باید از سمت چپ باز شود در RTL.
- Deal Drawer باید اطلاعات کامل Deal را نشان دهد.
- Deal Drawer باید فرم ویرایش Deal داشته باشد.
- Deal Drawer باید Timeline Deal را نشان دهد.
- Deal Drawer باید اقدامات سریع داشته باشد.

### بخش‌های Deal Drawer
- عنوان Deal
- وضعیت با Badge
- مشتری مرتبط
- ملک مرتبط
- مبلغ معامله
- Agent مسئول
- Stage فعلی
- تاریخ تخمینی
- توضیحات
- Timeline تعامل‌ها
- اقدامات: ویرایش، حذف، ثبت برد/باخت

### قواعد
- Deal Drawer باید Skeleton داشته باشد.
- Deal Drawer باید Empty State برای Timeline داشته باشد.
- Deal Drawer باید Validation Error نشان دهد.
- Deal Drawer باید Unsaved Changes تأیید بگیرد.

---

## 11. Deal Form

### فیلدها
- عنوان معامله
- مشتری مرتبط
- ملک مرتبط
- Agent مسئول
- Pipeline
- Stage
- مبلغ معامله
- احتمال موفقیت
- تاریخ تخمینی بسته شدن
- منبع
- توضیحات

### رفتار
- فرم باید در Modal یا Drawer باز شود.
- فرم باید Inline Validation داشته باشد.
- فرم باید Dirty Check داشته باشد.
- فرم باید Toast موفقیت نشان دهد.
- فرم باید از Submit تکراری جلوگیری کند.

### قواعد
- عنوان الزامی است.
- مشتری الزامی است.
- مبلغ باید عدد صحیح و مثبت باشد.
- Stage باید متعلق به Pipeline انتخاب‌شده باشد.
- در صورت تغییر Pipeline، Stage باید بازنشانی شود.

---

## 12. Stage Settings

### رفتار
- باید برای Admin و Manager در دسترس باشد.
- باید در Dropdown یا Modal باشد.
- باید امکان ایجاد Stage جدید داشته باشد.
- باید امکان ویرایش Stage داشته باشد.
- باید امکان تغییر ترتیب Stageها داشته باشد.
- باید امکان تغییر رنگ Stage داشته باشد.
- باید امکان فعال/غیرفعال کردن Stage داشته باشد.

### قواعد
- Stage Settings باید تأیید بگیرد.
- Stage Settings باید Skeleton داشته باشد.
- Stage Settings باید Validation Error نشان دهد.
- Stage Settings باید Toast موفقیت نشان دهد.

### فیلدهای Stage
- نام Stage
- رنگ Stage
- ترتیب Stage
- Pipeline مرتبط
- وضعیت فعال/غیرفعال
- آیا Stage برنده است
- آیا Stage بازنده است

---

## 13. Empty State در Kanban

### Empty Pipeline
- پیام: «هیچ معامله‌ای در این پایپ‌لاین وجود ندارد»
- دکمه: «ایجاد Deal»
- آیکون: مناسب

### Empty Stage
- پیام: «Deal به این مرحله اضافه نشده است»
- دکمه: «Quick Add Deal» در صورت دسترسی
- آیکون: مناسب

### قواعد
- Empty State باید در هر Stage نمایش داده شود.
- Empty State باید ساده و کوتاه باشد.
- Empty State نباید با Error State اشتباه گرفته شود.

---

## 14. Loading State در Kanban

### Skeleton
- Skeleton برای Stage Headers
- Skeleton برای Deal Cards
- Skeleton برای Pipeline Selector

### رفتار
- Skeleton باید اندازه واقعی محتوا را شبیه‌سازی کند.
- Skeleton باید pulse ملایم داشته باشد.
- Skeleton باید در Dark Mode کم‌رنگ باشد.

---

## 15. Error State در Kanban

### رفتار
- Error State باید پیام فارسی داشته باشد.
- Error State باید دکمه Retry داشته باشد.
- Error State باید آیکون مناسب داشته باشد.

### انواع خطا
- خطای دریافت Dealها
- خطای دریافت Pipelineها
- خطای دریافت Stageها
- خطای Drag & Drop
- خطای دسترسی

### قواعد
- خطای Drag & Drop باید Undo داشته باشد.
- خطای دسترسی باید پیام مناسب داشته باشد.
- خطای سرور باید Alert نمایش دهد.

---

## 16. Kanban در موبایل

### رفتار
- Board باید Scroll افقی داشته باشد.
- ستون‌ها باید حداقل 85% عرض صفحه باشند.
- Deal Cards باید فشرده شوند.
- Drag & Drop باید با Long Press شروع شود.
- Quick Add Deal باید در دسترس باشد.
- Deal Drawer باید تمام‌عرض یا نزدیک به تمام‌عرض باشد.

### قواعد
- Kanban نباید در موبایل به‌صورت عمودی شکسته شود.
- Scroll افقی باید روان باشد.
- Drag & Drop باید با Touch کار کند.
- هدف‌های لمسی باید حداقل 44px باشند.

---

## 17. Kanban در RTL

### رفتار
- Board باید راست‌به‌چپ باشد.
- ستون‌ها باید از راست به چپ مرتب شوند.
- Scroll افقی باید از راست شروع شود.
- Drag & Drop باید با RTL سازگار باشد.
- Deal Card باید راست‌چین باشد.

### قواعد
- Stage Header باید راست‌چین باشد.
- مبلغ‌ها باید راست‌چین باشند.
- تاریخ‌ها باید فارسی و راست‌چین باشند.
- آواتارها باید در سمت راست باشند.

---

## 18. دسترسی‌پذیری Kanban

- Board باید با کیبورد قابل پیمایش باشد.
- Deal Cards باید با Enter یا Space باز شوند.
- Drag & Drop باید جایگزین کیبورد داشته باشد.
- Stage باید با کیبورد قابل انتخاب باشد.
- Quick Add Deal باید با کیبورد قابل دسترس باشد.
- Deal Drawer باید Focus Trap داشته باشد.
- Toastها باید با کیبورد قابل دسترس باشند.

### جایگزین Drag & Drop
- منوی «انتقال به Stage» در Deal Card یا Deal Drawer
- Select برای تغییر Stage در DealForm
- دکمه‌های جابجایی در Deal Drawer

---

## 19. چک‌لیست Kanban

- [ ] Drag & Drop کار می‌کند.
- [ ] Optimistic Update فوری است.
- [ ] Undo Move در صورت خطا کار می‌کند.
- [ ] Stage رنگ مشخص دارد.
- [ ] Stage جمع مبلغ Dealها را نشان می‌دهد.
- [ ] Quick Add Deal در دسترس است.
- [ ] Deal Card اطلاعات کلیدی دارد.
- [ ] Deal Drawer کامل است.
- [ ] DealForm Validation دارد.
- [ ] Stage Settings برای Admin/Manager در دسترس است.
- [ ] Empty State نمایش داده می‌شود.
- [ ] Skeleton Loading نمایش داده می‌شود.
- [ ] Error State با Retry نمایش داده می‌شود.
- [ ] در موبایل Scroll افقی دارد.
- [ ] در RTL درست نمایش داده می‌شود.
- [ ] دسترسی‌پذیری کیبورد رعایت شده است.

---

## 20. جمع‌بندی

| موضوع | رفتار استاندارد |
|---|---|
| Drag & Drop | با موس و لمس، با Feedback بصری |
| Optimistic Update | فوری، بدون انتظار برای سرور |
| Undo Move | در صورت خطای سرور |
| Stage Color | رنگ ملایم در پس‌زمینه، رنگ قوی در نشانگر |
| Stage Total | جمع مبلغ با فرمت فارسی |
| Quick Add Deal | در هر Stage، با فرم ساده |
| Deal Card | عنوان، مشتری، مبلغ، Agent، وضعیت، تاریخ |
| Deal Drawer | اطلاعات کامل، Timeline، اقدامات |
| موبایل | Scroll افقی، Deal Cards فشرده |
| RTL | راست‌به‌چپ کامل |
