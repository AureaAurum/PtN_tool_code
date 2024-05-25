<template>
    <v-dialog scrollable width="70%" min-width="400px">
        <template v-slot:activator="{ props }">
            <v-btn flat v-bind="props" class="pa-0" size="32">
                <template v-slot:default>
                    <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 26 26">
                        <path :d="mdiInformationBoxOutline" stroke="white" fill="white"></path>
                    </svg>
                </template>
            </v-btn>
        </template>
        <template v-slot:default="{ isActive }">
            <v-card>
                <v-card-text>
                    <div v-html="markdown" class="markdown"></div>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="isActive.value = false">閉じる</v-btn>
                </v-card-actions> </v-card>
        </template>
    </v-dialog>
</template>

<script setup lang="ts">
import { marked } from 'marked';
import { baseUrl } from 'marked-base-url';
import { mdiInformationBoxOutline } from '@mdi/js';

const readme:string = await $fetch('https://raw.githubusercontent.com/AureaAurum/PtN_tool_code/main/README.md');
marked.use(baseUrl("https://github.com/AureaAurum/PtN_tool_code/blob/main/"))
const markdown = marked(readme);
</script>

<style>
.markdown p {
    margin: 1em;
}

.markdown img {
    max-width: 100%;
}

.markdown h1:nth-child(n+2) {
    margin-top: 150px;
}

.markdown h2 {
    margin-top: 50px;
}

.markdown h1,
.markdown h2,
.markdown h3,
.markdown h4,
.markdown h5,
.markdown h6 {
    font-weight: normal;
    line-height: 1em;
}

.markdown h4,
.markdown h5,
.markdown h6 {
    font-weight: bold;
}

.markdown h1 {
    font-size: 2.5em;
}

.markdown h2 {
    font-size: 2em;
}

.markdown h3 {
    font-size: 1.5em;
}

.markdown h4 {
    font-size: 1.2em;
}

.markdown h5 {
    font-size: 1em;
}

.markdown h6 {
    font-size: 0.9em;
}

.markdown ol {
    margin: 1em 0;
    padding: 0 0 0 2em;
}

.markdown ul {
    margin: 1em 0;
    padding: 0 0 0 2em;
    list-style: disc;
}

.markdown dd {
    margin: 0 0 0 2em;
}

.markdown table {
    margin: 10px 0 15px 0;
    border-collapse: collapse;
}

.markdown td,
.markdown th {
    border: 2px solid;
    padding: 3px 10px;
}

.markdown th {
    padding: 5px 10px;
}

.markdown blockquote {
    padding-left: 1em;
    margin: 0;
    color: #333333;
    border-left: 0.3em solid;
}
</style>