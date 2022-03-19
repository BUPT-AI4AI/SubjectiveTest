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
    <button type="primary" class='topcorner' @click="show_label=!show_label">显示标签</button>

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
            <el-select v-model="type" placeholder="请选择测试方法" style="margin:20px;">
              <el-option
                v-for="type in type_list"
                :key="type"
                :label="type"
                :value="type">
              </el-option>
            </el-select>

            <!-- <div v-if="type === 'mos'">
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
            </div> -->

            <div v-if="type">
              <h2>{{type}} test</h2>

              <table style="height: 100px" border="2" width="80%">
                <tbody>
                  <tr>
                    <th></th>

                    <th
                      v-for="(model, model_index) in wav_data.model_list"
                      :key="model"
                    >
                    {{ model | formatModelName(model_index, type, show_label) }}
                    </th>

                  </tr>
                  <tr
                    v-for="wav in wav_data.wav_list"
                    :key="wav"
                  >
                    <th colspan="1" style="font-size: 2px">{{ wav }}</th>

                    <td
                      v-for="model in wav_data.model_list"
                      :key="model"
                    >
                      <audio controls>
                        <source
                          :src="wav_data.model_wav_list[model][wav]"
                          type="audio/wav"
                        />
                        Your browser does not support the audio element.
                      </audio>

                      <el-input-number
                        v-if="type !== 'abx'"
                        v-model="wav_data.model_wav_score_list[model][wav]"
                        :precision="2"
                        :step="0.1"
                        :min="1"
                        :max="5"
                        size="small">
                      </el-input-number>
                      <el-input-number
                        v-if="type === 'abx'"
                        v-model="wav_data.model_wav_score_list[model][wav]"
                        :step="1"
                        :min="1"
                        :max="3"
                        size="small">
                      </el-input-number>

                    </td>
                  </tr>
                </tbody>
              </table>

              <button
                @click="submitScore"
                type="button"
                class="btn btn-primary"
              >
                提交
              </button>

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
  name: 'evaluate',
  filters: {
    formatModelName: (model, modelIndex, type, showLabel) => {
      if (showLabel) { return model }
      if (type === 'abx') {
        let modelname = model.toLowerCase()
        if (modelname === 'proposed') {
          return model
        } else {
          return 'model' + '_' + modelIndex
        }
      } else if (type === 'similarity') {
        if (['raw'].includes(model)) {
          return model
        } else {
          return 'model_' + modelIndex
        }
      } else {
        return 'model_' + modelIndex
      }
    }
  },
  data () {
    return {
      id: '',
      type: '',
      type_list: ['mos', 'similarity', 'abx'],
      resource_id_list: null,
      resource_type: null,
      show_label: false,
      has_mos: false,
      has_similarity: false,
      mos_data: null,
      similarity_data: null,
      wav_data: null,
      error: ''
    }
  },
  watch: {
    id: function (val) {
      this.id = val
      if (this.type !== '') {
        this.fetchWavPathResource(this.type, this.id)
      }
    },
    type: function (val) {
      this.type = val
      if (this.id !== '') {
        this.fetchWavPathResource(this.type, this.id)
      }
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

    fetchWavPathResource (type, id) {
      $backend
        .fetchWavPathResource(type, id)
        .then((res) => {
          this.wav_data = res
        })
        .catch((error) => {
          // console.log('error!!!!')
          this.type = ''
          this.wav_data = null
          this.error = error.message
        })
    },

    submitScore () {
      $backend.submitScore(this.type, this.id, this.wav_data)
        .then((res) => {
          this.$message({
            message: '提交成功',
            type: 'success'
          })
        })
        .catch((error) => {
          this.error = error.message
        })
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

.topcorner {
   position:absolute;
   top:0;
   right:0;
   color: transparent;
   background-color: transparent;
   border-color: transparent;
   /* display: none; */
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
