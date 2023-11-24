<script>
    import AcItem from "./ACItem.svelte";
    export let inputValue = "";
    export let placeholder = "";
    export let completions = [];

    /* FILTERING countres DATA BASED ON INPUT */
    let filteredItems = [];

    const filterItems = () => {
        let storageArr = [];
        if (inputValue && completions) {
            completions.forEach((item) => {
                if (
                    item.toLowerCase().startsWith(inputValue.toLowerCase())
                ) {
                    storageArr = [...storageArr, makeMatchBold(item)];
                }
            });
        }
        filteredItems = storageArr;
    };

    /* HANDLING THE INPUT */
    let searchInput; // use with bind:this to focus element

    $: if (!inputValue) {
        filteredItems = [];
        hiLiteIndex = null;
    }

    const setInputVal = (itemName) => {
        filteredItems = [];
        hiLiteIndex = null;
        inputValue = removeBold(itemName);
        searchInput.focus();
    };

    const makeMatchBold = (str) => {
        // replace part of (item name === inputValue) with strong tags
        let matched = str.substring(0, inputValue.length);
        let makeBold = `<strong>${matched}</strong>`;
        let boldedMatch = str.replace(matched, makeBold);
        return boldedMatch;
    };

    const removeBold = (str) => {
        //replace < and > all characters between
        if (str) {
            str = str.replace(/<(.)*?>/g, "");
        }
        return str;
    };

    /* NAVIGATING OVER THE LIST OF COUNTRIES W HIGHLIGHTING */
    let hiLiteIndex = null;
    $: hiLitedCountry = filteredItems[hiLiteIndex];

    const navigateList = (e) => {
        if (
            e.key === "ArrowDown" &&
            hiLiteIndex <= filteredItems.length - 1
        ) {
            hiLiteIndex === null ? (hiLiteIndex = 0) : (hiLiteIndex += 1);
        } else if (e.key === "ArrowUp" && hiLiteIndex !== null) {
            hiLiteIndex === 0
                ? (hiLiteIndex = filteredItems.length - 1)
                : (hiLiteIndex -= 1);
        } else if (e.key === "Enter") {
            setInputVal(filteredItems[hiLiteIndex]);
        } else {
            return;
        }
    };
</script>

<svelte:window on:keydown={navigateList} />

<div class="autocomplete">
    <input
        type="text"
        placeholder="{placeholder}"
        bind:this={searchInput}
        bind:value={inputValue}
        on:input={filterItems}
    />
    <!-- FILTERED LIST OF COUNTRIES -->
    {#if filteredItems.length > 0}
        <ul id="autocomplete-items-list">
            {#each filteredItems as item, i}
                <AcItem
                    itemLabel={item}
                    highlighted={i === hiLiteIndex}
                    on:click={() => setInputVal(item)}
                />
            {/each}
        </ul>
    {/if}
</div>

<style>
    div.autocomplete {
        /*the container must be positioned relative:*/
        position: relative;
        @apply m-1 w-9/12 left-0 right-auto col-span-4;
    }
    input {
        background-color: #fff;
        padding: 5px;
        @apply border-2 rounded border-black;
    }
    input[type="text"] {
        background-color: #fff;
        width: 100%;
    }
    #autocomplete-items-list {
        position: absolute;
        top: 38px;
        z-index: 10;
        width: 100%;
        max-height: 80vh;
        overflow-y: scroll;
        border: 1px solid #000;
        background-color: #ddd;
    }
</style>
