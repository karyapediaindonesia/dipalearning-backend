import os
import django
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

def document_models():
    project_apps = ['core', 'dashboard', 'accounts', 'branches', 'academics', 'attendance', 'finance', 'audit', 'students', 'hr', 'billing']
    
    with open('model_relations.txt', 'w') as f:
        for app_config in apps.get_app_configs():
            if app_config.name.split('.')[-1] in project_apps:
                f.write(f"\nAPP: {app_config.name}\n")
                f.write("="*40 + "\n")
                
                for model in app_config.get_models():
                    f.write(f"\nModel: {model.__name__}\n")
                    f.write("-" * 20 + "\n")
                    
                    for field in model._meta.get_fields():
                        if field.is_relation:
                            f.write(f"  - {field.name} ({field.get_internal_type()})\n")
                            if hasattr(field, 'remote_field') and field.remote_field:
                                related_model = field.remote_field.model
                                if related_model:
                                    f.write(f"    -> Targets: {related_model.__name__}\n")
                                on_delete = getattr(field, 'remote_field', None)
                                if on_delete and hasattr(on_delete, 'on_delete'):
                                    on_delete_func = on_delete.on_delete.__name__ if hasattr(on_delete.on_delete, '__name__') else str(on_delete.on_delete)
                                    f.write(f"    -> On Delete: {on_delete_func}\n")

if __name__ == '__main__':
    document_models()
    print("Done generating model_relations.txt")
