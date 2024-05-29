<template>
    <v-dialog width="80%" max-width="500px" min-width="400px">
        <template v-slot:activator="{ props }">
            <v-chip v-bind="props" @click:close="remove(p.item.raw)" :text="$t(p.item.raw.name)" label class="bg-indigo-darken-3"></v-chip>
        </template>
        <template v-slot:default="{ isActive }">
            <v-card>
                <v-card-title style="font-size: 24px;" class="pb-0 d-flex">
                    <v-avatar style="width: 70px; height: 50px; border-radius: 25%;" tile class="my-0">
                        <template v-slot:default>
                            <v-img cover :src='"/img/characters/" + p.item.raw.ename + ".png"' :alt="p.item.raw.ename"></v-img>
                        </template>
                    </v-avatar>
                    <div class="my-2 mx-4 me-auto">{{ $t(p.item.raw.name) }}</div>
                    <div class="d-flex my-2">
                        <v-tooltip bottom :text="`${ $t(p.item.raw.sin) }`" location="bottom">
                            <template v-slot:activator="{ props }">
                                <v-img v-bind="props" :src="'/img/materials/' + materialstore.categories[p.item.raw.sin + '原素'][2].id + '.png'" aspect-ratio="1" height="30px" width="30px"></v-img>
                            </template>
                        </v-tooltip>
                        <v-tooltip bottom :text="`${$t('$tableHeaderRUM1')}:${ $t(p.item.raw.rankup_material1) }`" location="bottom">
                            <template v-slot:activator="{ props }">
                                <v-img v-bind="props" :src="'/img/materials/' + materialstore.categories[p.item.raw.rankup_material1][3].id + '.png'" aspect-ratio="1" height="30px" width="30px"></v-img>
                            </template>
                        </v-tooltip>
                        <v-tooltip bottom :text="`${$t('$tableHeaderRUM2')}:${ $t(p.item.raw.rankup_material2) }`" location="bottom">
                            <template v-slot:activator="{ props }">
                                <v-img v-bind="props" :src="'/img/materials/' + materialstore.categories[p.item.raw.rankup_material2][3].id + '.png'" aspect-ratio="1" height="30px" width="30px"></v-img>
                            </template>
                        </v-tooltip>
                        <v-tooltip bottom :text="`${$t('$tableHeaderSUM')}:${ $t(p.item.raw.skill_material) }`" location="bottom">
                            <template v-slot:activator="{ props }">
                                <v-img v-bind="props" :src="'/img/materials/' + materialstore.categories[p.item.raw.skill_material][3].id + '.png'" aspect-ratio="1" height="30px" width="30px"></v-img>
                            </template>
                        </v-tooltip>
                        <v-tooltip bottom :text="`${$t('$tableHeaderNaikai')}:${ $t(p.item.raw.naikai) }`" location="bottom">
                            <template v-slot:activator="{ props }" v-if="show">
                                <v-img v-bind="props" :src="'/img/materials/' + materialstore.categories['内海'][nID].id + '.png'" aspect-ratio="1" height="30px" width="30px"></v-img>
                            </template>
                        </v-tooltip>
                    </div>
                </v-card-title>
                <v-card-text class="pa-0">
                    <v-container class="pa-o">
                        <v-row>
                            <v-col>
                                <div style="position: relative; top: -18px">
                                    <span style="font-size: 13px; position: relative; top:20px; z-index: 10;">{{ $t('$Level') }}</span>
                                    <div class="d-flex flex-frow ma-0 pa-0">
                                        <v-text-field type="number" class="py-0" hide-details hide-no-data v-model="p.item.raw.condition.level"
                                            @update:modelValue="reCalc(p.item.raw)" label="" bg-color="grey-darken-4" variant="underlined"></v-text-field>
                                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="-4 -12 32 32">
                                            <path :d="mdiArrowRight" stroke="white" fill="white"></path>
                                        </svg>
                                        <v-text-field type="number" hide-details hide-no-data v-model="p.item.raw.condition.target_level" @update:modelValue="reCalc(p.item.raw)"
                                            label="" bg-color="grey-darken-4" variant="underlined"></v-text-field>
                                    </div>
                                </div>
                                <div>
                                    <span style="font-size: 10px;">{{$t('$checkoff')}}</span>
                                    <v-checkbox color="indigo-lighten-1" v-model="p.item.raw.condition.ru1" @input="reCalc(p.item.raw)" :disabled="(p.item.raw.condition.ru2.toString() === 'true')">
                                        <template v-slot:label>
                                            <div style="font-size: 1em;">{{$t('$phase')}} 1</div>
                                        </template>
                                    </v-checkbox>
                                    <v-checkbox color="indigo-lighten-1" v-model="p.item.raw.condition.ru2" @input="reCalc(p.item.raw)"
                                        :disabled="!(p.item.raw.condition.ru1.toString() === 'true') || (p.item.raw.condition.ru3.toString() === 'true')">
                                        <template v-slot:label>
                                            <div style="font-size: 1em;">{{$t('$phase')}} 2</div>
                                        </template>
                                    </v-checkbox>
                                    <v-checkbox color="indigo-lighten-1" v-model="p.item.raw.condition.ru3" @input="reCalc(p.item.raw)"
                                        :disabled="!(p.item.raw.condition.ru2.toString() === 'true' && p.item.raw.condition.ru1.toString() === 'true')">
                                        <template v-slot:label>
                                            <div style="font-size: 1em;">{{$t('$phase')}} 3</div>
                                        </template>
                                    </v-checkbox>
                                </div>
                            </v-col>
                            <v-col>
                                <div style="position: relative; top: -18px">
                                    <span style="font-size: 13px; position: relative; top:20px; z-index: 10;">{{ $t('$normalAttack') }}</span>
                                    <div class="d-flex flex-frow ma-0 pa-0">
                                        <v-select class="py-0" hide-details hide-no-data :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" v-model="p.item.raw.condition.slv[0]"
                                            @update:modelValue="reCalc(p.item.raw)" label="" bg-color="grey-darken-4" variant="underlined"></v-select>
                                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="-4 -12 32 32">
                                            <path :d="mdiArrowRight" stroke="white" fill="white"></path>
                                        </svg>
                                        <v-select hide-details hide-no-data :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" v-model="p.item.raw.condition.target_slv[0]" @update:modelValue="reCalc(p.item.raw)"
                                            label="" bg-color="grey-darken-4" variant="underlined"></v-select>
                                    </div>
                                </div>
                                <div style="position: relative; top: -18px">
                                    <span style="font-size: 13px; position: relative; top:20px; z-index: 10;">{{ $t('$ultimate') }}</span>
                                    <div class="d-flex flex-frow ma-0 pa-0">
                                        <v-select class="py-0" hide-details hide-no-data :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" v-model="p.item.raw.condition.slv[1]"
                                            @update:modelValue="reCalc(p.item.raw)" label="" bg-color="grey-darken-4" variant="underlined"></v-select>
                                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="-4 -12 32 32">
                                            <path :d="mdiArrowRight" stroke="white" fill="white"></path>
                                        </svg>
                                        <v-select hide-details hide-no-data :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" v-model="p.item.raw.condition.target_slv[1]" @update:modelValue="reCalc(p.item.raw)"
                                            label="" bg-color="grey-darken-4" variant="underlined"></v-select>
                                    </div>
                                </div>
                                <div style="position: relative; top: -18px">
                                    <span style="font-size: 13px; position: relative; top:20px; z-index: 10;">{{ $t('$passive') }}1</span>
                                    <div class="d-flex flex-frow ma-0 pa-0">
                                        <v-select class="py-0" hide-details hide-no-data :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" v-model="p.item.raw.condition.slv[2]"
                                            @update:modelValue="reCalc(p.item.raw)" label="" bg-color="grey-darken-4" variant="underlined"></v-select>
                                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="-4 -12 32 32">
                                            <path :d="mdiArrowRight" stroke="white" fill="white"></path>
                                        </svg>
                                        <v-select hide-details hide-no-data :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" v-model="p.item.raw.condition.target_slv[2]" @update:modelValue="reCalc(p.item.raw)"
                                            label="" bg-color="grey-darken-4" variant="underlined"></v-select>
                                    </div>
                                </div>
                                <div style="position: relative; top: -18px">
                                    <span style="font-size: 13px; position: relative; top:20px; z-index: 10;">{{ $t('$passive') }}2</span>
                                    <div class="d-flex flex-frow ma-0 pa-0">
                                        <v-select class="py-0" hide-details hide-no-data :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" v-model="p.item.raw.condition.slv[3]"
                                            @update:modelValue="reCalc(p.item.raw)" label="" bg-color="grey-darken-4" variant="underlined"></v-select>
                                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="-4 -12 32 32">
                                            <path :d="mdiArrowRight" stroke="white" fill="white"></path>
                                        </svg>
                                        <v-select hide-details hide-no-data :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" v-model="p.item.raw.condition.target_slv[3]" @update:modelValue="reCalc(p.item.raw)"
                                            label="" bg-color="grey-darken-4" variant="underlined"></v-select>
                                    </div>
                                </div>
                            </v-col>
                        </v-row>
                        <!-- <div>{{ characters.data[item.title] }}</div> -->
                        <!--
                            <div class="ma-0 pa-0">
                            <span>ランク素材1: {{ p.item.raw.rankup_material1 }}　</span>
                            <span>ランク素材2: {{ p.item.raw.rankup_material2 }}　</span>
                            <span>スキル素材: {{ p.item.raw.skill_material }}　</span>
                        </div>
-->
                    </v-container>
                </v-card-text>
                <v-card-actions class="ma-0">
                    <v-spacer></v-spacer>
                    <v-btn @click="isActive.value = false">閉じる</v-btn>
                </v-card-actions>
            </v-card>
        </template>
    </v-dialog>
</template>

<script setup lang="ts">
const p = defineProps<{ item: any; }>();
const nID: number = p.item.raw.naikai == "囁き" ? 0 : p.item.raw.naikai == "亡骸" ? 1 : p.item.raw.naikai == "狂念" ? 2 : -1;
const show = nID >= 0 ? true : false;
import type { Character, Characters, ChJsonData, Condition, Material } from '~/types/types';
import { useMaterialStore } from '@/store/material';
import { useCharacterStore } from '@/store/characters';
import { mdiArrowRight } from '@mdi/js';
const characters = useCharacterStore();
const materialstore = useMaterialStore();

function remove(item: Character) {
    const index = characters.selected.indexOf(item);
    if (index >= 0) characters.selected.splice(index, 1);
}

function reCalc(item: Character) {
    const index = characters.selected.indexOf(item);
    if (index >= 0) characters.selected.splice(index, 1);
    characters.selected.push(item);
    console.log(item);
}


//watch(p.item.raw, (v)=>{
//    if (p.item.raw.condition.level < 21) {
//        p.item.raw.condition.ru1 = false;
//    }
//    if (p.item.raw.condition.level >= 21) {
//        p.item.raw.condition.ru1 = true;
//    }
//    if (p.item.raw.condition.level < 41) {
//        p.item.raw.condition.ru2 = false;
//    }
//    if (p.item.raw.condition.level >= 41) {
//        p.item.raw.condition.ru2 = true;
//    }
//    if (p.item.raw.condition.level < 71) {
//        p.item.raw.condition.ru3 = false;
//    }
//    if (p.item.raw.condition.level >= 71) {
//        p.item.raw.condition.ru3 = true;
//    }
//    reCalc(p.item.raw);
//})

</script>

