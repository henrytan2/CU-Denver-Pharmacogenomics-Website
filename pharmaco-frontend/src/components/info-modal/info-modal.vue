<script lang="tsx" setup>
const props = defineProps<{
  modalText: string
}>()
</script>
<template>
  <button
    type="button"
    class="btn btn-secondary"
    data-bs-toggle="modal"
    data-bs-target="#info-modal"
  >
    Info
  </button>
  <div class="modal fade" id="info-modal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Info</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body" v-html="props.modalText"></div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>
