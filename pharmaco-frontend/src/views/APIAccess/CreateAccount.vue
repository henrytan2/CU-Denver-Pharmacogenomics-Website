<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import { ApiLoadingState } from '@/constants/enums'
import Button from '@/components/button/button.vue'
import { useUserStore } from '@/stores/UserStore'
import StatusModal from './status-modal/StatusModal.vue'

const userStore = useUserStore()

let firstName = ''
let lastName = ''
let email = ''
let password = ''

const signup = () => {
  userStore.signup({ first_name: firstName, last_name: lastName, email: email, password: password })
}
</script>
<template>
  <div v-show="userStore.signUpLoadingState == ApiLoadingState.Success">
    <StatusModal :modal-text="userStore.signUpResponse?.status ?? ''" />
  </div>
  <div style="margin-top: 40px" class="flex-row w-50">
    <p>Enter account info here:</p>
    <label style="margin-top: 10px">First Name</label
    ><input type="text" class="form-control" aria-label="First Name" v-model="firstName" />

    <label style="margin-top: 10px">Last Name</label
    ><input type="text" class="form-control" aria-label="Last Name" v-model="lastName" />

    <label style="margin-top: 10px">Email</label
    ><input type="text" class="form-control" aria-label="Email" v-model="email" />

    <label style="margin-top: 10px">Password</label
    ><input type="password" class="form-control" aria-label="Password" v-model="password" />

    <div style="margin-top: 10px" class="d-flex justify-content-end">
      <Button
        :button-type="'submit'"
        :className="'btn btn-primary'"
        :buttonText="'Submit'"
        :on-click="signup"
        :show-spinner="userStore.signUpLoadingState == ApiLoadingState.Pending"
      ></Button>
    </div>
  </div>
</template>
