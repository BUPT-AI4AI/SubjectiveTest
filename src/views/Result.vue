<template>
  <div>
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1, shrink-to-fit=no"
    />

    <!-- Bootstrap CSS -->
    <link
      rel="stylesheet"
      href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
      integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO"
      crossorigin="anonymous"
    />
    <div class="container">
      <div class="row" id="result">
        <div class="col-md-12">
          <div class="big-screen">

            <h1>TTS 主观评测</h1>
            <el-select v-model="id" placeholder="请选择测试模型" style="margin:20px;">
              <el-option
                v-for="id in resource_id_list"
                :key="id"
                :label="id"
                :value="id"
                :disabled="id.disabled">
              </el-option>
            </el-select>
            <div>
              <span
                >平均意见评分（MOS）：语音质量的衡量标准，是一种用于评估语音质量的指标。</span
              >
              <ul class="col-md-4 m-auto text-left">
                <li>完美。 像面对面的对话或无线电接收。</li>
                <li>一般。 缺陷可以被感知，但声音仍然清晰。</li>
                <li>讨厌。</li>
                <li>非常讨厌。 几乎不可能沟通。</li>
                <li>不可能沟通。</li>
              </ul>
            </div>
            <div v-if="has_mos">
              <el-divider></el-divider>
              <h2>Mos Test</h2>

              <table style="height: 100px" border="2" width="80%">
                <tbody>
                  <tr>
                    <td>wav\model</td>
                    <th v-for="model in mos_data.model_list" :key="model">
                      {{ model }}
                    </th>
                  </tr>
                  <tr v-for="wav in mos_data.wav_list" :key="wav">
                    <th colspan="1" style="font-size: 2px">{{ wav }}</th>

                    <td v-for="model in mos_data.model_list" :key="model">
                      <span>
                        {{ mos_data.model_wav_score_list[model][wav] }}
                      </span>
                    </td>
                  </tr>
                  <tr>
                    <td>average</td>
                    <td v-for="model in mos_data.model_list" :key="model">
                        {{ mos_data.model_score_list[model] }}
                    </td>
                  </tr>
                </tbody>
              </table>
              <el-divider></el-divider>
            </div>

            <div v-if="has_similarity">
              <h2>Similarity Test</h2>

              <table style="height: 100px" border="2" width="80%">
                <tbody>
                  <tr>
                    <td>wav\model</td>
                    <th
                      v-for="model in similarity_data.model_list"
                      :key="model"
                    >
                      {{ model }}
                    </th>
                  </tr>
                  <tr
                    v-for="wav in similarity_data.wav_list"
                    :key="wav"
                  >
                    <th colspan="1" style="font-size: 2px">{{ wav }}</th>

                    <td
                      v-for="model in similarity_data.model_list"
                      :key="model"
                    >
                      <span>
                        {{ similarity_data.model_wav_score_list[model][wav] }}
                      </span>
                    </td>
                  </tr>
                  <tr>
                    <td>average</td>
                    <td v-for="model in similarity_data.model_list" :key="model">
                        {{ similarity_data.model_score_list[model] }}
                    </td>
                  </tr>
                </tbody>
              </table>
              <el-divider></el-divider>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $backend from '../backend'

export default {
  name: 'result',
  data () {
    return {
      id: '',
      resource_id_list: null,
      api_prefix: '/api/wav/resource',
      resource_type: null,
      has_mos: false,
      has_similarity: false,
      mos_data: {
        model_list: null,
        wav_list: null,
        text_list: null,
        model_wav_list: {},
        model_wav_score_list: null,
        model_score_list: null
      },
      similarity_data: {
        model_list: null,
        wav_list: null,
        text_list: null,
        model_wav_list: {},
        model_wav_score_list: {}
      },
      error: ''
    }
  },
  watch: {
    id: function (val) {
      this.id = val
      this.fetchWavResourceType(this.id)
    }
  },
  created () {
    this.fetchResourceID()
  },
  methods: {
    fetchResourceID () {
      $backend.fetchResourceID().then(res => {
        this.resource_id_list = res.resource_id_list
      })
    },

    fetchWavResourceType (id) {
      $backend.fetchWavResourceType(id).then((res) => {
        this.resource_type = res.resource_type
        if (this.resource_type.indexOf('mos') >= 0) {
          this.has_mos = true
          this.fetchWavPathResource('mos', id)
        } else {
          this.has_mos = false
        }
        if (this.resource_type.indexOf('similarity') >= 0) {
          this.has_similarity = true
          this.fetchWavPathResource('similarity', id)
        } else {
          this.has_similarity = false
        }
      })
    },

    fetchWavPathResource (type, id) {
      $backend
        .fetchWavPathResource(type, id)
        .then((res) => {
          let data = null
          if (type === 'mos') {
            data = this.mos_data
          } else if (type === 'similarity') {
            data = this.similarity_data
          } else {
            this.error = '未知的资源类型'
          }
          data.model_list = res.model_list
          data.wav_list = res.wav_list
          data.text_list = res.text_list
          this.fetchScoreResource(type, id)
          this.process_data(type, id, data)
        })
        .catch((error) => {
          this.error = error.message
        })
    },

    fetchScoreResource (type, id) {
      $backend.fetchScoreResource(type, id).then((res) => {
        let data = null
        if (type === 'mos') {
          data = this.mos_data
        } else if (type === 'similarity') {
          data = this.similarity_data
        } else {
          this.error = '未知的资源类型'
        }
        data.model_wav_score_list = res.model_wav_score_list
        data.model_score_list = res.model_score_list
      })
    },

    process_data (type, id, data) {
      data.model_list.forEach((model) => {
        data.model_wav_list[model] = []
        data.wav_list.forEach((wav) => {
          data.model_wav_list[model].push(
            this.getWavPath(type, id, model, wav)
          )
        })
      })
    },

    getWavPath (type, id, model, wav) {
      return [this.api_prefix, type, id, model, wav].join('/')
    }

  }
}
</script>

<style>
.el-row {
  margin-bottom: 10px;
}
.el-col {
  border-radius: 4px;
  margin-bottom: 20px;
}

table {
  width: 100%;
  table-layout: fixed;
}

audio {
  width: 100%;
  margin-top: 5px;
}
.btn {
  margin: 10px;
}
th {
  word-wrap: break-word;
  word-break: break-all;
}
thead > tr > th:first-child {
  width: 96px;
}

@media (max-width: 767px) {
  .big-screen {
    display: none;
  }
}

@media (min-width: 767px) {
  .small-screen {
    display: none;
  }
}
</style>
