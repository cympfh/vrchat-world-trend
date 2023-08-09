<script lang="ts">
  import { onMount } from "svelte";
  import Icon from "svelte-awesome";
  import { globe, caretRight } from "svelte-awesome/icons";
  import Footer from "./components/Footer.svelte";

  const pathname = location.pathname;

  let greeting_message = "...";

  function update_greeting() {
    let params = {};
    if (pathname != "/") {
      params.name = pathname;
    }
    let query = new URLSearchParams(params).toString();
    fetch(`/api/greeting?${query}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.msg) {
          greeting_message = data.msg;
        } else {
          console.warn(`Bad Response: ${data}`);
        }
      });
  }

  onMount(() => {
    update_greeting();
  });
</script>

<svelte:head>
  <title>FastSvelte App - {pathname}</title>
</svelte:head>

<section class="hero">
  <div class="hero-body">
    <p class="title">{greeting_message}</p>
  </div>
</section>

<div class="section">
  <div class="container">
    {#if pathname == "/"}
      <div class="content">
        You are on the toplevel <code>/</code>. Try Access to other pages.
      </div>
    {:else if pathname.startsWith("/info")}
      <div class="content">
        This is a <code>/info</code> page.
      </div>
    {:else}
      <div class="content">
        Unknown page <code>{pathname}</code>.
      </div>
    {/if}
  </div>
</div>

<div class="section">
  <div class="container">
    <div class="content">
      <ul>
        <li><a href="/">/</a>,</li>
        <li><a href="/info">/info</a>,</li>
        <li><a href="/info/xxx">/info/xxx</a>.</li>
      </ul>
    </div>
  </div>
</div>

<Footer>A Template by @cympfh. Please use freely under MIT LICENSE.</Footer>

<style global lang="scss">
  @import "main.scss";
</style>
