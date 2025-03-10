function editStaff(staff) {
    var editStaffModal = document.getElementById('edit-staff');
    editStaffModal.querySelector('#edit-id').value = staff.id;
    editStaffModal.querySelector('#edit-name').value = staff.name;
    editStaffModal.querySelector('#edit-address').value = staff.address;
    editStaffModal.querySelector('#edit-phone').value = staff.phone;
    editStaffModal.querySelector('#edit-cccd').value = staff.cccd;
    editStaffModal.querySelector('#edit-email').value = staff.email;
    editStaffModal.querySelector('#edit-dob').value = convertDate(staff.dob);
    editStaffModal.querySelector('#edit-stk').value = staff.stk;
    editStaffModal.querySelector('#edit-selected_bank').value = staff.bank_shortName;
    editStaffModal.querySelector('#edit-bank_id').value = staff.bank_id;
}

function convertDate(dateStr) {
    var parts = dateStr.split('/');
    var day = parts[0];
    var month = parts[1];
    var year = parts[2];

    var newDateStr = `${year}-${month}-${day}`;
    return newDateStr;
}

function deleteStaff(staffID) {
    fetch(`/staff/delete/${staffID}`, {
        method: 'POST',
    }).then((_res) => {
        window.location.href = "/staff";
    });
}


document.getElementById('edit-selected_bank').addEventListener('change', function() {
    const selectedValue = this.value;
    const datalist = document.getElementById('edit-browsers');
    const options = datalist.options;
  
    for (let i = 0; i < options.length; i++) {
      if (options[i].value === selectedValue) {
        document.getElementById('edit-bank_id').value = options[i].getAttribute('data-id');
        return;
      }
    }
});