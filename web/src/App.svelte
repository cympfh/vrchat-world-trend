<script lang="ts">
  import { onMount } from "svelte";
  import Icon from "svelte-awesome";
  import { globe, caretRight, refresh } from "svelte-awesome/icons";
  import Info from "./components/Info.svelte";
  import Worlds from "./components/Worlds.svelte";

  let worlds = {
    'teiban': [],
    'trend': [],
    'hottrend': [],
    'featured': [],
    'new': [],
  };
  let hr_trend = 24 * 7;
  let hr_hottrend = 24;
  let hr_featured = 24;
  let hr_new = 24;
  let last_updated = false;

  function reload_last_update() {
    fetch('/worlds/api/last_updated')
      .then((res) => res.json())
      .then((res) => {
        last_updated = res.dt;
      });
  }

  function reload_teiban() {
    console.log('reload teiban');
    fetch('/worlds/api/teiban?limit=20')
      .then((res) => res.json())
      .then((res) => {
        worlds['teiban'] = res;
      });
  }

  function reload_trend() {
    console.log('reload trend');
    fetch(`/worlds/api/trend?limit=20&hr=${hr_trend}`)
      .then((res) => res.json())
      .then((res) => {
        worlds['trend'][hr_trend] = res;
      });
  }

  function reload_hottrend() {
    console.log('reload hottrend');
    fetch(`/worlds/api/hottrend?limit=20&hr=${hr_hottrend}`)
      .then((res) => res.json())
      .then((res) => {
        worlds['hottrend'][hr_hottrend] = res;
      });
  }

  function reload_featured() {
    console.log('reload featured');
    fetch(`/worlds/api/featured?limit=20&hr=${hr_featured}`)
      .then((res) => res.json())
      .then((res) => {
        worlds['featured'][hr_featured] = res;
      });
  }

  function reload_new() {
    console.log('reload new');
    fetch(`/worlds/api/new?limit=20&hr=${hr_new}`)
      .then((res) => res.json())
      .then((res) => {
        worlds['new'][hr_new] = res;
      });
  }

  function reload() {
    reload_teiban();
    reload_trend();
    reload_hottrend();
    reload_featured();
    reload_new();
    reload_last_update();
  }

  onMount(() => {
    reload();
  });
</script>

<section class="hero">
  <div class="hero-body">
    <p class="title">Worlds</p>
    <p>last updated: <time>{last_updated}</time></p>
  </div>
</section>

<div class="section">
  <div class="container">
    <p class="title">HotTrend</p>
    <div class="select">
      <select bind:value={hr_hottrend} on:change={reload}>
        <option value={8}>realtime</option>
        <option value={24} selected>today</option>
        <option value={24 * 7}>this week</option>
        <option value={24 * 7 * 4}>this month</option>
        <option value={24 * 7 * 4 * 3}>3 month</option>
      </select>
    </div>
    <button class="button" on:click={reload}>
      <Icon data={refresh} />
    </button>
  </div>
</div>

<div class="section">
  <div class="container">
    <Worlds worlds={worlds.hottrend[hr_hottrend]} />
  </div>
</div>

<div class="section">
  <div class="container">
    <p class="title">Featured</p>
    <div class="select">
      <select bind:value={hr_featured} on:change={reload}>
        <option value={8}>realtime</option>
        <option value={24} selected>today</option>
        <option value={24 * 7}>this week</option>
        <option value={24 * 7 * 4}>this month</option>
        <option value={24 * 7 * 4 * 3}>3 month</option>
      </select>
    </div>
    <button class="button" on:click={reload}>
      <Icon data={refresh} />
    </button>
  </div>
</div>

<div class="section">
  <div class="container">
    <Worlds worlds={worlds['featured'][hr_featured]} />
  </div>
</div>

<div class="section">
  <div class="container">
    <p class="title">New</p>
    <div class="select">
      <select bind:value={hr_new} on:change={reload}>
        <option value={8}>realtime</option>
        <option value={24} selected>today</option>
        <option value={24 * 7}>this week</option>
        <option value={24 * 7 * 4}>this month</option>
      </select>
    </div>
    <button class="button" on:click={reload}>
      <Icon data={refresh} />
    </button>
  </div>
</div>

<div class="section">
  <div class="container">
    <Worlds worlds={worlds['new'][hr_new]} />
  </div>
</div>

<div class="section">
  <div class="container">
    <p class="title">Trend</p>
    <div class="select">
      <select bind:value={hr_trend} on:change={reload}>
        <option value={8}>realtime</option>
        <option value={24}>today</option>
        <option value={24 * 7} selected>this week</option>
        <option value={24 * 7 * 4}>this month</option>
        <option value={24 * 7 * 4 * 3}>3 month</option>
      </select>
    </div>
    <button class="button" on:click={reload}>
      <Icon data={refresh} />
    </button>
  </div>
</div>

<div class="section">
  <div class="container">
    <Worlds worlds={worlds.trend[hr_trend]} />
  </div>
</div>

<div class="section">
  <div class="container">
    <p class="title">Teiban</p>
    <button class="button" on:click={reload}>
      <Icon data={refresh} />
    </button>
  </div>
</div>

<div class="section">
  <div class="container">
    <Worlds worlds={worlds.teiban} />
  </div>
</div>

<div class="section">
  <div class="container">
    <Info />
  </div>
</div>

<style global lang="scss">
  @import "main.scss";

  div.columns {
    display: flex;
    overflow-x: auto;
    white-space: nowrap;
  }
</style>
