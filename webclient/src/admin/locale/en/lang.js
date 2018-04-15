export default {
  language: 'en-us',
  app: {
    title: 'neoinvoice',
    logout: 'Logout',
    menu: 'Menu',
    add: 'Add',
    export: 'Export',
    select: 'Select',
    persistedSuccessfully: 'Persisted Successfully! Wait until it\'s broadcasted and published.',
    confirmRemove: 'Are you sure you want to remove this item?',
    remove: 'Remove',
    cancel: 'Cancel',
    transfer: 'Transfer',
    viewPayment: 'View Payment',
    makeAPayment: 'Make a Payment',
    passwordMustHaveAtleast6Chars: 'The password must have at least 6 characters',
    onlyIfWantChangePassword: 'Fill this field only if you want to change the password',
    noDataToShow: 'No data to show',
    downloadCsv: 'Download CSV',
    search: 'Search',
    totalLines: '{total} total lines',
    version: 'Version',
    addOneMoreLine: 'Add one more line',
    paymentInfo: 'Payment Info',
  },

  dateFormat: {
    millisecond: 'YY/MM/DD hh:mm:ss',
    second: 'YY/MM/DD hh:mm:ss',
    minute: 'YY/MM/DD hh:mm',
    hour: 'YY/MM/DD hh:mm',
    day: 'YY/MM/DD hh:mm',
    week: 'YY/MM/DD',
    month: 'YY/MM/DD',
    quarter: 'YY/MM/DD',
    year: 'YY/MM/DD',
    date: 'YYYY/MM/DD',
    datetime: 'YYYY/MM/DD hh:mm',
    time: 'hh:mm',
    datemask: '####/##/##',
    datetimemask: '####/##/## ##:##',
  },

  format: {
    cpf: '###.###.###-##',
    cnpj: '##.###.###/####-##',
    rg: '##.###.###-#',
    cep: '#####-###',
    phone: '(##) #####-####',
  },

  boolean: {
    true: 'True',
    false: 'False',
  },


  login: {
    title: 'Login',
    subtitle: 'Please sign in',
    passphrase: 'Passphrase',
    encryptedKey: 'EncryptedKey',
    signin: 'Sign in',
  },

  home: {
    title: 'Home',
    subtitle: 'Home',
  },

  persist: {
    number: 'Number',
    submit: 'Submit',
  },

  classes: {
    Admin: {
      title: 'Admin',
      columns: {
        idAdminPk: 'Id Admin Pk',
        email: 'Email',
        password: 'Password',
      },
    },
    Attribute: {
      title: 'Attribute',
      columns: {
        walletTransaction: 'Wallet Transaction',
        idTransactionAttributePk: 'Id Transaction Attribute Pk',
        attribute: 'Attribute',
      },
    },
    Domain: {
      title: 'Domain',
      columns: {
        masterWallet: 'Master Wallet',
        masterWalletPublicKey: 'Master Wallet Public Key',
        idDomainPk: 'Id Domain Storage Pk',
        domain: 'Domain Name',
        meta: 'Metadata',
        registrationDate: 'Registration Date',
        active: 'Active',
      },
      methods: {
        registerDomain: 'Register Domain',
        registerSubdomain: 'Request to join a Domain',
        transferDomain: 'Transfer Domain',
        persistMeta: 'Edit Metadata',
        persistSubdomain: 'Add Wallet as Subdomain',
        paymentForDomain: 'Payment for {domainName}',
      },
      format: {
        newDomainForWalletAddress: 'New Domain for {publicKey}',
        requestToJoinDomainAsWalletAddress: 'Request to join a Domain as {newPublicKey}',
        addAsSubdomainOfDomain: 'Add Wallet as Subdomain of {domainName}',
        transferDomain: 'Transfer Domain {domainName}',
        editMetadataOfDomain: 'Edit Metadata of {domainName}',
      },
      messages: {
        requestSentWaitApproval: 'Request sent, wait for approval',
        requestSentWaitAcceptance: 'Request sent, wait for wallet acceptance',
        areYouSureYouWantToTransferDomain: 'Are you sure you want to transfer the Domain?',
      },
    },
    Input: {
      title: 'Input',
      columns: {
        walletTransaction: 'Wallet Transaction',
        idTransactionInputPk: 'Id Transaction Input Pk',
        input: 'Input',
      },
    },
    MetaKeyValue: {
      title: 'Meta Key Value',
      columns: {
        domain: 'Domain Storage',
        idMetaKeyValuePk: 'Id Meta Key Value Pk',
        key: 'Key',
        value: 'Value',
      },
    },
    Output: {
      title: 'Output',
      columns: {
        walletTransaction: 'Wallet Transaction',
        idOutputPk: 'Id Output Pk',
        output: 'Output',
      },
    },
    PendingTransaction: {
      title: 'Pending Transaction',
      columns: {
        idPendingTransaction: 'ID',
        recipientWallet: 'Recipient Wallet',
        recipientDomain: 'Recipient Domain',
        expirationDate: 'Expiration Date',
        value: 'Value',
        amount: 'Price',
        assetID: 'Asset ID',
        paid: 'Paid',
        notFound: 'Transaction not found',
      },
      methods: {
        createPendingTransaction: 'Create Pending Transaction',
        createPendingTransactionForWalletOnDomain: 'Create pending transaction for {publicKey} on {domainName}',
        pay: 'Pay',
      },
    },
    Transaction: {
      title: 'Transaction',
      columns: {
        recipientWallet: 'Recipient Wallet',
        value: 'Valor',
        from: 'From',
        to: 'To',
      },
    },
    Script: {
      title: 'Script',
      columns: {
        walletTransaction: 'Wallet Transaction',
        idScriptPk: 'Id Script Pk',
        script: 'Script',
      },
    },
    SlaveWallet: {
      title: 'Slave Wallet',
      columns: {
        domain: 'Domain Storage',
        wallet: 'Wallet',
        idSlaveWalletPk: 'Id Slave Wallet Pk',
        registrationDate: 'Registration Date',
        masterApproved: 'Master Approved',
        slaveApproved: 'Slave Approved',
        active: 'Active',
      },
    },
    Wallet: {
      title: 'Wallet',
      columns: {
        idWalletPk: 'Id Wallet Pk',
        address: 'Wallet Address',
        domains: 'Domains',
        subdomains: 'Subdomains',
        subdomainName: 'Subdomain name',
      },
    },
    WalletTransaction: {
      title: 'Wallet Transaction',
      columns: {
        wallet: 'Wallet',
        idWalletTransactionPk: 'Id Wallet Transaction Pk',
        type: 'Type',
        version: 'Version',
      },
    },
  },
};
