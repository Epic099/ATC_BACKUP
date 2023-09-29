const input = document.getElementById('filter-input');
const list = document.getElementById('objects-list');
// Listen for changes to the input value.
/* input.addEventListener('input', function() {
    // Get the filtered list of objects.
    var filteredObjects = objects.filter(function(object) {
        return object.Callsign.toLowerCase().startsWith(input.value.toLowerCase());
    });
    console.log(input.value);
    // Clear the list.
    list.innerHTML = '';

    // Add the filtered objects to the list.
    filteredObjects.forEach(function(object) {
        list.innerHTML += '<li>' + object.Callsign + '</li>';
    });
});

list.addEventListener('click', function(event) {
    // Get the clicked item.
    var item = event.target;

    // Get the value of the item.
    var value = item.textContent;

    // Put the value into the input field.
    input.value = value;
});*/

let url = 'wss://' + window.location.host + '/ws/socket-server/';
const socket = new WebSocket(url);

socket.onmessage = function(e){
    let data = JSON.parse(e.data);
    console.log('Data: ', data);
}

/*setTimeout(function(e) {
    websocket.send(JSON.stringify({"message" : message}))
}, 2000);*/
