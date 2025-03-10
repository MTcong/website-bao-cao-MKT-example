function editBank(bank) {
    var editBankModal = document.getElementById('edit-bank');
    editBankModal.querySelector('#edit-id').value = bank.id;
    editBankModal.querySelector('#edit-name').value = bank.name;
    editBankModal.querySelector('#edit-shortName').value = bank.shortName;
    editBankModal.querySelector('#edit-code').value = bank.code;
    editBankModal.querySelector('#edit-bin').value = bank.bin;
    editBankModal.querySelector('#edit-swift_code').value = bank.swift_code;
}

function deleteBank(bankID) {
    fetch(`/bank/delete/${bankID}`, {
        method: 'POST',
    }).then((_res) => {
        window.location.href = "/bank";
    });
}
