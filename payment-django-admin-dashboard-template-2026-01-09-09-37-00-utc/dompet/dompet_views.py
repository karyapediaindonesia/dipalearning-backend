from django.shortcuts import render

def index(request):
    context={
        "page_title":"Dashboard Light"
    }
    return render(request,'dompet/index.html',context)

def index_2(request):
    context={
        "page_title":"Dashboard Dark"
    }
    return render(request,'dompet/index-2.html',context)


def index_3(request):
    context={
        "page_title":"Dashboard 3"
    }
    return render(request,'dompet/index-3.html',context)


def index_4(request):
    context={
        "page_title":"Dashboard 4"
    }
    return render(request,'dompet/index-4.html',context)


def index_5(request):
    context={
        "page_title":"Dashboard 5"
    }
    return render(request,'dompet/index-5.html',context)


def index_6(request):
    context={
        "page_title":"Dashboard 6"
    }
    return render(request,'dompet/index-6.html',context)


def index_7(request):
    context={
        "page_title":"Dashboard 7"
    }
    return render(request,'dompet/index-7.html',context)


def index_8(request):
    context={
        "page_title":"Dashboard 8"
    }
    return render(request,'dompet/index-8.html',context)

def content(request):
    context={
        "page_title":"Content"
    }
    return render(request,'dompet/cms/content.html',context)

def content_add(request):
    context={
        "page_title":"Content Add"
    }
    return render(request,'dompet/cms/content-add.html',context)

def menu(request):
    context={
        "page_title":"Menu"
    }
    return render(request,'dompet/cms/menu.html',context)

def email_template(request):
    context={
        "page_title":"Email Template"
    }
    return render(request,'dompet/cms/email-template.html',context)

def add_email(request):
    context={
        "page_title":"Add Email"
    }
    return render(request,'dompet/cms/add-email.html',context)

def blog(request):
    context={
        "page_title":"Blog"
    }
    return render(request,'dompet/cms/blog.html',context)

def add_blog(request):
    context={
        "page_title":"Add Blog"
    }
    return render(request,'dompet/cms/add-blog.html',context)

def blog_category(request):
    context={
        "page_title":"Blog Category"
    }
    return render(request,'dompet/cms/blog-category.html',context)

def my_wallet(request):
    context={
        "page_title":"My Wallet"
    }
    return render(request,'dompet/my-wallet.html',context)

def page_invoices(request):
    context={
        "page_title":"Page Invoices"
    }
    return render(request,'dompet/page-invoices.html',context)


def cards_center(request):
    context={
        "page_title":"Card Center"
    }
    return render(request,'dompet/cards-center.html',context)

def page_transaction(request):
    context={
        "page_title":"Page Transaction"
    }
    return render(request,'dompet/page-transaction.html',context)


def transaction_details(request):
    context={
        "page_title":"Transaction Details"
    }
    return render(request,'dompet/transaction-details.html',context)


def app_profile(request):
    context={
        "page_title":"App Profile"
    }
    return render(request,'dompet/apps/app-profile.html',context)

def post_details(request):
    context={
        "page_title":"Post Details"
    }
    return render(request,'dompet/apps/post-details.html',context)


def email_compose(request):
    context={
        "page_title":"Compose"
    }
    return render(request,'dompet/apps/email/email-compose.html',context)

def email_inbox(request):
    context={
        "page_title":"Inbox"
    }
    return render(request,'dompet/apps/email/email-inbox.html',context)

def email_read(request):
    context={
        "page_title":"Read"
    }
    return render(request,'dompet/apps/email/email-read.html',context)

def app_calender(request):
    context={
        "page_title":"Calendar"
    }
    return render(request,'dompet/apps/app-calender.html',context)



def ecom_product_grid(request):
    context={
        "page_title":"Product Grid"
    }
    return render(request,'dompet/apps/shop/ecom-product-grid.html',context)

def ecom_product_list(request):
    context={
        "page_title":"Product List"
    }
    return render(request,'dompet/apps/shop/ecom-product-list.html',context)

def ecom_product_detail(request):
    context={
        "page_title":"Product Detail"
    }
    return render(request,'dompet/apps/shop/ecom-product-detail.html',context)

def ecom_product_order(request):
    context={
        "page_title":"Product Order"
    }
    return render(request,'dompet/apps/shop/ecom-product-order.html',context)

def ecom_checkout(request):
    context={
        "page_title":"Checkout"
    }
    return render(request,'dompet/apps/shop/ecom-checkout.html',context)

def ecom_invoice(request):
    context={
        "page_title":"Invoice"
    }
    return render(request,'dompet/apps/shop/ecom-invoice.html',context)
    
def ecom_customers(request):
    context={
        "page_title":"Customers"
    }
    return render(request,'dompet/apps/shop/ecom-customers.html',context)



def chart_flot(request):
    context={
        "page_title":"Chart Flot"
    }
    return render(request,'dompet/charts/chart-flot.html',context)


def chart_morris(request):
    context={
        "page_title":"Chart Morris"
    }
    return render(request,'dompet/charts/chart-morris.html',context)

def chart_chartjs(request):
    context={
        "page_title":"Chart Chartjs"
    }
    return render(request,'dompet/charts/chart-chartjs.html',context)

def chart_chartist(request):
    context={
        "page_title":"Chart Chartist"
    }
    return render(request,'dompet/charts/chart-chartist.html',context)

def chart_sparkline(request):
    context={
        "page_title":"Chart Sparkline"
    }
    return render(request,'dompet/charts/chart-sparkline.html',context)

def chart_peity(request):
    context={
        "page_title":"Chart Peity"
    }
    return render(request,'dompet/charts/chart-peity.html',context)




def ui_accordion(request):
    context={
        "page_title":"Accordion"
    }
    return render(request,'dompet/bootstrap/ui-accordion.html',context)

def ui_alert(request):
    context={
        "page_title":"Alert"
    }
    return render(request,'dompet/bootstrap/ui-alert.html',context)
    
def ui_badge(request):
    context={
        "page_title":"Badge"
    }
    return render(request,'dompet/bootstrap/ui-badge.html',context)
    
def ui_button(request):
    context={
        "page_title":"Button"
    }
    return render(request,'dompet/bootstrap/ui-button.html',context)

def ui_modal(request):
    context={
        "page_title":"Modal"
    }
    return render(request,'dompet/bootstrap/ui-modal.html',context)

def ui_button_group(request):
    context={
        "page_title":"Button Group"
    }
    return render(request,'dompet/bootstrap/ui-button-group.html',context)

def ui_list_group(request):
    context={
        "page_title":"List Group"
    }
    return render(request,'dompet/bootstrap/ui-list-group.html',context)

def ui_card(request):
    context={
        "page_title":"Card"
    }
    return render(request,'dompet/bootstrap/ui-card.html',context)

def ui_carousel(request):
    context={
        "page_title":"Carousel"
    }
    return render(request,'dompet/bootstrap/ui-carousel.html',context)

def ui_dropdown(request):
    context={
        "page_title":"Dropdown"
    }
    return render(request,'dompet/bootstrap/ui-dropdown.html',context)

def ui_popover(request):
    context={
        "page_title":"Popover"
    }
    return render(request,'dompet/bootstrap/ui-popover.html',context)

def ui_progressbar(request):
    context={
        "page_title":"Progressbar"
    }
    return render(request,'dompet/bootstrap/ui-progressbar.html',context)

def ui_tab(request):
    context={
        "page_title":"Tab"
    }
    return render(request,'dompet/bootstrap/ui-tab.html',context)

def ui_typography(request):
    context={
        "page_title":"Typography"
    }
    return render(request,'dompet/bootstrap/ui-typography.html',context)

def ui_pagination(request):
    context={
        "page_title":"Pagination"
    }
    return render(request,'dompet/bootstrap/ui-pagination.html',context)

def ui_grid(request):
    context={
        "page_title":"Grid"
    }
    return render(request,'dompet/bootstrap/ui-grid.html',context)





def uc_select2(request):
    context={
        "page_title":"Select"
    }
    return render(request,'dompet/plugins/uc-select2.html',context)

def uc_nestable(request):
    context={
        "page_title":"Nestable"
    }
    return render(request,'dompet/plugins/uc-nestable.html',context)

def uc_noui_slider(request):
    context={
        "page_title":"UI Slider"
    }
    return render(request,'dompet/plugins/uc-noui-slider.html',context)

def uc_sweetalert(request):
    context={
        "page_title":"Sweet Alert"
    }
    return render(request,'dompet/plugins/uc-sweetalert.html',context)


def uc_toastr(request):
    context={
        "page_title":"Toastr"
    }
    return render(request,'dompet/plugins/uc-toastr.html',context)

def map_jqvmap(request):
    context={
        "page_title":"Jqvmap"
    }
    return render(request,'dompet/plugins/map-jqvmap.html',context)

def uc_lightgallery(request):
    context={
        "page_title":"LightGallery"
    }
    return render(request,'dompet/plugins/uc-lightgallery.html',context)

def widget_card(request):
    context={
        "page_title":"Widget Card"
    }
    return render(request,'dompet/widget-card.html',context)

def widget_chart(request):
    context={
        "page_title":"Widget Chart"
    }
    return render(request,'dompet/widget-chart.html',context)

def widget_list(request):
    context={
        "page_title":"Widget List"
    }
    return render(request,'dompet/widget-list.html',context)


def form_element(request):
    context={
        "page_title":"Form Element"
    }
    return render(request,'dompet/forms/form-element.html',context)

def form_wizard(request):
    context={
        "page_title":"Form Wizard"
    }
    return render(request,'dompet/forms/form-wizard.html',context)

def form_ckeditor(request):
    context={
        "page_title":"Form Ckeditor"
    }
    return render(request,'dompet/forms/form-ckeditor.html',context)

def form_pickers(request):
    context={
        "page_title":"Pickers"
    }
    return render(request,'dompet/forms/form-pickers.html',context)

def form_validation(request):
    context={
        "page_title":"Form Validation"
    }
    return render(request,'dompet/forms/form-validation.html',context)

def table_bootstrap_basic(request):
    context={
        "page_title":"Table Bootstrap"
    }
    return render(request,'dompet/table/table-bootstrap-basic.html',context)

def table_datatable_basic(request):
    context={
        "page_title":"Table Datatable"
    }
    return render(request,'dompet/table/table-datatable-basic.html',context)



def page_login(request):
    return render(request,'dompet/pages/page-login.html')

def page_register(request):
    return render(request,'dompet/pages/page-register.html')

def page_lock_screen(request):
    return render(request,'dompet/pages/page-lock-screen.html')

def page_forgot_password(request):
    return render(request,'dompet/pages/page-forgot-password.html')


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
    return render(request,'dompet/pages/empty-page.html',context)












