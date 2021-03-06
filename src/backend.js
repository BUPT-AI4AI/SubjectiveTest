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
// WAV
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
  // VIDEO
  fetchVideoResourceID () {
    return $axios.get('video/id')
      .then(response => response.data)
  },

  fetchVideoResourceType (id) {
    return $axios.get(`video/type/${id}`)
      .then(response => response.data)
  },

  fetchVideoPathResource (type, id) {
    return $axios.get(`video/path/${type}/${id}`)
      .then(response => response.data)
  },

  fetchVideoScoreResource (type, id) {
    return $axios.get(`video/result/${type}/${id}`)
      .then(response => response.data)
  },

  submitVideoScore (type, id, data) {
    return $axios.post(`video/path/${type}/${id}`, data)
      .then(response => response.data)
  },
  // DEMO
  fetchResource () {
    return $axios.get(`resource/xxx`)
      .then(response => response.data)
  },

  fetchSecureResource () {
    return $axios.get(`secure-resource/zzz`)
      .then(response => response.data)
  }
}
