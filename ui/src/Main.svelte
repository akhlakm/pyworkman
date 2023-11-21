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

    <form class="jobform" on:submit|preventDefault={handleRequest}>
      <span>Service</span>
      <input class="textinput" type="text" bind:value={service} placeholder="service name">
      <span>Job ID</span>
      <input class="textinput" type="text" bind:value={job} placeholder="job id">
      <span>Payload</span>
      <input class="textinput" type="text" bind:value={message} placeholder="message">
      <div class="col-start-2 col-span-3">
        <input class="btn" type="submit" name="submit" value="Submit Job" />
        <input class="btn" type="submit" name="status" value="Check Status" />
      </div>
    </form>
    
    <div>{tadata}</div>
  </center>
</main>

<style>


  .jobform {
    @apply grid grid-cols-5 mx-auto w-11/12;
    @apply items-center;
  }

  .textinput {
    @apply m-1 py-1 px-3 w-9/12 left-0 right-auto col-span-4;
    @apply border rounded border-black;
  }

</style>