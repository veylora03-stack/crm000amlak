# کامپوننت‌ها — CRM تخصصی املاک

این سند کامپوننت‌های پایه و مشترک محصول را تعریف می‌کند. همه کامپوننت‌ها باید RTL، فارسی، Dark Mode، Responsive و دسترس‌پذیر باشند. هیچ کامپوننتی نباید خارج از این لیست و بدون نیاز ماژول‌های تعریف‌شده اضافه شود.

---

## قواعد عمومی کامپوننت‌ها

- همه کامپوننت‌ها باید از Design Tokens استفاده کنند.
- همه کامپوننت‌ها باید در Dark Mode درست نمایش داده شوند.
- همه کامپوننت‌ها باید با RTL سازگار باشند.
- همه عناصر تعاملی باید focus visible داشته باشند.
- همه فرم‌ها باید Validation Error را به‌صورت فارسی نمایش دهند.
- هیچ کامپوننتی نباید متن انگلیسی بدون ضرورت فنی نمایش دهد.
- کامپوننت‌ها باید تا حد امکان stateless یا نیمه‌stateless باشند و داده از Store یا API گرفته شود.
- برای هر کامپوننت باید حالت‌های Loading، Disabled، Error و Empty در صورت نیاز تعریف شود.

---

## 1. Button

### هدف
انجام یک عمل اصلی یا ثانویه.

### انواع
- Primary
- Secondary
- Ghost
- Danger
- Icon Button
- Loading Button

### Props اصلی
- variant
- size
- disabled
- loading
- icon
- type
- block

### رفتار
- در حالت loading باید Spinner نمایش داده شود و کلیک غیرفعال شود.
- دکمه Primary فقط برای مهم‌ترین اقدام صفحه استفاده شود.
- دکمه Danger باید برای حذف و عملیات پرخطر استفاده شود.
- حداقل ارتفاع دکمه باید 44px باشد.
- متن دکمه باید فارسی، کوتاه و عملیاتی باشد.

### حالت‌ها
- Default
- Hover
- Focus
- Active
- Disabled
- Loading

---

## 2. Input

### هدف
دریافت متن، عدد، مبلغ یا شناسه.

### انواع
- Text Input
- Number Input
- Money Input
- Password Input
- Search Input

### Props اصلی
- label
- placeholder
- value
- error
- hint
- disabled
- required
- type
- dir

### رفتار
- Label باید همیشه نمایش داده شود.
- Placeholder نباید جایگزین Label شود.
- پیام خطا باید زیر فیلد و به فارسی باشد.
- فیلد مبلغ باید جداکننده هزارگان را فقط در نمایش نشان دهد.
- فیلد موبایل یا ایمیل می‌تواند dir مناسب داشته باشد.
- در موبایل باید از زوم ناخواسته جلوگیری شود.

### حالت‌ها
- Default
- Focus
- Error
- Disabled
- Loading در صورت نیاز

---

## 3. Select

### هدف
انتخاب یک مقدار از لیست گزینه‌ها.

### Props اصلی
- label
- options
- value
- placeholder
- error
- disabled
- searchable
- clearable

### رفتار
- باید با کیبورد قابل استفاده باشد.
- گزینه انتخاب‌شده باید واضح باشد.
- در موبایل باید تجربه انتخاب ساده داشته باشد.
- برای لیست‌های طولانی می‌تواند جستجو داخلی داشته باشد.
- گزینه غیرفعال باید کم‌رنگ باشد.

### حالت‌ها
- Closed
- Open
- Focus
- Error
- Disabled
- Empty Options

---

## 4. MultiSelect

### هدف
انتخاب چند مقدار از لیست گزینه‌ها.

### Props اصلی
- label
- options
- selected
- placeholder
- maxSelected
- searchable
- error
- disabled

### رفتار
- گزینه‌های انتخاب‌شده باید به‌صورت Tag نمایش داده شوند.
- هر Tag باید دکمه حذف داشته باشد.
- باید امکان پاک کردن همه وجود داشته باشد.
- در موبایل باید به‌صورت Modal یا Drawer انتخاب شود.
- جستجو باید با Debounce انجام شود.

### حالت‌ها
- Empty
- Selected
- Focus
- Error
- Disabled
- Loading Options

---

## 5. Date Picker

### هدف
انتخاب تاریخ شمسی.

### Props اصلی
- label
- value
- min
- max
- error
- disabled
- placeholder

### رفتار
- نمایش تاریخ باید شمسی باشد.
- ذخیره در دیتابیس باید به‌صورت timezone-aware انجام شود.
- انتخاب روز باید با کیبورد ممکن باشد.
- باید قابلیت پاک کردن تاریخ وجود داشته باشد.
- در موبایل باید به‌صورت Drawer یا Modal نمایش داده شود.

### حالت‌ها
- Default
- Open
- Selected
- Error
- Disabled
- Empty

---

## 6. Tag Input

### هدف
ورود چند برچسب یا مقدار متنی کوتاه.

### Props اصلی
- label
- tags
- placeholder
- maxTags
- error
- disabled

### رفتار
- با Enter یا کاما برچسب جدید اضافه شود.
- برچسب‌ها باید قابل حذف باشند.
- برچسب تکراری نباید ثبت شود.
- در موبایل باید ورود برچسب ساده باشد.
- برای مناطق مورد نظر، امکانات رفاهی و برچسب‌های مشتری استفاده شود.

### حالت‌ها
- Empty
- Typing
- Selected Tags
- Error
- Disabled

---

## 7. Modal

### هدف
نمایش فرم، تأیید یا اطلاعات مهم بدون ترک صفحه.

### Props اصلی
- title
- open
- size
- closable
- loading
- footer

### رفتار
- با Escape بسته شود.
- با کلیک روی Overlay فقط در صورت نداشتن تغییرات ذخیره‌نشده بسته شود.
- فوکوس اولیه باید داخل Modal باشد.
- فوکوس باید بعد از بسته شدن به عنصر قبلی برگردد.
- اسکرول بدنه باید هنگام باز بودن قفل شود.

### حالت‌ها
- Loading
- Empty
- Error
- Confirm
- Form Validation Error
- Unsaved Changes

---

## 8. Drawer

### هدف
نمایش جزئیات، فرم‌های کناری یا ویرایش سریع بدون تغییر کامل صفحه.

### Props اصلی
- title
- open
- width
- side
- closable
- footer

### رفتار
- در RTL بهتر است Drawer جزئیات از سمت چپ باز شود.
- با Escape بسته شود.
- باید Overlay داشته باشد.
- باید اسکرول داخلی داشته باشد.
- برای Client Detail، Deal Drawer و فرم‌های سریع استفاده شود.

### حالت‌ها
- Loading
- Empty
- Error
- Form Validation Error
- Unsaved Changes

---

## 9. Toast

### هدف
نمایش پیام کوتاه موفقیت، خطا، هشدار یا اطلاعات.

### انواع
- Success
- Error
- Warning
- Info

### Props اصلی
- type
- title
- message
- duration
- action

### رفتار
- باید به‌صورت خودکار بسته شود، مگر برای خطاهای مهم.
- باید در پایین یا گوشه مناسب نمایش داده شود.
- نباید بیش از 3 Toast همزمان نمایش داده شود.
- باید با آیکون و رنگ وضعیت همراه باشد.
- باید در Dark Mode خوانا باشد.

### حالت‌ها
- Visible
- Closing
- Action Available
- Error Retry

---

## 10. Alert

### هدف
نمایش پیام ثابت و مهم داخل صفحه.

### انواع
- Success
- Warning
- Danger
- Info

### Props اصلی
- type
- title
- message
- closable
- icon

### رفتار
- باید در بالای فرم یا بخش مرتبط نمایش داده شود.
- برای خطای سرور، عدم دسترسی و هشدارهای مهم استفاده شود.
- نباید جایگزین Validation زیر فیلد شود.
- باید آیکون و متن فارسی داشته باشد.

### حالت‌ها
- Visible
- Dismissed
- Error
- Retry Action

---

## 11. Badge

### هدف
نمایش وضعیت، تعداد یا برچسب کوچک.

### انواع
- Status Badge
- Count Badge
- Color Badge
- Pill Badge

### Props اصلی
- label
- color
- count
- dot

### رفتار
- Badge باید کوتاه باشد.
- رنگ Badge باید از توکن‌های وضعیت پیروی کند.
- Count Badge برای نوتیفیکیشن‌ها استفاده شود.
- در جدول‌ها باید وضعیت‌ها با Badge نمایش داده شوند.

### حالت‌ها
- Default
- Active
- Muted
- Danger
- Success
- Warning
- Info

---

## 12. Avatar

### هدف
نمایش تصویر کاربر یا حرف اول نام.

### Props اصلی
- src
- name
- size
- status

### رفتار
- اگر تصویر نبود، حرف اول نام نمایش داده شود.
- باید در اندازه‌های کوچک، متوسط و بزرگ پشتیبانی شود.
- باید در Topbar، جدول‌ها و Detail Pages استفاده شود.
- باید در RTL با متن کنار خود فاصله مناسب داشته باشد.

### حالت‌ها
- Image
- Initials
- Loading
- Error
- Offline/Online در صورت نیاز

---

## 13. Tabs

### هدف
جابجایی بین بخش‌های مرتبط داخل یک صفحه.

### Props اصلی
- tabs
- activeTab
- onChange
- scrollable

### رفتار
- باید با کیبورد قابل پیمایش باشد.
- Tab فعال باید واضح باشد.
- در موبایل باید قابل اسکرول افقی باشد.
- برای Client Detail، Settings و Property Detail استفاده شود.
- محتوای Tab باید Loading و Empty State داشته باشد.

### حالت‌ها
- Active
- Hover
- Focus
- Disabled
- Loading Content
- Empty Content

---

## 14. Table

### هدف
نمایش داده‌های لیستی با Pagination، Sort و فیلتر.

### Props اصلی
- columns
- rows
- loading
- emptyText
- selectable
- stickyHeader
- density

### رفتار
- Pagination باید سمت سرور باشد.
- Sort باید با آیکون مشخص باشد.
- Row Hover باید مشخص باشد.
- کلیک روی Row باید به صفحه Detail برود.
- در موبایل باید به کارت یا Scroll افقی تبدیل شود.
- Header باید در دسکتاپ sticky باشد.

### حالت‌ها
- Loading Skeleton
- Empty
- Error
- Selected Rows
- No Permission
- Sorting

---

## 15. Pagination

### هدف
جابجایی بین صفحات نتایج.

### Props اصلی
- page
- pageSize
- total
- onChange

### رفتار
- باید شماره صفحه، تعداد نتایج و صفحه‌بندی را نشان دهد.
- در موبایل باید ساده و فشرده شود.
- باید با API Pagination هماهنگ باشد.
- نباید داده بیشتری از max_page_size درخواست کند.
- باید Loading State داشته باشد.

### حالت‌ها
- Default
- Active Page
- Disabled
- Loading
- First/Last

---

## 16. Skeleton

### هدف
نمایش حالت بارگذاری به‌جای Spinner خالی.

### انواع
- Text Skeleton
- Card Skeleton
- Table Skeleton
- Chart Skeleton
- Avatar Skeleton
- Kanban Skeleton

### رفتار
- باید با توکن surface-muted ساخته شود.
- باید اندازه واقعی محتوا را شبیه‌سازی کند.
- باید در Dashboard، جدول‌ها، Detail Pages و جستجو استفاده شود.
- نباید بیش از حد چشمک بزند.
- باید در Dark Mode کم‌رنگ باشد.

### حالت‌ها
- Loading
- Partial Loading
- Infinite Loading در صورت نیاز

---

## 17. Empty State

### هدف
نمایش پیام مناسب وقتی داده‌ای وجود ندارد.

### Props اصلی
- title
- description
- icon
- action

### رفتار
- باید متن فارسی داشته باشد.
- باید آیکون مرتبط داشته باشد.
- در صورت امکان باید CTA داشته باشد.
- برای لیست خالی، جستجوی بدون نتیجه و Dashboard خالی استفاده شود.
- نباید با Error State اشتباه گرفته شود.

### حالت‌ها
- No Data
- No Search Result
- No Permission
- No Notifications
- No Tasks

---

## 18. Error State

### هدف
نمایش خطای دریافت داده یا عملیات.

### Props اصلی
- title
- message
- retryAction
- icon

### رفتار
- باید پیام فارسی و قابل فهم داشته باشد.
- باید دکمه تلاش مجدد داشته باشد.
- نباید جزئیات فنی حساس نمایش دهد.
- باید در جدول‌ها، Dashboard، Detail Pages و جستجو استفاده شود.
- برای خطای Validation باید زیر فیلد برود، نه به‌صورت Error State کلی.

### حالت‌ها
- Network Error
- Server Error
- Permission Denied
- Not Found
- Export Error

---

## 19. Card

### هدف
نگه‌داری محتوای مرتبط در یک سطح جدا.

### Props اصلی
- title
- subtitle
- footer
- loading
- padding
- clickable

### رفتار
- باید surface، border و radius استاندارد داشته باشد.
- در Dashboard، Settings و Detail Pages استفاده شود.
- کارت clickable باید focus و hover مشخص داشته باشد.
- نباید بیش از حد تو در تو شود.

### حالت‌ها
- Default
- Hover
- Loading
- Empty
- Error
- Clickable

---

## 20. KPI Card

### هدف
نمایش یک شاخص کلیدی در Dashboard.

### Props اصلی
- title
- value
- change
- icon
- loading
- link

### رفتار
- مقدار باید بزرگ و فارسی باشد.
- عنوان باید کوتاه باشد.
- تغییر نسبت به دوره قبل باید با رنگ success یا danger نمایش داده شود.
- باید قابل کلیک به لیست مرتبط باشد.
- باید Skeleton داشته باشد.

### حالت‌ها
- Loading
- Positive Change
- Negative Change
- Neutral Change
- Empty
- Error

---

## 21. Chart Card

### هدف
نمایش نمودار داخل Dashboard یا Reports.

### Props اصلی
- title
- type
- data
- loading
- emptyAction
- filters

### رفتار
- باید Skeleton داشته باشد.
- باید Empty State داشته باشد.
- باید Tooltip فارسی داشته باشد.
- باید در Dark Mode خوانا باشد.
- باید برای لیدها، Dealها، Funnel و وضعیت املاک استفاده شود.

### حالت‌ها
- Loading
- Empty
- Error
- Filtered
- No Permission

---

## 22. Timeline

### هدف
نمایش تعامل‌ها و فعالیت‌های مشتری یا Deal به ترتیب زمان.

### Props اصلی
- items
- loading
- emptyText
- loadMore

### رفتار
- باید راست‌به‌چپ باشد.
- هر آیتم باید نوع تعامل، تاریخ، کاربر و خلاصه را نشان دهد.
- باید آیکون مخصوص هر نوع تعامل داشته باشد.
- باید پیوست‌ها را نمایش دهد.
- باید Load More برای داده زیاد داشته باشد.

### حالت‌ها
- Loading
- Empty
- Error
- Load More
- No Permission

---

## 23. Kanban Board

### هدف
مدیریت Dealها در Stageهای مختلف.

### Props اصلی
- pipeline
- stages
- deals
- loading
- canEdit

### رفتار
- باید Drag & Drop داشته باشد.
- باید Optimistic Update داشته باشد.
- در صورت خطا، تغییر باید Undo شود.
- باید جمع مبلغ و تعداد Deal هر Stage را نشان دهد.
- باید در موبایل Scroll افقی داشته باشد.

### حالت‌ها
- Loading
- Empty Pipeline
- Empty Stage
- Dragging
- Error
- No Permission

---

## 24. Kanban Card

### هدف
نمایش خلاصه یک Deal در Board.

### Props اصلی
- deal
- onClick
- draggable
- selected

### رفتار
- باید عنوان، مشتری، مبلغ، Agent، وضعیت و تاریخ را نشان دهد.
- باید با کلیک باز شود و Deal Drawer را نمایش دهد.
- باید Drag Feedback داشته باشد.
- باید در Dark Mode خوانا باشد.
- نباید اطلاعات زیاد و شلوغ نمایش دهد.

### حالت‌ها
- Default
- Hover
- Dragging
- Selected
- Error/Undo
- Won/Lost Status

---

## 25. Dropdown

### هدف
نمایش منوی اقدامات یا انتخاب‌های سریع.

### Props اصلی
- trigger
- items
- align
- disabled

### رفتار
- باید با کیبورد قابل پیمایش باشد.
- باید با Escape بسته شود.
- باید با کلیک بیرون بسته شود.
- برای Row Actions، User Menu و Stage Settings استفاده شود.
- نباید آیتم‌های زیاد بدون گروه‌بندی داشته باشد.

### حالت‌ها
- Closed
- Open
- Hover
- Focus
- Disabled
- Selected

---

## 26. Tooltip

### هدف
نمایش راهنمای کوتاه روی عناصر.

### Props اصلی
- content
- position
- delay

### رفتار
- باید با فوکوس کیبورد هم نمایش داده شود.
- نباید اطلاعات مهم را فقط داخل Tooltip قرار دهد.
- باید کوتاه باشد.
- باید در Dark Mode کنتراست کافی داشته باشد.
- برای آیکون‌ها و متن‌های کوتاه استفاده شود.

### حالت‌ها
- Hidden
- Visible
- Focus
- Disabled Target

---

## 27. File Upload

### هدف
آپلود فایل برای تعامل‌ها یا تصاویر ملک.

### Props اصلی
- accept
- maxSize
- multiple
- value
- error

### رفتار
- باید Preview برای تصویر داشته باشد.
- باید محدودیت 10MB را اعتبارسنجی کند.
- باید فرمت‌های مجاز را کنترل کند.
- باید Progress نشان دهد.
- باید امکان حذف فایل قبل از ذخیره وجود داشته باشد.

### حالت‌ها
- Empty
- Uploading
- Preview
- Error
- Success
- Disabled

---

## 28. Image Gallery

### هدف
نمایش تصاویر ملک.

### Props اصلی
- images
- primaryImage
- loading
- canManage

### رفتار
- باید تصویر اصلی را بزرگ نشان دهد.
- باید Thumbnailها را نمایش دهد.
- باید امکان مرتب‌سازی برای کاربر مجاز داشته باشد.
- باید امکان تعیین تصویر اصلی داشته باشد.
- باید در موبایل به‌صورت Swipe باشد.

### حالت‌ها
- Loading
- Empty
- Error
- Selected Image
- Manage Mode
- No Permission

---

## 29. Map

### هدف
نمایش موقعیت ملک و انتخاب Lat/Lng.

### Props اصلی
- latitude
- longitude
- zoom
- editable
- markers

### رفتار
- فقط در ماژول املاک استفاده شود.
- باید موقعیت ملک را نشان دهد.
- باید در حالت ویرایش قابل کلیک برای انتخاب موقعیت باشد.
- باید در موبایل قابل استفاده باشد.
- نباید به‌صورت غیرضروری لود شود؛ Lazy Load شود.

### حالت‌ها
- Loading
- Empty
- Error
- Editable
- Readonly
- No Location

---

## 30. Notification Bell

### هدف
نمایش نوتیفیکیشن‌ها در Topbar.

### Props اصلی
- unreadCount
- notifications
- loading

### رفتار
- باید Dropdown داشته باشد.
- باید تعداد خوانده‌نشده را نشان دهد.
- باید کلیک برای خوانده‌شده داشته باشد.
- باید به صفحه Notifications لینک دهد.
- باید Skeleton برای Dropdown داشته باشد.

### حالت‌ها
- Empty
- Loading
- Unread
- Read
- Error

---

## 31. Search Box

### هدف
جستجوی سریع در Topbar یا Command Palette.

### Props اصلی
- value
- placeholder
- loading
- results
- shortcut

### رفتار
- باید Debounce حداقل 300ms داشته باشد.
- باید Skeleton هنگام جستجو داشته باشد.
- باید Empty State برای نتیجه نداشتن داشته باشد.
- باید نتایج را گروه‌بندی کند.
- باید با Ctrl + K فعال شود.

### حالت‌ها
- Empty
- Typing
- Loading
- Results
- No Results
- Error

---

## 32. Command Palette

### هدف
دسترسی سریع به جستجو و دستورات محدود.

### Props اصلی
- open
- query
- results
- commands

### رفتار
- باید با Ctrl + K باز شود.
- باید با Escape بسته شود.
- باید با کیبورد پیمایش شود.
- باید نتایج گروه‌بندی‌شده داشته باشد.
- باید در ز-index بالاتر از Modal و Drawer باشد.

### حالت‌ها
- Closed
- Open
- Loading
- No Results
- Error
- Selected Item

---

## جمع‌بندی کامپوننت‌ها

| دسته | کامپوننت‌ها |
|---|---|
| فرم | Button، Input، Select، MultiSelect، Date Picker، Tag Input، File Upload |
| بازخورد | Toast، Alert، Skeleton، Empty State، Error State |
| نمایش داده | Badge، Avatar، Table، Pagination، Timeline، Card، KPI Card، Chart Card |
| ناوبری | Tabs، Dropdown، Tooltip، Search Box، Command Palette |
| صفحه‌ای | Modal، Drawer |
| ماژولی | Kanban Board، Kanban Card، Image Gallery، Map، Notification Bell |
