<script>
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  let tadata = "";
  let service = 'echo';
  let job = 'job1';
  let message = 'hello';

  async function postData(url = "", data = {}) {
    const response = await fetch(url, {
      method: "POST",
      cache: "no-cache",
      body: JSON.stringify(data), // body data type must match "Content-Type" header
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': csrftoken
      },
      mode: 'same-origin'
    });
    return response.json();
  }

  function handleRequest(event) {
    const {submitter: submitButton} = event;
    let payload = {
      'service': service,
      'job': job,
      'message': message,
    }
    payload['action'] = submitButton.name;
    postData("/main/", payload).then((data) => {
      console.log(data);
      tadata = JSON.stringify(data);
    });
  }
</script>

<main>
  <center>

    <form on:submit|preventDefault={handleRequest}>
      <input type="text" bind:value={service} placeholder="service name">
      <input type="text" bind:value={job} placeholder="job id">
      <input type="text" bind:value={message} placeholder="message">
      <input class="btn" type="submit" name="submit" value="Submit Job" />
      <input class="btn" type="submit" name="status" value="Check Status" />
    </form>
    
    <div>{tadata}</div>
  </center>
</main>

<style>
  .btn {
    @apply px-2 py-1 m-1 border drop-shadow bg-blue-500 text-white cursor-pointer;
    @apply rounded;
  }

  .btn:hover {
    @apply drop-shadow-md bg-slate-700 text-amber-400;
  }

</style>