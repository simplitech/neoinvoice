<template>

    <div class="verti">
        <h1 class="header px-30 py-10 m-0">
            {{ $t("classes.PendingTransaction.methods.createPendingTransactionForWalletOnDomain", { publicKey: myPublicKey, domainName }) }}
        </h1>

        <section class="verti scroll weight-1 items-center-top p-30">

            <form @submit.prevent="persist" class="verti dark-bg w-full max-w-650 p-20">

                <div class="horiz">
                    <input-group required
                                 type="text"
                                 v-model="amount"
                                 class="weight-1 mr-10">
                        {{ $t("classes.PendingTransaction.columns.amount") }}
                    </input-group>

                    <select-group required
                                  v-model="assetID">
                        <span slot="label">{{ $t("classes.PendingTransaction.columns.assetID") }}</span>
                        <option v-for="item in possibleAssets" :value="item.id">
                            {{ item.name }}
                        </option>
                    </select-group>
                </div>

                <h2>Other Attributes of the transaction</h2>
                <div class="horiz" v-for="item in transactionAttributesAsArray">
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
                <button class="self-right" type="button" @click="transactionAttributesAsArray.push({ key: null, meta: null })">{{ $t("app.addOneMoreLine") }}</button>

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
  import WalletStore from '../service/WalletStore';

  export default {
    name: 'PersistPendingTransaction',
    components: { ClipLoader },
    data() {
      return {
        loading: false,
        myPublicKey: null,
        domainName: null,
        amount: null,
        assetID: '602c79718b16e442de58778e148d0b1084e3b2dffd5de6b7b16cee7969282de7',
        transactionAttributesAsArray: [{ key: null, meta: null }],
        possibleAssets: [
          { name: 'GAS', id: '602c79718b16e442de58778e148d0b1084e3b2dffd5de6b7b16cee7969282de7' },
        ],
      };
    },
    mounted() {
      this.myPublicKey = WalletStore.wallet ? WalletStore.wallet.publicKey : null;
      this.domainName = this.$route.params.domain;
    },
    methods: {
      persist() {
        const transactionAttributes = this.transactionAttributesAsArray.filter(item => item.key)
          .reduce((whole, item) => ({ ...whole, [item.key]: item.value }), {});

        this.loading = true;
        this.$resources.createPendingTransaction(
          this.domainName,
          this.amount,
          this.assetID,
          transactionAttributes)
          .then(() => {
            this.loading = false;
            this.$bus.success(this.$lang.app.persistedSuccessfully, 3000);
            this.$router.go(-1);
          });
      },
    },
  };
</script>