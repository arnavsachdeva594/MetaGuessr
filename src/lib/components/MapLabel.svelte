<script lang="ts">
  let { mapId }: { mapId: string } = $props();
</script>

<div class="geometa-map-label-container">
  <p>LearnableMeta Enabled</p>
  <a href={`https://learnablemeta.com/maps/${mapId}`} target="_blank">
    <button>Meta List</button>
  </a>
</div>

<style>
  .geometa-map-label-container {
    background-color: #0003;
    color: #fff;
    text-align: center;
    z-index: 999999;
    position: absolute;
    bottom: 4px;
    right: 4px;
    box-sizing: border-box;
    border-radius: 8px;
    padding: 8px;
    backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    gap: 8px;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
}

  p {
    font-size: 14px;
    font-weight: bold;
  }

  button {
    padding: 6px 12px;
    font-size: 12px;
    color: #fff;
    background-color: #4CAF50;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
</style>
