<script>
    import { send } from "../utils";
    import { clear, selected_service, selected_job, alert } from "../store";

    function handleRequest(event) {
        clear();
        const { submitter: submitButton } = event;
        if (submitButton.name == "listsvc" && $selected_service == "") {
            alert.set("Select a service from the list");
            return;
        }
        send(submitButton.name, $selected_service, $selected_job, "");
    }
</script>

<form class="topbar" on:submit|preventDefault={handleRequest}>
    <div class="col-span-5 mx-auto">
        {#if $selected_job}
            <input
                class="hover:underline px-2 cursor-pointer uppercase"
                type="submit"
                name="status"
                value="Refresh {$selected_job}"
            />
        {/if}
        {#if $selected_service}
            <input
                class="hover:underline px-2 cursor-pointer uppercase"
                type="submit"
                name="listsvc"
                value="{$selected_service} Service"
            />
        {/if}
        <input
            class="hover:underline px-2 cursor-pointer uppercase"
            type="submit"
            name="listall"
            value="List All"
        />
    </div>
</form>

<style>
    .topbar {
        @apply grid grid-cols-5 mx-auto py-1 w-11/12;
    }
</style>
