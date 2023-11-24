import * as store from "./store";

async function postData(url = "", data = {}) {
    const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const response = await fetch(url, {
        method: "POST",
        cache: "no-cache",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        mode: "same-origin",
    });
    return response.json();
};


function handle_response(action, response) {
    store.last_response.set(response);

    if (response["error"]) {
        store.alert.set(response['error']);
        return;
    } else {
        store.alert.set("");
    }

    if (action == "submit") {
        // New task
        store.job_status.set(response);
    }
    
    else if (action == "status") {
        store.job_status.set(response);
    }
    
    else if (action == "listall") {
        store.service_list.set(Object.keys(response));
    }

    else if (action == "listsvc") {
        store.service_details.set(response);
        let jobitems = [];
        for (var type in response['jobs']) {
            jobitems = jobitems.concat(response['jobs'][type]);
        }

        store.job_list.set(jobitems);
        if (response['definition']) {
            store.job_definition.set(response['definition']);
        }
    }

    else {
        console.log("Response for unknown action:", action);
    }
}

export function send(action, service, job, message) {
    let payload = {
        service: service,
        job: job,
        message: message,
        action: action
    };

    store.selected_service.set(service);
    
    postData("/main/", payload).then((data) => {
        handle_response(action, data);
    });
}
