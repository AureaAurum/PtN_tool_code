<template>
  <VAutocomplete base-color="grey-darken-1" color="grey-darken-3" item-color="white" hide-details
    hide-no-data clearable flat closable-chips multiple placeholder="" :items="items" item-title="name"
    return-object v-model="characters.selected" :custom-filter="customfilter" variant="underlined">
    <template v-slot:chip="{ item, index, props }">
      <CharacterDetail :item="item"></CharacterDetail>
    </template>
    <template v-slot:item="{ item, props }:any">
      <v-list-item v-bind="props" class="my-0 py-0" bg-color="grey-darken-">
        <template v-slot:title>
          {{ $t(item.raw.name) }}
        </template>
        <template v-slot:prepend>
          <v-avatar style="width: 70px; height: 50px; border-radius: 20%;" tile class="my-0">
            <template v-slot:default>
              <v-img cover :src='"/img/characters/" + item.raw.ename + ".png"'
                :alt="item.raw.name"></v-img>
            </template>
          </v-avatar>
        </template>
      </v-list-item>
    </template>
  </VAutocomplete>
</template>

<script setup lang ="ts">
import { useCharacterStore } from '@/store/characters';
import type { Character, Characters, ChJsonData, Condition, Material } from '~/types/types';
import { useI18n, useLocalePath } from '#imports'
const { t } = useI18n()

const characters = useCharacterStore();
const items: Character[] = Object.values(characters.data);
const sinOrder:{[key: string]: number } = {
  "エンデュア": 1,
  "フューリー": 2,
  "アンブラ": 3,
  "レチクル": 4,
  "アーケイン": 5,
  "カタリシス": 6,
};

const rarityOrder:{[key: string]: number } = {
  "S": 1,
  "A": 2,
  "B": 3,
};

items.sort((a, b) => {
  const sinResult = sinOrder[a.sin] - sinOrder[b.sin];
  if (sinResult !== 0) {
    return sinResult;
  }
  const rareResult = rarityOrder[a.rarity] - rarityOrder[b.rarity];
  if (rareResult !== 0){
    return rareResult;
  }
  return a.name.localeCompare(b.name);
});

function customfilter(itemTitle: string, queryText: string, item: any) {
  const jName = hiraganaToKatakana(t(item.raw.name));
  const searchText = hiraganaToKatakana(queryText);
  const englishSeach = queryText.toLowerCase();
  const eName = characters.data[item.raw.ename].ename.toLowerCase();

  return jName.indexOf(searchText) > -1 || eName.indexOf(englishSeach) > -1;
}

function hiraganaToKatakana(src: string) {
  return src.replace(/[\u3041-\u3096]/g, function (match) {
    const chr = match.charCodeAt(0) + 0x60;
    return String.fromCharCode(chr);
  });
}
</script>
