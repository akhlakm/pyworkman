<script>
  import AcInput from "./lib/ACInput.svelte";

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
      <AcInput bind:inputValue={service} placeholder="Service name ..." />

      <span>Job ID</span>
      <AcInput bind:inputValue={job} placeholder="Job id ..." />

      <span>Payload</span>
      <AcInput bind:inputValue={message} placeholder="Payload ..." />

      <div class="col-start-2 col-span-3">
        <input class="btn" type="submit" name="submit" value="Submit Job" />
        <input class="btn" type="submit" name="status" value="Check Status" />
        <input class="btn" type="submit" name="list" value="List All" />
        <input class="btn" type="submit" name="cancel" value="Cancel Job" />
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

</style>