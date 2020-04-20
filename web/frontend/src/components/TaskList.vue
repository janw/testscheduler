<template>
  <div>
    <b-card class="mb-3">
      <h2>New request</h2>
      <b-row class="mt-3">
        <b-col>
          <TaskCreate />
        </b-col>
      </b-row>
    </b-card>
    <b-card class="mb-3">
      <h2>Test execution requests</h2>
      <b-row class="mt-3">
        <b-col>
          <b-table
            ref="tests_table"
            stacked="md"
            primary-key="id"
            :items="data"
            :fields="fields"
            :busy="isBusy"
            :tbody-tr-class="rowClass"
            responsive
          >
            <template v-slot:table-busy>
              <div class="text-center my-2">
                <b-spinner class="align-middle"></b-spinner>
                <p class="mt-2">Loading …</p>
              </div>
            </template>

            <template v-slot:cell(details)="data">
              <b-link :to="{ name: 'TaskDetail', params: { id: data.item.id } }">View Details</b-link>
            </template>
          </b-table>
        </b-col>
      </b-row>
    </b-card>
  </div>
</template>

<script>
import TaskCreate from "./TaskCreate";
export default {
  sockets: {
    connect: function() {
      console.log("Socket connected");
    },
    taskAdded: function(data) {
      console.log("New task added");
      this.data.unshift(data);
    },
    taskChanged: function(data) {
      console.log("Task changed");
      var elementPos = this.data
        .map(function(x) {
          return x.id;
        })
        .indexOf(data.id);
      this.data[elementPos] = data;
      this.$refs.tests_table.refresh();
    }
  },
  props: ["id"],
  created() {
    this.$api.get(`/api/tasks`).then(response => {
      this.data = response.data;
      this.isBusy = false;
    });
  },
  data() {
    return {
      endpoint: `/api/tasks/${this.id}/`,
      page: 1,
      fields: [
        { key: "id", label: "ID" },
        { key: "username", label: "Requester" },
        "created_at",
        { key: "env_id", label: "Test Env" },
        "path",
        "status",
        "details"
      ],
      data: [],
      selectedItem: {},
      selectedModal: false,
      isBusy: true
    };
  },
  components: {
    TaskCreate
  },
  methods: {
    rowClass(item, type) {
      if (!item || type !== "row") return;
      if (item.status === "succeeded") return "table-success";
      if (item.status === "failed") return "table-danger";
      if (item.status === "unknown") return "table-warning";
    }
  }
};
</script>
