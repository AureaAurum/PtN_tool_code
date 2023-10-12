<template>
    <v-dialog width="80%" max-width="500px" min-width="400px">
        <template v-slot:activator="{ props }">
            <v-chip v-bind="props" @click:close="remove(p.item.raw)" :text="p.item.title" label
                class="bg-indigo-darken-3"></v-chip>
        </template>
        <template v-slot:default="{ isActive }">
            <v-card>
                <v-card-title style="font-size: 24px;" class="pb-0">
                    <v-avatar style="width: 70px; height: 50px; border-radius: 25%;" tile class="my-0">
                        <template v-slot:default>
                            <v-img cover :src='"/img/characters/" + p.item.raw.ename + ".png"'
                                :alt="p.item.raw.ename"></v-img>
                        </template>
                    </v-avatar>
                    {{ p.item.title }}
                </v-card-title>
                <v-card-text class="pa-0">
                    <v-container class="pa-o">
                        <v-row>
                            <v-col>
                                <div>
                                    <span style="font-size: 8px;">RU済みならチェックしてください</span>
                                    <v-checkbox color="indigo-lighten-1" v-model="p.item.raw.condition.ru1"
                                        @input="reCalc(p.item.raw)">
                                        <template v-slot:label>
                                            <div style="font-size: 1em;">
                                                ランクアップ1
                                            </div>
                                        </template>
                                    </v-checkbox>
                                    <v-checkbox color="indigo-lighten-1" v-model="p.item.raw.condition.ru2"
                                        @input="reCalc(p.item.raw)"
                                        :disabled="!(p.item.raw.condition.ru1.toString() === 'true')">
                                        <template v-slot:label>
                                            <div style="font-size: 1em;">
                                                ランクアップ2
                                            </div>
                                        </template>
                                    </v-checkbox>
                                    <v-checkbox color="indigo-lighten-1" v-model="p.item.raw.condition.ru3"
                                        @input="reCalc(p.item.raw)"
                                        :disabled="!(p.item.raw.condition.ru2.toString() === 'true' && p.item.raw.condition.ru1.toString() === 'true')">
                                        <template v-slot:label>
                                            <div style="font-size: 1em;">
                                                ランクアップ3
                                            </div>
                                        </template>
                                    </v-checkbox>
                                </div>
                            </v-col>
                            <v-col>
                                <div style="position: relative; top: -18px">
                                    <span style="font-size: 13px; position: relative; top:20px; z-index: 10;">通常攻撃</span>
                                    <div class="d-flex flex-frow ma-0 pa-0">
                                        <v-select class="py-0"  hide-details hide-no-data
                                            :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" v-model="p.item.raw.condition.slv[0]"
                                            @update:modelValue="reCalc(p.item.raw)" label="" bg-color="grey-darken-4"
                                            variant="underlined"></v-select>
                                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="48" height="48"
                                            viewBox="-4 -12 32 32">
                                            <path :d="mdiArrowRight" stroke="white" fill="white"></path>
                                        </svg>
                                        <v-select hide-details hide-no-data :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
                                            v-model="p.item.raw.condition.target_slv[0]"
                                            @update:modelValue="reCalc(p.item.raw)" label="" bg-color="grey-darken-4"
                                            variant="underlined"></v-select>
                                    </div>
                                </div>
                                <div style="position: relative; top: -18px">
                                    <span style="font-size: 13px; position: relative; top:20px; z-index: 10;">必殺</span>
                                    <div class="d-flex flex-frow ma-0 pa-0">
                                        <v-select class="py-0"  hide-details hide-no-data
                                            :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" v-model="p.item.raw.condition.slv[1]"
                                            @update:modelValue="reCalc(p.item.raw)" label="" bg-color="grey-darken-4"
                                            variant="underlined"></v-select>
                                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="48" height="48"
                                            viewBox="-4 -12 32 32">
                                            <path :d="mdiArrowRight" stroke="white" fill="white"></path>
                                        </svg>
                                        <v-select hide-details hide-no-data :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
                                            v-model="p.item.raw.condition.target_slv[1]"
                                            @update:modelValue="reCalc(p.item.raw)" label="" bg-color="grey-darken-4"
                                            variant="underlined"></v-select>
                                    </div>
                                </div>
                                <div style="position: relative; top: -18px">
                                    <span style="font-size: 13px; position: relative; top:20px; z-index: 10;">パッシブ1</span>
                                    <div class="d-flex flex-frow ma-0 pa-0">
                                        <v-select class="py-0"  hide-details hide-no-data
                                            :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" v-model="p.item.raw.condition.slv[2]"
                                            @update:modelValue="reCalc(p.item.raw)" label="" bg-color="grey-darken-4"
                                            variant="underlined"></v-select>
                                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="48" height="48"
                                            viewBox="-4 -12 32 32">
                                            <path :d="mdiArrowRight" stroke="white" fill="white"></path>
                                        </svg>
                                        <v-select hide-details hide-no-data :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
                                            v-model="p.item.raw.condition.target_slv[2]"
                                            @update:modelValue="reCalc(p.item.raw)" label="" bg-color="grey-darken-4"
                                            variant="underlined"></v-select>
                                    </div>
                                </div>
                                <div style="position: relative; top: -18px">
                                    <span style="font-size: 13px; position: relative; top:20px; z-index: 10;">パッシブ2</span>
                                    <div class="d-flex flex-frow ma-0 pa-0">
                                        <v-select class="py-0"  hide-details hide-no-data
                                            :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" v-model="p.item.raw.condition.slv[3]"
                                            @update:modelValue="reCalc(p.item.raw)" label="" bg-color="grey-darken-4"
                                            variant="underlined"></v-select>
                                        <svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="48" height="48"
                                            viewBox="-4 -12 32 32">
                                            <path :d="mdiArrowRight" stroke="white" fill="white"></path>
                                        </svg>
                                        <v-select hide-details hide-no-data :items="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
                                            v-model="p.item.raw.condition.target_slv[3]"
                                            @update:modelValue="reCalc(p.item.raw)" label="" bg-color="grey-darken-4"
                                            variant="underlined"></v-select>
                                    </div>
                                </div>
                            </v-col>
                        </v-row>
                       <!-- <div>{{ characters.data[item.title] }}</div> -->
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn @click="isActive.value = false">閉じる</v-btn>
                </v-card-actions>
            </v-card>
        </template>
    </v-dialog>
</template>

<script setup lang="ts">
const p = defineProps<{ item: any; }>();

import { useCharacterStore } from '@/store/characters';
import { mdiArrowRight } from '@mdi/js';
const characters = useCharacterStore();

function remove(item: Character) {
    characters.data[item.name].condition = {
        "level": 1,
        "ru1": "false",
        "ru2": "false",
        "ru3": "false",
        "slv": [1, 1, 1, 1],
        "target_slv": [10, 10, 10, 10]
    };
    const index = characters.selected.indexOf(item);
    if (index >= 0) characters.selected.splice(index, 1);
}

function reCalc(item: Character) {
    const index = characters.selected.indexOf(item);
    if (index >= 0) characters.selected.splice(index, 1);
    characters.selected.push(item);
    characters.data[item.name] = item;
    console.log(item);
}
</script>

