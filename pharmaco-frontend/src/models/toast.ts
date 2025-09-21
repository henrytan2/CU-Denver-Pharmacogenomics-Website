export interface ToastState {
  show: boolean
  header?: string
  message?: string
  type?: ToastType
}

export enum ToastType {
  SUCCESS,
  INFO,
  WARNING,
  ERROR
}
