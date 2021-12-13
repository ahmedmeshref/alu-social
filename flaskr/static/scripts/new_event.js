// add new event form
document.getElementById("new_event").onsubmit = async function add_post(e) {
    e.preventDefault();
    const title = document.getElementById("title");
    const title_val = title.value;
    const description = document.getElementById("description");
    const description_val = description.value;
    const date = document.getElementById("date")
    const date_val = date.value;
    let invalid_title = document.getElementById("invalid_title");
    let invalid_description = document.getElementById("invalid_description");
    let success = true;
    if (title_val.length > 50 || title_val.length < 3) {
        title.className = "form-control is-invalid";
        invalid_title.innerHTML = "title should be between 3 to 50 characters long";
        success = false;
    }
    if (description_val.length > 500 || description_val.length < 10) {
        description.className = "form-control is-invalid";
        invalid_description.innerHTML = "description should be between 10 to 500 characters long";
        success = false;
    }
    if (success) {
        try {
            let response = await fetch("/events/add", {
                method: "POST",
                body: JSON.stringify({
                    'title': title_val,
                    'description': description_val,
                    'date': date_val,
                }),
                headers: {
                    'Content-type': 'application/json'
                }
            })
            let res_val = await response.json();
            write_post(res_val);
            title.value = null;
            description.value = null;
            date.value = null;
        } catch (e) {
            console.log(e)
        }
    } else {
        console.log("Error in the title and/or description")
    }
    return;
}


function write_post(res_val) {
    document.getElementById("add_new_event").innerHTML = `
        <article class="media content-section post_container" id='${res_val["id"]}'>
          <div class="media-body">
              <div class="container article-metadata mb-3">
                  <div class="row mt-1">
                    <div class="col-sm">
                       <a class="mr-2" href=''>
                            ${res_val["username"]}
                       </a>
                       <small class="text-muted">
                            ${res_val["date"]}
                      </small>
                    </div>
                    <div class=".col-sm-">
                        <div class="container">
                            <button class="btn btn-outline-danger border-0 mb-1 mt-0 p-1 font-weight-bold" type="submit" onclick="delete_event('{{ event.id }}')">
                                <i class="fa fa-trash" aria-hidden="true"></i>
                            </button>
                        </div>
                    </div>
                  </div>
              </div>
            <h2 class="article-title">
                ${res_val["title"]}
            </h2>
            <p class="article-content text-dark">${res_val["description"]}</p>
          </div>
        </article>`
}
