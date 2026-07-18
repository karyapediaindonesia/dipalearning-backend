from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.branches.models import Branch, Room, Holiday
from django.utils import timezone

class BranchDeleteTestCase(TestCase):
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
        
    def test_branch_soft_delete(self):
        # Soft delete branch
        self.branch.delete()
        with self.assertRaises(Branch.DoesNotExist):
            self.branch.refresh_from_db()
        
        
    def test_branch_cascade_soft_delete(self):
        room = Room.objects.create(
            branch=self.branch,
            code="RM01",
            name="Room 01",
            room_type="CLASSROOM",
            capacity_ideal=10,
            capacity_max=15,
            status="ACTIVE"
        )
        holiday = Holiday.objects.create(
            branch=self.branch,
            name="Test Holiday",
            holiday_type="NATIONAL",
            date_start=timezone.now().date(),
            date_end=timezone.now().date(),
            operational_impact="FULL_CLOSE",
            status="ACTIVE"
        )
        
        # Soft delete branch
        self.branch.delete()
        
        with self.assertRaises(Room.DoesNotExist):
            room.refresh_from_db()
        with self.assertRaises(Holiday.DoesNotExist):
            holiday.refresh_from_db()
        
