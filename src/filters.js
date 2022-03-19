// Vue.js Filters
// https://vuejs.org/v2/guide/filters.html

import Vue from 'vue'

let filters = {

  formatTimestamp (timestamp) {
    let datetime = new Date(timestamp)
    return datetime.toLocaleTimeString('en-US')
  },

  formatModelName (model, modelIndex, type) {
    if (type === 'abx') {
      let modelname = model.toLowerCase()
      if (modelname === 'proposed') {
        return model
      } else {
        return 'model' + '_' + modelIndex
      }
    } else {
      if (['raw', 'reconstruct'].includes(model)) {
        return model
      } else {
        return 'model_' + modelIndex
      }
    }
  }
}

// Register All Filters on import
Object.keys(filters).forEach(function (filterName) {
  Vue.filter(filterName, filters[filterName])
})
