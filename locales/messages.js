import LocaleEnCharacters from './en/en_characters.json';
import LocaleEnMaterials from './en/en_materials.json';
import LocaleEnUI from './en/en_UI.json';
import LocaleJaCharacters from './ja/ja_characters.json';
import LocaleJaMaterials from './ja/ja_materials.json';
import LocaleJaUI from './ja/ja_UI.json';
import LocaleZhCharacters from './zh/zh_characters.json';
import LocaleZhMaterials from './zh/zh_materials.json';
import LocaleZhUI from './zh/zh_UI.json';

export default {
    en:{
        ...LocaleEnCharacters,
        ...LocaleEnMaterials,
        ...LocaleEnUI
    },
    ja:{
        ...LocaleJaCharacters,
        ...LocaleJaMaterials,
        ...LocaleJaUI
    },
    zh:{
        ...LocaleZhCharacters,
        ...LocaleZhMaterials,
        ...LocaleZhUI
    }
}