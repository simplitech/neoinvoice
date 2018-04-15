<template>

    <div class="verti w-window h-window items-center">
        <h1 class="accent">neoinvoice</h1>
        <form @submit.prevent="login" class="verti w-300 dark-bg p-30">
            <h2 class="mt-0">{{ $t("login.subtitle") }}</h2>
            <input v-model="passphrase" class="mb-10" type="password" :placeholder="$t('login.passphrase')" required autofocus/>
            <input v-model="encryptedKey" class="mb-10" type="password" :placeholder="$t('login.encryptedKey')" required>
            <button class="accent" type="submit">
                <clip-loader v-if="loading" color="#185c67"></clip-loader>
                <template v-if="!loading">{{ $t("login.signin") }}</template>
            </button>
        </form>
    </div>

</template>

<script>
  import ClipLoader from 'vue-spinner/src/ClipLoader.vue';
  import WalletStore from '../service/WalletStore';

  export default {
    name: 'Login',
    components: { ClipLoader },
    data() {
      return {
        passphrase: null,
        encryptedKey: null,
        loading: false,
      };
    },
    mounted() {
      if (WalletStore.wallet) {
        this.$router.push('/home');
      }
    },
    methods: {
      login() {
        this.loading = true;
        setTimeout(() => {
          this.$resources.login(this.passphrase, this.encryptedKey).then(() => {
            this.loading = false;
            if (WalletStore.beforeLoginIntention) {
              const href = WalletStore.beforeLoginIntention;
              WalletStore.beforeLoginIntention = null;
              location.href = href;
            } else {
              this.$router.push('/home');
            }
          }).catch((e) => {
            this.loading = false;
            this.$bus.error(e.message, 3000);
          });
        }, 100);
      },
    },
  };
</script>