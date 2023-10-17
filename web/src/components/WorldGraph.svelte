<script>
  import { onMount } from "svelte";
  import Chart from 'chart.js/auto';

  export let world_id;
  let data = [];

  function reload() {
    console.log(`fetch world=${world_id}`);
    fetch(`/worlds/api/world?world_id=${world_id}`)
      .then((res) => res.json())
      .then((res) => {
        data = res;
        console.log(data);
      });
  }

  onMount(() => {
    reload();
  });
</script>

<div class="section">
  <div class="container">
  </div>
</div>
