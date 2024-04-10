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
      const json: ChJsonData = await $fetch('/json/characters.json?url');
      data.value = json.Characters;
      refreshdate.value = new Date(json.createdDate);

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
