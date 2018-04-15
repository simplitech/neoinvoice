import Neon, { wallet, rpc, api } from '@cityofzion/neon-js';
import WalletStore from './WalletStore';

const contractPath = 'http://18.231.135.105:30333';
const neoScanPath = 'http://18.231.135.105:4000/api/main_net';
const scriptHash = '899d9f8f2b210014972e3e46eb385cfbd79eeaaf';

export default {
  install(Vue) {
    const resources = {

      hexstring2str(hex) {
        return hex && hex.length ? Neon.u.hexstring2str(hex) : '';
      },

      hex2number(hex) {
        return hex && hex.length ? parseInt(hex, 16) : '';
      },

      /**
       * makes operations that dont spend money
       * @param operation
       * @param args
       * @returns {Promise.<null>}
       */
      async testInvoke(operation, ...args) {
        WalletStore.routeToLoginIfNoWallet();

        const script = Neon.create.script({ scriptHash, operation, args });

        const resp = await rpc.Query.invokeScript(script).execute(contractPath);

        return resp.result.stack && resp.result.stack.length ? resp.result.stack[0].value : null;
      },

      /**
       * makes operations that spend money
       * @param operation
       * @param gas
       * @param args
       * @returns {Promise<string>}
       */
      async doInvoke(operation, gas, ...args) {
        WalletStore.routeToLoginIfNoWallet();

        const resp = await api.doInvoke({
          net: neoScanPath,
          privateKey: WalletStore.wallet.privateKey,
          address: WalletStore.wallet.address,
          intents: [{
            assetId: Neon.CONST.ASSET_ID.GAS,
            value: gas,
            scriptHash,
          }],
          script: { scriptHash, operation, args },
          gas: 0,
        });

        return resp.response;
      },


      /**
       * authenticates the user
       * @param passphrase
       * @param encryptedKey
       * @returns {String} publicKey
       */
      async login(passphrase, encryptedWIF) {
        if (!wallet.isNEP2(encryptedWIF)) {
          throw new Error('That is not a valid encrypted key');
        }

        const wif = await wallet.decrypt(encryptedWIF, passphrase);
        WalletStore.wallet = new wallet.Account(wif);
      },

      /**
       * lists the domains of the wallet
       * @param walletPublicKey
       * @returns { domains[], subdomains[] }
       */
      async listDomains(walletPublicKey) {
        const resp = await this.testInvoke('listDomains', walletPublicKey);

        if (!resp) {
          return [];
        }

        const arrayOfAllDomains = this.hexstring2str(resp)
          .split(';').filter(r => r && r.length);

        const final = arrayOfAllDomains.reduce((domAndSub, item) => {
          const itemAsArray = item.split(':');
          const domains = domAndSub.domains ? [...domAndSub.domains] : [];
          const subdomains = domAndSub.subdomains ? [...domAndSub.subdomains] : [];

          if (itemAsArray[0] === 'm') {
            domains.push(itemAsArray[1]);
          } else if (itemAsArray[1] === 's') {
            subdomains.push(itemAsArray[1]);
          }

          return {
            domains,
            subdomains,
          };
        }, {});

        return final;
      },

      /**
       * gets the domain information
       * @param domainName
       * @returns Promise{score, masterWallet, subdomainWallets, meta, pendingTransactions}
       */
      async readDomain(domainName) {
        const resp = await this.testInvoke(
          'readDomain',
          Neon.u.str2hexstring(domainName));

        // resp:
        // 0 - score
        // 1 - hashMaster
        // 2 - subdomains
        // 3 - metadata
        // 4 - pending transactions

        if (!resp || !resp.length) {
          return null;
        }

        const subDsJoined = resp && resp.length >= 3 ? this.hexstring2str(resp[2].value).split(';') : [];

        const subdomainWallets = subDsJoined.length ? subDsJoined.map((i) => {
          const subDArr = i.split(':');
          return {
            domain: subDArr[0],
            wallet: subDArr[1] ? subDArr[1] : null,
          };
        }) : null;

        const metaJoined = resp && resp.length >= 4 ? this.hexstring2str(resp[3].value).split(';') : [];

        const meta = metaJoined.length ? metaJoined.reduce((holder, i) => {
          const mArr = i.split(':');
          return {
            ...holder,
            [mArr[0]]: mArr[1],
          };
        }, {}) : null;

        const ptsAttrs = resp && resp.length >= 5 && resp[4].value.length ? this.hexstring2str(resp[4].value).split('|') : [];

        let pendingTransactions = null;
        if (ptsAttrs) {
          pendingTransactions = ptsAttrs.map(p => (p.length ? p.split(';').reduce((holder, i) => {
            const mArr = i.split(':');
            if (mArr[1]) {
              return {
                ...holder,
                [mArr[0]]: mArr[1],
              };
            }
            return holder;
          }, {}) : null));
        }

        const final = {
          score: resp[0] && resp[0].value.length ? this.hexstring2str(resp[0].value) : null,
          masterWallet: resp[1] ? resp[1].value : null,
          subdomainWallets,
          meta,
          pendingTransactions,
        };

        return final;
      },

      /**
       * registers a domainname for the current logged wallet
       * @param domainName is an alphanumeric phrase with 80 character limit
       * @returns Boolean true if the domain was registered
       */
      async registerDomain(domainName) {
        const resp = await this.doInvoke('registerDomain', 0.1,
          WalletStore.wallet.publicKey,
          Neon.u.str2hexstring(domainName));

        if (!resp) {
          throw new Error('Failed at test');
        }

        return resp; // respTest;
      },

      /**
       * replaces the metadata of the domain, some keys are designed for a specific purpose
       * @param domainName
       * @param metaAsObject with key and value
       * @returns Boolean true if the meta was saved
       */
      saveMeta(domainName, metaAsObject) {
        const joinedMeta = Object.keys(metaAsObject)
          .map(attr => `${attr}:${metaAsObject[attr]}`).join(';');
        return this.doInvoke('saveMeta',
          0.1,
          WalletStore.wallet.publicKey,
          Neon.u.str2hexstring(domainName),
          Neon.u.str2hexstring(joinedMeta));
      },

      /**
       * transfer a domain to another master wallet and removes all slave wallets
       * @param domainName
       * @param newPublicKey a new master wallet public key
       * @returns {Boolean} true if the domain was transfered
       */
      transferDomain(domainName, newPublicKey) {
        return this.testInvoke('transferDomain',
          WalletStore.wallet.publicKey,
          domainName,
          newPublicKey);
      },

      /**
       * creates a pending transaction to be completed by any other wallet
       * @param domainName
       * @param amount is the price
       * @param transactionAttributes neo transaction object
       * @returns {Boolean} true if the pending transaction was created
       */
      createPendingTransaction(domainName, amount, assetID, transactionAttributes) {
        const joinedTransaction = Object.keys(transactionAttributes)
          .map(attr => `${attr}:${transactionAttributes[attr]}`).join(';');
        return this.doInvoke('createPendingTransaction',
          0.1,
          WalletStore.wallet.publicKey,
          Neon.u.str2hexstring(domainName),
          Neon.u.str2hexstring(amount),
          // assetID,
          Neon.u.str2hexstring(joinedTransaction));
      },

      /**
       * gets the pending transaction information
       * @param domainName
       * @param idPendingTransaction
       * @returns {Promise{publicKey, executed, attributes, price}}
       */
      async readPendingTransaction(domainName, idPendingTransaction) {
        const resp = await this.testInvoke('readPendingTransaction',
          Neon.u.str2hexstring(domainName),
          Neon.u.str2hexstring(idPendingTransaction));

        const metaJoined = resp && resp.length >= 3 ? this.hexstring2str(resp[2].value).split(';') : [];

        const meta = metaJoined.length ? metaJoined.reduce((holder, i) => {
          const mArr = i.split(':');
          return {
            ...holder,
            [mArr[0]]: mArr[1],
          };
        }, {}) : null;

        return {
          publicKey: resp && resp.length ? resp[0].value : null,
          executed: resp && resp.length >= 2 ? resp[1].value !== '30' : null,
          attributes: meta,
          price: resp && resp.length >= 4 ? this.hexstring2str(resp[3].value) : null,
        };
      },

      // removePendingTransaction(domainName, idPendingTransaction) {
      //   return this.testInvoke('removePendingTransaction',
      //     WalletStore.wallet.publicKey, domainName, idPendingTransaction);
      // },

      completePendingTransaction(domainName, price, idPendingTransaction) {
        return this.doInvoke('completePendingTransaction',
          price,
          WalletStore.wallet.publicKey,
          Neon.u.str2hexstring(domainName),
          Neon.u.str2hexstring(idPendingTransaction));
      },
    };

    Object.assign(Vue.prototype, { $resources: resources });
    Object.assign(Vue, { $resources: resources });
  },
};
