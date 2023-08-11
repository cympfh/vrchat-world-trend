<script>
  const changeLog = [
    ["2023/08/15", "v1.0.0, first release"],
  ];
</script>

<div class="content">
  <article class="message">
    <div class="message-header">
      <p>ChangeLog</p>
    </div>
    <div class="message-body">
      <dl>
        {#each changeLog as row}
          <dt><time>{row[0]}</time></dt>
          <dd>{row[1]}</dd>
        {/each}
      </dl>
    </div>
  </article>
</div>
