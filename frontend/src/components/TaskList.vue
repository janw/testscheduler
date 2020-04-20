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
            :busy="isBusy"
            :fields="fields"
            :items="data"
            :sort-by.sync="sortBy"
            :sort-desc.sync="sortDesc"
            :tbody-tr-class="rowClass"
            :tbody-transition-props="{name: 'flip-list'}"
            @row-clicked="onRowClicked"
            class="mt-3"
            id="tests_table"
            primary-key="id"
            ref="tests_table"
            responsive
            show-empty
            stacked="md"
          >
            <template v-slot:table-busy>
              <div class="text-center my-2">
                <b-spinner class="align-middle"></b-spinner>
                <p class="mt-2">Loading …</p>
              </div>
            </template>
            <template v-slot:empty>
              <div class="text-center my-2">
                <p class="mt-2">No requests to display. Create a new request above.</p>
              </div>
            </template>
            <template v-slot:cell(details)="data">
              <small>
                <b-link :to="{ name: 'TaskDetail', params: { id: data.item.id } }">View &raquo;</b-link>
              </small>
            </template>
          </b-table>
        </b-col>
      </b-row>
    </b-card>
  </div>
</template>

<style lang="scss">
table#tests_table .flip-list-move {
  transition: transform 0.4s;
}
</style>

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
    this.$api.get("/api/testruns").then(response => {
      this.data = response.data;
      this.isBusy = false;
    });
  },
  data() {
    return {
      sortBy: "id",
      sortDesc: true,
      isBusy: true,
      fields: [
        { key: "id", label: "ID", sortable: true },
        { key: "username", label: "Requester", sortable: true },
        { key: "created_at", sortable: true },
        { key: "env_id", label: "Env", sortable: true },
        { key: "path", sortable: true },
        { key: "status", sortable: true },
        { key: "details", label: "" }
      ],
      data: []
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
    },
    onRowClicked(item, index) {
      this.$router.push({ name: "TaskDetail", params: { id: item.id } });
    }
  }
};
</script>
