let table1 = new DataTable('#dataTable1', {
    language: { url: 'https://cdn.datatables.net/plug-ins/1.13.7/i18n/vi.json' },
    lengthMenu: [[-1, 10, 25, 50], ["Toàn bộ", 10, 25, 50]],
    order: [[0, "desc"]],
    drawCallback: function(settings) {
        let totalCost = 0;
        let totalPhoneNumber = 0;
        let totalRevenue = 0;

        let data = this.api().rows({ page: 'current' }).data();

        data.each(function(row) {
            totalCost += parseFloat(row[1].replace(/[^0-9.-]+/g, "")) || 0;
            totalPhoneNumber += parseInt(row[2].replace(/[^0-9.-]+/g, "")) || 0;
            totalRevenue += parseFloat(row[4].replace(/[^0-9.-]+/g, "")) || 0;
        });

        let totalCostPerPhone = parseInt(totalCost / totalPhoneNumber) || 0;
        let totalcpqc = (parseFloat(totalCost / totalRevenue * 100) || 0).toFixed(2);
        let totalroat = (parseFloat(totalRevenue / totalCost) || 0).toFixed(2);

        $('#total-cost1').html(totalCost.toLocaleString() + " VND");
        $('#total-phoneNumber1').html(totalPhoneNumber.toLocaleString());
        $('#total-costPerPhone1').html(totalCostPerPhone.toLocaleString() + " VND");
        $('#total-revenue1').html(totalRevenue.toLocaleString() + " VND");
        $('#total-cpqc1').html(totalcpqc.toLocaleString() + "%");
        $('#total-roat1').html(totalroat.toLocaleString());
    }
});


let table2 = new DataTable('#dataTable2', {
    language: { url: 'https://cdn.datatables.net/plug-ins/1.13.7/i18n/vi.json' },
    lengthMenu: [[-1, 10, 25, 50], ["Toàn bộ", 10, 25, 50]],
    order: [[0, "desc"]],
    drawCallback: function(settings) {
        let totalCost = 0;
        let totalPhoneNumber = 0;
        let totalRevenue = 0;

        let data = this.api().rows({ page: 'current' }).data();

        data.each(function(row) {
            totalCost += parseFloat(row[1].replace(/[^0-9.-]+/g, "")) || 0;
            totalPhoneNumber += parseInt(row[2].replace(/[^0-9.-]+/g, "")) || 0;
            totalRevenue += parseFloat(row[4].replace(/[^0-9.-]+/g, "")) || 0;
        });

        let totalCostPerPhone = parseInt(totalCost / totalPhoneNumber) || 0;
        let totalcpqc = (parseFloat(totalCost / totalRevenue * 100) || 0).toFixed(2);
        let totalroat = (parseFloat(totalRevenue / totalCost) || 0).toFixed(2);

        $('#total-cost2').html(totalCost.toLocaleString() + " VND");
        $('#total-phoneNumber2').html(totalPhoneNumber.toLocaleString());
        $('#total-costPerPhone2').html(totalCostPerPhone.toLocaleString() + " VND");
        $('#total-revenue2').html(totalRevenue.toLocaleString() + " VND");
        $('#total-cpqc2').html(totalcpqc.toLocaleString() + "%");
        $('#total-roat2').html(totalroat.toLocaleString());
    }
});


document.getElementById('dateInput').addEventListener('change', function() {
    const selectedDate = dateInput.value;
    const baseUrl = "/bao-cao-gio";
    const [year, month, day] = selectedDate.split('-');
    const newUrl = `${baseUrl}/${year}-${month}-${day}`;
    window.location.href = newUrl;
});


function nextDay() {
    const selectedDate = dateInput.value;
    const currentDate = new Date(selectedDate);
    currentDate.setDate(currentDate.getDate() + 1);
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, '0');
    const day = String(currentDate.getDate()).padStart(2, '0');
    const newUrl = `/bao-cao-gio/${year}-${month}-${day}`;
    window.location.href = newUrl;
}

function lastDay() {
    const selectedDate = dateInput.value;
    const currentDate = new Date(selectedDate);
    currentDate.setDate(currentDate.getDate() - 1);
    const year = currentDate.getFullYear();
    const month = String(currentDate.getMonth() + 1).padStart(2, '0');
    const day = String(currentDate.getDate()).padStart(2, '0');
    const newUrl = `/bao-cao-gio/${year}-${month}-${day}`;
    window.location.href = newUrl;
}