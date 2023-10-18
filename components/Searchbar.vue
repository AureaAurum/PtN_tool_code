<template>
  <VAutocomplete base-color="grey-darken-1" color="grey-darken-3" item-color="white" hide-details
    hide-no-data clearable flat closable-chips multiple placeholder="コンビクト名で検索" :items="items" item-title="name"
    return-object v-model="characters.selected" :custom-filter="customfilter" variant="underlined">
    <template v-slot:chip="{ item, index, props }">
      <CharacterDetail :item="item"></CharacterDetail>
    </template>
    <template v-slot:item="{ item, props }">
      <v-list-item v-bind="props" class="my-0 py-0" bg-color="grey-darken-">
        <template v-slot:prepend>
          <v-avatar style="width: 70px; height: 50px; border-radius: 20%;" tile class="my-0">
            <template v-slot:default>
              <v-img cover :src='"/img/characters/" + characters.data[item.title].ename + ".png"'
                :alt="characters.data[item.title].ename"></v-img>
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

const characters = useCharacterStore();
const items = Object.values(characters.data);


function customfilter(itemTitle: string, queryText: string, item: any) {
  const jName = hiraganaToKatakana(item.title);
  const searchText = hiraganaToKatakana(queryText);
  const englishSeach = queryText.toLowerCase();
  const eName = characters.data[item.title].ename.toLowerCase();

  return jName.indexOf(searchText) > -1 || eName.indexOf(englishSeach) > -1;
}

function hiraganaToKatakana(src: string) {
  return src.replace(/[\u3041-\u3096]/g, function (match) {
    const chr = match.charCodeAt(0) + 0x60;
    return String.fromCharCode(chr);
  });
}
</script>
