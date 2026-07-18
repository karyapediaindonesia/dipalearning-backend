from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.conf import settings
@login_required(login_url='dashboard:page_login')
def index(request):
    context={
        "page_title":"Dashboard Light"
    }
    return render(request,'dashboard/index.html',context)

def index_2(request):
    context={
        "page_title":"Dashboard Dark"
    }
    return render(request,'dashboard/index-2.html',context)


def index_3(request):
    context={
        "page_title":"Dashboard 3"
    }
    return render(request,'dashboard/index-3.html',context)


def index_4(request):
    context={
        "page_title":"Dashboard 4"
    }
    return render(request,'dashboard/index-4.html',context)


def index_5(request):
    context={
        "page_title":"Dashboard 5"
    }
    return render(request,'dashboard/index-5.html',context)


def index_6(request):
    context={
        "page_title":"Dashboard 6"
    }
    return render(request,'dashboard/index-6.html',context)


def index_7(request):
    context={
        "page_title":"Dashboard 7"
    }
    return render(request,'dashboard/index-7.html',context)


def index_8(request):
    context={
        "page_title":"Dashboard 8"
    }
    return render(request,'dashboard/index-8.html',context)

def content(request):
    context={
        "page_title":"Content"
    }
    return render(request,'dashboard/cms/content.html',context)

def content_add(request):
    context={
        "page_title":"Content Add"
    }
    return render(request,'dashboard/cms/content-add.html',context)

def menu(request):
    context={
        "page_title":"Menu"
    }
    return render(request,'dashboard/cms/menu.html',context)

def email_template(request):
    context={
        "page_title":"Email Template"
    }
    return render(request,'dashboard/cms/email-template.html',context)

def add_email(request):
    context={
        "page_title":"Add Email"
    }
    return render(request,'dashboard/cms/add-email.html',context)

def blog(request):
    context={
        "page_title":"Blog"
    }
    return render(request,'dashboard/cms/blog.html',context)

def add_blog(request):
    context={
        "page_title":"Add Blog"
    }
    return render(request,'dashboard/cms/add-blog.html',context)

def blog_category(request):
    context={
        "page_title":"Blog Category"
    }
    return render(request,'dashboard/cms/blog-category.html',context)

def my_wallet(request):
    context={
        "page_title":"My Wallet"
    }
    return render(request,'dashboard/my-wallet.html',context)

def page_invoices(request):
    context={
        "page_title":"Page Invoices"
    }
    return render(request,'dashboard/page-invoices.html',context)


def cards_center(request):
    context={
        "page_title":"Card Center"
    }
    return render(request,'dashboard/cards-center.html',context)

def page_transaction(request):
    context={
        "page_title":"Page Transaction"
    }
    return render(request,'dashboard/page-transaction.html',context)


def transaction_details(request):
    context={
        "page_title":"Transaction Details"
    }
    return render(request,'dashboard/transaction-details.html',context)


@login_required(login_url='dashboard:page_login')
def app_profile(request):
    if request.method == 'POST':
        user = request.user
        
        # Get data from POST
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        
        # Update user fields
        user.first_name = first_name
        user.last_name = last_name
        
        if email:
            user.email = email
            
        # Handle photo upload
        if 'photo' in request.FILES:
            user.photo = request.FILES['photo']
            
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('dashboard:app-profile')

    context={
        "page_title":"Account Settings"
    }
    return render(request,'dashboard/apps/app-profile.html',context)

def post_details(request):
    context={
        "page_title":"Post Details"
    }
    return render(request,'dashboard/apps/post-details.html',context)


def email_compose(request):
    context={
        "page_title":"Compose"
    }
    return render(request,'dashboard/apps/email/email-compose.html',context)

def email_inbox(request):
    context={
        "page_title":"Inbox"
    }
    return render(request,'dashboard/apps/email/email-inbox.html',context)

def email_read(request):
    context={
        "page_title":"Read"
    }
    return render(request,'dashboard/apps/email/email-read.html',context)

def app_calender(request):
    context={
        "page_title":"Calendar"
    }
    return render(request,'dashboard/apps/app-calender.html',context)



def ecom_product_grid(request):
    context={
        "page_title":"Product Grid"
    }
    return render(request,'dashboard/apps/shop/ecom-product-grid.html',context)

def ecom_product_list(request):
    context={
        "page_title":"Product List"
    }
    return render(request,'dashboard/apps/shop/ecom-product-list.html',context)

def ecom_product_detail(request):
    context={
        "page_title":"Product Detail"
    }
    return render(request,'dashboard/apps/shop/ecom-product-detail.html',context)

def ecom_product_order(request):
    context={
        "page_title":"Product Order"
    }
    return render(request,'dashboard/apps/shop/ecom-product-order.html',context)

def ecom_checkout(request):
    context={
        "page_title":"Checkout"
    }
    return render(request,'dashboard/apps/shop/ecom-checkout.html',context)

def ecom_invoice(request):
    context={
        "page_title":"Invoice"
    }
    return render(request,'dashboard/apps/shop/ecom-invoice.html',context)
    
def ecom_customers(request):
    context={
        "page_title":"Customers"
    }
    return render(request,'dashboard/apps/shop/ecom-customers.html',context)



def chart_flot(request):
    context={
        "page_title":"Chart Flot"
    }
    return render(request,'dashboard/charts/chart-flot.html',context)


def chart_morris(request):
    context={
        "page_title":"Chart Morris"
    }
    return render(request,'dashboard/charts/chart-morris.html',context)

def chart_chartjs(request):
    context={
        "page_title":"Chart Chartjs"
    }
    return render(request,'dashboard/charts/chart-chartjs.html',context)

def chart_chartist(request):
    context={
        "page_title":"Chart Chartist"
    }
    return render(request,'dashboard/charts/chart-chartist.html',context)

def chart_sparkline(request):
    context={
        "page_title":"Chart Sparkline"
    }
    return render(request,'dashboard/charts/chart-sparkline.html',context)

def chart_peity(request):
    context={
        "page_title":"Chart Peity"
    }
    return render(request,'dashboard/charts/chart-peity.html',context)




def ui_accordion(request):
    context={
        "page_title":"Accordion"
    }
    return render(request,'dashboard/bootstrap/ui-accordion.html',context)

def ui_alert(request):
    context={
        "page_title":"Alert"
    }
    return render(request,'dashboard/bootstrap/ui-alert.html',context)
    
def ui_badge(request):
    context={
        "page_title":"Badge"
    }
    return render(request,'dashboard/bootstrap/ui-badge.html',context)
    
def ui_button(request):
    context={
        "page_title":"Button"
    }
    return render(request,'dashboard/bootstrap/ui-button.html',context)

def ui_modal(request):
    context={
        "page_title":"Modal"
    }
    return render(request,'dashboard/bootstrap/ui-modal.html',context)

def ui_button_group(request):
    context={
        "page_title":"Button Group"
    }
    return render(request,'dashboard/bootstrap/ui-button-group.html',context)

def ui_list_group(request):
    context={
        "page_title":"List Group"
    }
    return render(request,'dashboard/bootstrap/ui-list-group.html',context)

def ui_card(request):
    context={
        "page_title":"Card"
    }
    return render(request,'dashboard/bootstrap/ui-card.html',context)

def ui_carousel(request):
    context={
        "page_title":"Carousel"
    }
    return render(request,'dashboard/bootstrap/ui-carousel.html',context)

def ui_dropdown(request):
    context={
        "page_title":"Dropdown"
    }
    return render(request,'dashboard/bootstrap/ui-dropdown.html',context)

def ui_popover(request):
    context={
        "page_title":"Popover"
    }
    return render(request,'dashboard/bootstrap/ui-popover.html',context)

def ui_progressbar(request):
    context={
        "page_title":"Progressbar"
    }
    return render(request,'dashboard/bootstrap/ui-progressbar.html',context)

def ui_tab(request):
    context={
        "page_title":"Tab"
    }
    return render(request,'dashboard/bootstrap/ui-tab.html',context)

def ui_typography(request):
    context={
        "page_title":"Typography"
    }
    return render(request,'dashboard/bootstrap/ui-typography.html',context)

def ui_pagination(request):
    context={
        "page_title":"Pagination"
    }
    return render(request,'dashboard/bootstrap/ui-pagination.html',context)

def ui_grid(request):
    context={
        "page_title":"Grid"
    }
    return render(request,'dashboard/bootstrap/ui-grid.html',context)





def uc_select2(request):
    context={
        "page_title":"Select"
    }
    return render(request,'dashboard/plugins/uc-select2.html',context)

def uc_nestable(request):
    context={
        "page_title":"Nestable"
    }
    return render(request,'dashboard/plugins/uc-nestable.html',context)

def uc_noui_slider(request):
    context={
        "page_title":"UI Slider"
    }
    return render(request,'dashboard/plugins/uc-noui-slider.html',context)

def uc_sweetalert(request):
    context={
        "page_title":"Sweet Alert"
    }
    return render(request,'dashboard/plugins/uc-sweetalert.html',context)


def uc_toastr(request):
    context={
        "page_title":"Toastr"
    }
    return render(request,'dashboard/plugins/uc-toastr.html',context)

def map_jqvmap(request):
    context={
        "page_title":"Jqvmap"
    }
    return render(request,'dashboard/plugins/map-jqvmap.html',context)

def uc_lightgallery(request):
    context={
        "page_title":"LightGallery"
    }
    return render(request,'dashboard/plugins/uc-lightgallery.html',context)

def widget_card(request):
    context={
        "page_title":"Widget Card"
    }
    return render(request,'dashboard/widget-card.html',context)

def widget_chart(request):
    context={
        "page_title":"Widget Chart"
    }
    return render(request,'dashboard/widget-chart.html',context)

def widget_list(request):
    context={
        "page_title":"Widget List"
    }
    return render(request,'dashboard/widget-list.html',context)


def form_element(request):
    context={
        "page_title":"Form Element"
    }
    return render(request,'dashboard/forms/form-element.html',context)

def form_wizard(request):
    context={
        "page_title":"Form Wizard"
    }
    return render(request,'dashboard/forms/form-wizard.html',context)

def form_ckeditor(request):
    context={
        "page_title":"Form Ckeditor"
    }
    return render(request,'dashboard/forms/form-ckeditor.html',context)

def form_pickers(request):
    context={
        "page_title":"Pickers"
    }
    return render(request,'dashboard/forms/form-pickers.html',context)

def form_validation(request):
    context={
        "page_title":"Form Validation"
    }
    return render(request,'dashboard/forms/form-validation.html',context)

def table_bootstrap_basic(request):
    context={
        "page_title":"Table Bootstrap"
    }
    return render(request,'dashboard/table/table-bootstrap-basic.html',context)

def table_datatable_basic(request):
    context={
        "page_title":"Table Datatable"
    }
    return render(request,'dashboard/table/table-datatable-basic.html',context)



def page_login(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        next_url = request.POST.get('next') or request.GET.get('next')
        
        # We can try to authenticate using standard authenticate first.
        # If username is an email, it will require a custom backend if not set up.
        # But we can try to fetch the user by email first and then check password.
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        user = authenticate(request, username=u, password=p)
        if user is None:
            # Maybe they used email as username
            try:
                user_obj = User.objects.get(email=u)
                if user_obj.check_password(p):
                    user = user_obj
            except User.DoesNotExist:
                pass
                
        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            if next_url:
                return redirect(next_url)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.error(request, 'Invalid email/username or password.')
            
    return render(request,'dashboard/pages/page-login.html')


def page_logout(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

def page_register(request):
    return render(request,'dashboard/pages/page-register.html')

@login_required(login_url='dashboard:page_login')
def billing_index(request):
    from apps.billing.models import Invoice
    invoices = Invoice.objects.select_related('student').all().order_by('-created_at')
    context = {
        "page_title": "Data Tagihan (Billing)",
        "invoices": invoices
    }
    return render(request, 'dashboard/pages/billing.html', context)

def page_lock_screen(request):
    return render(request,'dashboard/pages/page-lock-screen.html')

def page_forgot_password(request):
    return render(request,'dashboard/pages/page-forgot-password.html')


def page_error_400(request):
    return render(request,'400.html')
    
def page_error_403(request):
    return render(request,'403.html')

def page_error_404(request):
    return render(request,'404.html')

def page_error_500(request):
    return render(request,'500.html')

def page_error_503(request):
    return render(request,'503.html')

def empty_page(request):
    context={
        "page_title":"Page Empty"
    }
    return render(request,'dashboard/pages/empty-page.html',context)

from apps.branches.models import Branch

from django.contrib.auth import get_user_model

def master_cabang(request):
    branches = Branch.objects.all()
    User = get_user_model()
    employees = User.objects.filter(is_active=True)
    context={
        'page_title':'Master Cabang',
        'branches': branches,
        'employees': employees
    }
    return render(request,'dashboard/pages/master-cabang.html',context)


from apps.branches.models import Room
from apps.academics.models import Course, Level

@login_required
def master_ruangan(request):
    rooms = Room.objects.select_related('branch').all().order_by('code')
    branches = Branch.objects.filter(is_active=True)
    return render(request, 'dashboard/pages/master-ruangan.html', {
        'rooms': rooms,
        'branches': branches,
        'page_title': 'Master Ruangan'
    })

@login_required
def master_kursus(request):
    courses = Course.objects.all().order_by('code')
    return render(request, 'dashboard/pages/master-kursus.html', {
        'courses': courses,
        'page_title': 'Master Kursus'
    })

@login_required
def master_level(request):
    levels = Level.objects.select_related('course', 'prerequisite').all().order_by('course__code', 'order')
    courses = Course.objects.filter(is_active=True)
    return render(request, 'dashboard/pages/master-level.html', {
        'levels': levels,
        'courses': courses,
        'page_title': 'Master Level'
    })



from apps.branches.models import Holiday
from apps.attendance.models import AbsenceReason
from apps.finance.models import PaymentMethod, FeeCategory

@login_required
def master_hari_libur(request):
    holidays = Holiday.objects.select_related('branch').all().order_by('-date_start')
    branches = Branch.objects.filter(is_active=True)
    return render(request, 'dashboard/pages/master-hari-libur.html', {
        'holidays': holidays,
        'branches': branches,
        'page_title': 'Master Hari Libur'
    })

@login_required
def master_alasan_absen(request):
    reasons = AbsenceReason.objects.all().order_by('code')
    return render(request, 'dashboard/pages/master-alasan-absen.html', {
        'reasons': reasons,
        'page_title': 'Master Alasan Ketidakhadiran'
    })


@login_required
def master_metode_bayar(request):
    methods = PaymentMethod.objects.all().order_by('code')
    return render(request, 'dashboard/pages/master-metode-bayar.html', {
        'methods': methods,
        'page_title': 'Master Metode Pembayaran'
    })

@login_required
def master_kategori_biaya(request):
    categories = FeeCategory.objects.select_related('parent').all().order_by('code')
    return render(request, 'dashboard/pages/master-kategori-biaya.html', {
        'categories': categories,
        'page_title': 'Master Kategori Biaya'
    })

from apps.students.models import Prospect, Enrollment, Student, ProspectStatus
from apps.hr.models import Employee, JobPosition
from apps.academics.models import Package, AcademicYear, AcademicPeriod, Course

@login_required
def master_status_prospek(request):
    statuses = ProspectStatus.objects.all().order_by('sequence')
    return render(request, 'dashboard/pages/master-status-prospek.html', {
        'statuses': statuses,
        'page_title': 'Master Status Prospek'
    })

@login_required
def master_jabatan(request):
    positions = JobPosition.objects.select_related('parent_position').all().order_by('level', 'name')
    return render(request, 'dashboard/pages/master-jabatan.html', {
        'positions': positions,
        'page_title': 'Master Jabatan'
    })

@login_required
def master_karyawan(request):
    employees = Employee.objects.select_related('job_position').all().order_by('-created_at')
    branches = Branch.objects.filter(is_active=True)
    courses = Course.objects.filter(is_active=True)
    job_positions = JobPosition.objects.filter(status=True).order_by('name')
    return render(request, 'dashboard/pages/master-karyawan.html', {
        'employees': employees,
        'branches': branches,
        'courses': courses,
        'job_positions': job_positions,
        'page_title': 'Master Karyawan'
    })

@login_required
def registrasi_siswa(request):
    prospects = Prospect.objects.prefetch_related('invoices').all().order_by('-created_at')
    branches = Branch.objects.filter(is_active=True)
    return render(request, 'dashboard/pages/registrasi-siswa.html', {
        'prospects': prospects,
        'branches': branches,
        'page_title': 'Registrasi Calon Siswa'
    })

@login_required
def enrollment_siswa(request):
    students = Student.objects.all().order_by('-created_at')
    enrollments = Enrollment.objects.prefetch_related('student__invoices').all().order_by('-created_at')
    branches = Branch.objects.filter(is_active=True)
    courses = Course.objects.filter(is_active=True)
    packages = Package.objects.filter(status='ACTIVE')
    periods = AcademicPeriod.objects.exclude(status='ARCHIVED')
    coaches = Employee.objects.filter(job_position__name__icontains='Coach', status='ACTIVE')
    
    return render(request, 'dashboard/pages/enrollment-siswa.html', {
        'students': students,
        'enrollments': enrollments,
        'branches': branches,
        'courses': courses,
        'packages': packages,
        'periods': periods,
        'coaches': coaches,
        'page_title': 'Enrollment Siswa'
    })



@login_required
def validasi_pembayaran(request):
    from apps.billing.models import Payment
    # Hanya tagihan yang masih PENDING
    payments = Payment.objects.filter(status='PENDING').select_related('invoice').order_by('-created_at')
    
    # Cek apakah user punya hak akses (finance validator)
    is_finance = False
    if hasattr(request.user, 'employee_profile') and request.user.employee_profile and request.user.employee_profile.job_position:
        is_finance = request.user.employee_profile.job_position.is_finance_validator
        
    # Sementara untuk demo, izinkan admin atau semua
    if request.user.is_superuser:
        is_finance = True
        
    return render(request, 'dashboard/pages/validasi-pembayaran.html', {
        'payments': payments,
        'is_finance': is_finance,
        'page_title': 'Validasi Pembayaran'
    })

@login_required
def master_tahun_ajaran(request):
    academic_years = AcademicYear.objects.all().order_by('-start_year')
    academic_periods = AcademicPeriod.objects.select_related('academic_year').all().order_by('-academic_year__start_year', 'sequence')
    branches = Branch.objects.filter(is_active=True)
    return render(request, 'dashboard/pages/master-tahun-ajaran.html', {
        'academic_years': academic_years,
        'academic_periods': academic_periods,
        'branches': branches,
        'page_title': 'Master Tahun Ajaran / Periode'
    })
