<script>
    export let status = {
        id: "job1",
        service: "echo",
        task: "hello",
        queued: false,
        running: false,
        complete: true,
        cancelled: false,
        abandoned: false,
        workerid: "echo-worker",
        updates: ["Preparing response.", "Almost done.", "95% complete."],
        result: "hello",
    };

    let state = "queue";
    if (status["running"]) {
        state = "running";
    } else if (status["complete"]) {
        state = "finished";
    } else if (status["cancelled"]) {
        state = "cancelled";
    } else if (status["abandoned"]) {
        state = "abandoned";
    }
</script>

<div class="status">
    <span class="font-bold">ID:</span>
    <span class="col-span-4">{status["id"]}</span>
    <span class="font-bold">Service:</span>
    <span class="col-span-4">{status["service"]}</span>
    <span class="font-bold">Status:</span>
    <span class="col-span-4">{state}</span>
    <span class="font-bold">Worker:</span>
    <span class="col-span-4">{status["workerid"]}</span>
    <span class="font-bold">Input:</span>
    <span class="col-span-4">{status["task"]}</span>
    <span class="font-bold">Logs:</span>
    <span class="col-span-4">
        <ul class="my-8 text-sm flex flex-col justify-start">
            {#each status["updates"] as item, i}
                <li><pre class="wrap">{item}</pre></li>
            {/each}
        </ul>
    </span>
    <span class="font-bold">Output:</span>
    <span class="col-span-4">{status["result"]}</span>
    {#if status["error"]}
        <span class="font-bold">Error:</span>
        <span class="col-span-4 text-red-500">{status["error"]}</span>
    {/if}
</div>

<style>
    .status {
        @apply grid grid-cols-5 w-11/12 mx-auto my-4;
    }
    .row {
        @apply col-span-5;
        @apply flex flex-row justify-start py-2;
    }
</style>
