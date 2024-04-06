function updateStatus(id) {
    var status = document.getElementById('status-' + id).value;
    fetch('/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: parseInt(id), status: status }),
    })
    .then(response => {
        if (response.ok) {
            alert('Status updated successfully');
        } else {
            alert('Failed to update status');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to update status');
    });
}
function search() {
        var input, filter, table, tr, td, i, txtValue;
        input = document.getElementById("search-input");
        filter = input.value.toUpperCase();
        table = document.querySelector("table");
        tr = table.getElementsByTagName("tr");
        for (i = 1; i < tr.length; i++) {
            td = tr[i].getElementsByTagName("td")[0]; // Change 4 to the column index you want to search
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }