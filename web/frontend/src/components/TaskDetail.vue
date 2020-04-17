<template>
  <div v-if="data">
    <b-card class="mb-3">
      <h2 class="mb-1 text-center text-md-left">Details for test ID {{data.id}}</h2>
      <div v-bind:key="name" v-for="(value, name) in processedData" class="row">
        <div class="col">{{name}}</div>
        <b-col>{{value}}</b-col>
      </div>
    </b-card>
    <b-card class="mb-3" bg-variant="dark" header="Log Output" text-variant="white">
      <div class="row">
        <div class="col">
          <p v-html="data.logs" class="logs-output text-monospace"></p>
        </div>
      </div>
    </b-card>
  </div>
</template>

<style lang="scss" scoped>
.logs-output {
  font-size: 0.8rem;
  white-space: pre-wrap;
}
</style>

<script>
export default {
  props: ["id"],
  data() {
    return {
      data: null,
      fields: {
        id: "ID",
        requester: "Requester",
        env_id: "Environment",
        path: "Path",
        status: "Status"
      }
    };
  },
  created() {
    this.$api
      .get(`/api/tasks/${this.id}`)
      .then(response => (this.data = response.data))
      .catch(error => {});
  },
  computed: {
    processedData() {
      let copy = {};
      for (var attr in this.data) {
        if (this.fields.hasOwnProperty(attr))
          copy[this.fields[attr]] = this.data[attr];
      }
      return copy;
    }
  }
};
</script>
