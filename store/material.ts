import { ref, computed } from 'vue';
import { defineStore } from 'pinia';


export const useMaterialStore = defineStore(
  'MaterialStore',
  () => {
    const categories:Ref<any> = ref({})
    const selectedCategories = ref<string[]>([]);
    const showRequiredMaterials = ref(false);





    async function init() {
        //const { data: json } = await useFetch('https://aureaaurum.github.io/PtN_JsonAPI/material/');
        //categories.value = JSON.parse(json.value as string);
        categories.value = await $fetch('/json/material.json?url');
        console.log("materials init");

      }

    return { categories,selectedCategories,showRequiredMaterials, init };
  },
  {
    persist: {
      storage:persistedState.localStorage
    }
  }
);
