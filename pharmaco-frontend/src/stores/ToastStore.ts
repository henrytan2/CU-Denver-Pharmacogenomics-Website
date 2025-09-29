import { defineStore } from 'pinia'
import type { ToastState } from '@/models/toast'

export const useToastStore = defineStore('Toast', {
  state: () => {
    return {
      state: {} as ToastState
    }
  },
  actions: {
    setToastState: function (toastState: ToastState) {
      this.state = toastState
    },
    dismissToast: function () {
      this.state = { show: false }
    }
  }
})
