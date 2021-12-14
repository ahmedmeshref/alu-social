// delete existing job
function delete_job(job_id) {
    let result = confirm("Are you sure?");
    if (result) {
        let event_container = document.getElementById(`${job_id}`);
        event_container.remove()
        return send_request(job_id);
    } else {
        return;
    }
}

function send_request(job_id) {
    console.log("job card is deleted successfully")
    fetch(`${window.origin}/jobs/delete`, {
        method: "POST",
        body: JSON.stringify({
            "job_id": job_id
        }),
        headers: {
            'Content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(resVal => console.log(`id: ${resVal['id']}, title: ${resVal['title']} `))
        .catch(err => console.log(err))
}