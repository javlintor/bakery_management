const dateInputEl = document.getElementById("date-input");

function dateFormHandler (e) {
    dateInputEl.form.submit();
}

function filterElements(inputElement, ulElement) {
    var filter, li, a, i, txtValue;
    filter = inputElement.value.toUpperCase();
    li = ulElement.getElementsByTagName("li");
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

function filterCustomer() {
    input = document.getElementById("customerSearchInput");
    customers = document.getElementById("customers");
    filterElements(input, customers)
}

function filterBreads() {
    input = document.getElementById("breadSearchInput");
    breads = document.getElementById("breads");
    filterElements(input, breads)
}