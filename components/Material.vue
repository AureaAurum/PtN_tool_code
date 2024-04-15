<template>
    <v-card elevation="8" :style="color"
        class="d-flex justify-space-around align-center materialCard">
        <div class="matImages">
            <v-img :src="'/img/materials/' + mat.id + '.png'" aspect-ratio="1" height="60px" width="60px"></v-img>
            <div :style="name" class="name">{{ $t(mat.name) }}</div>
        </div>
        <div style="width: 60px;">
            <v-text-field bg-color="grey-darken-4" hide-details type="number" density="compact" :placeholder="$t('$need')"
                v-model.number="mat.required"></v-text-field>
            <v-text-field bg-color="grey-darken-4" hide-details type="number" density="compact" :placeholder="$t('$owned')"
                v-model.number="mat.owned"></v-text-field>
            <v-text-field bg-color="grey-darken-4" hide-details density="compact" disabled placeholder=""
                v-model="shortage"></v-text-field>
        </div>

    </v-card>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useMaterialStore } from '@/store/material';
import type { Categories, Material } from '@/types/types'
const { locale,t } = useI18n();

const materialstore = useMaterialStore();

const props = defineProps<{
  mat: Material, // 素材情報をプロップスとして受け取る
  prev: Material[],
  hideEnoughMaterials: Boolean,
}>()

const color = computed(() => {
  const rarity = props.mat.rarity;
  let bcolor;
  switch (rarity) {
    case '1':
      bcolor = "white";
      break;
    case '2':
      bcolor = "green";
      break;
    case '3':
      bcolor = "blue";
      break;
    case '4':
      bcolor = "purple";
      break;
    default:
      bcolor = "yellow";
  }
  const enough = props.mat.short <= 0 ? true : false;
  const req = Number(props.mat.required) > 0;
  let opacity = 1;
  if (enough && req && props.mat.category != "箱" && props.hideEnoughMaterials) {
    opacity = 0.1;
  }
  var fsize = props.mat.name == "ディスコイン" ? "12px" : "14px";

  return { '--bcolor': bcolor, '--opacity': opacity, '--fsize': fsize };
});

const name = computed(() => {
  const length = t(props.mat.name).length;
  const maxlength = locale.value == "en" ? 15 : 9;
  var namefont = length > maxlength ? "9px" : "12px";
  var wrap = length > maxlength ? "wrap" : "nowrap";
  return { '--namefont': namefont, '--wrap': wrap};
});

const shortage = computed(() => {
  const previousmaterials = props.prev;
  const owned = typeof props.mat.owned == "number" ? props.mat.owned : 0;
  const required = Number(props.mat.required);
  props.mat.totalRequired = required;
  let shortage = 0;
  if (props.prev.length > 0) {
    const prevMaterial = previousmaterials[0];
    const prevShortage = typeof prevMaterial.short == "number" ? prevMaterial.short : 0;
    if (prevShortage > 0 && typeof prevMaterial.short == "number" && prevMaterial.category != "内海") {
      const conversionRate = 3;
      const convertedShortage = prevShortage * conversionRate;

      props.mat.totalRequired += convertedShortage;
    }
  }
  shortage += props.mat.totalRequired - owned; // 不足分を計算
  props.mat.short = shortage;
  return shortage;
});
</script>

<style>
.materialCard input {
    font-size: var(--fsize) !important;
    padding-inline-end: 0px !important;
    padding-inline-start: 0px !important;
    text-align: center !important;
}

.materialCard {
    max-height:fit-content;
    width:200px;
    min-width: 200px;
    border-color: var(--bcolor) !important;
    border: solid 0.5px;
    opacity: var(--opacity) !important;
}
.matImages{
    width: 100px;
    display: flex;
    flex-wrap: wrap;
    font-size: 12px;
    justify-content: center;
    text-wrap: nowrap;
    text-align: center;
}
.name {
    margin-top: 10px;
    min-width: 60px;
    font-size: var(--namefont) !important;
    text-wrap: var(--wrap) !important;
  }

</style>