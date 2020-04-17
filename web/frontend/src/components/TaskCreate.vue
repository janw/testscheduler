<template>
  <b-form inline>
    <label class="mr-sm-2" for="inline-form-input-username">Requester</label>
    <b-input id="inline-form-input-username" class="mb-2 mr-sm-2 mb-xs-0" placeholder="Jane Doe"></b-input>

    <label class="mr-sm-2" for="inline-form-input-envid">Environment ID</label>
    <b-input id="inline-form-input-envid" class="mb-2 mr-sm-2 mb-sm-0" placeholder="42"></b-input>

    <label class="mr-sm-2" for="inline-form-input-testpath">Test Path</label>
    <b-input
      id="inline-form-input-testpath"
      class="mb-2 mr-sm-2 mb-sm-0"
      placeholder="Tests/test_1.py"
    ></b-input>

    <b-button variant="primary">Submit</b-button>
  </b-form>
</template>
