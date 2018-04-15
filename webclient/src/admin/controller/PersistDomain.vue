<template>

    <div class="verti">
        <h1 class="header px-30 py-10 m-0">
            {{ $t("classes.Domain.format.newDomainForWalletAddress", { publicKey: myPublicKey }) }}
        </h1>

        <section class="verti scroll weight-1 items-center-top p-30">

            <form @submit.prevent="persist" class="dark-bg w-full max-w-650 p-20">

                <input-group required
                    type="text" 
                    maxlength="80"
                    v-model="domain">
                    {{ $t("classes.Domain.columns.domain") }}
                </input-group>

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
  import WalletStore from '../service/WalletStore';

  export default {
    name: 'PersistDomain',
    components: { ClipLoader },
    data() {
      return {
        loading: false,
        myPublicKey: null,
        domain: null,
      };
    },
    mounted() {
      this.myPublicKey = WalletStore.wallet ? WalletStore.wallet.publicKey : null;
    },
    methods: {
      persist() {
        this.loading = true;
        this.$resources.registerDomain(this.domain).then(() => {
          this.loading = false;
          this.$bus.success(this.$lang.app.persistedSuccessfully, 3000);
          this.$router.go(-1);
        });
      },
    },
  };
</script>