from django.contrib import admin
from .models import StudentQuota, QuotaTransaction

class QuotaTransactionInline(admin.TabularInline):
    model = QuotaTransaction
    extra = 1

@admin.register(StudentQuota)
class StudentQuotaAdmin(admin.ModelAdmin):
    list_display = ('student', 'package', 'total_quota', 'used_quota', 'balance', 'status', 'valid_until')
    list_filter = ('status', 'package')
    search_fields = ('student__full_name', 'student__student_number')
    inlines = [QuotaTransactionInline]

@admin.register(QuotaTransaction)
class QuotaTransactionAdmin(admin.ModelAdmin):
    list_display = ('quota', 'transaction_type', 'amount', 'reference')
    list_filter = ('transaction_type',)
    search_fields = ('quota__student__full_name', 'reference')
