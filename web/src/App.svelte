<script lang="ts">
  import ChangeLog from "./components/ChangeLog.svelte";
  import LastUpdated from "./components/LastUpdated.svelte";
  import WorldKanban from "./components/WorldKanban.svelte";
  import WorldGraph from "./components/WorldGraph.svelte";

  const pathname = location.pathname;
  let world_id = pathname.match(/^\/worlds\/([^\/]*)\/?$/)[1];
  let is_top = !world_id;
  console.log(world_id, is_top);
</script>

<section class="hero">
  <div class="hero-body">
    <p class="title">Worlds</p>
    <LastUpdated />
  </div>
</section>

{#if is_top}
<WorldKanban title="HotTrend" api_endpoint="/worlds/api/hottrend" />
<WorldKanban title="Featured" api_endpoint="/worlds/api/featured" />
<WorldKanban title="Teiban" api_endpoint="/worlds/api/teiban" default_hr={24 * 7} />
{:else}
<WorldGraph {world_id} />
{/if}

<div class="section">
  <div class="container">
    <ChangeLog />
  </div>
</div>

<style global lang="scss">
  @import "main.scss";
</style>
