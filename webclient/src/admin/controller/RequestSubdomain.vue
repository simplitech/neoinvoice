<template>

    <div class="verti">
        <h1 class="header px-30 py-10 m-0">
            {{ $t("classes.Domain.format.requestToJoinDomainAsWalletAddress", { newPublicKey: myPublicKey }) }}
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
                    <button type="submit" class="accent">{{ $t("persist.submit") }}</button>
                </div>
            </form> 
        </section>
    </div>

</template>

<script>
  import WalletStore from '../service/WalletStore';

  export default {
    name: 'RequestSubdomain',
    data() {
      return {
        myPublicKey: null,
        domain: null,
      };
    },
    mounted() {
      this.myPublicKey = WalletStore.wallet.publicKey;
    },
    methods: {
      persist() {
        this.$resources.addDomainAsSubaccount(this.domain).then(() => {
          this.$bus.success(this.$lang.classes.Domain.messages.requestSentWaitApproval, 3000);
          this.$router.go(-1);
        });
      },
    },
  };
</script>