const inputEls = document.querySelectorAll(".table-input");
const plusButton = document.getElementById("plus");
const minusButton = document.getElementById("minus");
const formEl = document.getElementById("form");
const saveinputEl = document.getElementById("save");


function activate(inputEl) {
    inputEl.style.backgroundColor = "#0056b3";
    inputEl.isActive = true;
}

function increase(inputEl) {
    inputEl.value++;
    inputEl.innerHTML++;
}

function decrease(inputEl) {
    const newValue = Math.max(0, inputEl.value - 1);
    inputEl.value = newValue;
    inputEl.innerHTML = newValue;
}

function deactivate(inputEl) {
    inputEl.style.backgroundColor = "";
    inputEl.isActive = false;
}

function disableIncrementalInputEls() {
    [minusButton, plusButton].forEach(button => {
        button.classList.add("disable");
    });
}

function enableIncrementalInputEls() {
    [minusButton, plusButton].forEach(button => {
        button.classList.remove("disable");
    });
}

function setInputEl(inputEl) {
    const value = inputEl.dataset.column * inputEl.dataset.index;
    inputEl.value = value;
    inputEl.isActive = false;
    inputEl.addEventListener("click", () => {
        if (inputEl.isActive === false) {
            inputEls.forEach(deactivate);
            activate(inputEl);
            enableIncrementalInputEls();
        } else {
            deactivate(inputEl);
            disableIncrementalInputEls();
        }
    });
};

function sendTableData() {
    var data = {};
    inputEls.forEach(inputEl => {
        const column = inputEl.dataset.column;
        const index = inputEl.dataset.index;
        if (data[column] === undefined) {
            data[column] = {};
        }
        data[column][index] = inputEl.value;
    });
    fetch("https://reqres.in/api/users", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-type": "application/json"
        }
    }).then(res => res.json())
    .then(data => console.log(data))
    .catch(error => console.log(error));
}

disableIncrementalInputEls();
inputEls.forEach(setInputEl);
plusButton.addEventListener("click", () => {
    const ActiveinputEls = [...inputEls].filter((inputEl) => inputEl.isActive);
    ActiveinputEls.forEach(increase);
});
minusButton.addEventListener("click", () => {
    const ActiveinputEls = [...inputEls].filter((inputEl) => inputEl.isActive);
    ActiveinputEls.forEach(decrease);
});
formEl.addEventListener("submit", (event) => {
    event.preventDefault();
    inputEls.forEach(deactivate);
    disableIncrementalInputEls();
    sendTableData();
});