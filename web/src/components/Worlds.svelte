<script>
  import Empty from "./Empty.svelte";
  import World from "./World.svelte";
  export let worlds;
</script>

<div class="columns">
  {#if worlds && worlds.length > 0}
  {#each worlds as world}
    <div class="column is-one-third">
      <World
        world_id={world.world_id}
        score={world.score}
        name={world.name}
        author_id={world.author_id}
        author_name={world.author_name}
        capacity={world.capacity}
        image_url={world.image_url}
        updated_at={world.updated_at}
        description={world.description}
      />
    </div>
  {/each}
  {:else}
    <div class="column is-full">
      <Empty />
    </div>
  {/if}
</div>

<style global lang="scss">
  div.columns {
    display: flex;
    overflow-x: auto;
    white-space: nowrap;
  }
</style>
