import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import type { Character, Characters, ChJsonData, Condition, Material } from '~/types/types';

export const useCharacterStore = defineStore(
  'CharacterStore',
  () => {
    //保持したいデータ
    //const data: Ref<any> = ref([]);
    const data: Ref<Characters> = ref({});
    const selected: Ref<Character[]> = ref([]);
    const refreshdate: Ref<Date> = ref(new Date(1000));

    async function init() {
      //const { data: json } = await useFetch('https://aureaaurum.github.io/PtN_JsonAPI/characters/');
      //const characters = JSON.parse(json.value as string);
      const json: ChJsonData = await $fetch('/json/characters.json?url');
      var temp: Character[] = [];
      if (selected.value) {
        temp = selected.value;
      }

      data.value = json.Characters;
      refreshdate.value = new Date(json.createdDate);
      if (temp.length > 0) {
        for (const c of temp) {
          if (!data.value[c.ename]) {
            console.log(`translated ${c.ename}`);
            var translated = Object.values(data.value).find((element) => element.ename == c.ename);
            console.log(translated);
            if (translated) {
              data.value[translated.ename].condition = c.condition;
              const index = selected.value.indexOf(c);
              if (index >= 0) selected.value[index] = data.value[translated.ename];
            }
          } else {
            data.value[c.ename].condition = c.condition;
          }
          //console.dir(data.value[c.ename],{depth:null})
        }
      }
      console.log('characters init');
    }
    return { data, selected, refreshdate, init };
  },
  {
    persist: {
      storage: persistedState.localStorage,
    },
  }
);