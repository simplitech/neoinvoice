export default {
  language: 'pt-br',
  app: {
    title: 'neoinvoice',
    logout: 'Sair',
    menu: 'Menu',
    add: 'Cadastrar',
    export: 'Exportar',
    select: 'Selecione',
    persistedSuccessfully: 'Salvo com Sucesso! Aguarde até que a operação seja publicada.',
    confirmRemove: 'Tem certeza que deseja remover este item?',
    remove: 'Remover',
    cancel: 'Cancelar',
    transfer: 'Transferir',
    viewPayment: 'Visualizar Pagamento',
    makeAPayment: 'Realizar Pagamento',
    passwordMustHaveAtleast6Chars: 'A senha deve conter pelo menos 6 caracteres',
    onlyIfWantChangePassword: 'Preencha este campo somente se quiser alterar a senha',
    noDataToShow: 'Nenhum dado para apresentar',
    downloadCsv: 'Baixar CSV',
    search: 'Buscar',
    totalLines: '{total} entradas no total',
    version: 'Versão',
    addOneMoreLine: 'Adicionar mais uma linha',
    paymentInfo: 'Informações para Pagamento',
  },

  dateFormat: {
    millisecond: 'DD/MM/YY HH:mm:ss',
    second: 'DD/MM/YY HH:mm:ss',
    minute: 'DD/MM/YY HH:mm',
    hour: 'DD/MM/YY HH:mm',
    day: 'DD/MM/YY HH:mm',
    week: 'DD/MM/YY',
    month: 'DD/MM/YY',
    quarter: 'DD/MM/YY',
    year: 'DD/MM/YY',
    date: 'DD/MM/YYYY',
    datetime: 'DD/MM/YYYY HH:mm',
    time: 'hh:mm',
    datemask: '##/##/####',
    datetimemask: '##/##/#### ##:##',
  },

  format: {
    cpf: '###.###.###-##',
    cnpj: '##.###.###/####-##',
    rg: '##.###.###-#',
    cep: '#####-###',
    phone: '(##) #####-####',
  },

  boolean: {
    true: 'Sim',
    false: 'Não',

  },

  login: {
    title: 'Login',
    subtitle: 'Faça Login',
    passphrase: 'Senha',
    encryptedKey: 'Chave criptografada',
    signin: 'Entrar',
  },

  home: {
    title: 'Home',
    subtitle: 'Home',
  },

  persist: {
    number: 'Numérico',
    datetime: 'Data e Hora',
    submit: 'Enviar',
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
      title: 'Domínio',
      columns: {
        masterWallet: 'Master Wallet',
        masterWalletPublicKey: 'Master Wallet Public Key',
        idDomainPk: 'Id Domain Storage Pk',
        domain: 'Nome do Domínio',
        meta: 'Metadados',
        registrationDate: 'Registration Date',
        active: 'Active',
      },
      methods: {
        registerDomain: 'Registrar Domínio',
        registerSubdomain: 'Solicitar para se juntar à um Domínio',
        transferDomain: 'Transferir domínio',
        persistMeta: 'Alterar Metadados',
        persistSubdomain: 'Adicionar Wallet como Subdomínio',
        paymentForDomain: 'Pagamento para {domainName}',
      },
      format: {
        newDomainForWalletAddress: 'Novo domínio para {publicKey}',
        requestToJoinDomainAsWalletAddress: 'Solicitar para se juntar à um Domínio como {newPublicKey}',
        addAsSubdomainOfDomain: 'Adicionar Carteira como Subdomínio de {domainName}',
        transferDomain: 'Transferir Domínio {domainName}',
        editMetadataOfDomain: 'Alterar Metadados de {domainName}',
      },
      messages: {
        requestSentWaitApproval: 'Solicitação enviada, aguarde aprovação',
        requestSentWaitAcceptance: 'Solicitação enviada, aguarde aceitação da carteira',
        areYouSureYouWantToTransferDomain: 'Tem certeza que deseja transferir o domínio?',
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
      title: 'Transação Pendente',
      columns: {
        recipientWallet: 'Carteira Destinatário',
        recipientDomain: 'Domínio Destinatário',
        expirationDate: 'Data de Expiração',
        value: 'Valor',
        amount: 'Preço',
        assetID: 'Asset ID',
        paid: 'Pago',
        notFound: 'Transação não encontrada',
      },
      methods: {
        pay: 'Pay',
        createPendingTransaction: 'Criar Transação Pendente',
        createPendingTransactionForWalletOnDomain: 'Criar transação pendente para {newPublicKey} em {domainName}',
      },
    },
    Transaction: {
      title: 'Transação',
      columns: {
        recipientWallet: 'Carteira Destinatário',
        value: 'Valor',
        from: 'Origem',
        to: 'Destino',
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
      title: 'Carteira',
      columns: {
        idWalletPk: 'Id Wallet Pk',
        address: 'Endereço da Carteira',
        domains: 'Domínios',
        subdomains: 'Subdomínios',
        subdomainName: 'Nome do Subdomínio',
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
