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
            <el-select v-model="type" placeholder="请选择测试方法" style="margin:20px;">
              <el-option
                v-for="type in type_list"
                :key="type"
                :label="type"
                :value="type">
              </el-option>
            </el-select>
            <!-- <div>
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
                    <td>wav\model</td>
                    <th
                      v-for="model in wav_data.model_list"
                      :key="model"
                    >
                      {{ model }}
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
                      <span>
                        {{ wav_data.model_wav_score_list[model][wav] }}
                      </span>
                    </td>
                  </tr>
                  <tr>
                    <td>average</td>
                    <td v-for="model in wav_data.model_list" :key="model">
                        {{ wav_data.model_score_list[model] }}
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
      type: '',
      type_list: ['mos', 'similarity', 'abx'],
      resource_id_list: null,
      resource_type: null,
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
        this.fetchScoreResource(this.type, this.id)
      }
    },
    type: function (val) {
      this.type = val
      if (this.id !== '') {
        this.fetchScoreResource(this.type, this.id)
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

    fetchScoreResource (type, id) {
      $backend
        .fetchScoreResource(type, id)
        .then((res) => {
          this.wav_data = res
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
