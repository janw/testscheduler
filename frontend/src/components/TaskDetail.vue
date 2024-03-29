<template>
  <div>
    <b-card no-body class="mb-3">
      <b-card-body>
        <h2 v-if="data" class="mb-1 float-md-left">Test Run Details: {{data.id}}</h2>
        <h2 v-else class="mb-1 float-md-left">Test Run Details</h2>

        <b-button class="float-md-right" :to="{name: 'TaskList'}" variant="primary">Go back</b-button>
      </b-card-body>
      <div v-if="data">
        <b-list-group flush>
          <b-list-group-item>
            <strong>ID:</strong>
            {{data.id}}
          </b-list-group-item>
          <b-list-group-item>
            <strong>Requested by:</strong>
            {{data.username}}
          </b-list-group-item>
          <b-list-group-item>
            <strong>Created at:</strong>
            {{data.created_at}}
          </b-list-group-item>
          <b-list-group-item>
            <strong>Environment:</strong>
            {{data.env_id}}
          </b-list-group-item>
          <b-list-group-item>
            <strong>Path:</strong>
            <span class="text-monospace">{{data.path}}</span>
          </b-list-group-item>
          <b-list-group-item v-bind:variant="itemVariant">
            <strong>Status:</strong>
            {{data.status}}
          </b-list-group-item>
        </b-list-group>
      </div>
      <div v-if="loading">
        <div class="text-center my-2">
          <b-spinner class="align-middle"></b-spinner>
          <p class="mt-2">Loading …</p>
        </div>
      </div>
      <div v-if="errorMsg">
        <div class="text-center my-2">
          <p class="mt-2">{{errorMsg}}</p>
        </div>
      </div>
    </b-card>
    <b-card v-if="data" class="mb-3" bg-variant="dark" header="Log Output" text-variant="white">
      <div class="row">
        <div class="col logs-output">
          <p v-if="logs" v-html="logs" class="text-monospace my-0"></p>
          <p v-else class="text-center my-3">No logs generated yet.</p>
        </div>
      </div>
    </b-card>
  </div>
</template>

<style lang="scss">
@import "~bootstrap/scss/functions";
@import "~bootstrap/scss/variables";
@import "~bootstrap/scss/mixins";
@import "~bootstrap/scss/tables";

.logs-output {
  font-size: 0.7rem;
  @include media-breakpoint-up(xl) {
    font-size: 0.9rem;
  }
}

.highlighttable {
  @extend .table-responsive;
}

.linenodiv {
  margin-right: 0.5em;
  padding-right: 0.8em;
  border-right: 1px solid $gray-500;
  & pre {
    color: $gray-300;
    margin-bottom: 0;
  }
}
.highlight {
  pre {
    margin-bottom: 0;
    color: $white;

    .-Color {
      &.-Color-Black {
        color: $black;
      }
      &.-Color-Red {
        color: $red;
      }
      &.-Color-Green {
        color: $green;
      }
      &.-Color-Yellow {
        color: $yellow;
      }
      &.-Color-Blue {
        color: $blue;
      }
      &.-Color-Magenta {
        color: $pink;
      }
      &.-Color-Cyan {
        color: $cyan;
      }
      &.-Color-White {
        color: $white;
      }
    }
  }
}
</style>

<script>
import { BButton, BListGroup, BListGroupItem } from "bootstrap-vue";
export default {
  components: {
    BListGroup,
    BListGroupItem,
    BButton
  },
  sockets: {
    connect: function() {
      console.log("Socket connected");
    },
    taskChanged: function(data) {
      console.log("Task changed");
      if (data.id == this.data.id) {
        this.data = data;
      }
    },
    logsChanged: function(data) {
      console.log("Logs changed");
      if (data.id == this.data.id) {
        this.logs = data.logs;
      }
    }
  },

  props: ["id"],
  data() {
    return {
      loading: true,
      errorMsg: null,
      data: null,
      logs: null
    };
  },
  created() {
    this.$api
      .get(`/api/testruns/${this.id}`)
      .then(response => {
        this.data = response.data;
        if (this.data.logs) {
          this.$api
            .get(`/api/testruns/${this.id}/logs`)
            .then(response => (this.logs = response.data.logs))
            .catch(error => {});
        }
      })
      .catch(error => {
        var prefix = `Error ${error.status}: `;
        if (error.status == 404) {
          this.errorMsg = `${prefix}Test Run ${this.id} does not exist.`;
        } else {
          this.errorMsg = `${prefix}Something went wrong.`;
        }
      })
      .then(() => {
        this.loading = false;
      });
  },
  computed: {
    itemVariant() {
      if (this.data.status === "succeeded") return "success";
      if (this.data.status === "failed") return "danger";
      if (this.data.status === "unknown") return "warning";
    }
  }
};
</script>
