<template>

    <div class="verti">
        <h1 class="header px-30 py-10 m-0">
            {{ $t("classes.Domain.format.editMetadataOfDomain", { domainName }) }}
        </h1>

        <section class="verti scroll weight-1 items-center-top p-30">

            <form @submit.prevent="persist" class="verti dark-bg w-full max-w-650 p-20">

                <div class="horiz" v-for="item in metaAsArray">
                    <input-group required
                        type="text"
                        v-model="item.key"
                        class="weight-1 mr-10">
                        {{ $t("classes.MetaKeyValue.columns.key") }}
                    </input-group>
                    <input-group required
                         type="text"
                         v-model="item.value"
                         class="weight-1">
                        {{ $t("classes.MetaKeyValue.columns.value") }}
                    </input-group>
                </div>
                <button class="self-right" type="button" @click="metaAsArray.push({ key: null, meta: null })">{{ $t("app.addOneMoreLine") }}</button>
            

                <hr class="mb-20"/>
                <div class="verti items-center">
                    <button type="submit" class="accent">
                        <clip-loader v-if="loading" color="#185c67"></clip-loader>
                        <template v-if="!loading">{{ $t("persist.submit") }}</template>
                    </button>
                </div>
            </form> 
        </section>
    </div>

</template>

<script>
  import ClipLoader from 'vue-spinner/src/ClipLoader.vue';

  export default {
    name: 'PersistMeta',
    components: { ClipLoader },
    data() {
      return {
        loading: false,
        domainName: null,
        metaAsArray: [],
      };
    },
    mounted() {
      this.domainName = this.$route.params.domain;
      this.populate();
    },
    methods: {
      async populate() {
        const info = await this.$resources.readDomain(this.domainName);

        this.metaAsArray = info.meta ? Object.keys(info.meta)
          .map(key => ({ key, value: info.meta[key] })) : [];
      },
      persist() {
        const meta = this.metaAsArray.filter(item => item.key)
          .reduce((whole, item) => ({ ...whole, [item.key]: item.value }), {});

        this.loading = true;
        this.$resources.saveMeta(this.domainName, meta).then(() => {
          this.loading = false;
          this.$bus.success(this.$lang.app.persistedSuccessfully, 3000);
          this.$router.go(-1);
        });
      },
    },
  };
</script>