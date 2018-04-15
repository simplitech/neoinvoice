<template>

    <div class="verti">
        <h1 class="header px-30 py-10 m-0">
            {{ $t("classes.Domain.format.addAsSubdomainOfDomain", { domainName }) }}
        </h1>

        <section class="verti scroll weight-1 items-center-top p-30">

            <form @submit.prevent="persist" class="dark-bg w-full max-w-650 p-20">

                <input-group required
                    type="text"
                    v-model="newPublicKey">
                    {{ $t("classes.Wallet.columns.address") }}
                </input-group>

                <input-group required
                     type="text"
                     maxlength="80"
                     v-model="subdomainName">
                    {{ $t("classes.Wallet.columns.subdomainName") }}
                </input-group>

                <div class="verti items-center">
                    <button type="submit" class="accent">{{ $t("persist.submit") }}</button>
                </div>
            </form> 
        </section>
    </div>

</template>

<script>
  export default {
    name: 'PersistSubdomain',
    data() {
      return {
        domainName: null,
        newPublicKey: null,
        subdomainName: null,
      };
    },
    mounted() {
      this.domainName = this.$route.params.domain;
    },
    methods: {
      persist() {
        this.$resources.addSlaveAsMaster(this.domainName, this.newPublicKey, this.subdomainName)
          .then(() => {
            this.$bus.success(this.$lang.classes.Domain.messages.requestSentWaitAcceptance, 3000);
            this.$router.go(-1);
          });
      },
    },
  };
</script>