const inputEls = document.querySelectorAll(".input");
const plusButton = document.getElementById("plus");
const minusButton = document.getElementById("minus");
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