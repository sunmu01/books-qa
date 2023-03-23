<script setup>
import { ref, onBeforeMount, computed } from "vue";
import download from "downloadjs";

const booksUrl = ref(import.meta.env.VITE_BOOK_URL);
const appUrl = ref(import.meta.env.VITE_APP_URL);

const error = ref(null);
const answer = ref(null);
const reference = ref(null);

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
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": `${appUrl.value}`,
    },
  })
    .then((response) => response.json())
    .then((data) => {
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

const invalid = computed(() => {
  return !payload.value.question;
});

const asking = ref(false);

const askHandler = () => {
  error.value = null;
  answer.value = null;
  asking.value = true;
  fetch(`${api}/get_chatgpt_answer`, {
    method: "POST",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": `${appUrl.value}`,
    },
    body: JSON.stringify(payload.value),
  })
    .then((response) => response.json())
    .then((data) => {
      answer.value = data.answer.replace(/\n/g, "<br>");
      reference.value = data.reference.replace(/\n/g, "<br>");
      payload.value.previous_question = payload.value.question;
      payload.value.previous_answer = answer.value;
    })
    .catch((error) => {
      error.value = error;
    })
    .finally(() => {
      asking.value = false;
    });
};

const downloading = ref(false);
const handleDownload = () => {
  downloading.value = true;
  const filename = `${payload.value.bookname}-${payload.value.qa_level}.txt`;
  fetch(`${booksUrl.value}/${filename}`)
    .then((response) => response.blob())
    .then((blob) => {
      download(blob, filename, "text/pain");
    })
    .finally(() => {
      downloading.value = false;
    });
};
</script>

<template>
  <div
    class="sm:p-4 md:p-8 flex flex-col items-center fixed inset-0 overflow-auto bg-slate-200"
  >
    <div class="p-4 md:p-8 bg-white shadow">
      <div class="prose max-w-none">
        <div class="text-2xl border-l-4 pl-4 border-blue-600">
          ChatBook v0.0.1 - lauched on 2023-03-22
        </div>

        <p>
          We use Pinecone, OpenAI embeddings and ChatGPT to find answers from
          the relevant books.
        </p>

        <div>
          <i>Choose book for Q&A (optional):</i>
          <div class="py-2">
            <select
              class="form-select rounded pl-4 pr-8 py-1.5 max-w-full"
              name="bookname"
              title="bookname"
              v-model="payload.bookname"
              :disabled="asking"
            >
              <option value="" selected>All books</option>
              <option :value="book.book_name" v-for="book in books">
                《{{ book.book_name }}》
              </option>
            </select>
          </div>
        </div>

        <div>
          <i>Choose content level (default is "book"):</i>
          <div class="py-2 flex">
            <label class="flex items-center mr-4" v-for="level in levels">
              <input
                class="form-radio mr-1"
                type="radio"
                name="qa_level"
                :value="level.value"
                v-model="payload.qa_level"
                :disabled="asking"
              />
              {{ level.name }}
            </label>
          </div>
        </div>

        <div>
          <i>Ask a question based on the content of books:</i>
          <div class="py-2">
            <input
              class="form-input rounded w-full"
              type="search"
              name="question"
              v-model="payload.question"
              placeholder="e.g. What is the Central Bank? or 什么是中国历史的空间结构？"
              :disabled="asking"
            />
          </div>
        </div>

        <div class="py-2">
          <button
            type="button"
            class="px-6 py-2 rounded text-white bg-blue-400 cursor-progress flex items-center"
            disabled
            v-if="asking"
          >
            <svg
              class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            Loading..
          </button>
          <button
            type="button"
            class="px-6 py-2 rounded text-white bg-blue-400 cursor-not-allowed"
            disabled
            v-else-if="invalid"
          >
            Ask question
          </button>
          <button
            type="button"
            class="px-6 py-2 rounded text-white bg-blue-600 hover:bg-blue-700"
            @click="askHandler"
            v-else
          >
            Ask question
          </button>
          <div class="py-2 text-red-500" v-if="error">Error: {{ error }}</div>
        </div>
      </div>

      <div class="border-t-1 border-gray-50">
        <article class="prose max-w-none" v-if="asking">
          <div class="p-8 w-full bg-slate-50 border-slate-50 flex items-center">
            <svg
              class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            GPT is loading...
          </div>
        </article>
        <article class="prose max-w-none" v-else>
          <div v-if="payload.bookname">
            <p>Book Content or Summary:</p>
            <div class="p-8 w-full bg-slate-50 border-slate-50">
              <button
                type="button"
                class="cursor-progress text-slate-500 bg-slate-200 w-full px-2 flex items-center justify-between"
                v-if="downloading"
              >
                {{ payload.bookname }}-{{ payload.qa_level }}.txt
                <svg
                  class="animate-spin -ml-1 mr-3 h-5 w-5 text-slate-500"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    class="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    stroke-width="4"
                  ></circle>
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
              </button>
              <button
                type="button"
                class="cursor-pointer text-slate-900 hover:text-blue-600 hover:bg-slate-200 border-b-1 hover:border-blue-500 w-full px-2 flex items-center justify-between"
                @click="handleDownload"
                v-else
              >
                {{ payload.bookname }}-{{ payload.qa_level }}.txt
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="18"
                  height="18"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
              </button>
            </div>
          </div>
          <div v-if="answer">
            <p>Answer:</p>
            <div
              class="p-8 w-full bg-slate-50 border-slate-50"
              v-html="answer"
            ></div>
          </div>
          <div v-if="reference">
            <p>Reference:</p>
            <div
              class="p-8 w-full bg-slate-50 border-slate-50"
              v-html="reference"
            ></div>
          </div>
        </article>
      </div>
    </div>
  </div>
</template>
