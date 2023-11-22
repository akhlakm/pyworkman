<script>
    import { send } from "../utils";
    import { clear, selected_service, service_list, job_list } from "../store";
    import AcInput from "./ACInput.svelte";

    let job = "job1";
    let message = "hello";

    function handleRequest(event) {
        clear();
        const { submitter: submitButton } = event;
        send(submitButton.name, $selected_service, job, message);
    }
</script>

<form class="jobform" on:submit|preventDefault={handleRequest}>
    <span>Service</span>
    <AcInput bind:inputValue={$selected_service} completions={$service_list} placeholder="Service name ..." />

    <span>Job ID</span>
    <AcInput bind:inputValue={job} completions={$job_list} placeholder="Job id ..." />

    <span>Payload</span>
    <AcInput bind:inputValue={message} placeholder="Payload ..." />

    <div class="col-start-2 col-span-4">
        <input class="btn" type="submit" name="listsvc" value="List Service" />
        <input class="btn" type="submit" name="listall" value="List All" />
        <input class="btn" type="submit" name="submit" value="Submit Job" />
        <input class="btn" type="submit" name="status" value="Check Status" />
        <input class="btn" type="submit" name="cancel" value="Cancel Job" />
    </div>
</form>

<style>
    .jobform {
      @apply grid grid-cols-5 mx-auto py-8 w-11/12;
    }
  </style>
  