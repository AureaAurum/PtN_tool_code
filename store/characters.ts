import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const useCharacterStore = defineStore(
  'CharacterStore',
  () => {
    //保持したいデータ
    //const data: Ref<any> = ref([]);
    const data:Ref<Characters> =  ref({})
    const selected: Ref<Character[]> = ref([]);
    const refreshdate:Ref<Date> =ref(new Date(1000))

    async function init() {
      //const { data: json } = await useFetch('https://aureaaurum.github.io/PtN_JsonAPI/characters/');
      //const characters = JSON.parse(json.value as string);
      const json:ChJsonData = await $fetch('/json/characters.json?url');
      var temp:Character[] = []
      if (selected.value) {
        temp = selected.value
      }

      data.value = json.Characters
      refreshdate.value = new Date(json.createdDate)
      if (temp.length > 0) {
        for (const c of temp) {
          data.value[c.name].condition = c.condition;
          //console.dir(data.value[c.name],{depth:null})
        }
      }
      console.log("characters init");

    }
    return { data, selected,refreshdate, init };
  },
  {
    persist: {
      storage:persistedState.localStorage
    }
  }
);
