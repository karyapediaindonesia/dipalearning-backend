import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.academics.models import Course, Level

courses = Course.objects.all()
print(f"Courses: {courses.count()}")
for c in courses:
    print(f"- {c.name} ({c.code})")

levels = Level.objects.all()
print(f"\nLevels: {levels.count()}")
for l in levels:
    print(f"- {l.course.code} - {l.name} ({l.code})")
