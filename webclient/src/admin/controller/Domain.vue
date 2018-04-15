<template>

    <div class="verti">

        <div class="header horiz items-left-center gutter-10 px-30 py-10">
            <div class="score w-60 h-60 text-center line-h-60">{{ domainInfo.score }}</div>
            <h1 class="m-0 weight-1">
                {{ domainName }}
            </h1>
        </div>

        <section class="verti scroll weight-1 p-30">

            <div class="horiz">
                <h2 class="weight-1">{{ $t("classes.Domain.columns.masterWallet") }}</h2>
                <!--<router-link :to="`/transferDomain/${domainName}`" class="btn danger" v-if="domainInfo.masterWallet === myPublicKey">{{ $t("classes.Domain.methods.transferDomain") }}</router-link>-->
            </div>
            <a class="dark-bg horiz p-15 masterWallet" @click="$router.push(`/wallet/${domainInfo.masterWallet}`)">
                <span class="weight-1">{{ domainInfo.masterWallet }}</span>
                <i class="icon icon-arrow-right ml-3"/>
            </a>

            <div class="horiz mt-25">
                <h2 class="weight-1">{{ $t("classes.Domain.columns.meta") }}</h2>
                <router-link :to="`/persistMeta/${this.domainName}`" class="btn" v-if="domainInfo.masterWallet === myPublicKey">{{ $t("classes.Domain.methods.persistMeta") }}</router-link>
            </div>
            <div class="dark-bg" v-if="domainInfo.meta">
                <div class="horiz liMeta p-3" v-for="(value, key) in domainInfo.meta">
                    <span class="w-140 text-right mr-10">{{ key }}</span>
                    <span class="accent">{{ value }}</span>
                </div>
            </div>

            <!--SUBDOMAINS-->

            <!--<div class="horiz mt-25">-->
                <!--<h2 v-if="domainInfo.subdomainWallets && domainInfo.subdomainWallets.length" class="weight-1">{{ $t("classes.Wallet.columns.subdomains") }}</h2>-->
                <!--<router-link :to="`/persistSubdomain/${domainName}`" class="btn" v-if="domainInfo.masterWallet === myPublicKey">{{ $t("classes.Domain.methods.persistSubdomain") }}</router-link>-->
            <!--</div>-->
            <!--<div v-if="domainInfo.subdomainWallets && domainInfo.subdomainWallets.length" class="dark-bg p-0 animated fadeIn">-->
                <!--<div class="horiz p-15 liSubdomain" v-for="item in domainInfo.subdomainWallets">-->
                    <!--<a @click="subdomainToRemove = item" class="icon icon-trash mr-10"></a>-->
                    <!--<a @click="$router.push(`/wallet/${item.wallet}`)" class="horiz weight-1">-->
                        <!--<b class="weight-1 text-right mr-10">{{ item.domain }}</b>-->
                        <!--<span class="weight-4">{{ item.wallet }}</span>-->
                        <!--<i class="icon icon-arrow-right ml-3"/>-->
                    <!--</a>-->
                <!--</div>-->
            <!--</div>-->

            <div class="horiz mt-25">
                <h2 v-if="domainInfo.pendingTransactions && domainInfo.pendingTransactions.length" class="weight-1">{{ $t("classes.PendingTransaction.title") }}</h2>
                <router-link :to="`/persistPendingTransaction/${domainName}`" class="btn" v-if="domainInfo.masterWallet === myPublicKey">{{ $t("classes.PendingTransaction.methods.createPendingTransaction") }}</router-link>
            </div>
            <div v-if="domainInfo.pendingTransactions && domainInfo.pendingTransactions.length" class="dark-bg p-0 animated fadeIn">
                <div class="horiz p-15 liPendingTransaction" v-for="item in domainInfo.pendingTransactions">
                    <!--<a @click="pendingTransactionToRemove = item" class="icon icon-trash mr-10 self-center"></a>-->
                    <a class="horiz weight-1 gutter-10" @click="$router.push(`/payment/${domainName}/${item.id}`)">
                        <div class="w-140 verti" v-for="(value, key) in item">
                            <b class="line-h-30 text-center">{{ key }}</b>
                            <span class="line-h-30 text-center accent">{{ value }}</span>
                        </div>
                    </a>
                </div>
            </div>

            <!--COMPLETE TRANSACTIONS-->

            <!--<h2 v-if="domainInfo.transactions && domainInfo.transactions.length" class="mt-25">{{ $t("classes.Transaction.title") }}</h2>-->
            <!--<div v-if="domainInfo.transactions && domainInfo.transactions.length" class="dark-bg p-0 animated fadeIn">-->
                <!--<a class="horiz p-15 liTransaction" v-for="item in domainInfo.transactions">-->
                    <!--<div class="w-140 verti mr-10">-->
                        <!--<b class="text-right line-h-30">{{ $t('classes.Transaction.columns.from') }}</b>-->
                        <!--<b class="text-right line-h-30">{{ $t('classes.Transaction.columns.to') }}</b>-->
                    <!--</div>-->
                    <!--<div class="weight-1">-->
                        <!--<div class="line-h-30">{{ item.subdomainName }}</div>-->
                        <!--<div class="line-h-30">{{ item.expirationDate | moment($t("dateFormat.datetime")) }}</div>-->
                    <!--</div>-->
                    <!--<div class="w-140 verti">-->
                        <!--<b class="line-h-30 text-center">{{ $t('classes.PendingTransaction.columns.value') }}</b>-->
                        <!--<span class="line-h-30 text-center">{{ calcValue(item.transaction) }} of asset{{ item.transaction.outputs[0].assetId }}</span>-->
                    <!--</div>-->
                    <!--<i class="icon icon-arrow-right ml-3 self-center"/>-->
                <!--</a>-->
            <!--</div>-->

        </section>

        <!--<modal v-if="subdomainToRemove != null">-->
            <!--<div class="verti">-->
                <!--<div class="horiz">-->
                    <!--<h4 class="weight-1 mt-0 mr-10">-->
                        <!--{{ $t("app.confirmRemove") }}-->
                    <!--</h4>-->
                    <!--<a class="close" @click="subdomainToRemove = null"></a>-->
                <!--</div>-->
                <!--<p class="text-center">{{ subdomainToRemove.domain }}<br/>{{ subdomainToRemove.wallet }}</p>-->
                <!--<div class="horiz items-center">-->
                    <!--<button type="button" @click="subdomainToRemove = null">{{ $t("app.cancel") }}</button>-->
                    <!--<button type="button" class="danger ml-10" @click="removeSubdomain()">{{ $t("app.remove") }}</button>-->
                <!--</div>-->
            <!--</div>-->
        <!--</modal>-->

        <!--<modal v-if="pendingTransactionToRemove != null">-->
            <!--<div class="verti">-->
                <!--<div class="horiz">-->
                    <!--<h4 class="weight-1 mt-0 mr-10">-->
                        <!--{{ $t("app.confirmRemove") }}-->
                    <!--</h4>-->
                    <!--<a class="close" @click="pendingTransactionToRemove = null"></a>-->
                <!--</div>-->
                <!--<p class="text-center">{{ pendingTransactionToRemove.idPendingTransaction }}</p>-->
                <!--<div class="horiz items-center">-->
                    <!--<button type="button" @click="pendingTransactionToRemove = null">{{ $t("app.cancel") }}</button>-->
                    <!--<button type="button" class="danger ml-10" @click="removePendingTransaction()">{{ $t("app.remove") }}</button>-->
                <!--</div>-->
            <!--</div>-->
        <!--</modal>-->

    </div>
</template>

<script>
  import WalletStore from '../service/WalletStore';

  export default {
    name: 'Wallet',
    data() {
      return {
        myPublicKey: null,
        domainName: null,
        subdomainToRemove: null,
        pendingTransactionToRemove: null,
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
      this.populate();
    },
    methods: {
      async populate() {
        this.domainInfo = await this.$resources.readDomain(this.domainName);
      },
      calcValue(transaction) {
        const scriptHash = WalletStore.wallet ? WalletStore.wallet.scriptHash : null;
        return transaction.outputs
          .filter(o => o.scriptHash === scriptHash)
          .reduce((sum, o) => sum + o.value, 0);
      },
      async removeSubdomain() {
        const resp = await this.$resources
          .removeSlaveAsMaster(this.domainName, this.subdomainToRemove.wallet);
        if (resp) {
          this.domainInfo.subdomainWallets
            .splice(this.domainInfo.subdomainWallets.indexOf(this.subdomainToRemove), 1);
          this.subdomainToRemove = null;
        }
      },
      async removePendingTransaction() {
        const resp = await this.$resources.removePendingTransaction(
          this.domainName,
          this.pendingTransactionToRemove.idPendingTransaction);
        if (resp) {
          this.domainInfo.pendingTransactions
            .splice(this.domainInfo.pendingTransactions.indexOf(this.pendingTransactionToRemove), 1);
          this.pendingTransactionToRemove = null;
        }
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

    .masterWallet {
        font-size: 18px;
        text-decoration: none;

        &:hover {
            background: $navyhighlight;
        }
    }

    .liMeta {
        font-size: 18px;
    }

    .liSubdomain {
        font-size: 16px;
        border-bottom: 1px solid $navy;

        a {
            text-decoration: none;
        }
    }

    .liPendingTransaction {
        font-size: 16px;
        border-bottom: 1px solid $navy;

        a {
            text-decoration: none;
        }
    }
</style>