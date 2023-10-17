<script>
  const changeLog = [
    ["2023/10/17", "v1.1.4, New feature algorithm"],
    ["2023/10/17", "v1.1.3, ttl caching. Trend and Teiban are merged as Teiban"],
    ["2023/08/30", "v1.1.2, slightly updated"],
    ["2023/08/17", "v1.1.1, :art: refactoring, :new: new filter (recently updated), :fire: remove new kanban"],
    ["2023/08/16", "v1.1.0, :new: hottrend & featured"],
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
