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
import { mdiInformationBoxOutline } from '@mdi/js';



const markdown = marked(`
# PtN 素材計算機
本サイトで引用されている『無期迷途』内の文章・画像等の著作権はZIYI GROUP HK LIMITED又は権利を有する第三者に帰属します。
また、権利者様側からの画像等の削除の依頼や警告は速やかに対処いたします。\n
[GitHub](https://github.com/AureaAurum/PtN_tool_code)

## 使い方
検索欄からコンビクトを選択すると素材の必要数が計算されます。選択後のキャラをクリックするとランクアップや各スキルレベルの目標を設定できます。\n
各素材、一番下の不足数の表示には上位素材を合成するための必要数が含まれています(ex.紫素材1つにつき白素材27個)。\n
フィルタで、各種素材の表示の有無を切り替えられます。

## 謝辞
wiki\n
- JP [無期迷途 日本語wiki](https://wikiwiki.jp/ptn/)\n
- CN [biligame](https://wiki.biligame.com/wqmt/%E9%A6%96%E9%A1%B5)

This project is inspired by [arkntools/arknights-toolbox](https://github.com/arkntools/arknights-toolbox)

# 更新履歴

2023-10-12 Readme等の記載、軽微なバグ修正

`);
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