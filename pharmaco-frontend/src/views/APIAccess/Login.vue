<!-- eslint-disable vue/multi-word-component-names -->
<script setup lang="tsx">
import { ApiLoadingState } from '@/constants/enums'
import { PATH_NAME, paths } from '@/constants/paths'
import Button from '@/components/button/button.vue'
import { useUserStore } from '@/stores/UserStore'
import { nextTick, onMounted, ref } from 'vue'
import * as bootstrap from 'bootstrap'

const userStore = useUserStore()

const copyButton = ref<HTMLButtonElement | null>(null) 
let tooltipInstance: bootstrap.Tooltip | null = null 

let username = ''
let password = ''

const login = () => {
  userStore.getAPIToken({
    username: username,
    password: password
  })
}

onMounted(async () => {
  await nextTick()
  if (copyButton.value) {
    try {
      tooltipInstance = new bootstrap.Tooltip(copyButton.value, {
        trigger: 'hover'
      })
    } catch (error) {
      console.error('Tooltip initialization failed:', error)
    }
  }
})

const copyToken = () => {

  navigator.clipboard.writeText(userStore.getAPITokenResponse.access)

  if (tooltipInstance && copyButton.value) {
    tooltipInstance.setContent({ '.tooltip-inner': 'Copied!' }) 
    tooltipInstance.show()
  }

  copyButtonClicked.value = true
}

let copyButtonClicked = ref(false)

let copyTokenToolTip = ref("Copy Token") 

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL
</script>
<template>
  <div style="margin-top: 40px" class="d-flex-row w-100">
    <span>
      An account is not needed to access this website. To access some APIs you must log in to an
      active account.
      <div style="margin-top: 10px">
        <a :href="`${apiBaseUrl}/swagger`"> Swagger </a>
      </div>
    </span>
    <div style="margin-top: 40px" class="w-100">
      <p>Status:</p>
      <p v-if="userStore.logInState == true" class="text-success">Logged In</p>
      <p v-else class="text-danger">Not Logged In</p>
      <div class="accordion" id="tokenAccordion">
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button
              class="accordion-button bg-primary-subtle"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#tokenCollapse"
              aria-expanded="true"
              aria-controls="tokenCollapse"
            >
              Token
            </button>
          </h2>
        </div>
      </div>
      <div
        id="tokenCollapse"
        class="accordion-collapse collapse show bg-secondary-subtle"
        data-bs-parent="#tokenAccordion"
      >
        <div class="accordion-body border d-flex">
          <div class="ms-4 mt-2 d-flex">
            <div v-if="userStore.logInState" class="d-flex align-items-center me-2 mb-2">
              <p class="text-break mb-0 me-2">
                {{ userStore.getAPITokenResponse.access }}
              </p>
              <button
                class="btn btn-secondary"
                ref="copyButton"
                @click="copyToken"
                data-bs-toggle="tooltip"
                :title="copyTokenToolTip"
              >
                <i v-if="copyButtonClicked==false" class="bi bi-clipboard"></i>
                <i v-else class="bi bi-clipboard-check-fill"></i>
              </button>
            </div>
            <p v-else class="text-danger">Not Logged In</p>
          </div>
        </div>
      </div>
      <span v-if="userStore.logInState == false">
        Please log in or <a :href="paths[PATH_NAME.CREATE_ACCOUNT]">Create an Account</a>.</span
      >
    </div>
    <div class="input-group mb-3 w-50" style="margin-top: 10px">
      <span class="input-group-text">Username</span>
      <input type="text" class="form-control" aria-label="Username" v-model="username" />
    </div>
    <div class="input-group mb-3 w-50">
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
  </div>
</template>
