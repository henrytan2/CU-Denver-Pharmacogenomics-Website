import axios, { type AxiosResponse } from 'axios'

const axiosWithRetry = async <T>(
  url: string,
  requestBody: object,
  headers: Record<string, string>,
  retries: number = 3
): Promise<AxiosResponse<T>> => {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await axios.post<T>(url, JSON.stringify(requestBody), {
        headers
      })
      return response // Return response if successful
    } catch (error) {
      if (attempt === retries) {
        throw error // Throw error if retries are exhausted
      }
      console.log(`Retry ${attempt} failed. Retrying...`)
    }
  }
  throw new Error('Retries exhausted') // This line will never be reached because of the `throw` inside the loop
}

export { axiosWithRetry }
