// delete existing event
function delete_event(event_id) {
    let result = confirm("Are you sure?");
    if (result) {
        let event_container = document.getElementById(`${event_id}`);
        event_container.remove()
        return send_request(event_id);
    } else {
        return;
    }
}

function send_request(event_id) {
    console.log("event card is deleted successfully")
    fetch(`${window.origin}/events/delete`, {
        method: "POST",
        body: JSON.stringify({
            "event_id": event_id
        }),
        headers: {
            'Content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(resVal => console.log(`id: ${resVal['id']}, title: ${resVal['title']} `))
        .catch(err => console.log(err))
}