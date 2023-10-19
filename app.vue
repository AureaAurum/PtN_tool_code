<template>
  <v-app theme="dark" id="PtNtool" class="bg-grey-darken-4">
    <v-app-bar :elevation="2" color="indigo darken-4">
      <v-app-bar-title>無期迷途 育成素材計算機</v-app-bar-title>
      <v-spacer></v-spacer>
      <ReadMe></ReadMe>
    </v-app-bar>
    <v-main class="text-shades-white ma-5" style="min-width: 500px !important;">
      <v-container fluid class="bg-grey-darken-3">
        <v-row>
          <v-btn width="100px" height="40px" color="#000000" disabled rounded="0" class="my-2 mr-3" text="検索"></v-btn>
          <Searchbar style="position: relative; top:-6px"></Searchbar>
        </v-row>
        <v-row>
          <v-btn width="100px" height="40px" color="#000000" disabled rounded="0" class="my-2 mr-3" text="フィルタ"></v-btn>
          <v-btn class="mx-1 mt-3 bg-indigo" @click="toggleCategory('ディスコイン')"
            :class="{ 'active': isSelected('ディスコイン') }">ディスコイン</v-btn>
          <v-btn class="mx-1 mt-3 bg-indigo" @click="toggleCategory('箱')" :class="{ 'active': isSelected('箱') }">箱</v-btn>
          <v-btn class="mx-1 mt-3 bg-indigo" @click="toggleCategory('モジュール')"
            :class="{ 'active': isSelected('モジュール') }">モジュール</v-btn>
          <v-btn class="mx-1 mt-3 bg-indigo" @click="toggleCategory('原素')"
            :class="{ 'active': isSelected('原素') }">原素</v-btn>
          <v-btn class="mx-1 mt-3 bg-indigo" @click="toggleCategory('コア')"
            :class="{ 'active': isSelected('コア') }">コア</v-btn>
          <v-btn class="mx-1 mt-3 bg-indigo" @click="toggleCategory('内海')"
            :class="{ 'active': isSelected('内海') }">内海</v-btn>
          <v-btn class="mx-1 mt-3 bg-indigo" @click="toggleRequiredMaterials()"
            :class="{ 'active': materialstore.showRequiredMaterials }">不要素材</v-btn>
        </v-row>
        <v-row>
          <v-btn height="40px" width="100px" color="#000000" disabled rounded="0" class="my-2 mr-3" text="オプション"></v-btn>
          <v-tooltip bottom text="素材の所持数や必要数、コンビクトの選択をリセットします" location="bottom">
            <template v-slot:activator="{ props }">
              <VBtn width="100px" height="40px" dark v-bind="props" class="bg-red-darken-2 my-2 mx-1 pa-2"
                @click="reset()" text="reset"></VBtn>
            </template>
          </v-tooltip>
        </v-row>
      </v-container>
      <v-container class="d-flex flex-wrap align-content-start justify-start">
        <Material class="ma-2" style="max-width: 200px;" v-for=" (material, index) in filteredMaterials"
          :class="{ 'left-align': isLastRow(index) }" :mat="material" :prev="prevMaterials(material)"></Material>
      </v-container>
    </v-main>
  </v-app>
</template>
<script lang="ts" setup>
import { useCharacterStore } from '@/store/characters';
import { useMaterialStore } from '@/store/material';
import { useDisplay } from "vuetify";
import type { Character, Characters, ChJsonData, Condition, Material } from '~/types/types';

const display = useDisplay();


const materialstore = useMaterialStore();
if (Object.keys(materialstore.categories).length === 0) {
  await materialstore.init();
}


const characters = useCharacterStore();
const json: ChJsonData = await $fetch('/json/characters.json?url');
const now = new Date(json.createdDate);
let compdate = new Date(characters.refreshdate);
console.log(`storeDate: ${compdate} \n now: ${now}`);
if (compdate < now) {
  await characters.init();
  await materialstore.init()
  console.log("データを更新しました");
}

const prevMaterials = (material: Material) => {
  return materialstore.categories[material.category].slice(materialstore.categories[material.category].indexOf(material) + 1);
};

function requirednum(category: string) {
  for (const mat of materialstore.categories[category]) {
    if (typeof mat.required != 'number') {
      if (typeof mat.required === 'string' && !isNaN(Number(mat.required))) {
        // 文字列で数値として解釈できる場合、数値に変換して返す
        mat.required = Number(mat.required);
      }
    }

  }
}


const calcMaterial = (character: Character) => {
  const { rarity, sin, rankup_material1: rum1, rankup_material2: rum2, skill_material: sm, naikai, condition } = character;
  //console.log(`${[character.name, rarity, sin, rum1, rum2, sm, naikai]}`);
  if (Object.keys(materialstore.categories).length === 0) {
    console.error('empty materials');
    return;
  }
  if (materialstore.categories["ディスコイン"][0].required == "") {
      materialstore.categories["ディスコイン"][0].required = 0;
      requirednum('ディスコイン');
  }
  if (condition.ru1.toString() === "false") {
    switch (rarity) {
      case "S":
        materialstore.categories["ディスコイン"][0].required += 36000;
        materialstore.categories[rum1][1].required += 16;
        materialstore.categories[rum2][1].required += 8;
        materialstore.categories[sin + "原素"][0].required += 18;
        break;
      case "A":
        materialstore.categories["ディスコイン"][0].required += 30000;
        materialstore.categories[rum1][1].required += 12;
        materialstore.categories[rum2][0].required += 18;
        materialstore.categories[sin + "原素"][0].required += 15;
        break;
      case "B":
        materialstore.categories["ディスコイン"][0].required += 24000;
        materialstore.categories[rum1][0].required += 30;
        materialstore.categories[rum2][0].required += 15;
        materialstore.categories[sin + "原素"][0].required += 12;
        break;
      default:
        break;
    }
  }
  if (condition.ru2.toString() === "false") {
    switch (rarity) {
      case "S":
        materialstore.categories["ディスコイン"][0].required += 120000;
        materialstore.categories[rum1][2].required += 16;
        materialstore.categories[rum2][2].required += 8;
        materialstore.categories[sin + "原素"][1].required += 18;
        break;
      case "A":
        materialstore.categories["ディスコイン"][0].required += 100000;
        materialstore.categories[rum1][2].required += 12;
        materialstore.categories[rum2][1].required += 18;
        materialstore.categories[sin + "原素"][1].required += 15;
        break;
      case "B":
        materialstore.categories["ディスコイン"][0].required += 80000;
        materialstore.categories[rum1][1].required += 30;
        materialstore.categories[rum2][1].required += 15;
        materialstore.categories[sin + "原素"][1].required += 12;
        break;
      default:
        break;
    }
  }
  if (condition.ru3.toString() === "false") {
    switch (rarity) {
      case "S":
        materialstore.categories["ディスコイン"][0].required += 560000;
        materialstore.categories[rum1][3].required += 28;
        materialstore.categories[rum2][3].required += 15;
        materialstore.categories[sin + "原素"][2].required += 30;
        break;
      case "A":
        materialstore.categories["ディスコイン"][0].required += 480000;
        materialstore.categories[rum1][3].required += 24;
        materialstore.categories[rum2][2].required += 36;
        materialstore.categories[sin + "原素"][2].required += 25;
        break;
      case "B":
        materialstore.categories["ディスコイン"][0].required += 350000;
        materialstore.categories[rum1][2].required += 54;
        materialstore.categories[rum2][2].required += 30;
        materialstore.categories[sin + "原素"][2].required += 20;

        break;
      default:
        break;
    }
    // 目標のスキルレベル
    const targetSkillLevel = condition.target_slv;
    // 各スキルの素材必要数
    const materialRequiredPerLevel: number[] = rarity == "S" ? [6, 10, 6, 10, 6, 8, 4, 6, 8] : rarity == "A" ? [5, 8, 5, 8, 5, 6, 3, 5, 6] : rarity == "B" ? [4, 6, 4, 6, 4, 5, 2, 4, 5] : [];
    const moduleRequiredPerLevel: number[] = rarity == "S" ? [8, 16, 10, 16, 8, 10, 8, 10, 15] : rarity == "A" ? [6, 12, 8, 12, 6, 8, 6, 8, 12] : rarity == "B" ? [5, 10, 6, 10, 5, 6, 5, 6, 10] : [];
    const naikaiRequiredPerLevel: number[] = rarity == "S" ? [0, 0, 0, 0, 0, 0, 1, 2, 2] : rarity == "A" ? [0, 0, 0, 0, 0, 0, 1, 1, 2] : rarity == "B" ? [0, 0, 0, 0, 0, 0, 1, 1, 1] : [];
    const disCoinRequiredPerLevel: number[] = rarity == "S" ? [4000, 6000, 8500, 12800, 19200, 30000, 86000, 175000, 260000] : rarity == "A" ? [3000, 5000, 7000, 10500, 16000, 25000, 72000, 150000, 210000] : rarity == "B" ? [0, 0, 0, 0, 0, 0, 1, 1, 1] : [];
    const nID: number = naikai == "囁き" ? 0 : naikai == "亡骸" ? 1 : naikai == "狂念" ? 2 : 0;
    // 各スキルごとの必要素材数を計算して合計する
    for (let i = 0; i < condition.slv.length; i++) {
      const currentLevel = condition.slv[i];
      if (currentLevel < targetSkillLevel[i]) {
        for (let j = currentLevel; j < targetSkillLevel[i]; j++) {
          let r = Math.floor((j - 1) / 2);
          if (r > 3) { r = 3; };
          materialstore.categories[sm][r].required += materialRequiredPerLevel[j - 1];
          materialstore.categories['モジュール'][r].required += moduleRequiredPerLevel[j - 1];
          materialstore.categories['内海'][nID].required += naikaiRequiredPerLevel[j - 1];
          materialstore.categories['ディスコイン'][0].required += disCoinRequiredPerLevel[j - 1];
          if (j == 9) {
            materialstore.categories['コア'][0].required += 1;
            requirednum('コア');
          }
          requirednum(sm);
          requirednum('ディスコイン');
          requirednum('モジュール');
          requirednum('内海');
        }
      }
    }




    requirednum(rum1);
    requirednum(rum2);
    requirednum(sm);
    requirednum(sin + "原素");

  }



  for (const mat of materialstore.categories[rum1]) {
    if (typeof mat.required === 'string') {
      // 文字列で数値として解釈できる場合、数値に変換して返す
      mat.required = Number(mat.required);
    }
  }
  for (const mat of materialstore.categories[rum2]) {
    if (typeof mat.required === 'string') {
      // 文字列で数値として解釈できる場合、数値に変換して返す
      mat.required = Number(mat.required);
    }
  }
};


watch(() => [...characters.selected], (after, before) => {
  for (const category of Object.values<Material[]>(materialstore.categories)) {
    for (const material of category) {
      material.required = "";
    }
  }

  //console.log(after);
  for (const select of after) {
    //const ch = characters.data[select];
    const ch = select;
    calcMaterial(ch);
  }


});

async function reset() {
  await materialstore.init();
  for (const c of characters.selected) {
    if (characters.data[c.name]) {
      characters.data[c.name].condition = {
        "level": 1,
        "ru1": "false",
        "ru2": "false",
        "ru3": "false",
        "slv": [1, 1, 1, 1],
        "target_slv": [10, 10, 10, 10]
      };
    }

  }
  characters.selected = [];
}







const toggleCategory = (category: string) => {
  if (category == "原素") {
    const gensos = ["エンデュア原素", "フューリー原素", "アンブラ原素", "レチクル原素", "アーケイン原素", "カタリシス原素"];
    for (const genso of gensos) {
      if (materialstore.selectedCategories.includes(genso)) {
        materialstore.selectedCategories = materialstore.selectedCategories.filter((c: string) => c !== genso);
      } else {
        materialstore.selectedCategories.push(genso);
      }
    }
  }
  if (materialstore.selectedCategories.includes(category)) {
    materialstore.selectedCategories = materialstore.selectedCategories.filter((c: string) => c !== category);
  } else {
    materialstore.selectedCategories.push(category);
  }


  //  console.log(materialstore.selectedCategories);
};

const toggleRequiredMaterials = () => {
  materialstore.showRequiredMaterials = !materialstore.showRequiredMaterials;
};

const filteredMaterials = computed(() => {
  let materials = [];
  const materialList: Material[] = Object.keys(materialstore.categories).flatMap((cat) => {
    return materialstore.categories[cat];
  });
  if (materialstore.selectedCategories.length === 0) {
    materials = materialList; // カテゴリが選択されていない場合、すべての材料を表示
  } else {
    materials = materialList.filter((material: Material) => !materialstore.selectedCategories.includes(material.category));
  }
  if (materialstore.showRequiredMaterials) {
    materials = materials.filter((material: Material) => material.required >= 1 || material.category == "箱");
  }
  return materials;

  //const filterdCategory = Object.fromEntries(
  //  Object.entries(materialstore.categories).filter(([key]) => !materialstore.selectedCategories.includes(key))
  //);
  //const filterd = Object.values(filterdCategory).flat();
  //return filterd;
  //
});
const isSelected = (category: string) => {
  return materialstore.selectedCategories.includes(category);
};

const col = computed(() => {
  if (display.xxl.value) {
    return 10;
  } else if (display.xl.value) {
    return 8;
  } else if (display.lg.value) {
    return 5;
  } else if (display.md.value) {
    return 4;
  } else if (display.sm) {
    return 3;
  } else if (display.xs) {
    return 2;
  } else {
    return 1;
  }
});

const isLastRow = (index: number) => {
  const numRows = Math.ceil(filteredMaterials.value.length / col.value);
  const row = Math.floor(index / col.value);
  return row === numRows - 1;
};



</script>

<style scoped>
.active {
  background-color: black !important;
  /* カテゴリが選択されている場合のボタンの背景色 */
  color: white;
  /* カテゴリが選択されている場合のボタンのテキスト色 */
}

.left-align {
  flex-grow: 1 !important;
}
</style>