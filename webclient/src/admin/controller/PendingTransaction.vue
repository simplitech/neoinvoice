<template>

    <div class="verti">

        <div class="header horiz items-left-center gutter-10 px-30 py-10">
            <div class="score w-60 h-60 text-center line-h-60">{{ pendingTransaction.score }}</div>
            <h1 class="m-0 weight-1">
                {{ $t('classes.Domain.methods.paymentForDomain', { domainName }) }}
            </h1>
        </div>

        <section class="verti scroll weight-1 p-30" v-if="pendingTransaction.publicKey && pendingTransaction.publicKey.length">

            <h2>{{ $t("classes.Wallet.title") }}</h2>
            <a class="dark-bg horiz p-15 wallet" @click="$router.push(`/wallet/${pendingTransaction.publicKey}`)">
                <span class="weight-1">{{ pendingTransaction.publicKey }}</span>
                <i class="icon icon-arrow-right ml-3"/>
            </a>

            <h2 class="mt-25">{{ $t("classes.Domain.columns.meta") }}</h2>
            <div class="dark-bg">
                <div class="horiz liMeta p-3" v-for="(value, key) in pendingTransaction.attributes">
                    <b class="w-140 text-right mr-10">{{ key }}</b>
                    <span class="accent">{{ value }}</span>
                </div>
            </div>

            <h2>{{ $t("classes.Domain.title") }}</h2>
            <div class="dark-bg" v-if="domainInfo.meta">
                <div class="horiz liMeta p-3" v-for="(value, key) in domainInfo.meta">
                    <span class="w-140 text-right mr-10">{{ key }}</span>
                    <span class="accent">{{ value }}</span>
                </div>
            </div>

            <h2 class="mt-25">{{ $t("app.paymentInfo") }}</h2>
            <div class="dark-bg horiz p-15 pendingTransaction">
                <b class="w-140 text-right mr-10">{{ $t('classes.PendingTransaction.columns.value') }}</b>
                <span class="accent">{{ pendingTransaction.price }} GAS</span>
            </div>

            <clip-loader v-if="loading" color="#185c67"></clip-loader>
            <button v-if="!loading && !pendingTransaction.executed" @click="complete">
                {{ $t('classes.PendingTransaction.methods.pay') }}
            </button>
            <h1 class="text-center accent mt-10" v-if="pendingTransaction.executed">{{ $t('classes.PendingTransaction.columns.paid') }}</h1>

        </section>

        <div v-else class="text-center">
            {{ $t('classes.PendingTransaction.columns.notFound') }}
        </div>

    </div>
</template>

<script>
  import ClipLoader from 'vue-spinner/src/ClipLoader.vue';
  import WalletStore from '../service/WalletStore';

  export default {
    name: 'PendingTransaction',
    components: { ClipLoader },
    data() {
      return {
        loading: false,
        myPublicKey: null,
        domainName: null,
        idPendingTransaction: null,
        pendingTransaction: {
          publicKey: null,
          executed: false,
          attributes: {},
          price: null,
        },
        domainInfo: {
          score: null,
          masterWallet: null,
          subdomainWallets: [],
          meta: null,
          pendingTransactions: [],
          transactions: [],
        },
      };
    },
    mounted() {
      this.myPublicKey = WalletStore.wallet ? WalletStore.wallet.publicKey : null;
      this.domainName = this.$route.params.domain;
      this.idPendingTransaction = this.$route.params.idPendingTransaction;
      this.populate();
    },
    methods: {
      async populate() {
        this.pendingTransaction = await this.$resources
          .readPendingTransaction(this.domainName, this.idPendingTransaction);
        this.domainInfo = await this.$resources.readDomain(this.domainName);
      },

      async complete() {
        this.loading = true;
        await this.$resources.completePendingTransaction(
          this.domainName,
          this.pendingTransaction.price,
          this.idPendingTransaction);
        this.loading = false;
        this.$bus.success(this.$lang.app.persistedSuccessfully, 3000);
        this.$router.go(-1);
      },
    },
  };
</script>

<style lang="scss" scoped>
    @import '../scss/colors.scss';

    .score {
        background: $navyhighlight;
        border-radius: 50%;
        font-size: 36px;
    }

    .wallet {
        font-size: 18px;
        text-decoration: none;

        &:hover {
            background: $navyhighlight;
        }
    }

    .liMeta {
        font-size: 18px;
    }

    .pendingTransaction {
        font-size: 16px;

        a {
            text-decoration: none;
        }
    }
</style>