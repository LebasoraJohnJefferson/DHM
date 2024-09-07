//input search
document.getElementById('searchInput').addEventListener('input', function() {
    var input = this.value.toLowerCase();
    var tableRows = document.querySelectorAll('#homeownersTable tr');

    tableRows.forEach(function(row) {
        var textContent = row.textContent.toLowerCase();
        var cells = row.querySelectorAll('td');
        
        // Reset previous highlights
        cells.forEach(function(cell) {
            cell.innerHTML = cell.textContent; // Remove previous highlight
        });

        // Check if the input is empty
        if (input === '') {
            location.reload()
        } else if (textContent.includes(input)) {
            row.style.display = ''; // Show matching row

            // Highlight matched text
            cells.forEach(function(cell) {
                var cellText = cell.textContent.toLowerCase();
                if (cellText.includes(input)) {
                    var regex = new RegExp(`(${input})`, 'gi');
                    cell.innerHTML = cell.textContent.replace(regex, '<span class="highlight">$1</span>');
                }
            });
        } else {
            row.style.display = 'none'; // Hide non-matching row
        }
    });
});