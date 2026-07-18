from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.finance.models import PaymentMethod, FeeCategory
from apps.billing.models import Invoice, Payment
from apps.students.models import Student

class FinanceDeleteTestCase(TestCase):
    def setUp(self):
        self.method = PaymentMethod.objects.create(
            code="TF-BCA",
            name="Transfer BCA",
            processing_mode="MANUAL"
        )
        self.category = FeeCategory.objects.create(
            code="OPEX-01",
            name="Operational",
            classification="OPEX",
            cost_nature="VARIABLE"
        )

    def test_payment_method_soft_delete(self):
        self.method.delete()
        with self.assertRaises(PaymentMethod.DoesNotExist):
            self.method.refresh_from_db()
        
    def test_payment_method_with_payment_fails_delete(self):
        # Create a payment using this method
        # First we need a student and invoice
        student = Student.objects.create(
            full_name="Jane Doe",
            status="ACTIVE"
        )
        invoice = Invoice.objects.create(
            student=student,
            invoice_number="INV-001",
            total_amount=100000,
            status="UNPAID"
        )
        payment = Payment.objects.create(
            invoice=invoice,
            payment_number="PAY-001",
            amount=100000,
            payment_method=self.method,
            status="VERIFIED"
        )
        
        with self.assertRaises(ValidationError):
            self.method.delete()
            
        self.method.refresh_from_db()
        self.assertTrue(self.method.is_active)

    def test_fee_category_soft_delete(self):
        self.category.delete()
        with self.assertRaises(FeeCategory.DoesNotExist):
            self.category.refresh_from_db()
        
    def test_fee_category_with_subcategory_fails_delete(self):
        subcategory = FeeCategory.objects.create(
            code="OPEX-SUB",
            name="Sub Operational",
            parent=self.category,
            classification="OPEX",
            cost_nature="VARIABLE"
        )
        
        with self.assertRaises(ValidationError):
            self.category.delete()
            
        self.category.refresh_from_db()
        self.assertTrue(self.category.is_active)
