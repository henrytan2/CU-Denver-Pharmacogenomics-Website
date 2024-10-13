import { defineStore } from 'pinia'
import axios from 'axios'
import { ApiLoadingState } from '@/constants/enums'
import type {
  GetAPITokenRequest,
  GetAPITokenResponse,
  SignUpRequest,
  SignUpResponse,
  SendResetEmailRequest,
  SendResetEmailResponse
} from '@/models/user'
import { API_URL_NAME, apiUrls } from '@/constants/paths'

export const useUserStore = defineStore('user', {
  state: () => {
    return {
      getAPITokenLoadingState: ApiLoadingState.Idle,
      getAPITokenResponse: undefined as unknown as GetAPITokenResponse,
      signUpLoadingState: ApiLoadingState.Idle,
      signUpResponse: undefined as unknown as SignUpResponse,
      sendResetEmailLoadingState: ApiLoadingState.Idle,
      SendResetEmailResponse: undefined as unknown as SendResetEmailResponse,
      logInState: false,
      logOutLoadingState: ApiLoadingState.Idle
    }
  },
  actions: {
    getAPIToken: function (getAPITokenRequest: GetAPITokenRequest) {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.GET_API_TOKEN]}`
      this.getAPITokenLoadingState = ApiLoadingState.Pending

      axios
        .post(url, JSON.stringify(getAPITokenRequest), {
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
          }
        })
        .then(async (response) => {
          if (response.status == 200) {
            this.getAPITokenLoadingState = ApiLoadingState.Success
            const json = response.data
            this.getAPITokenResponse = json
            this.logInState = true
          } else {
            this.getAPITokenLoadingState = ApiLoadingState.Failed
            throw Error('Get API Token failed')
          }
        })
        .catch((error) => {
          this.getAPITokenLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    signup: function (getSignUpRequest: SignUpRequest) {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.CREATE_ACCOUNT]}`
      this.signUpLoadingState = ApiLoadingState.Pending

      axios
        .post(url, JSON.stringify(getSignUpRequest), {
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
          }
        })
        .then(async (response) => {
          if (response.status == 200) {
            this.signUpLoadingState = ApiLoadingState.Success
            const json = response.data
            this.signUpResponse = json
          } else {
            this.signUpLoadingState = ApiLoadingState.Failed
            throw Error('Sign Up Failed')
          }
        })
        .catch((error) => {
          this.signUpLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    sendResetEmail: function (sendResetEmailRequest: SendResetEmailRequest) {
      const url = `${import.meta.env.VITE_API_BASE_URL}${apiUrls[API_URL_NAME.PASSWORD_RESET]}`
      this.sendResetEmailLoadingState = ApiLoadingState.Pending

      axios
        .post(url, JSON.stringify(sendResetEmailRequest), {
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json'
          }
        })
        .then(async (response) => {
          if (response.status == 200) {
            this.sendResetEmailLoadingState = ApiLoadingState.Success
            const json = response.data
            this.SendResetEmailResponse = json
          } else {
            this.sendResetEmailLoadingState = ApiLoadingState.Failed
            throw Error('Send Reset Email Failed')
          }
        })
        .catch((error) => {
          this.sendResetEmailLoadingState = ApiLoadingState.Failed
          console.log(error)
        })
    },
    logout: function (logOutLoadingState)
  }
})
