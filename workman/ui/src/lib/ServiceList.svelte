<script>
    import { service_list } from "../store";
    import { send } from "../utils";

    function onclick(ev) {
        let service = ev.target.innerText;
        send("listsvc", service, null, null);
    }

</script>

{#if $service_list}
    <ul>
        {#each $service_list as item, i}
            <li class="hover:underline" on:click={onclick}>{item}</li>
        {/each}
    </ul>
{/if}

<style>
    ul {
        @apply flex flex-col list-inside;
        @apply mx-auto w-11/12;
    }
    li {
        border-bottom: 1px solid black;
        padding: 5px 0;
        cursor: pointer;
    }
</style>
