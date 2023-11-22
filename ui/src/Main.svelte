<script>
  import JobForm from "./lib/JobForm.svelte";
  import ServiceDetails from "./lib/ServiceDetails.svelte";
  import JobStatus from "./lib/JobStatus.svelte";
  import ServiceList from "./lib/ServiceList.svelte";

  import { alert, job_status } from "./store";
  import { send } from "./utils";
  import { onMount } from "svelte";

  onMount(() => {
    send('listall', null, null, null);
  })
</script>

<JobForm />

{#if $alert}
  <h3 class="mx-auto text-red-500 w-full text-left px-10">{$alert}</h3>
{/if}

<ServiceList />
<ServiceDetails />

{#if $job_status}
  <JobStatus status={$job_status} />
{/if}
