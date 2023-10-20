import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import type { Character, Characters, ChJsonData, Condition, Material, Categories } from '~/types/types';


export const useMaterialStore = defineStore(
  'MaterialStore',
  () => {
    const categories:Ref<Categories> = ref({})
    const selectedCategories = ref<string[]>([]);
    const showRequiredMaterials = ref(false);
    const hideEnoughMaterials = ref(false);





    async function init() {
        //const { data: json } = await useFetch('https://aureaaurum.github.io/PtN_JsonAPI/material/');
        //categories.value = JSON.parse(json.value as string);
        var  jsondata:Categories = await $fetch('/json/material.json?url');
        Object.assign(jsondata, categories.value)
        categories.value = jsondata
        console.log("materials init");

      }

    return { categories,selectedCategories,showRequiredMaterials,hideEnoughMaterials, init };
  },
  {
    persist: {
      storage:persistedState.localStorage
    }
  }
);
