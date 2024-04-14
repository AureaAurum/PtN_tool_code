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
# 無期迷途 素材計算機
本サイトで引用されている『無期迷途』内の文章・画像等の著作権はZIYI GROUP HK LIMITED又は権利を有する第三者に帰属します。\n
また、権利者様側からの画像等の削除の依頼や警告は速やかに対処いたします。\n
大陸版wikiにのってない内海素材は基本的にデータが入っていません。情報提供いただければ反映させます。\n
バグ報告、機能の要望等はGithub、マシュマロ、もしくはX(旧Twitter)まで。

## 使い方
検索欄からコンビクトを選択すると素材の必要数が計算されます。選択後のキャラをクリックするとランクアップや各スキルレベルの目標を設定できます。\n
各素材、一番下の不足数の表示には上位素材を合成するための必要数が含まれています(ex.紫素材1つにつき白素材27個)。\n
ディスコインはランクアップ、スキルレベルアップに必要な分のみの計算となっています。レベルアップに別途ディスコインが必要です。\n
フィルタで、各種素材の表示の有無を切り替えられます。\n
挙動が変でしたらお手数ですが当サイトのキャッシュ・データ削除をお試しください。

## 連絡先
[GitHub](https://github.com/AureaAurum/PtN_tool_code) [X](https://twitter.com/Aurea_Aurum) [マシュマロ](https://marshmallow-qa.com/1lhdgcbb5qqm1yg)

## 謝辞
wiki\n
- JP [無期迷途 日本語wiki](https://wikiwiki.jp/ptn/)
- CN [biligame](https://wiki.biligame.com/wqmt/%E9%A6%96%E9%A1%B5)

This project is inspired by [arkntools/arknights-toolbox](https://github.com/arkntools/arknights-toolbox)

# 更新履歴
2024-04-15 コンビクト一覧を追加。 \n
2024-04-10 データ更新処理の変更。自動スケジュール化。\n
2024-04-05 多言語対応テスト。追加:Bianca,Shawn \n
2024-03-12 追加:Angel, Golan。 \n
2024-02-04 追加:Du Ruo, Yanyan, Yao。 \n
2024-01-14 追加:Vanilla, Thistle。\n
2024-01-07 翻訳追加:イヴ, エウレカ。\n
2023-12-19 追加:Lady Pearl, Echo。翻訳追加:エブン, ニノ。コンビクト詳細画面に内海素材の表示を追加。\n
2023-12-03 翻訳追加:マンティス, カシア。リセット機能の調整。\n
2023-11-25 唐, 玛蒂尔达を追加。スマホでの背景色の乱れを修正\n
2023-10-31 伊芙, 优利卡を追加\n
2023-10-22 コンビクト詳細画面に使用する素材の種類表示を追加\n
2023-10-22 ランクアップ3済みの場合素材が正しく計算されないバグを修正\n
2023-10-21 翻訳追加:コクリコ, クリスティナ\n
2023-10-20 収集済み素材の表示切り替えをオプション化\n
2023-10-19 ディスコイン対応 軽微なバグ修正\n
2023-10-18 翻訳追加:シャローム\n
2023-10-15 集めきった素材は暗く表示するように\n
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