function validString(input) {
    // Regular expression to match letters followed by numbers
    return false;
}

function checkString() {
    const input = document.getElementById("inputString").value;
    const result = validString(input);
    document.getElementById("result").textContent = result ? "Valid string!" : "Invalid string format.";
}
