<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import { ApiLoadingState } from '@/constants/enums'
import { PATH_NAME, paths } from '@/constants/paths'
import Button from '@/components/button/button.vue'
import { useUserStore } from '@/stores/UserStore'

const userStore = useUserStore()

let username = ''
let password = ''

const login = () => {
  userStore.getAPIToken({
    username: username,
    password: password
  })
}
</script>
<template>
  <div style="margin-top: 40px">
    <span>
      An account is not needed to access this website. To access some APIs you must log in to an
      active account.
      <div style="margin-top: 10px">
        <a href="https://pharmacogenomics.clas.ucdenver.edu/api/public-best-resolution"
          >Best resolution API</a
        >
      </div>
      <div style="margin-top: 10px">
        <a href="https://pharmacogenomics.clas.ucdenver.edu/api/public-plddt-score">
          Find PLDDT score API</a
        >
      </div>
      <div style="margin-top: 10px">
        <a href="https://pharmacogenomics.clas.ucdenver.edu/api/public-faspr-prep"
          >FASPR prep (mutated sequence) API
        </a>
      </div>
    </span>
    <div style="margin-top: 40px">
      <p>Status:</p>
      <p v-if="userStore.logInState == true" class="text-success">Logged In</p>
      <p v-else class="text-danger">Logged Out</p>
      <span v-if="userStore.logInState == false"
        >Please log in or <a :href="paths[PATH_NAME.CREATE_ACCOUNT]">Create an Account</a>.</span
      >
    </div>
    <div class="input-group mb-3" style="margin-top: 10px">
      <span class="input-group-text">Username</span>
      <input type="text" class="form-control" aria-label="Username" v-model="username" />
    </div>
    <div class="input-group mb-3">
      <span class="input-group-text">Password</span>
      <input type="password" class="form-control" aria-label="Password" v-model="password" />
    </div>
    <div style="margin-top: 10px">
      <a :href="paths[PATH_NAME.PASSWORD_RESET]">Reset Password</a>
    </div>
    <div class="d-flex justify-content-end">
      <Button
        v-show="userStore.logInState == false"
        :button-type="'submit'"
        :className="'btn btn-primary'"
        :buttonText="'Login'"
        :on-click="login"
        :show-spinner="userStore.getAPITokenLoadingState == ApiLoadingState.Pending"
      ></Button>
    </div>

    <div v-if="userStore.logInState == true" style="margin-top: 10px"><a :href="paths[PATH_NAME.LOGOUT]">Logout</a></div>
  </div>
</template>
