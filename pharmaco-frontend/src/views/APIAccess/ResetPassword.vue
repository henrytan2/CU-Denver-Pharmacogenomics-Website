<script lang="tsx" setup>
import { useUserStore } from '@/stores/UserStore'
import Button from '@/components/button/button.vue'
import { ApiLoadingState } from '@/constants/enums'

const userStore = useUserStore()

let username = ''

const sendResetEmail = () => {
  userStore.sendResetEmail({
    username: username
  })
}
</script>
<template>
  <div class="w-50">
    <div style="margin-top: 60px">
      <div v-show="userStore.SendResetEmailResponse?.status" style="margin-top: 40px">
        {{ userStore.SendResetEmailResponse?.status }}
      </div>
    </div>
    <div class="input-group mb-3">
      <span class="input-group-text">Username</span>
      <input type="text" class="form-control" aria-label="Username" v-model="username" />
    </div>
    <div class="d-flex justify-content-end">
      <Button
        :show-spinner="userStore.sendResetEmailLoadingState == ApiLoadingState.Pending"
        :button-type="'submit'"
        :className="'btn btn-primary'"
        :buttonText="'Send reset email'"
        :on-click="sendResetEmail"
      ></Button>
    </div>
  </div>
</template>
