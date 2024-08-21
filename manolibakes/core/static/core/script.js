const dateInputEl = document.getElementById("date-input");

function dateFormHandler (e) {
    dateInputEl.form.submit();
}

function filterCustomers() {
    console.log("filtrando clientes...")
    var input, filter, customers, li, a, i, txtValue;
    input = document.getElementById("customerSearchInput");
    filter = input.value.toUpperCase();
    customers = document.getElementById("customers");
    li = customers.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}