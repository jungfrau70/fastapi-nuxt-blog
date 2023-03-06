<template>
  <v-card height="100%">
    <v-tabs>
      <v-tab to="/discussion/list">리스트</v-tab>
      <!-- <v-tab to="/discussion/graph">그래프</v-tab>
      <v-tab to="/discussion/dashboard">대시보드</v-tab>
      <v-tab to="/discussion/analyzer">분석기</v-tab> -->
    </v-tabs>
    <nuxt-child />
    <v-dialog v-model="dialog">
      <template #[`activator`]="{ on }">
        <v-card-actions class="justify-space-between">
          <v-col sm="2">
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              class="ml-auto ma-3"
              maxlength="25"
              single-line
              hide-details
            ></v-text-field>
          </v-col>
          <v-btn color="primary" dark class="ml-auto ma-3" v-on="on">
            New Record
            <v-icon small>mdi-plus-circle-outline</v-icon>
          </v-btn>
          <v-btn
            color="primary"
            dark
            class="ml-auto ma-3"
            @click="exportData()"
          >
            Download
            <v-icon small>mdi-arrow-right-circle-outline</v-icon>
          </v-btn>
        </v-card-actions>
      </template>
      <v-card v-model="dialogAdd">
        <VulnerabilityDetail
          :edited-item="newItem"
          @submit-item="submitItem"
          @close="close(newItem.id)"
        />
      </v-card>
    </v-dialog>

    <v-data-table
      v-model="selected"
      dense
      :search="search"
      :headers="headers"
      :items="filteredItems"
      :options.sync="options"
      show-select
      item-key="id"
      class="elevation-1"
    >
      <template #[`body.prepend`]>
        <tr>
          <th>
            <v-icon>filters</v-icon>
          </th>

          <th v-for="header in headers" :key="header.text">
            <div>
              <v-select
                v-model="filters[header.value]"
                :items="columnValueList(header.value)"
                flat
                hide-details
                small
                multiple
                clearable
              >
              </v-select>
            </div>
          </th>
        </tr>
      </template>
      <template #[`item.actions`]="{ item }">
        <div class="text-truncate">
          <v-btn icon>
            <v-icon>mdi-dots-vertical</v-icon>
            <v-icon
              small
              class="mr-2"
              color="primary"
              @click="showEditDialog(item)"
            >
              mdi-pencil || "E"
            </v-icon>
          </v-btn>
          <v-icon small color="pink" @click="showDeleteDialog(item)">
            mdi-delete || "D"
          </v-icon>
        </div>
      </template>
    </v-data-table>

    <!-- Edit dialog -->
    <v-dialog v-model="dialogEdit">
      <v-card>
        <DiscussionDetail
          v-if="dialogEdit"
          :edited-item="editedItem"
          @submit-item="submitItem"
          @close="close(editedItem.id)"
        />
      </v-card>
    </v-dialog>

    <!-- delete dialog -->
    <v-dialog v-model="dialogDelete" max-width="500px">
      <v-card>
        <v-card-title>Delete</v-card-title>
        <v-card-text
          >제목(이벤트) `{{ itemToDelete.event }}`를(을) 삭제
          할까요?</v-card-text
        >
        <v-card-actions>
          <v-btn color="primary" text @click="dialogDelete = false"
            >Close</v-btn
          >
          <v-btn color="primary" text @click="deleteItem()">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>
<script>
import axios from 'axios'
import DiscussionDetail from '~/components/DiscussionDetail.vue'

const API_URL = `${process.env.BASE_URL}/discussion`

export default {
  components: { DiscussionDetail },

  data() {
    return {
      search: '',

      headers: [
        // { text: 'Id', value: 'id' },
        { text: 'Year', value: 'year', width: '75' },
        { text: 'Month', value: 'month', width: '75', sortable: true },
        { text: 'Region', value: 'region', width: '75', sortable: true },
        { text: 'AZ', value: 'az', width: '75', sortable: true },
        { text: 'Tenant', value: 'tenant', width: '75', sortable: true },

        { text: 'Progress', value: 'progress', width: '110', sortable: true },
        { text: 'Status', value: 'status', width: '75', sortable: true },

        // { text: 'Title', value: 'title', sortable: true },
        {
          text: 'Description(Topic)',
          value: 'discussion_topic',
          sortable: true,
          // width: '240',
        },
        { text: 'Edit / Delete', value: 'actions', sortable: false },
      ],

      filters: {
        id: [],
        year: [],
        month: [],
        region: [],
        tenant: [],
        progress: [],
        status: [],
      },

      options: {
        sortBy: ['id'],
        sortDesc: ['true'],
      },

      items: [],
      selected: [],
      currentItems: [],
      newItem: {},
      editedItem: {},

      dialog: false,
      dialogAdd: false,
      dialogEdit: false,
      dialogDelete: false,
      itemToDelete: {},
      // pyodide: null,
      // pyodideLoaded: null,
      output: '',
    }
  },

  computed: {
    filteredItems() {
      return this.items.filter((d) => {
        return Object.keys(this.filters).every((f) => {
          return this.filters[f].length < 1 || this.filters[f].includes(d[f])
        })
      })
    },
  },
  watch: {
    // dialogAdd: function () {
    //   this.newItem = {}
    // },
  },
  created() {
    // console.log('list created')
    this.loadItems()
  },
  mounted() {
    // console.log('list mounted')
  },
  updated() {
    // console.log('list updated')
    // console.log(this.editedItem.id)
    // this.loadItems()
  },

  beforeDestroy() {
    // console.log('list beforeDestroy')
  },
  methods: {
    vueDatetime(datetime) {
      // return this.$moment(datetime).format('YYYY-MM-DD HH:mm:ss')
      return this.$moment(datetime).format('YYYY-MM-DD HH:mm')
    },
    dbDatetime(datetime) {
      //   return datetime.toISOString()

      const today = new Date(datetime)
      const utcTodayDate = today.toISOString()
      return utcTodayDate
      // return this.$moment(datetime).format('YYYY-MM-DDTHH:mm:ss')
    },

    submitItem(item) {
      // airtable API needs the data to be placed in fields object
      // const today = new Date("2022-12-27 22:00")
      // const utcTodayDate = today.toISOString()
      // console.log(utcTodayDate)
      const data = {
        // id: item.id,
        year: item.year,
        month: item.month,
        region: item.region,
        az: item.az,
        tenant: item.tenant,

        progress: item.progress,
        status: item.status,

        // title: item.title,
        discussion_topic: item.discussion_topic,

        // creator: item.creator,
        // reviewer: item.reviewer,
        // updater: item.updater,
      }
      const id = item.id || null
      let method = null
      let url = null

      if (id) {
        // if the item has an id, we're updating an existing item
        console.log(id)
        method = 'put'
        url = `${API_URL}/${id}`

        this.item = {}
        // must remove id from the data for airtable patch to work
        // delete data.id

        // 편집창 종료
        this.dialogAdd = false
        this.dialogEdit = false
        // this.dialog = !this.dialog
        this.dialog = false
      } else {
        method = 'post'
        url = `${API_URL}`

        // 편집창 종료
        this.dialogAdd = false
        this.dialogEdit = false
        // this.dialog = !this.dialog
        this.dialog = false
      }

      console.log(data)

      // save the record
      // headers: {
      //     Authorization: 'Bearer ' + apiToken,
      //     'Content-Type': 'application/json',
      //   },
      console.log(method)
      this.$axios
        .$post(url, { data 
      // axios[method](url, data, {
        // headers: {
        //   'Access-Control-Allow-Origin': '*',
        //   'Access-Control-Allow-Methods':
        //     'GET, POST, PATCH, PUT, DELETE, OPTIONS',
        //   'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
        //   'Content-Type': 'application/json',
        //   'Authorization': 'Bearer',
        // },
      }).then((response) => {
        if (response.data && response.data.id) {
          // add new item to state
          this.editedItem.id = response.data.id
          if (!id) {
            // add the new item to items state
            this.items.push(this.editedItem)
          }
          this.editedItem = {}
          this.loadItems()
        }
      })

      // if (id) {
      //   this.dialogEdit = false
      //   this.editedItem = {}
      // } else {
      //   this.dialogAdd = false
      // }
      // this.dialogAdd = false

      this.$forceUpdate()
    },

    close(id) {
      // console.log('list close')
      // this.editedItem = {}
      if (id) {
        this.dialogEdit = false
        this.editedItem = {}
      } else {
        this.dialogAdd = false
        this.newItem = {}
      }
      this.dialog = false
    },
    getFiltered(e) {
      this.currentItems = e
    },
    toggleAll() {
      if (this.selected.length) this.selected = []
      else this.selected = this.currentItems.slice()
    },

    changeSort(column) {
      if (this.options.sortBy === column) {
        this.options.descending = !this.options.descending
      } else {
        this.options.sortBy = column
        this.options.descending = false
      }
    },

    columnValueList(val) {
      return this.items.map((d) => d[val])
    },

    showEditDialog(item) {
      if (!item.id) {
        item = {}
      }
      // console.log(item)
      this.editedItem = item || {}
      this.dialogEdit = !this.dialogEdit
    },

    async loadItems() {
      this.items = []
      await axios
        .get(`${API_URL}/all`, {
          headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods':
              'GET, POST, PATCH, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers':
              'Origin, Content-Type, X-Auth-Token',
          },
        })
        .then((response) => {
          this.items = response.data.map((item) => {
            return {
              id: item.id,
              year: item.year,
              month: item.month,
              region: item.region,
              az: item.az,
              tenant: item.tenant,

              progress: item.progress,
              status: item.status,

              // discussion_topic: item.title,
              discussion_topic: item.discussion_topic,

              creator: item.creator,
              reviewer: item.reviewer,
              updater: item.updater,
            }
          })
        })
        .catch((error) => {
          console.log(error)
        })
    },

    deleteItem() {
      const id = this.itemToDelete.id

      console.log(id)
      const method = 'delete'
      axios[method](`${API_URL}/${id}`, {
        // headers: {
        //   Authorization: 'Bearer ' + apiToken,
        //   'Content-Type': 'application/json',
        // },
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods':
            'GET, POST, PATCH, PUT, DELETE, OPTIONS',
          'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
          'Content-Type': 'application/json',
          // 'Authorization': 'Bearer ' + this.$apiToken,
        },
              // {{ $auth.user.email }}
      // return this.$store.getters.isAuthenticated
      }).then((response) => {
        this.items.splice(id, 1)
        this.loadItems()
      })
      this.dialogDelete = false
    },

    showDeleteDialog(item) {
      this.itemToDelete = item
      this.dialogDelete = !this.dialogDelete
    },

    pivot(arr) {
      const mp = new Map()

      function setValue(a, path, val) {
        if (Object(val) !== val) {
          // primitive value
          const pathStr = path.join('.')
          const i = (mp.has(pathStr) ? mp : mp.set(pathStr, mp.size)).get(
            pathStr
          )
          a[i] = val
        } else {
          for (const key in val) {
            setValue(a, key === '0' ? path : path.concat(key), val[key])
          }
        }
        return a
      }

      const result = arr.map((obj) => setValue([], [], obj))
      return [[...mp.keys()], ...result]
    },

    toCsv(arr) {
      return arr
        .map((row) =>
          row.map((val) => (isNaN(val) ? JSON.stringify(val) : +val)).join(',')
        )
        .join('\n')
    },

    exportData() {
      let data = []
      if (this.selected.length === 0) {
        data = this.toCsv(this.pivot(this.filteredItems))
      } else {
        data = this.toCsv(this.pivot(this.selected))
      }

      const pom = document.createElement('a')

      const blob = new Blob(['\uFEFF' + data], {
        type: 'text/csv; charset=utf-8',
      })
      const url = URL.createObjectURL(blob)
      pom.href = url
      pom.setAttribute('download', 'export.csv')
      pom.click()
    },
  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
  margin-top: 0px;
}

.container {
  max-width: 100vw;
  padding: 0px 0px 0px 0px;
}

.v-application--wrap {
  max-width: 100vw;
  padding: 0px 0px 0px 0px;
}

.v-main {
  max-width: 100vw;
  padding: 0px 0px 0px 0px;
}

.v-main__wrap {
  max-width: 100vw;
  padding: 0px 0px 0px 0px;
}
</style>
-->
