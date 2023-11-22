<script>
    import { clear, service_details, selected_service } from "../store";
    import { send } from "../utils";

    function onclick(ev) {
        let job = ev.target.innerText;
        clear();
        send("status", $selected_service, job, null);
    }
</script>

{#if $service_details}
    <h2 class="mx-auto w-fit uppercase font-bold">{$selected_service} service</h2>
    <div class="grid grid-cols-10 mx-auto w-7/12 my-3">
        {#each Object.entries($service_details) as [key, value]}
            <p class="col-start-1 col-span-9 font-bold border-b pt-2 pb-1 mt-1">{key}</p>
            {#each Object.entries(value) as [type, job]}
                <p class="col-start-2 col-span-8 pb-2">{type}</p>
                {#each job as jobname}
                    <p class="col-start-4 col-span-5 pb-1 cursor-pointer hover:underline" on:click={onclick}>{jobname}</p>
                {/each}
            {/each}
        {/each}
    </div>
{/if}
