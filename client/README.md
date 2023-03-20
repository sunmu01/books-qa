# Development

## nodejs npm OR pnpm

Install `nodejs` OR `pnpm` ([https://pnpm.io/installation](https://pnpm.io/installation)).

Install pnpm: `brew install pnpm`.

Use pnpm install nodejs: `pnpm env use --global lts`.

## Install dependencies

`pnpm install` OR `npm install`

## Run dev

`pnpm dev` OR `pnpm run dev` OR `npm run dev`

## Run build

`pnpm build` OR `pnpm run build` OR `npm run build`

## Entry file

`/src/main.js` , router is in this file too.

route's view: `/` => `/src/views/QA.vue` , `/up` => `/src/views/UP.vue` (upload is not finished).

## Config file

`/.env`

only a `API_URL` in `.env` config file

## Requests

`GET ${API_URL}/get_bookname_list` at `/src/views/QA.vue` line 26

`POST ${API_URL}/get_chatgpt_answer` at `/src/views/QA.vue` line 43

Get answer request body data format:

```json
{
  "question": "blablabla",
  "bookname": "blablabla", // nullable
  "qa_level": 0, // 0: book, 1: summary, 2: outline, default is 0
}
```