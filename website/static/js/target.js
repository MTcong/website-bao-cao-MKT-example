function nextMonth(month, year) {
    month += 1;
    if (month > 12) {
        month = 1;
        year += 1;
    }
    const newUrl = `/target/${year}-${month}`;
    window.location.href = newUrl;
}

function lastMonth(month, year) {
    month -= 1;
    if (month < 1) {
        month = 12;
        year -= 1;
    }
    const newUrl = `/target/${year}-${month}`;
    window.location.href = newUrl;
}
