let table1 = new DataTable('#dataTable1', {
    language: { url: 'https://cdn.datatables.net/plug-ins/1.13.7/i18n/vi.json' },
    lengthMenu: [[-1, 10, 25, 50], ["Toàn bộ", 10, 25, 50]],
    order: [[0, "desc"]],
    drawCallback: function(settings) {
        let totalNewRevenue = 0;
        let totalShopeeRevenue = 0;
        let totalAdvanceBudget = 0;
        let totalRealBudget = 0;
        let totalPhone = 0;
        let totalMess = 0;
        let totalRefund = 0

        let data = this.api().rows({ page: 'current' }).data();

        data.each(function(row) {
            totalNewRevenue += parseInt(row[2].replace(/[^0-9.-]+/g, "")) || 0;
            totalShopeeRevenue += parseInt(row[3].replace(/[^0-9.-]+/g, "")) || 0;
            totalAdvanceBudget += parseInt(row[4].replace(/[^0-9.-]+/g, "")) || 0;
            totalRealBudget += parseInt(row[5].replace(/[^0-9.-]+/g, "")) || 0;
            totalPhone += parseInt(row[8].replace(/[^0-9.-]+/g, "")) || 0;
            totalMess += parseInt(row[10].replace(/[^0-9.-]+/g, "")) || 0;
            totalRefund += parseInt(row[12].replace(/[^0-9.-]+/g, "")) || 0;
        });

        let totalRevenue = totalNewRevenue + totalShopeeRevenue - totalRefund;
        let totalCPP = parseInt(totalRealBudget / totalPhone) || 0;
        let totalCPR = (parseFloat(totalAdvanceBudget / totalRevenue * 100) || 0).toFixed(2);
        let totalPPM = (parseFloat(totalPhone / totalMess * 100) || 0).toFixed(2);
        let totalBPM = parseInt(totalRealBudget / totalMess) || 0;

        $('#total-totalRevenue').html(totalRevenue.toLocaleString() + " VND");
        $('#total-newRevenue').html(totalNewRevenue.toLocaleString() + " VND");
        $('#total-shopeeRevenue').html(totalShopeeRevenue.toLocaleString() + " VND");
        $('#total-advanceBudget').html(totalAdvanceBudget.toLocaleString() + " VND");
        $('#total-realBudget').html(totalRealBudget.toLocaleString() + " VND");
        $('#total-cpp').html(totalCPP.toLocaleString() + " VND");
        $('#total-cpr').html(totalCPR.toLocaleString() + "%");
        $('#total-phoneNumber').html(totalPhone.toLocaleString());
        $('#total-ppm').html(totalPPM.toLocaleString() + "%");
        $('#total-mess').html(totalMess.toLocaleString());
        $('#total-bpm').html(totalBPM.toLocaleString() + " VND");
        $('#total-refund').html(totalRefund.toLocaleString() + " VND");
    }
});