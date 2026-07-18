from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.students.models import Prospect, ProspectParent, ProspectAddress, ProspectSource, ProspectGuardian, ProspectInterest, Student
from apps.branches.models import Branch
from django.utils import timezone

class ProspectDeleteTestCase(TestCase):
    def setUp(self):
        self.branch = Branch.objects.create(
            code="BR01",
            name="Branch Test",
            branch_type="BRANCH",
            address="Test Address",
            province="DKI Jakarta",
            city="Jakarta Selatan",
            status="ACTIVE"
        )
        self.prospect = Prospect.objects.create(
            full_name="John Doe",
            gender="L",
            edu_status="STUDENT",
            edu_level="SD",
            target_branch=self.branch
        )
        
    def test_prospect_soft_delete(self):
        # Create related profiles
        parent = ProspectParent.objects.create(
            prospect=self.prospect,
            relation="AYAH",
            full_name="Father Doe",
            whatsapp="08123456789"
        )
        address = ProspectAddress.objects.create(
            prospect=self.prospect,
            full_address="Test Address",
            province="DKI Jakarta",
            city="Jakarta Selatan"
        )
        source = ProspectSource.objects.create(
            prospect=self.prospect,
            source="WEBSITE"
        )
        guardian = ProspectGuardian.objects.create(
            prospect=self.prospect,
            guardian_name="Guardian Doe",
            relationship="SAUDARA",
            phone="08123456789"
        )
        interest = ProspectInterest.objects.create(
            prospect=self.prospect,
            level_estimation="Beginner"
        )
        
        # Perform deletion
        self.prospect.delete()
        self.prospect.refresh_from_db()
        
        # Verify prospect soft deleted
        self.assertFalse(self.prospect.is_active)
        self.assertIsNotNone(self.prospect.deleted_at)
        
        # Verify related records soft deleted
        parent.refresh_from_db()
        address.refresh_from_db()
        source.refresh_from_db()
        guardian.refresh_from_db()
        interest.refresh_from_db()
        
        self.assertFalse(parent.is_active)
        self.assertFalse(address.is_active)
        self.assertFalse(source.is_active)
        self.assertFalse(guardian.is_active)
        self.assertFalse(interest.is_active)

    def test_prospect_converted_to_student_fails_delete(self):
        # Create related Student profile pointing to this prospect
        student = Student.objects.create(
            prospect=self.prospect,
            full_name=self.prospect.full_name,
            status="ACTIVE"
        )
        
        # Deletion should raise ValidationError
        with self.assertRaises(ValidationError):
            self.prospect.delete()
            
        # Verify prospect remains active
        self.prospect.refresh_from_db()
        self.assertTrue(self.prospect.is_active)
