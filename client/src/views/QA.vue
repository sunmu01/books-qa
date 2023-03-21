<script setup>
import { ref, onBeforeMount } from "vue";

const error = ref(null);
const answer = ref(null);

const levels = ref([
  {
    name: "book",
    value: "L0",
  },
  {
    name: "summary",
    value: "L1",
  },
  {
    name: "outline",
    value: "L2",
  },
]);

const books = ref([]);

const api = import.meta.env.VITE_API_URL;
onBeforeMount(() => {
  fetch(`${api}/get_bookname_list`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      books.value = data;
    })
    .catch((error) => {
      books.value = [];
    });
});

const payload = ref({
  question: "",
  bookname: "",
  qa_level: "L0",
  previous_question: "",
  previous_answer: "",
});

const askHandler = async () => {
  fetch(`${api}/get_chatgpt_answer`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload.value),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      answer.value = data.answer;
      payload.value.previous_question = payload.value.question;
      payload.value.previous_answer = answer.value;
    })
    .catch((error) => {
      error.value = error;
    });
};
</script>

<template>
  <div>
    <div class="prose max-w-none">
      <div class="text-2xl border-l-4 pl-4 border-blue-600">Books Q&A with ChatGPT</div>

      <p>
        We use OpenAI embeddings and ChatGPT to find answers from the
        relevant books.
      </p>

      <div>
        <i>Choose book for Q&A (optional):</i>
        <div class="py-2">
          <select
            class="form-select rounded pl-4 pr-8 py-1.5"
            name="bookname"
            title="bookname"
            v-model="payload.bookname"
          >
            <option value="" selected>All books</option>
            <option :value="book.book_name" v-for="book in books">
              《{{ book.book_name }}》
            </option>
          </select>
        </div>
      </div>

      <div>
        <i>Choose search level (default is "book"):</i>
        <div class="py-2 flex">
          <label class="flex items-center mr-4" v-for="level in levels">
            <input
              class="form-radio mr-1"
              type="radio"
              name="qa_level"
              :value="level.value"
              v-model="payload.qa_level"
            />
            {{ level.name }}
          </label>
        </div>
      </div>

      <div>
        <i>Ask a question based on the content of these books:</i>
        <div class="py-2">
          <input
            class="form-input rounded w-full"
            type="search"
            name="question"
            v-model="payload.question"
            placeholder="e.g. What is the Central Bank? or 什么是中国历史的空间结构？"
          />
        </div>
      </div>

      <div class="py-2">
        <button
          type="button"
          class="px-6 py-2 rounded text-white bg-blue-600 hover:bg-blue-700"
          @click="askHandler"
        >
          Ask question
        </button>
        <div class="py-2 text-red-500" v-if="error">Error: {{ error }}</div>
      </div>
    </div>

    <div class="pt-4" v-if="answer">
      <article class="prose max-w-none">
        <p>Answer:</p>
        <div
          class="p-8 w-full bg-slate-50 border-slate-50"
          v-html="answer"
        ></div>
      </article>
    </div>
  </div>
</template>

<style scoped></style>
