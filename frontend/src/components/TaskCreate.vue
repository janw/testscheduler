<template>
  <b-form @submit.prevent="handleSubmit">
    <b-form-row class="justify-content-between">
      <b-col cols="6" md="3">
        <label class="sr-only" for="inline-form-input-username">Username</label>
        <b-input
          id="inline-form-input-username"
          placeholder="Username"
          v-model="data.username"
          :state="valid_fields.username"
        ></b-input>
        <b-form-invalid-feedback
          v-bind:key="error"
          v-for="error in errors.username"
          :state="valid_fields.username"
        >{{error}}</b-form-invalid-feedback>
      </b-col>
      <b-col cols="6" md="2">
        <label class="sr-only" for="inline-form-input-envid">Environment ID</label>
        <b-input
          type="number"
          id="inline-form-input-envid"
          placeholder="Env ID"
          v-model="data.env_id"
          :state="valid_fields.env_id"
        ></b-input>
        <b-form-invalid-feedback
          v-bind:key="error"
          v-for="error in errors.env_id"
          :state="valid_fields.env_id"
        >{{error}}</b-form-invalid-feedback>
      </b-col>
      <b-col class="mt-2 mt-md-0">
        <label class="sr-only" for="inline-form-input-testpath">Test Path</label>
        <b-form-input
          list="testpath-list"
          id="inline-form-input-testpath"
          placeholder="Test Path"
          v-model="data.path"
          :state="valid_fields.path"
        ></b-form-input>
        <b-form-invalid-feedback
          v-bind:key="error"
          v-for="error in errors.path"
          :state="valid_fields.path"
        >{{error}}</b-form-invalid-feedback>

        <datalist id="testpath-list">
          <option v-bind:key="path" v-for="path in paths">{{ path }}</option>
        </datalist>
      </b-col>
      <b-col md="auto" class="mt-2 mt-md-0">
        <b-button :disabled="submit_disabled" type="submit" variant="primary">Submit</b-button>
      </b-col>
      <div class="w-100"></div>
    </b-form-row>
  </b-form>
</template>

<script>
export default {
  data() {
    return {
      errors: {},
      valid_fields: {
        username: null,
        env_id: null,
        path: null
      },
      data: {
        username: "",
        env_id: "",
        path: ""
      },
      paths: [],
      submit_disabled: false
    };
  },
  created() {
    this.paths = [];
    this.$api
      .get("/api/tests")
      .then(response => {
        this.paths = response.data;
      })
      .catch(error => {});
  },
  methods: {
    handleSubmit() {
      var self = this;
      this.submit_disabled = true;
      this.errors = [];
      for (var field in this.valid_fields) {
        this.valid_fields[field] = null;
      }
      this.$api
        .post("/api/testruns", this.data)
        .then(response => {
          this.paths = response.data;
        })
        .catch(error => {
          // Translate API validation results into frontend error displayal
          for (var field in error.data.errors) {
            this.valid_fields[field] = false;
            this.errors = error.data.errors;
          }
        })
        .then(() => {
          // Re-enable button after short timeout to prevent multiple queries at once.
          setTimeout(() => {
            self.submit_disabled = false;
          }, 500);
        });
    }
  }
};
</script>
