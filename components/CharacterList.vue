<template>
  <v-data-table :items="filterdItems" item-key="name" :headers="headers" :items-per-page="-1">
    <template v-slot:headers>
      <tr>
        <th v-for="header of headers">{{ $t(header.title) }}</th>
      </tr>
      <tr>
        <th>
          <v-text-field v-model="search" density="compact" hide-details flat></v-text-field>
        </th>
        <th>
          <v-select v-model="SinValue" :items="sinname" density="compact" hide-details flat>
            <template v-slot:selection="{ item }">
              {{ $t(item.value) }}
            </template>
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :title="$t(item.value)"></v-list-item>
            </template>
          </v-select>
        </th>
        <th>
          <v-select v-model="RareValue" :items="rarename" density="compact" hide-details flat>
            <template v-slot:selection="{ item }">
              {{ $t('$rare' + item.value) }}
            </template>
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :title="$t('$rare' + item.value)"></v-list-item>
            </template>
          </v-select>
        </th>
        <th>
          <v-select v-model="RUM1Value" :items="matname" density="compact" hide-details flat>
            <template v-slot:selection="{ item }">
              {{ $t(item.value) }}
            </template>
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :title="$t(item.value)"></v-list-item>
            </template>
          </v-select>
        </th>
        <th>
          <v-select v-model="RUM2Value" :items="matname" density="compact" hide-details flat>
            <template v-slot:selection="{ item }">
              {{ $t(item.value) }}
            </template>
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :title="$t(item.value)"></v-list-item>
            </template>
          </v-select>
        </th>
        <th>
          <v-select v-model="SUMValue" :items="matname" density="compact" hide-details flat>
            <template v-slot:selection="{ item }">
              {{ $t(item.value) }}
            </template>
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :title="$t(item.value)"></v-list-item>
            </template>
          </v-select>
        </th>
        <th>
          <v-select v-model="NaikaiValue" :items="naikainame" density="compact" hide-details flat>
            <template v-slot:selection="{ item }">
              {{ $t(item.value) }}
            </template>
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props" :title="$t(item.value)"></v-list-item>
            </template>
          </v-select>
        </th>
      </tr>
    </template>
    <template v-slot:item.rankup_material1="{ item }">
      <v-tooltip bottom :text="`${$t(item.raw.rankup_material1)}`" location="bottom">
        <template v-slot:activator="{ props }">
          <v-img v-bind=props :src="'/img/materials/' + materialstore.categories[item.raw.rankup_material1][3].id + '.png'" aspect-ratio="1" height="60px" width="60px"></v-img>
        </template>
      </v-tooltip>    </template>
    <template v-slot:item.rankup_material2="{ item }">
      <v-tooltip bottom :text="`${$t(item.raw.rankup_material2)}`" location="bottom">
        <template v-slot:activator="{ props }">
          <v-img v-bind=props :src="'/img/materials/' + materialstore.categories[item.raw.rankup_material2][3].id + '.png'" aspect-ratio="1" height="60px" width="60px"></v-img>
        </template>
      </v-tooltip>    </template>
    <template v-slot:item.skill_material="{ item }">
      <v-tooltip bottom :text="`${$t(item.raw.skill_material)}`" location="bottom">
        <template v-slot:activator="{ props }">
          <v-img v-bind=props :src="'/img/materials/' + materialstore.categories[item.raw.skill_material][3].id + '.png'" aspect-ratio="1" height="60px" width="60px"></v-img>
        </template>
      </v-tooltip>
    </template>
    <template v-slot:item.naikai="{ item }">
      <v-tooltip bottom :text="`${$t(item.raw.naikai)}`" location="bottom">
        <template v-slot:activator="{ props }">
          <v-img v-if="show(nID(item.raw.naikai))" v-bind="props" :src="'/img/materials/' + materialstore.categories['内海'][nID(item.raw.naikai)].id + '.png'" aspect-ratio="1" height="60px" width="60px"></v-img>
        </template>
      </v-tooltip>
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
const search = ref('');

const materialstore = useMaterialStore();
const matname: string[] = ['', ...Object.keys(materialstore.categories).slice(1, 12)];

const SinValue = ref('');
const sinname: string[] = ['', 'エンデュア', 'フューリー', 'アンブラ', 'レチクル', 'アーケイン', 'カタリシス'];

const RareValue = ref('');
const rarename: string[] = ['', 'S', 'A', 'B'];

const RUM1Value = ref('');
const RUM2Value = ref('');
const SUMValue = ref('');

const NaikaiValue = ref('');
const naikainame: string[] = ['', '囁き', '亡骸', '狂念'];
const nID = (naikai: string) => {
  const nID: number = naikai == '囁き' ? 0 : naikai == '亡骸' ? 1 : naikai == '狂念' ? 2 : -1;
  return nID;
};
const show = (id: number) => id >= 0 ? true: false;

const headers: any = [
  {
    title: '$tableHeaderCharacter',
    key: 'name',
    value: (item: { name: any; }) => t(item.name),
    align: 'start',
    sortable: false,
    width: '15%',
  },
  {
    title: '$tableHeaderSin',
    key: 'sin',
    value: (item: { sin: any; }) => t(item.sin),
    align: 'start',
    sortable: false,
    width: '15%',
  },
  {
    title: '$tableHeaderRarity',
    key: 'rarity',
    sortable: true,
    value: (item: { rarity: any; }) => t('$rare' + item.rarity),
    width: '10%',
  },
  { title: '$tableHeaderRUM1', key: 'rankup_material1', sortable: true, width: '15%' },
  { title: '$tableHeaderRUM2', key: 'rankup_material2', sortable: true, width: '15%' },
  { title: '$tableHeaderSUM', key: 'skill_material', sortable: true, width: '15%' },
  { title: '$tableHeaderNaikai', key: 'naikai', value: 'naikai', sortable: true, width: '15%' },
];

const filterdItems = computed(() => {
  const filtered = items.filter((item) => {
    return (
      (NaikaiValue.value === '' || item.naikai === NaikaiValue.value) &&
      (SinValue.value === '' || item.sin === SinValue.value) &&
      (RUM1Value.value === '' || item.rankup_material1 === RUM1Value.value) &&
      (RUM2Value.value === '' || item.rankup_material2 === RUM2Value.value) &&
      (SUMValue.value === '' || item.skill_material === SUMValue.value) &&
      (RareValue.value === '' || item.rarity === RareValue.value) &&
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
