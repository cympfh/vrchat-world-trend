<script lang="ts">
  import { onMount } from "svelte";
  import Icon from "svelte-awesome";
  import { refresh } from "svelte-awesome/icons";
  import Worlds from "./Worlds.svelte";

  export let api_endpoint;
  export let title;
  export let choice_hr = true;
  let worlds = [];
  let hr = 24;
  let new_filter = false;

  function reload() {
    console.log('reload featured');
    fetch(`${api_endpoint}?limit=20&hr=${hr}&new=${new_filter}`)
      .then((res) => res.json())
      .then((res) => {
        worlds = res;
      });
  }

  function toggle_new_filter() {
    new_filter = !new_filter;
    reload();
  }

  onMount(() => {
    reload();
  });
</script>

<div class="section">
  <div class="container">
    <p class="title">{title}</p>
    {#if choice_hr}
    <div class="select">
      <select bind:value={hr} on:change={reload}>
        <option value={8}>realtime</option>
        <option value={24} selected>today</option>
        <option value={24 * 7}>this week</option>
        <option value={24 * 7 * 4}>this month</option>
        <option value={24 * 7 * 4 * 3}>3 month</option>
      </select>
    </div>
    {/if}
    <button class="button" on:click={toggle_new_filter} class:is-dark={new_filter}>new</button>
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
