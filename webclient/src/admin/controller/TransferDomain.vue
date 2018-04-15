<template>

    <div class="verti">
        <h1 class="header px-30 py-10 m-0">
            {{ $t("classes.Domain.format.transferDomain", { domainName }) }}
        </h1>

        <section class="verti scroll weight-1 items-center-top p-30">

            <form @submit.prevent="modalOpen = true" class="dark-bg w-full max-w-650 p-20">

                <input-group required
                    type="text"
                    v-model="newPublicKey">
                    {{ $t("classes.Domain.columns.masterWalletPublicKey") }}
                </input-group>

                <div class="verti items-center">
                    <button type="submit" class="danger">{{ $t("persist.submit") }}</button>
                </div>
            </form> 
        </section>

        <modal v-if="modalOpen">
            <div class="verti">
                <div class="horiz">
                    <h4 class="weight-1 mt-0 mr-10">
                        {{ $t("classes.Domain.messages.areYouSureYouWantToTransferDomain") }}
                    </h4>
                    <a class="close" @click="modalOpen = false"></a>
                </div>
                <p class="text-center">{{ domainName }}</p>
                <div class="horiz items-center">
                    <button type="button" @click="modalOpen = false">{{ $t("app.cancel") }}</button>
                    <button type="button" class="danger ml-10" @click="persist()">{{ $t("app.transfer") }}</button>
                </div>
            </div>
        </modal>
    </div>

</template>

<script>
  export default {
    name: 'TransferDomain',
    data() {
      return {
        newPublicKey: null,
        domainName: null,
        modalOpen: false,
      };
    },
    mounted() {
      this.domainName = this.$route.params.domain;
    },
    methods: {
      persist() {
        this.$resources.transferDomain(this.domainName, this.newPublicKey).then(() => {
          this.$bus.success(this.$lang.app.persistedSuccessfully, 3000);
          this.$router.push('/home');
        });
      },
    },
  };
</script>