<script>
  export let world_id;
  export let score;
  export let name;
  export let author_id;
  export let author_name;
  export let capacity;
  export let image_url;
  export let updated_at;
  export let description;
</script>

<div class="card">
  <div class="card-image">
    <figure class="image is-4by3">
      <img src="{image_url}" alt="world" />
    </figure>
    <div class="card-content">
      <div class="media">
        <div class="media-left">
          <div class="media-content">
            <p class="title is-4">
              <a href="https://vrchat.com/home/world/{world_id}" target="_blank">{name}</a>
            </p>
            <p class="subtitle is-6">
              by <a href="https://vrchat.com/home/user/{author_id}" target="_blank">{author_name}</a>
            </p>
          </div>
        </div>
      </div>
      <div class="content">
        {description}
      </div>
    </div>
    <footer class="card-footer">
      <a href="#" class="card-footer-item">
        Updated: <time>{updated_at.split(' ')[0]}</time>
      </a>
    </footer>
    <footer class="card-footer">
      <a href="#" class="card-footer-item">
        Capacity: {capacity}
      </a>
      <a href="#" class="card-footer-item">
        Score: {Math.round(score)}
      </a>
    </footer>
  </div>
</div>

<style>
  div.media-content > p.title {
    max-width: 100%;
    display: flex;
    white-space: nowrap;
    overflow: hidden;
  }
  div.content {
    height: 6rem;
    min-height: 6rem;
    max-height: 6rem;
    display: flex;
    white-space: wrap;
    overflow-y: auto;
  }
  div.card-content {
    white-space: pre-line;
  }
</style>
