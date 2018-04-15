<template>
    <div class="horiz mob-verti w-window h-window nowrap">
        <aside class="menu des-w-200 tab-w-200 w-full verti">
            <div class="horiz items-center">
                <a class="mobile icon icon-menu" @click="showMenu = !showMenu"></a>
                <h1 class="weight-1 text-center accent">
                    {{ $t("app.title") }}
                </h1>
            </div>
            <div class="weight-1" :class="{ 'desktop-tablet': !showMenu }">
                <ul class="verti h-full p-0 py-10">

                    <li><router-link to="/home" @click.native="showMenu = false">
                        {{ $t("home.title") }}
                    </router-link></li>
                    <li><a @click="modalOpen = true">
                        {{ $t("app.makeAPayment") }}
                    </a></li>
                    <div class="weight-1"></div>
                    <li><a @click="logout">
                        <i class="icon icon-logout mr-3"/>
                        {{ $t("app.logout") }}
                    </a></li>
                </ul>
            </div>
            <footer class="p-10 desktop-tablet">
                <small><b>{{ $t("app.version") }}</b> {{ version }}</small>
            </footer>
        </aside>

        <router-view class="weight-1 des-w-0 mob-w-full" :key="$route.fullPath"></router-view>

        <modal v-if="modalOpen">
            <form class="verti" @submit.prevent="openPayment()">
                <a class="close self-right" @click="modalOpen = false"></a>
                <input-group required
                     type="text"
                     maxlength="80"
                     v-model="domainName">
                    {{ $t("classes.Domain.columns.domain") }}
                </input-group>
                <input-group required
                     type="text"
                     v-model="idPendingTransaction">
                    {{ $t("classes.PendingTransaction.columns.idPendingTransaction") }}
                </input-group>
                <div class="horiz items-center">
                    <button type="button" @click="modalOpen = false">{{ $t("app.cancel") }}</button>
                    <button type="submit" class="accent ml-10">
                        {{ $t("app.viewPayment") }}
                    </button>
                </div>
            </form>
        </modal>
    </div>
</template>

<script>
  import WalletStore from '../../service/WalletStore';
  import { version } from '../../../../package.json';

  export default {
    data() {
      return {
        showMenu: false,
        version,
        modalOpen: false,
        domainName: null,
        idPendingTransaction: null,
      };
    },
    mounted() {
      WalletStore.routeToLoginIfNoWallet();
    },
    methods: {
      logout() {
        WalletStore.wallet = null;
        this.$router.push('/login');
      },
      openPayment() {
        this.modalOpen = false;
        this.$router.push(`/payment/${this.domainName}/${this.idPendingTransaction}`);
      },
    },
  };

</script>