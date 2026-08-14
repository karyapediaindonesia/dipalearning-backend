import os

filepath = r"c:\Users\PC-HMK\Desktop\Project\dipalearning\backend\templates\dashboard\pages\master-paket-edukasi.html"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "            let selectedLevelIds = [];" in line and not skip:
        # We inject the missing block
        injection = """        });
        
        $('#modalTitle').text('Edit Paket Edukasi');
        $('#packageModal').modal('show');
        calculateTotalSessions();
    }

    function deletePackage(id, name) {
        hapusData(`/api/v1/academics/packages/${id}/`, name);
    }

    $(document).ready(function() {
        availableSortable = new Sortable(document.getElementById('availableLevels'), {
            group: 'shared',
            animation: 150,
            delay: window.innerWidth < 768 ? 150 : 0,
            delayOnTouchOnly: true,
            fallbackTolerance: 3,
            onEnd: function() { calculateTotalSessions(); }
        });

        selectedSortable = new Sortable(document.getElementById('selectedLevels'), {
            group: 'shared',
            animation: 150,
            delay: window.innerWidth < 768 ? 150 : 0,
            delayOnTouchOnly: true,
            fallbackTolerance: 3,
            onEnd: function() { calculateTotalSessions(); }
        });

        $('#pkg_meetings').on('input', function() { calculateTotalSessions(); });

        $('#packageForm').on('submit', function(e) {
            e.preventDefault();
            clearErrors();
            
            const clientErrors = validateForm();
            if (clientErrors.length > 0) {
                showErrors(clientErrors);
                return;
            }

            let selectedLevelIds = [];
"""
        new_lines.append(injection)
        skip = True
    elif "        });" in line and not skip and "appendTo" in "".join(new_lines[-5:]):
        # We skip the original closing brace before the missing block
        pass
    else:
        new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Restored successfully.")
