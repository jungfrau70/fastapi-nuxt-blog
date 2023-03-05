<template>
  <v-card>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-container>
        <v-row>
          <v-card-title>
            <span v-if="editedItem.id">Edit {{ editedItem.id }}</span>
            <span v-else>Create</span>
          </v-card-title>
        </v-row>
        <v-row>
          <v-col
            v-for="(options, index) in colOptions"
            :key="index"
            cols="12"
            md="2"
          >
            <v-select
              v-model="item[index]"
              :items="options"
              :label="index"
              required
            >
            </v-select>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <v-text-field
              v-model="item['db_type']"
              label="Type(DB)"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="item['count']"
              label="Count"
            ></v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              v-model="item['status']"
              label="Status"
            ></v-text-field>
          </v-col>
        </v-row>

        <v-spacer></v-spacer>
        <v-row>
          <v-btn class="mr-4" color="green darken-1" @click="submitItem"
            >Submit</v-btn
          >
          <v-btn color="dark darken-1" @click="close(editedItem.id)"
            >Close</v-btn
          >
        </v-row>
        <!-- <v-row><p></p></v-row>
        <v-row><h1>Timestamp</h1></v-row>
        <v-row>
          <v-col>{{ item.acknowledged_at }} </v-col>
          <v-col>{{ vueDatetime(item.acknowledged_at) }} </v-col>
          <v-col>{{ dbDatetime(item.acknowledged_at) }} </v-col>

          <div>
            <div v-show="timestamp">Timestamp:{{ timestamp }}</div>
            <div v-show="date">Date:{{ date }}</div>

            <div v-show="time">Time:{{ time }}</div>

            <div v-show="currentYear">Only year:{{ currentYear }}</div>
          </div>
        </v-row> -->
        <v-spacer></v-spacer>
        <v-card-text style="height: 100px; position: relative">
          <v-fab-transition>
            <v-btn v-show="!hidden" color="pink" dark absolute top right fab>
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-fab-transition>
        </v-card-text>
      </v-container>
    </v-form>
  </v-card>
</template>

<script>
// import marked  from '@/plugins/mark '
export default {
  props: {
    editedItem: {
      type: Object,
      default: null,
    },
  },
  data: (vm) => ({
    // data() {
    //   return {
    dialog: '',
    hidden: true,
    valid: true,
    // convertedText: '',

    today: null,
    timestamp: null,
    date: null,
    time: null,
    currentYear: null,

    currentDatetime: null,
    DatetimePickerFormat: 'yyyy-MM-dd HH:mm',

    item: {
      // id: null,
      year: null,
      month: null,
      region: null,
      az: null,
      tenant: null,

      db_type: null,
      count: null,
      status: null,

      creator: null,
      reviewer: null,
      updater: null,
    },
    colOptions: {
      year: [2022, 2023, 2024, 2025],
      month: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
      region: [
        'CN',
        'EU',
        'IN',
        'KR',
        'KR Bigdata',
        'KR R&D',
        'NA',
        'RU',
        'SG',
      ],
      az: [1, 2, 3, 4, 5, 6, 7, 8],
      tenant: ['PRD', 'PRE_PRD', 'STG', 'DEV'],
      status: [
        'created',
        'scheduled',
        'work-in-progress',
        'completed',
        'cancelled',
        'delayed',
        'failed',
      ],
    },
  }),
  computed: {
    selected: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('input', value)
      },
    },
    // computedDateFormatted() {
    //   return this.formatDate(this.date)
    // },
    // actionMarkdown() {
    //   this.$marked.setOptions({
    //     renderer: new this.$marked.Renderer(),
    //     gfm: true,
    //     headerIds: false,
    //     tables: true,
    //     breaks: true,
    //     pedantic: false,
    //     sanitize: true,
    //     smartLists: true,
    //     smartypants: false,
    //   })
    //   return this.$marked(this.item.action)
    //   return this.$md.render(this.item.action)  || " "
    //   return ' '
    // },
  },
  watch: {},
  created() {
    // console.log('detail created')
    this.today = new Date()
    // if (this.editedItem.id) {
    //   this.loadItem()
    // } else {
    //   this.setDefaultItem()
    // }
  },
  beforeMounted() {
    console.log('detail mounted')
  },
  mounted() {
    console.log('detail mounted')
    if (this.editedItem.id) {
      this.loadItem()
    } else {
      this.setDefaultItem()
    }
    this.date = this.getDate()
    this.time = this.getTime()
    this.timestamp = this.getTimestamp()
    this.currentYear = this.getCurrentYear()
  },
  updated() {
    console.log('detail updated')
  },
  beforeDestroy() {
    console.log('detail beforeDestoryed')
  },
  methods: {
    getDate: function () {
      return new Date().toLocaleDateString()
    },
    getTime: function () {
      return new Date().toLocaleTimeString()
    },
    getTimestamp: function () {
      return Date.now()
    },
    getCurrentYear: function () {
      return new Date().getFullYear()
    },
    vueDatetime(datetime) {
      return this.$moment(datetime).format('YYYY-MM-DD HH:mm:ss')
    },
    dbDatetime(datetime) {
      return this.$moment(datetime).format('YYYY-MM-DDTHH:mm:ss')
    },
    setDefaultItem() {
      console.log('set default values to item')
      this.item.year = this.item.year || this.today.getFullYear()
      this.item.month = this.item.month || this.today.getMonth() + 1
      this.item.region = this.item.region || 'KR'
      this.item.az = this.item.az || 1
      this.item.tenant = this.item.tenant || 'PRD'

      this.item.db_type = this.item.db_type || 'PostgreSQL'
      this.item.count = this.item.count || 0
      this.item.status = this.item.status || 'PRD'

      this.item.creator = null
      this.item.reviewer = null
      this.item.updater = null
    },
    resetItem() {
      this.item = {}
    },
    getNow() {
      const today = new Date()
      const date =
        today.getFullYear() +
        '-' +
        (today.getMonth() + 1) +
        '-' +
        today.getDate()
      const time = today.getHours() + ':' + today.getMinutes()
      // const time = today.getHours() + ':' + today.getMinutes() + ':' + today.getSeconds()
      const timestamp = date + ' ' + time
      return timestamp
    },
    loadItem() {
      this.item = this.editedItem || {}
      this.$emit('showEditDialog', this.item)
      // console.log(this)
    },

    submitItem() {
      this.$emit('submit-item', this.item)
      this.resetItem()
      this.setDefaultItem()
    },
    close(id) {
      console.log('detail close')
      // this.item = {}
      // this.$parent.editedItem.id = null
      this.$emit('close', id)
    },
  },
}
</script>

<style scoped>
.container {
  max-width: 100vw;
  padding: 64px 64px 0px 256px;
}
</style>
