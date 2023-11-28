<script lang="ts">
  import { onMount } from "svelte";
  import Icon from "svelte-awesome";
  import { refresh } from "svelte-awesome/icons";
  import Worlds from "./Worlds.svelte";

  export let api_endpoint;
  export let title;
  export let default_hr = 24;

  let worlds = null;
  let hr = default_hr;

  function reload() {
    worlds = null;
    console.log('reload featured');
    fetch(`${api_endpoint}?limit=20&hr=${hr}`)
      .then((res) => res.json())
      .then((res) => {
        worlds = res;
      });
  }

  onMount(() => {
    reload();
  });
</script>

<div class="section">
  <div class="container">
    <p class="title">{title}</p>
    <div class="select">
      <select bind:value={hr} on:change={reload}>
        <option value={24}>today</option>
        <option value={24 * 7} selected>this week</option>
        <option value={24 * 7 * 4}>this month</option>
        <option value={3 * 24 * 7 * 4}>3mo</option>
      </select>
    </div>
    <button class="button" on:click={reload}>
      <Icon data={refresh} />
    </button>
  </div>
</div>

<div class="section">
  <div class="container">
    <Worlds worlds={worlds} />
  </div>
</div>
