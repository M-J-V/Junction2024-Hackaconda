<script setup>

import { ref } from 'vue'
const props = defineProps({
  title: String,
})

const result = ref(false)

let vote_value = ref(0)
function change_vote(vote) {
  vote_value.value = vote
}

let relevance_value = ref(0)

let discussion_value = ref('')

async function submit_vote() {
  let body = {
    question_uuid: 0,
    user_uuid: 0,
    answer_score: vote_value.value,
    relevance_score: parseInt(relevance_value.value),
    discussion_field: discussion_value.value,
  }
  result.value = !result.value
  console.log(body)
  // let response = await fetch(`${DOMAIN_NAME}/response`, {
  //   method: 'POST',
  //   body: JSON.stringify(body),
  // })
  // console.log(await response.text())
  // show_results(await response.json())
}

async function show_results(results) {
  // { for: 123, against: 2}
}
</script>

<template>
  <div class="card" style="width: 25rem;">
    <div >
      <div class="card-body">
        <h5 class="card-title">{{ title }}</h5>
        <p class="card-text">Background information on topic</p>
      </div>
<!--      Buttons-->
      <div v-if="!result" class="card-footer d-flex flex-column">
        <h5>How relevant is this question</h5>
        <input type="range" class="form-range" min="1" max="5" id="relevance" value="3" v-model="relevance_value" />
        <div class="d-flex justify-content-between">
          <button type="button" class="btn btn-danger" @click="change_vote(-1)">disagree</button>
          <button type="button" class="btn btn-primary" @click="change_vote(0)">unsure</button>
          <button type="button" class="btn btn-success" @click="change_vote(1)">agree</button>
        </div>
        <label class="form-label">Add your discussion points</label>
        <input class="form-control" id="discussion" placeholder="Add extra inside on your choice" v-model="discussion_value" >

        <label class="form-label">When ready</label>
        <button type="button" class="btn btn-success" @click="submit_vote()">Submit</button>
      </div>
<!--      Results-->
      <div v-else class="card-footer">
        <div class="progress bg-success" role="progressbar" aria-label="Basic example" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
          <div class="progress-bar bg-danger" style="width: 25%"></div>
          <div class="progress-bar bg-gray" style="width: 50%"></div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>

</style>