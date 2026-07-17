import glob
import re

for f in glob.glob('backend/templates/dashboard/pages/*.html'):
    c = open(f, encoding='utf-8').read()
    
    # Check if the file has the broken syntax
    # "            });" right after "            }" of paginate.
    if 'paginate: {' in c and '} });' not in c and '} \n        });' not in c and '} \r\n        });' not in c:
        # Let's do a simple string replace
        
        target = """                paginate: {
                    previous: '<i class="fa fa-angle-double-left"></i>',
                    next:     '<i class="fa fa-angle-double-right"></i>'
                }
            });"""
            
        target2 = """                paginate: {
                    previous: '<i class="fa fa-angle-double-left"></i>',
                    next:     '<i class="fa fa-angle-double-right"></i>'
                }
            }, """
            
        replacement = """                paginate: {
                    previous: '<i class="fa fa-angle-double-left"></i>',
                    next:     '<i class="fa fa-angle-double-right"></i>'
                }
            }
        });"""
        
        c = c.replace(target, replacement)
        open(f, 'w', encoding='utf-8').write(c)
        print('Fixed:', f)
