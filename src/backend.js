import axios from 'axios'

let $axios = axios.create({
  baseURL: '/api/',
  timeout: 5000,
  headers: {'Content-Type': 'application/json'}
})

// Request Interceptor
$axios.interceptors.request.use(function (config) {
  config.headers['Authorization'] = 'Fake Token'
  return config
})

// Response Interceptor to handle and log errors
$axios.interceptors.response.use(function (response) {
  return response
}, function (error) {
  // Handle Error
  console.log(error)
  return Promise.reject(error)
})

export default {

  fetchResourceID () {
    return $axios.get('wav/id')
      .then(response => response.data)
  },

  fetchWavResourceType (id) {
    return $axios.get(`wav/type/${id}`)
      .then(response => response.data)
  },

  fetchWavPathResource (type, id) {
    return $axios.get(`wav/path/${type}/${id}`)
      .then(response => response.data)
  },

  fetchScoreResource (type, id) {
    return $axios.get(`wav/result/${type}/${id}`)
      .then(response => response.data)
  },

  submitScore (type, id, data) {
    return $axios.post(`wav/path/${type}/${id}`, data)
      .then(response => response.data)
  },

  fetchResource () {
    return $axios.get(`resource/xxx`)
      .then(response => response.data)
  },

  fetchSecureResource () {
    return $axios.get(`secure-resource/zzz`)
      .then(response => response.data)
  }
}
