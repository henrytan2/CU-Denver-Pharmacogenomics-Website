<script lang="tsx" setup>
import { useRouter } from 'vue-router'
import { paths, PATH_NAME } from '@/constants/paths'
import { useUserStore } from '@/stores/UserStore'
import { ApiLoadingState } from '@/constants/enums'

const props = defineProps<{
  modalText: string
}>()

const router = useRouter()
const userStore = useUserStore()

const goBackToLogin = () => {
  router.push(paths[PATH_NAME.API_ACCESS])
}
</script>
<template>
  <div
    class="modal fade show"
    id="info-modal"
    tabindex="-1"
    aria-hidden="false"
    style="display: block"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Status</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body" v-html="props.modalText"></div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-primary"
            data-bs-dismiss="modal"
            @click="goBackToLogin"
          >
            Redirect to login
          </button>
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
            @click="() => (userStore.signUpLoadingState = ApiLoadingState.Idle)"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
