function moveToNext(current, nextFieldID) {
    if (current.value.length >= 1) {
        const nextField = document.getElementById(nextFieldID);
        if (nextField) {
            nextField.focus();
        }
    }
}

function moveToPrevious(current, previousFieldID) {
    if (current.value.length === 0) {
        const previousField = document.getElementById(previousFieldID);
        if (previousField) {
            previousField.focus();
        }
    }
}

function handleKeyUp(event, currentFieldID, previousFieldID) {
    if (event.key === "Backspace") {
        moveToPrevious(document.getElementById(currentFieldID), previousFieldID);
    }
}

function submitOTP(event) {
    event.preventDefault();  // Prevent form submission for demo purposes
    const otp1 = document.getElementById('otp1').value;
    const otp2 = document.getElementById('otp2').value;
    const otp3 = document.getElementById('otp3').value;
    const otp4 = document.getElementById('otp4').value;
    
    const otp = otp1 + otp2 + otp3 + otp4;
    
    if (otp.length === 4 && !isNaN(otp)) {
        alert('OTP Submitted: ' + otp);
        // Add your form submission logic here
    } else {
        alert('Please enter a valid 4-digit OTP.');
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('otp1').addEventListener('keyup', (e) => handleKeyUp(e, 'otp1', ''));
    document.getElementById('otp2').addEventListener('keyup', (e) => handleKeyUp(e, 'otp2', 'otp1'));
    document.getElementById('otp3').addEventListener('keyup', (e) => handleKeyUp(e, 'otp3', 'otp2'));
    document.getElementById('otp4').addEventListener('keyup', (e) => handleKeyUp(e, 'otp4', 'otp3'));
});


window.onload = function() {
    document.getElementById("otp1").focus();
};
