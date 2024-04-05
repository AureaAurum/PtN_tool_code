<template>
    <v-menu>
      <template v-slot:activator="{ props }">
        <v-btn v-bind="props">
          {{ $i18n.locale }}
        </v-btn>
      </template>
      <v-list @click:select="selected" :items="languages" item-title=title item-value=value> </v-list>
    </v-menu>
</template>

  <script setup lang="ts">
  const { locale, setLocale } = useI18n();
  const languages = [
    { title: 'En', value: 'en' },
    { title: 'Ja', value: 'ja' },
    { title: 'Zh', value: 'zh' },
  ];
  const selected = (lang: any) => {
    setLocale(lang.id);
  };
</script>
