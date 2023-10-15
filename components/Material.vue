<template>
    <v-card elevation="8" :style="color"
        class="d-flex justify-space-around align-center materialCard">
        <div class="matImages">
            <v-img :src="'/img/materials/' + mat.id + '.png'" aspect-ratio="1" height="60px" width="60px"></v-img>
            <div :style="name" class="name">{{ mat.name }}</div>
        </div>
        <div style="width: 60px;">
            <v-text-field bg-color="grey-darken-4" hide-details type="number" density="compact" placeholder="必要"
                v-model.number="mat.required"></v-text-field>
            <v-text-field bg-color="grey-darken-4" hide-details type="number" density="compact" placeholder="所持"
                v-model.number="mat.owned"></v-text-field>
            <v-text-field bg-color="grey-darken-4" hide-details density="compact" disabled placeholder="不足"
                v-model="shortage"></v-text-field>
        </div>

    </v-card>
</template>

<script>

export default {
    props: {
        mat: Object, // 素材情報をプロップスとして受け取る
        prev: Array
    },
    computed: {
        color() {
            const rarity = this.mat.rarity;
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
            const enough = this.mat.short <= 0 ? true:false
            const req = this.mat.required > 0
            let opacity = 1
            if (enough && req && this.mat.category != "箱") {
                opacity = 0.1
            }

            return { '--bcolor': bcolor, '--opacity':opacity };
        },
        name(){
            const length = this.mat.name.length
            let namefont;
            if (length > 9) {
                namefont = "8px"
            } else {
                namefont = "12px"
            }

            return{ '--namefont':namefont }

        },
        shortage() {
            const previousmaterials = this.prev;
            const owned = this.mat.owned;
            const required = Number(this.mat.required);
            this.mat.totalRequired = required;
            let shortage = 0;
            if (this.prev.length > 0) {
                const prevMaterial = previousmaterials[0];
                const prevShortage = typeof prevMaterial.short == "number" ? prevMaterial.short : 0;
                if (prevShortage > 0 && typeof prevMaterial.short == "number" && prevMaterial.category != "内海") {
                    const conversionRate = 3; // iを使用して正しい指数を計算
                    const convertedShortage = prevShortage * conversionRate;

                    this.mat.totalRequired += convertedShortage;
                }
            }


            shortage += this.mat.totalRequired - owned; // 不足分を計算
            this.mat.short = shortage;
            return shortage;
        }
    },
};
</script>

<style>
input {
    font-size: 14px;
    padding-inline-end: 0px !important;
    padding-inline-start: 0px;
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
}

</style>