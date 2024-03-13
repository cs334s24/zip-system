// send request-form to localhost:8080 on submit event
document.getElementById('request-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var form = event.target;
    var data = new FormData(form);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:8080/docket-id', true);
    xhr.send(data);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
        console.log(xhr.responseText);
        }
    }
    // delete the form data after submit
    form.reset();
});