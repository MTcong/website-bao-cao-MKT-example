let table = new DataTable('#dataTable', {
    language: { url: 'https://cdn.datatables.net/plug-ins/1.13.7/i18n/vi.json' },
    lengthMenu: [[-1, 10, 25, 50], ["Toàn bộ", 10, 25, 50]],
    "order": [[0, "desc"]],
    drawCallback: function(settings) {
        let totalLink = 0;
        let totalBudget = 0;
        let totalOrder = 0;

        let data = this.api().rows({ page: 'current' }).data();

        data.each(function(row) {
            totalLink += 1;
            totalBudget += parseInt(row[5].replace(/[^0-9.-]+/g, "")) || 0;
            totalOrder += parseInt(row[11].replace(/[^0-9.-]+/g, "")) || 0;
        });

        let totalBudgetPerOrder = totalOrder ? parseInt(totalBudget / totalOrder) : 0;

        $('#total-post').html(totalLink.toLocaleString() + " bài test");
        $('#total-budget').html(totalBudget.toLocaleString() + " VND");
        $('#total-order').html(totalOrder.toLocaleString() + " đơn");
        $('#total-budgetPerOrder').html(totalBudgetPerOrder.toLocaleString() + " VND / Đơn");
    }
});


function editPost(post) {
    var editPostModal = document.getElementById('edit-post');
    editPostModal.querySelector('#edit-post_id').value = post.id;
    editPostModal.querySelector('#edit-time').value = post.time;
    editPostModal.querySelector('#edit-link').value = post.link;
    editPostModal.querySelector('#edit-content').value = post.content;
    editPostModal.querySelector('#edit-type').value = post.type;
    editPostModal.querySelector('#edit-budget').value = post.budget.replace(/,/g, '');
    editPostModal.querySelector('#edit-cpm').value = post.cpm.replace(/,/g, '');
    editPostModal.querySelector('#edit-cpc').value = post.cpc.replace(/,/g, '');
    editPostModal.querySelector('#edit-ctr').value = post.ctr;
    editPostModal.querySelector('#edit-cpa').value = post.cpa.replace(/,/g, '');
    editPostModal.querySelector('#edit-order').value = post.order.replace(/,/g, '');
    editPostModal.querySelector('#edit-review').value = post.review;
}


function deletePost(postID) {
    fetch(`/post/delete/${postID}`, {
        method: 'POST',
    }).then((_res) => {
        window.location.href = "/bao-cao-bai-test";
    });
}