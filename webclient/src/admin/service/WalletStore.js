import Vue from 'vue';

export default {
  wallet: null,
  beforeLoginIntention: null,
  routeToLoginIfNoWallet() {
    if (!this.wallet) {
      this.beforeLoginIntention = location.href;
      Vue.$router.push('/login');
    }
  },
};
