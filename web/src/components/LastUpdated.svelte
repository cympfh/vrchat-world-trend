<script>
  import { onMount } from "svelte";

  let last_updated = false;

  function reload_last_update() {
    console.log('reload last_update');
    fetch('/worlds/api/last_updated')
      .then((res) => res.json())
      .then((res) => {
        last_updated = res.dt;
      });
  }

  onMount(() => {
    reload_last_update();
    setInterval(reload_last_update, 30000);
  });
</script>

<p>last updated: <time>{last_updated}</time></p>
