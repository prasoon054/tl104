function validString(input) {
    // Regular expression to match letters followed by numbers
    const regex = /^[a-z]+[0-9]+$/;
    return regex.test(input);
}

function checkString() {
    const input = document.getElementById("inputString").value;
    const result = validString(input);
    document.getElementById("result").textContent = result ? "Valid string!" : "Invalid string format.";
}
