<template>

    <div class="verti">

        <div class="header horiz items-left-center gutter-10 px-30 py-10">
            <h1 class="m-0">
                {{ $t("classes.Wallet.title") }} <div class="discrete">{{ walletPublicKey }}</div>
            </h1>
        </div>

        <section class="verti scroll weight-1 p-30">

            <div class="horiz">
                <h2 v-if="domains && domains.length" class="weight-1">{{ $t("classes.Wallet.columns.domains") }}</h2>
                <router-link to="/persistDomain" class="btn" v-if="walletPublicKey === myPublicKey">{{ $t("classes.Domain.methods.registerDomain") }}</router-link>
            </div>
            <div v-if="domains && domains.length" class="dark-bg p-0 animated fadeIn">
                <a class="horiz p-15 liDomain" v-for="item in domains" @click="$router.push(`/domain/${item}`)">
                    <span class="weight-1">{{ item }}</span>
                    <i class="icon icon-arrow-right ml-3"/>
                </a>
            </div>

            <!--<div class="horiz mt-25">-->
                <!--<h2 v-if="subdomains && subdomains.length" class="weight-1">{{ $t("classes.Wallet.columns.subdomains") }}</h2>-->
                <!--<router-link to="/requestSubdomain" class="btn" v-if="walletPublicKey === myPublicKey">{{ $t("classes.Domain.methods.registerSubdomain") }}</router-link>-->
            <!--</div>-->
            <!--<div v-if="subdomains && subdomains.length" class="dark-bg p-0 animated fadeIn">-->
                <!--<a class="horiz p-15 liDomain" v-for="item in subdomains" @click="$router.push(`/domain/${item}`)">-->
                    <!--<span class="weight-1">{{ item }}</span>-->
                    <!--<i class="icon icon-arrow-right ml-3"/>-->
                <!--</a>-->
            <!--</div>-->

        </section>

    </div>
</template>

<script>
  import WalletStore from '../service/WalletStore';

  export default {
    name: 'Wallet',
    data() {
      return {
        myPublicKey: null,
        walletPublicKey: null,
        domains: [],
        subdomains: [],
      };
    },
    mounted() {
      this.myPublicKey = WalletStore.wallet ? WalletStore.wallet.publicKey : null;
      this.walletPublicKey = this.$route.params.wallet || this.myPublicKey;
      this.populateLists();
    },
    methods: {
      async populateLists() {
        const resp = await this.$resources.listDomains(this.walletPublicKey);
        this.domains = resp.domains;
        this.subdomains = resp.subdomains;
      },
    },
  };
</script>

<style lang="scss" scoped>
    @import '../scss/colors.scss';

    .liDomain {
        text-decoration: none;
        border-bottom: 1px solid $navy;

        &:hover {
            background: $navyhighlight;
        }
    }
</style>