<template>
  <v-data-table :items="filterdItems" item-key="name" :headers="headers" :items-per-page="-1">
    <template v-slot:headers>
      <tr>
        <th v-for="header of headers ">{{ $t(header.title) }}</th>
      </tr>
      <tr>
        <th>
          <v-text-field v-model="search" density="compact" hide-details flat></v-text-field>
        </th>
        <th> <v-select v-model="SinValue" :items="sinname" density="compact" hide-details flat /></th>
        <th> <v-select v-model="RUM1Value" :items="matname" density="compact" hide-details flat /></th>
        <th> <v-select v-model="RUM2Value" :items="matname" density="compact" hide-details flat /></th>
        <th> <v-select v-model="SUMValue" :items="matname" density="compact" hide-details flat /></th>
        <th> <v-select v-model="NaikaiValue" :items="naikainame" density="compact" hide-details flat /></th>
      </tr>
    </template>
    <template v-slot:item.rankup_material1="{ item }">
      <v-img :src="'/img/materials/' + materialstore.categories[item.raw.rankup_material1][3].id + '.png'" aspect-ratio="1" height="60px" width="60px"></v-img>
    </template>
    <template v-slot:item.rankup_material2="{ item }">
      <v-img :src="'/img/materials/' + materialstore.categories[item.raw.rankup_material2][3].id + '.png'" aspect-ratio="1" height="60px" width="60px"></v-img>
    </template>
    <template v-slot:item.skill_material="{ item }">
      <v-img :src="'/img/materials/' + materialstore.categories[item.raw.skill_material][3].id + '.png'" aspect-ratio="1" height="60px" width="60px"></v-img>
    </template>
    <template v-slot:item.naikai="{ item }">
      <v-img :src="'/img/materials/' + materialstore.categories['内海'][naikai(item.raw.naikai)].id + '.png'" aspect-ratio="1" height="60px" width="60px"></v-img>
    </template>

  </v-data-table>
</template>

<script setup lang="ts">
import { useCharacterStore } from '@/store/characters';
import { useMaterialStore } from '@/store/material';
import { VDataTable } from 'vuetify/labs/VDataTable';
import type { Character, Characters, Material } from '~/types/types';
import { useI18n } from '#imports';
const { t } = useI18n();
const characters = useCharacterStore();
const items: Character[] = Object.values(characters.data);
const search = ref("");

const materialstore = useMaterialStore();
const matname: string[] = ["", ...Object.keys(materialstore.categories).slice(1, 12)];

const SinValue = ref('');
const sinname: string[] = ["", "エンデュア", "フューリー", "アンブラ", "レチクル", "アーケイン", "カタリシス"];

const RUM1Value = ref('');
const RUM2Value = ref('');
const SUMValue = ref('');

const NaikaiValue = ref('');
const naikainame: string[] = ["", "囁き", "亡骸", "狂念"];
const naikai = (naikai: string) => {
  const nID: number = naikai == "囁き" ? 0 : naikai == "亡骸" ? 1 : naikai == "狂念" ? 2 : -1;
  return nID;
};




const headers: any = [
  { title:'$tableHeaderCharacter', key: 'name', value: (item: { name: any; }) => t(item.name), align: 'start', sortable: false },
  { title:'$tableHeaderSin', key: 'sin', value: (item: { sin: any; }) =>t(item.sin), align: 'start', sortable: false },
  { title:'$tableHeaderRUM1', key: 'rankup_material1', sortable: true },
  { title:'$tableHeaderRUM2', key: 'rankup_material2', sortable: true },
  { title:'$tableHeaderSUM', key: 'skill_material', sortable: true },
  { title:'$tableHeaderNaikai', key: 'naikai', value: 'naikai', sortable: true },
];

const filterdItems = computed(() => {
  const filtered = items.filter((item) => {
    return (
      (NaikaiValue.value === '' || item.naikai === NaikaiValue.value) &&
      (SinValue.value === '' || item.sin === SinValue.value) &&
      (RUM1Value.value === '' || item.rankup_material1 === RUM1Value.value) &&
      (RUM2Value.value === '' || item.rankup_material2 === RUM2Value.value) &&
      (SUMValue.value === '' || item.skill_material === SUMValue.value) &&
      customfilter(item.name, search.value, item)
    );
  });
  return filtered;
});

function customfilter(itemTitle: string, queryText: string, item: any) {
  const jName = hiraganaToKatakana(t(itemTitle));
  const searchText = hiraganaToKatakana(queryText);
  const englishSeach = queryText.toLowerCase();
  const eName = characters.data[item.ename].ename.toLowerCase();

  return jName.indexOf(searchText) > -1 || eName.indexOf(englishSeach) > -1;
}

function hiraganaToKatakana(src: string) {
  return src.replace(/[\u3041-\u3096]/g, function (match) {
    const chr = match.charCodeAt(0) + 0x60;
    return String.fromCharCode(chr);
  });
}

</script>
