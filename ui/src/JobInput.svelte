<script>
    import { onMount } from "svelte";
    import { send } from "./utils";
    import { clear, alert, job_list, job_definition, selected_service, selected_job, job_fields } from "./store";

    let fields = {};
    let defn = JSON.parse($job_definition);
    let props = {};
    let service = {};

    onMount(() => {
        service.message = "";
        service.name = defn["name"];
        service.desc = defn["desc"];

        fields = $job_fields;
        let items = defn["fields"];

        Object.entries(items).map((list, i) => {
            let field = list[0];
            let defn = list[1];
            if (!fields[field]) {
                fields[field] = defn["default"] ? defn["default"] : "";
            }
            props[field] = {
                type: defn["type"],
                help: defn["help"],
                required: defn["required"] ? "Required" : "Optional",
            };
        });
        job_fields.set(fields);
    });

    function handleRequest(event) {
        clear();
        const { submitter: submitButton } = event;
        if (submitButton.name == "submit") {
            if ($job_list.includes($selected_job)) {
                alert.set("Please choose a new job ID.")
                return;
            }
            service.message = JSON.stringify(fields);
        }
        job_fields.set(fields);
        send(
            submitButton.name,
            $selected_service,
            $selected_job,
            service.message,
        );
    }
</script>

<form class="jobform" on:submit|preventDefault={handleRequest}>
    <div class="col-span-5 py-2 text-center text-sm">{service.desc}</div>
    <h2 class="col-span-5 my-2 border-b">Job ID</h2>
    <div class="col-start-2 col-span-2">
        <input
            class="col-start-2 col-span-3 mt-2 text-sm"
            type="text"
            bind:value={$selected_job}
            placeholder="Unique job ID"
            required
        />
    </div>

    <h2 class="col-span-5 mb-2 mt-4 border-b">Payload</h2>

    {#each Object.keys(fields) as field}
        <div class="col-start-1 my-auto mr-auto">
            <b>{field}</b> [{props[field].type}]:
        </div>
        <input
            class="col-start-2 col-span-3 mt-2"
            type="text"
            name={field}
            bind:value={fields[field]}
            placeholder={props[field].required}
            required={props[field].required == "Required"}
        />
        <p class="col-start-2 col-span-3 mb-2 text-sm">{props[field].help}</p>
    {/each}

    <div class="col-start-2 col-span-4 mt-2">
        <input class="btn" type="submit" name="submit" value="Submit Job" />
        <input class="btn" type="submit" name="status" value="Check Status" />
        <input class="btn" type="submit" name="cancel" value="Cancel Job" />
    </div>
</form>

<style>
    .jobform {
        @apply grid grid-cols-5 mx-auto w-11/12;
    }

    input[type="text"] {
        background-color: #fff;
        padding: 3px;
        @apply border-2 rounded border-black;
        width: 100%;
    }
</style>
