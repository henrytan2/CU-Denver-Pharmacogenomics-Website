export interface GetAPITokenRequest {
  username: string
  password: string
}

export interface GetAPITokenResponse {
  refresh: string
  access: string
}

export interface SignUpRequest {
  email: string
  password: string
  first_name: string
  last_name: string
}

export interface SignUpResponse {
  status?: string
}

export interface SendResetEmailRequest {
  username: string
}

export interface SendResetEmailResponse {
  status: string
}
