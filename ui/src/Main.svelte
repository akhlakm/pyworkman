<script>
    import TopBar from "./lib/TopBar.svelte";
    import ServiceDetails from "./lib/ServiceDetails.svelte";
    import JobStatus from "./lib/JobStatus.svelte";
    import ServiceList from "./lib/ServiceList.svelte";

    import { alert, job_status, job_definition, job_list } from "./store";
    import { send } from "./utils";
    import { onMount } from "svelte";
    import JobInput from "./JobInput.svelte";

    onMount(() => {
        send("listall", null, null, null);
    });
</script>

<TopBar />
<ServiceList />
{#if $alert}
    <h3 class="mx-auto text-red-500 w-full text-left px-10">{$alert}</h3>
{/if}

{#if $job_status}
    <JobStatus status={$job_status} />
{:else if $job_list}
    {#if $job_definition}
        <JobInput />
    {/if}
    <ServiceDetails />
{/if}
