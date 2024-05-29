<template>
  <v-app theme="dark" id="PtNtool" class="bg-grey-darken-4">
    <v-app-bar :elevation="2" color="indigo darken-4">
      <v-app-bar-title>無期迷途 育成素材計算機</v-app-bar-title>
      <v-tabs v-model="tab">
        <v-tab value="Main">Main</v-tab>
        <v-tab value="CList">List</v-tab>
      </v-tabs>
      <v-spacer></v-spacer>
      <i18n></i18n>
      <ReadMe></ReadMe>
    </v-app-bar>
    <v-main class="text-shades-white ma-5" style="min-width: 500px !important">
      <v-window v-model="tab">
        <v-window-item value="Main" transition="scroll-x">
          <v-container fluid class="bg-grey-darken-3">
            <v-row>
              <v-btn
                width="100px"
                height="40px"
                color="#000000"
                disabled
                rounded="0"
                class="my-2 mr-3"
                :text="$t('$search')"
              ></v-btn>
              <Searchbar style="position: relative; top: -6px"></Searchbar>
            </v-row>
            <v-row>
              <v-btn
                width="100px"
                height="40px"
                color="#000000"
                disabled
                rounded="0"
                class="my-2 mr-3"
                :text="$t('$filter')"
              ></v-btn>
              <v-btn
                class="mx-1 mt-3 bg-indigo"
                @click="toggleCategory('ディスコイン')"
                :class="{ active: isSelected('ディスコイン') }"
                >{{ $t('ディスコイン') }}</v-btn
              >
              <v-btn
                class="mx-1 mt-3 bg-indigo"
                @click="toggleCategory('ルナティックエッセンス')"
                :class="{ active: isSelected('ルナティックエッセンス') }"
                >{{ $t('エッセンス') }}</v-btn
              >
              <v-btn class="mx-1 mt-3 bg-indigo" @click="toggleCategory('箱')" :class="{ active: isSelected('箱') }">{{
                $t('箱')
              }}</v-btn>
              <v-btn
                class="mx-1 mt-3 bg-indigo"
                @click="toggleCategory('モジュール')"
                :class="{ active: isSelected('モジュール') }"
                >{{ $t('モジュール') }}</v-btn
              >
              <v-btn
                class="mx-1 mt-3 bg-indigo"
                @click="toggleCategory('原素')"
                :class="{ active: isSelected('原素') }"
                >{{ $t('原素') }}</v-btn
              >
              <v-btn
                class="mx-1 mt-3 bg-indigo"
                @click="toggleCategory('コア')"
                :class="{ active: isSelected('コア') }"
                >{{ $t('コア') }}</v-btn
              >
              <v-btn
                class="mx-1 mt-3 bg-indigo"
                @click="toggleCategory('内海')"
                :class="{ active: isSelected('内海') }"
                >{{ $t('内海') }}</v-btn
              >
              <v-btn
                class="mx-1 mt-3 bg-indigo"
                @click="toggleRequiredMaterials()"
                :class="{ active: materialstore.showRequiredMaterials }"
                >{{ $t('不要素材') }}</v-btn
              >
            </v-row>
            <v-row>
              <v-btn
                height="40px"
                width="100px"
                color="#000000"
                disabled
                rounded="0"
                class="my-2 mr-3"
                :text="$t('$options')"
              ></v-btn>
              <v-tooltip bottom :text="$t('$resetOwnedDesc')" location="bottom">
                <template v-slot:activator="{ props }">
                  <VBtn
                    width="140px"
                    height="40px"
                    dark
                    v-bind="props"
                    class="bg-red-darken-2 my-2 mx-1 pa-2"
                    @click="ownreset()"
                    :text="$t('$resetOwned')"
                  ></VBtn>
                </template>
              </v-tooltip>
              <v-tooltip bottom :text="$t('$resetNeededDesc')" location="bottom">
                <template v-slot:activator="{ props }">
                  <VBtn
                    width="140px"
                    height="40px"
                    dark
                    v-bind="props"
                    class="bg-red-darken-2 my-2 mx-1 pa-2"
                    @click="needreset()"
                    :text="$t('$resetNeeded')"
                  ></VBtn>
                </template>
              </v-tooltip>
              <v-switch
                color="indigo-accent-2"
                v-model="materialstore.hideEnoughMaterials"
                hide-details
                class="my-0 mx-5 pa-0"
                :label="$t('$enoughMaterials')"
              ></v-switch>
            </v-row>
          </v-container>
          <v-container class="d-flex flex-wrap align-content-start justify-start">
            <Material
              class="ma-2"
              style="max-width: 200px"
              v-for="(material, index) in filteredMaterials"
              :class="{ 'left-align': isLastRow(index) }"
              :mat="material"
              :prev="prevMaterials(material)"
              :hideEnoughMaterials="materialstore.hideEnoughMaterials"
            ></Material>
          </v-container>
        </v-window-item>
        <v-window-item value="CList" reverse-transition="scroll-x">
          <v-container>
            <CharacterList></CharacterList>
          </v-container>
        </v-window-item>
      </v-window>
    </v-main>
  </v-app>
</template>
<script lang="ts" setup>
import { useCharacterStore } from '@/store/characters';
import { useMaterialStore } from '@/store/material';
import { useDisplay } from 'vuetify';
import type { Character, Characters, ChJsonData, Condition, Material } from '~/types/types';
const { setLocale } = useI18n();
const display = useDisplay();
const materialstore = useMaterialStore();
var tab: any = ref(null);
const CookieLocale = useCookie('i18n_redirected');
if (CookieLocale.value) setLocale(CookieLocale.value);

if (Object.keys(materialstore.categories).length === 0) {
  await materialstore.init();
}
const prevMaterials = (material: Material) => {
  return materialstore.categories[material.category].slice(
    materialstore.categories[material.category].indexOf(material) + 1
  );
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
  const {
    rarity,
    sin,
    rankup_material1: rum1,
    rankup_material2: rum2,
    skill_material: sm,
    naikai,
  } = characters.data[character.ename];
  const { condition } = character;

  const exp_S = [
    0, 600, 750, 900, 1050, 1250, 1450, 1650, 1850, 2100, 2350, 2650, 2950, 3250, 3600, 3950, 4350, 4750, 5150, 5600,
    6550, 6850, 7200, 7550, 7900, 8300, 8650, 9000, 9400, 9750, 10150, 10550, 10950, 11400, 11800, 12250, 12700, 13150,
    13650, 14100, 14350, 14600, 14850, 15100, 15350, 15650, 15950, 16250, 16550, 16850, 17200, 17550, 17900, 18250,
    18600, 19000, 19400, 19800, 20200, 20600, 21050, 21500, 21950, 22400, 22850, 23350, 23850, 24350, 24850, 25350,
    26600, 28500, 31150, 34450, 38450, 43200, 48600, 54750, 61550, 69050, 77300, 86200, 95850, 106150, 117150, 128900,
    141300, 154450, 168250, 182750];

  const money_S = [
    0, 200, 250, 300, 350, 450, 550, 650, 750, 850, 1000, 1150, 1300, 1450, 1600, 1800, 2000, 2200, 2400, 2600, 2850,
    3050, 3300, 3550, 3800, 4050, 4300, 4600, 4850, 5150, 5400, 5700, 6000, 6300, 6600, 6900, 7200, 7500, 7850, 8150,
    8150, 8200, 8200, 8250, 8250, 8300, 8350, 8400, 8450, 8500, 8550, 8600, 8700, 8750, 8850, 8900, 9000, 9100, 9200,
    9300, 9400, 9550, 9650, 9800, 9900, 10050, 10200, 10350, 10500, 10650, 11050, 11800, 12800, 14050, 15600, 17450,
    19550, 21950, 24650, 27600, 30850, 34400, 38250, 42400, 46850, 51600, 56650, 62000, 67700, 73650];

  const exp_A = [
    0, 500, 600, 750, 850, 1000, 1200, 1350, 1500, 1750, 1950, 2200, 2450, 2700, 3000, 3250, 3600, 3950, 4250, 4650,
    5450, 5700, 6000, 6250, 6550, 6900, 7200, 7500, 7800, 8100, 8450, 8750, 9100, 9500, 9800, 10200, 10550, 10950,
    11350, 11750, 11950, 12150, 12350, 12550, 12750, 13000, 13250, 13500, 13750, 14000, 14300, 14600, 14900, 15200,
    15500, 15800, 16150, 16500, 16800, 17150, 17500, 17900, 18250, 18650, 19000, 19450, 19850, 20250, 20700, 21100,
    22150, 23750, 25950, 28700, 32000, 36000, 40500, 45600, 51250, 57500, 64400, 71800, 79850, 88450, 97600, 107400,
    117750, 128700, 140200, 152250];

  const money_A = [
    0, 150, 200, 250, 250, 350, 450, 500, 600, 700, 800, 950, 1050, 1200, 1300, 1500, 1650, 1800, 2000, 2150, 2350,
    2500, 2750, 2950, 3150, 3350, 3550, 3800, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750,
    6750, 6800, 6800, 6850, 6900, 6950, 6950, 7000, 7000, 7050, 7100, 7150, 7250, 7250, 7350, 7400, 7500, 7550, 7650,
    7750, 7800, 7950, 8000, 8150, 8250, 8350, 8500, 8600, 8750, 8850, 9200, 9800, 10650, 11700, 13000, 14500, 16250,
    18250, 20500, 23000, 25700, 28650, 31850, 35300, 39000, 43000, 47200, 51650, 56400, 61350];

  const exp_B = [
    0, 400, 500, 600, 700, 800, 950, 1100, 1200, 1400, 1550, 1750, 1950, 2150, 2400, 2600, 2900, 3150, 3400, 3700, 4350,
    4550, 4800, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000, 7300, 7600, 7850, 8150, 8450, 8750, 9100, 9400,
    9550, 9700, 9900, 10050, 10200, 10400, 10600, 10800, 11000, 11200, 11450, 11700, 11900, 12150, 12400, 12650, 12900,
    13200, 13450, 13700, 14000, 14300, 14600, 14900, 15200, 15550, 15900, 16200, 16550, 16900, 17700, 19000, 20750,
    22950, 25600, 28800, 32400, 36500, 41000, 46000, 51500, 57450, 63900, 70750, 78100, 85900, 94200, 102950, 112150,
    121800];

  const money_B = [
    0, 100, 150, 200, 200, 300, 350, 400, 500, 550, 650, 750, 850, 950, 1050, 1200, 1300, 1450, 1600, 1700, 1900, 2000,
    2200, 2350, 2500, 2700, 2850, 3050, 3200, 3400, 3600, 3800, 4000, 4200, 4400, 4600, 4800, 5000, 5200, 5400, 5400,
    5450, 5450, 5500, 5500, 5500, 5550, 5600, 5600, 5650, 5700, 5700, 5800, 5800, 5900, 5900, 6000, 6050, 6100, 6200,
    6250, 6350, 6400, 6500, 6600, 6700, 6800, 6900, 7000, 7100, 7350, 7850, 8500, 9350, 10400, 11600, 13000, 14600,
    16400, 18400, 20550, 22900, 25500, 28250, 31200, 34400, 37750, 41300, 45100, 49100];

  //console.log(`${[character.name, rarity, sin, rum1, rum2, sm, naikai]}`);
  if (Object.keys(materialstore.categories).length === 0) {
    console.error('empty materials');
    return;
  }
  if (materialstore.categories['ディスコイン'][0].required == '') {
    materialstore.categories['ディスコイン'][0].required = 0;
    requirednum('ディスコイン');
  }
  if (materialstore.categories['ルナティックエッセンス'][0].required == '') {
    materialstore.categories['ルナティックエッセンス'][0].required = 0;
    requirednum('ルナティックエッセンス');
  }

  if (condition.level > 0 && condition.target_level <= 90 && condition.level < condition.target_level) {
    switch (rarity) {
      case 'S':
        for (let i = condition.level; i < condition.target_level; i++) {
          materialstore.categories['ルナティックエッセンス'][0].required += exp_S[i];
          materialstore.categories['ディスコイン'][0].required += money_S[i];
        }
        break;
      case 'A':
        for (let i = condition.level; i < condition.target_level; i++) {
          materialstore.categories['ルナティックエッセンス'][0].required += exp_A[i];
          materialstore.categories['ディスコイン'][0].required += money_A[i];
        }
        break;
      case 'B':
        for (let i = condition.level; i < condition.target_level; i++) {
          materialstore.categories['ルナティックエッセンス'][0].required += exp_B[i];
          materialstore.categories['ディスコイン'][0].required += money_B[i];
        }
        break;
    }
  }


  if (condition.ru1.toString() === 'false') {
    switch (rarity) {
      case 'S':
        materialstore.categories['ディスコイン'][0].required += 36000;
        materialstore.categories[rum1][1].required += 16;
        materialstore.categories[rum2][1].required += 8;
        materialstore.categories[sin + '原素'][0].required += 18;
        break;
      case 'A':
        materialstore.categories['ディスコイン'][0].required += 30000;
        materialstore.categories[rum1][1].required += 12;
        materialstore.categories[rum2][0].required += 18;
        materialstore.categories[sin + '原素'][0].required += 15;
        break;
      case 'B':
        materialstore.categories['ディスコイン'][0].required += 24000;
        materialstore.categories[rum1][0].required += 30;
        materialstore.categories[rum2][0].required += 15;
        materialstore.categories[sin + '原素'][0].required += 12;
        break;
      default:
        break;
    }
  }
  if (condition.ru2.toString() === 'false') {
    switch (rarity) {
      case 'S':
        materialstore.categories['ディスコイン'][0].required += 120000;
        materialstore.categories[rum1][2].required += 16;
        materialstore.categories[rum2][2].required += 8;
        materialstore.categories[sin + '原素'][1].required += 18;
        break;
      case 'A':
        materialstore.categories['ディスコイン'][0].required += 100000;
        materialstore.categories[rum1][2].required += 12;
        materialstore.categories[rum2][1].required += 18;
        materialstore.categories[sin + '原素'][1].required += 15;
        break;
      case 'B':
        materialstore.categories['ディスコイン'][0].required += 80000;
        materialstore.categories[rum1][1].required += 30;
        materialstore.categories[rum2][1].required += 15;
        materialstore.categories[sin + '原素'][1].required += 12;
        break;
      default:
        break;
    }
  }
  if (condition.ru3.toString() === 'false') {
    switch (rarity) {
      case 'S':
        materialstore.categories['ディスコイン'][0].required += 560000;
        materialstore.categories[rum1][3].required += 28;
        materialstore.categories[rum2][3].required += 15;
        materialstore.categories[sin + '原素'][2].required += 30;
        break;
      case 'A':
        materialstore.categories['ディスコイン'][0].required += 480000;
        materialstore.categories[rum1][3].required += 24;
        materialstore.categories[rum2][2].required += 36;
        materialstore.categories[sin + '原素'][2].required += 25;
        break;
      case 'B':
        materialstore.categories['ディスコイン'][0].required += 350000;
        materialstore.categories[rum1][2].required += 54;
        materialstore.categories[rum2][2].required += 30;
        materialstore.categories[sin + '原素'][2].required += 20;

        break;
      default:
        break;
    }
  }

  requirednum(rum1);
  requirednum(rum2);
  requirednum(sm);
  requirednum(sin + '原素');
  // 目標のスキルレベル
  const targetSkillLevel = condition.target_slv;
  // 各スキルの素材必要数
  const materialRequiredPerLevel: number[] =
    rarity == 'S'
      ? [6, 10, 6, 10, 6, 8, 4, 6, 8]
      : rarity == 'A'
      ? [5, 8, 5, 8, 5, 6, 3, 5, 6]
      : rarity == 'B'
      ? [4, 6, 4, 6, 4, 5, 2, 4, 5]
      : [];
  const moduleRequiredPerLevel: number[] =
    rarity == 'S'
      ? [8, 16, 10, 16, 8, 10, 8, 10, 15]
      : rarity == 'A'
      ? [6, 12, 8, 12, 6, 8, 6, 8, 12]
      : rarity == 'B'
      ? [5, 10, 6, 10, 5, 6, 5, 6, 10]
      : [];
  const naikaiRequiredPerLevel: number[] =
    rarity == 'S'
      ? [0, 0, 0, 0, 0, 0, 1, 2, 2]
      : rarity == 'A'
      ? [0, 0, 0, 0, 0, 0, 1, 1, 2]
      : rarity == 'B'
      ? [0, 0, 0, 0, 0, 0, 1, 1, 1]
      : [];
  const disCoinRequiredPerLevel: number[] =
    rarity == 'S'
      ? [4000, 6000, 8500, 12800, 19200, 30000, 86000, 175000, 260000]
      : rarity == 'A'
      ? [3000, 5000, 7000, 10500, 16000, 25000, 72000, 150000, 210000]
      : rarity == 'B'
      ? [0, 0, 0, 0, 0, 0, 1, 1, 1]
      : [];
  const nID: number = naikai == '囁き' ? 0 : naikai == '亡骸' ? 1 : naikai == '狂念' ? 2 : -1;
  // 各スキルごとの必要素材数を計算して合計する
  for (let i = 0; i < condition.slv.length; i++) {
    const currentLevel = condition.slv[i];
    if (currentLevel < targetSkillLevel[i]) {
      for (let j = currentLevel; j < targetSkillLevel[i]; j++) {
        let r = Math.floor((j - 1) / 2);
        if (r > 3) {
          r = 3;
        }
        materialstore.categories[sm][r].required += materialRequiredPerLevel[j - 1];
        materialstore.categories['モジュール'][r].required += moduleRequiredPerLevel[j - 1];
        materialstore.categories['ディスコイン'][0].required += disCoinRequiredPerLevel[j - 1];
        if (!(nID < 0)) {
          materialstore.categories['内海'][nID].required += naikaiRequiredPerLevel[j - 1];
        }

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

const characters = useCharacterStore();
const json: ChJsonData = await $fetch('/json/characters.json?url');
const now = new Date(json.createdDate);
let compdate = new Date(characters.refreshdate);
console.log(`storeDate: ${compdate} \n now: ${now}`);
if (compdate < now) {
  await characters.init();
  await materialstore.init();

  var temp: Character[] = [];
  if (characters.selected) {
    temp = characters.selected;
  }

  if (temp.length > 0) {
    for (const category of Object.values<Material[]>(materialstore.categories)) {
      for (const material of category) {
        material.required = '';
      }
    }

    for (const c of temp) {
      characters.data[c.ename].condition = c.condition;
      const index = characters.selected.indexOf(c);
      if (index >= 0) characters.selected[index] = characters.data[c.ename];
      calcMaterial(c);
    }
  }

  console.log('データを更新しました');
}

watch(
  () => [...characters.selected],
  (after, before) => {
    for (const category of Object.values<Material[]>(materialstore.categories)) {
      for (const material of category) {
        material.required = '';
      }
    }
    if (after.length < before.length) {
      const diff = before.filter((i) => after.indexOf(i) == -1);
      for (const d of diff) {
        characters.data[d.ename].condition = {
          level: 1,
          target_level:90,
          ru1: 'false',
          ru2: 'false',
          ru3: 'false',
          slv: [1, 1, 1, 1],
          target_slv: [10, 10, 10, 10],
        };
      }
    }

    //console.log(after);
    for (const select of after) {
      //const ch = characters.data[select];
      const ch = select;
      calcMaterial(ch);
    }
  }
);

async function ownreset() {
  await materialstore.init();
  for (const category of Object.values<Material[]>(materialstore.categories)) {
    for (const material of category) {
      material.owned = '';
    }
  }
}
async function needreset() {
  characters.selected = [];
}

const toggleCategory = (category: string) => {
  if (category == '原素') {
    const gensos = [
      'エンデュア原素',
      'フューリー原素',
      'アンブラ原素',
      'レチクル原素',
      'アーケイン原素',
      'カタリシス原素',
    ];
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
    materials = materialList.filter(
      (material: Material) => !materialstore.selectedCategories.includes(material.category)
    );
  }
  if (materialstore.showRequiredMaterials) {
    materials = materials.filter((material: Material) => Number(material.required) >= 1 || material.category == '箱');
  }
  return materials;
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

<style>
body {
  background-color: #212121 !important;
}
</style>

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
