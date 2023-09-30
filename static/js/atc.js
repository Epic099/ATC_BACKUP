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

const RoomName = document.getElementById('my-element').dataset.name;

let url = 'wss://' + window.location.host + '/ws/' + RoomName.toString() + '/' ;
const socket = new WebSocket(url);

socket.onmessage = function(e){
    let data = JSON.parse(e.data);
    if (data["type"] != "edit")
    {
      console.log(data["message"]);
      return;
    }
    let changed = data["changed_attribute"]
    let aircraftli = document.getElementById(data["callsign"])
    let inp = document.getElementById(data["callsign"] + "-" + changed)
    inp.value = data["value"]
}

function focusout(id)
{
  var strs = id.split(/[-]+/);
  var callsign = strs[0];
  var changed = strs[1];
  var value = document.getElementById(id).value;
  socket.send(JSON.stringify({"callsign" : callsign, "changed_attribute" : changed, "value" : value, "type" : "", "message" : ""}))
}

socket.onerror = function(e)
{
  console.log(e);
}

socket.onopen = function(e){
  //socket.send(JSON.stringify({"callsign" : "Lufthansa 1543", "changed_attribute" : "Departure","value" : "IRFD" , "type" : "", "message" : ""}));
  //socket.send(JSON.stringify({"callsign" : "Lufthansa 1543", "changed_attribute" : "Departure","value" : "IRFD" , "type" : "", "message" : ""}));
  //socket.send(JSON.stringify({"callsign" : "Lufthansa 1543", "changed_attribute" : "Arrival","value" : "ITKO" , "type" : "", "message" : ""}));
  //socket.send(JSON.stringify({'room' : RoomName, 'message' : 'Testing Stuff Cool!'}));
}

socket.onclose = function(e){
  console.log(e);
}