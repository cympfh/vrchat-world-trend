<script lang="ts">
  import ChangeLog from "./components/ChangeLog.svelte";
  import LastUpdated from "./components/LastUpdated.svelte";
  import WorldKanban from "./components/WorldKanban.svelte";
</script>

<section class="hero">
  <div class="hero-body">
    <p class="title">Worlds</p>
    <LastUpdated />
  </div>
</section>

<WorldKanban title="HotTrend" api_endpoint="/worlds/api/hottrend" />
<WorldKanban title="Featured" api_endpoint="/worlds/api/featured" />
<WorldKanban title="Trend" api_endpoint="/worlds/api/trend" />
<WorldKanban title="Teiban" api_endpoint="/worlds/api/teiban" choice_hr={false} />

<div class="section">
  <div class="container">
    <ChangeLog />
  </div>
</div>

<style global lang="scss">
  @import "main.scss";
</style>
