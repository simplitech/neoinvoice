from boa.interop.Neo.Storage import Get,Put,Delete,GetContext
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash, GetScriptContainer
from boa.builtins import concat
from boa.interop.Neo.TriggerType import Application, Verification
from boa.interop.Neo.Transaction import Transaction
from boa.interop.Neo.Runtime import GetTrigger, Log, CheckWitness
from boa.interop.Neo.Output import GetScriptHash, GetAssetId
from boa.builtins import breakpoint

#
#
#
# ███████╗    ██╗    ███╗   ███╗    ██████╗     ██╗         ██╗
# ██╔════╝    ██║    ████╗ ████║    ██╔══██╗    ██║         ██║
# ███████╗    ██║    ██╔████╔██║    ██████╔╝    ██║         ██║
# ╚════██║    ██║    ██║╚██╔╝██║    ██╔═══╝     ██║         ██║
# ███████║    ██║    ██║ ╚═╝ ██║    ██║         ███████╗    ██║
# ╚══════╝    ╚═╝    ╚═╝     ╚═╝    ╚═╝         ╚══════╝    ╚═╝
#
#
#

OWNER = b'\x8e\x5b\x17\x79\x3c\xa9\xf5\xd9\x13\x1d\x67\x4d\xfc\x00\x0f\x5a\x65\x58\xa4\x65'
GAS_ASSET_ID = b'\xe7\x2d\x28\x69\x79\xee\x6c\xb1\xb7\xe6\x5d\xfd\xdf\xb2\xe3\x84\x10\x0b\x8d\x14\x8e\x77\x58\xde\x42\xe4\x16\x8b\x71\x79\x2c\x60';
FEE = 1

def Main(method, args):
    trigger = GetTrigger()

    #The 'correct' usage of this project would be using a correct implemented Verification Trigger;
    #Since the tools doesn't permit to test this, we are sending the transactions directly to the ownders
    if trigger == Verification():
        return CheckWitness(OWNER)

    elif trigger == Application():
        Log("met:"+method)
        if method == "name":
            return name()
        elif method == "readDomain":
            return readDomain(args[0])
        elif method == "listDomains":
            return listDomains(args[0])
        elif method == "registerDomain":
            return registerDomain(args[0], args[1])
        elif method == "saveMeta":
            return saveMeta(args[0], args[1], args[2])
        elif method == "addSlaveAsMaster":
            return addSubaccountAsMaster(args[0], args[1], args[2], args[3])
        elif method == "addDomainAsSlave":
            return addDomainAsSubaccount(args[0], args[1])
        elif method == "removeSlaveAsMaster":
            return removeSubaccountAsMaster(args[0], args[1], args[2])
        elif method == "transferDomain":
            return transferDomain(args[0], args[1], args[2])
        elif method == "createPendingTransaction":
            return createPendingTransaction(args[0], args[1], args[2], args[3])
        elif method == "readPendingTransaction":
            return readPendingTransaction(args[0], args[1])
        elif method == "removePendingTransaction":
            return removePendingTransaction(args[0], args[1], args[2])
        elif method == "completePendingTransaction":
            return completePendingTransaction(args[0], args[1], args[2])
        else:
            return False

    return False

def name():
    return "NeoInvoice"


#
# Returns all the information related to the domain, including its invoices
#
# RETURN array
#
# [
#   "87", // score
#   "scriptHashMaster",
#   "subdomain1:endereço1;subdomain2:endereço2", // all subdomain + scripthash
#   "attribute:value;attribute2:value2", // metadata
#   "id:0;attribute:value;price:0|id:1;attribute:value;price:0" // pending transactions
#   "id:0;attribute:value;price:0|id:1;attribute:value;price:0" // completed transactions
# ]
#
#   Storage count
#   GET 6
#   DELETE 0
#   PUT 0
#
def readDomain(domainName):
    ctx = GetContext()
    ownerHash = Get(ctx, domainName)
    #check if has domains cache
    if ownerHash is None:
        return ''

    #get score
    score = Get(ctx, createScoreKey(domainName))
    #get all subdomains
    subdomains = Get(ctx, createSubsKey(domainName))
    #get metadata
    meta = Get(ctx, createMetaKey(domainName))
    #get pending transactions
    pendingTransaction = Get(ctx, createPendingTransactionsKey(domainName))
    #get completed transactions
    completedTransaction = Get(ctx, createCompletedTransactionsKey(domainName))

    #construct results
    result = [score, ownerHash, subdomains, meta, pendingTransaction, completedTransaction]

    return result

#
# List all domains from an account.
#
# RETURN string
#
#   "m:domain1;m:domain2;s:subdomain1"
#
#   Storage count
#   GET 1
#   DELETE 0
#   PUT 0
#
def listDomains(executionerPublickey):
    key = createHashDomainsKey(executionerPublickey)
    domains = Get(GetContext(), key)
    if domains is None:
        return ''

    return domains

#
# Check if the name has been recorded in the blockchain
#
# RETURN boolean
#
#   true or false
#
#   Storage count
#   GET 1
#   DELETE 0
#   PUT 0
#
def existDomain(domainName):
    exists = Get(GetContext(), domainName)
    return exists is not None

# Check if the subdname has been recorded in the current name
#
# RETURN boolean
#
#   true or false
#
#   Storage count
#   GET 1
#   DELETE 0
#   PUT 0
#
def existSubDomain(key):
    exists = Get(GetContext(), key)
    return exists is not None

#
# RETURN boolean
#
#   true or false
#
#   Storage count
#   GET 1
#   DELETE 0
#   PUT 0
#
def owner(publicKey, domainName):
    ownerKey = Get(GetContext(), domainName)
    return publicKey is ownerKey

#
# RETURN boolean
#
#   true or false
#
#   Storage count
#   GET 2
#   DELETE 0
#   PUT 0
#
def existDomainAndOwnerWithHash(publicKey, domainName):
    if(not existDomain(domainName)):
        return False
    return owner(publicKey, domainName)

#
# RETURN boolean
#
#   true or false
#
#   Storage count
#   GET 3
#   DELETE 0
#   PUT 0
#
def existDomainAndOwnerOrSubaccountWithHash(publicKey, domainName):
	if not existDomain(domainName):
		return False
	if not owner(publicKey, domainName):
        #if not owner, check if Subaccount
		subaccountKey = createSubMainKey(domainName, publicKey)
		return existSubaccount(subaccountKey)
	return True

#
# RETURN boolean
#
#   true or false
#
#   Storage count
#   GET 1
#   DELETE 0
#   PUT 0
#
def existSubaccount(SubaccountKey):
	exists = Get(GetContext(), SubaccountKey)
	return exists is not None

#
# RETURN script hash of pending transaction
#
#   script hash
#
#   Storage count
#   GET 1
#   DELETE 0
#   PUT 0
#
def existPendingTransaction(domainName, idPendingTransaction):
	key = createPendingTransactionKey(domainName, idPendingTransaction)
	pendingTransaction = Get(GetContext(), key)
	if pendingTransaction is None:
		return None
	return pendingTransaction

#
# RETURN boolean
#
#   true or false
#
#   Storage count
#   GET 2
#   DELETE 0
#   PUT 4
#
def registerDomain(executionerPublickey, domainName):
    if not CheckWitness(executionerPublickey):
        return False

    #check domain length
    if len(domainName) > 80:
        return False

    #check if domain exists
    if existDomain(domainName):
        return False

    tx = GetScriptContainer()
    refs = tx.References
    if len(refs) < 1:
        return False
    ref = refs[0]
    sentAsset = GetAssetId(ref)
    if sentAsset is not GAS_ASSET_ID:
        False

    receiver = GetExecutingScriptHash()
    totalReceived = 0

    for output in tx.Outputs:
        scriptHashReceiver = GetScriptHash(output)
        if scriptHashReceiver == receiver:
            totalReceived = totalReceived + output.Value

    if(totalReceived < FEE):
        return False

    ctx = GetContext()
    #save owner
    Put(ctx, domainName, executionerPublickey)
    #save first transaction id
    Put(ctx, createLastTransactionKey(domainName), ("n" - 0x01))
    #save score
    Put(ctx, createScoreKey(domainName), 0x30)

    tr = concat("m:", domainName)
    addDomainToStorage(executionerPublickey, tr)
    return True

#
# RETURN boolean
#
#   true or false
#
#   Storage count
#   GET 2
#   DELETE 0
#   PUT 1
#
def saveMeta(executionerPublicKey, domainName, meta):
    if not CheckWitness(executionerPublicKey):
        return False

    #check if owner and domain exists
    if not existDomainAndOwnerWithHash(executionerPublicKey, domainName):
        return False

    #save meta
    Put(GetContext(), createMetaKey(domainName), meta)

    return True

#
# RETURN boolean
#
#   true or false
#
#   Storage count
#   GET 4~7
#   DELETE 0
#   PUT 5
#
def addSubaccountAsMaster(executionerPublicKey, domainName, subDomainName, walletHash):
    if not CheckWitness(executionerPublicKey):
        return False

    #check if owner and domain exists
    if not existDomainAndOwnerWithHash(executionerPublicKey, domainName):
        return False

    ctx = GetContext()
    # "simpli/sub/
    SubaccountKey = createSubMainKey(domainName, walletHash)
    subKey = createSubNameKey(SubaccountKey, subDomainName)

    #if exist subdomain name, return false
    if existSubDomain(subKey):
        return False

    if existSubaccount(SubaccountKey):
        masterApproved = Get(ctx, createMasterApprovedKey(SubaccountKey))
        masterApproved = masterApproved + 0x30
        if masterApproved is None:
            return False

        if not masterApproved:
            return False

        subsKeyValue = concat(subDomainName, ":")
        subsKeyValue = concat(subsKeyValue, walletHash)

        #save to all subs
        keyHashes = createSubsKey(domainName)
        addHashToHashes(keyHashes, subsKeyValue, ";")

        #save to all scripthash domains
        tr = concat("s:", subDomainName)
        addDomainToStorage(walletHash, tr)
    else:
        #save sub scripthash
        Put(ctx, SubaccountKey, walletHash)
        #save sub approved false
        Put(ctx, createSubApprovedKey(SubaccountKey), 0x30)

    #save master approved
    Put(ctx, createMasterApprovedKey(SubaccountKey), 0x01)
    Put(ctx, subKey, subDomainName)
    Put(ctx, createSubRootNameKey(SubaccountKey), subDomainName)

    return True

#
# RETURN boolean
#
#   true or false
#
#   Storage count
#   GET 3~6
#   DELETE 0
#   PUT 2~3
#
def addDomainAsSubaccount(executionerPublicKey, domainName):
    if not CheckWitness(executionerPublicKey):
        return False

    #check if domain exists
    if not existDomain(domainName):
        return False

    #check if owner
    if owner(executionerPublicKey, domainName):
        return False

    ctx = GetContext()
    # "simpli/sub/
    subaccountKey = createSubMainKey(domainName, executionerPublicKey)

    if existSubaccount(subaccountKey):
        subApproved = Get(ctx, createSubApprovedKey(subaccountKey))
        subApproved = subApproved + 0x30
        if subApproved is None:
            return False

        if not subApproved:
            return False

        #get subdomain
        subdomainName = Get(ctx, createSubRootNameKey(subaccountKey))
        subsKeyValue = concat(subdomainName, ":")
        subsKeyValue = concat(subsKeyValue, executionerPublicKey)

        #save to all subs
        keyHashes = createSubsKey(domainName)
        addHashToHashes(keyHashes, subsKeyValue, ";")
    else:
        #save sub scripthash
        Put(ctx, subaccountKey, executionerPublicKey)
        #save sub approved false
        Put(ctx, createMasterApprovedKey(subaccountKey), 0x30)

    #save sub approved
    Put(ctx, createSubApprovedKey(subaccountKey), 0x01)

    return True

#
# RETURN boolean
#
#   true or false
#
#   Storage count
#   GET 5~7
#   DELETE 3~5
#   PUT 1~2
#
def removeSubaccountAsMaster(executionerPublicKey, domainName, SubaccountHash):
    if not CheckWitness(executionerPublicKey):
        return False

    #check if owner and domains exists
    if not existDomainAndOwnerWithHash(executionerPublicKey, domainName):
        return False

    SubaccountKey = createSubMainKey(domainName, SubaccountHash)
    if existSubaccount(SubaccountKey):
        ctx = GetContext()
        subdomainName = Get(ctx, createSubRootNameKey(SubaccountKey))
        if subdomainName is not None:
            Delete(ctx, createSubNameKey(SubaccountKey, subdomainName))
            Delete(ctx, createSubRootNameKey(SubaccountKey))
            #get subdomain
            subdomainName = Get(ctx, createSubRootNameKey(SubaccountKey))
            subsKeyValue = concat(subdomainName, ":")
            subsKeyValue = concat(subsKeyValue, SubaccountHash)
            #remove from all subs
            hashesKey = createSubsKey(domainName)
            removeHashFromHashes(hashesKey, subsKeyValue, ";")

        Delete(ctx, SubaccountKey)
        Delete(ctx, createMasterApprovedKey(SubaccountKey))
        Delete(ctx, createSubApprovedKey(SubaccountKey))

        #remove from all scripthash subdomains
        tr = concat("s:", domainName)
        removeDomainFromStorage(SubaccountKey, tr)
        return True
    return False

#
# RETURN boolean
#
#   true or false
#
#   Storage count
#   GET 4
#   DELETE 0
#   PUT 3
#
def transferDomain(executionerPublicKey, domainName, newMasterWalletKey):
    if not CheckWitness(executionerPublicKey):
        return False

    #check if owner and exist domain
    if not existDomainAndOwnerWithHash(executionerPublicKey, domainName):
        return False

    #change script hash master
    Put(GetContext(), domainName, newMasterWalletKey)

    tr = concat("m:", domainName)
    #remove from all domains
    addDomainToStorage(newMasterWalletKey, tr)
    #add to all domains
    removeDomainFromStorage(executionerPublicKey, tr)

    return True

#
# RETURN int
#
#   id transaction
#
#   Storage count
#   GET 5
#   DELETE 0
#   PUT 6
#
def createPendingTransaction(executionerPublicKey, domainName, price, transactionAttr):
    if not CheckWitness(executionerPublicKey):
        return False

    #if owner or Subaccount and domains exist
    if not existDomainAndOwnerOrSubaccountWithHash(executionerPublicKey, domainName):
        return False

    ctx = GetContext()

    lastPendingTransaction = Get(ctx, createLastTransactionKey(domainName))

    #increment last transaction id
    lastPendingTransaction = lastPendingTransaction + 0x01

    #create root transaction key
    key = createPendingTransactionKey(domainName, lastPendingTransaction)
    Put(ctx, key, executionerPublicKey)
    Put(ctx, createExecutedKey(key), 0x30)
    Put(ctx, createAttributesKey(key), transactionAttr)
    Put(ctx, createPriceKey(key), price)

    #update last transaction id
    Put(ctx, createLastTransactionKey(domainName), lastPendingTransaction)

    keyAllPending = createPendingTransactionsKey(domainName)
    #create unique pending transaction
    tr = createTransactionHash(lastPendingTransaction, transactionAttr, price)

    #save to domains/pendingTransactions
    addHashToHashes(keyAllPending, tr, "|")

    return lastPendingTransaction

#
# RETURN int
#
#   id transaction
#
#
def readPendingTransaction(domainName, idPendingTransaction):
    #if owner or Subaccount and domains exist
    if not existDomain(domainName):
        return False

    ctx = GetContext()

    #create root transaction key
    key = createPendingTransactionKey(domainName, idPendingTransaction)
    ownerhash = Get(ctx, key)
    executed = Get(ctx, createExecutedKey(key))
    transactionAttr = Get(ctx, createAttributesKey(key))
    price = Get(ctx, createPriceKey(key))

    result = [ownerhash, executed, transactionAttr, price]

    return result

#
# RETURN int
#
#   id transaction
#
#   Storage count
#   GET 7
#   DELETE 4
#   PUT 1
#
def removePendingTransaction(executionerPublicKey, domainName, idPendingTransaction):
    if not CheckWitness(executionerPublicKey):
        return False

    #if owner or Subaccount and domains exist
    if not existDomainAndOwnerOrSubaccountWithHash(executionerPublicKey, domainName):
        return False

    #check if exist transaction
    if existPendingTransaction(domainName, idPendingTransaction) is None:
        return False

    #create root pending transaction
    key = createPendingTransactionKey(domainName, idPendingTransaction)

    ctx = GetContext()
    transactionAttr = Get(ctx, createAttributesKey(key))
    price = Get(ctx, createPriceKey(key))

    #recreate unique pending transaction
    tr = createTransactionHash(idPendingTransaction, transactionAttr, price)

    Delete(ctx, key)
    Delete(ctx, createExecutedKey(key))
    Delete(ctx, createAttributesKey(key))
    Delete(ctx, createPriceKey(key))

    #remove from domains/pendingTransactions
    keyAllPending = createPendingTransactionsKey(domainName)
    removeHashFromHashes(keyAllPending, tr, "|")

    return True

#
# RETURN boolean
#
#   true or false
#
#   Storage count
#   GET 10
#   DELETE 0
#   PUT 3
#
def completePendingTransaction(executionerPublicKey, domainName, idPendingTransaction):
    if not CheckWitness(executionerPublicKey):
        return False

    #if owner or Subaccount and domains exist
    if not existDomainAndOwnerOrSubaccountWithHash(executionerPublicKey, domainName):
        return False

    #check if exist transaction
    if existPendingTransaction(domainName, idPendingTransaction) is None:
        return False

    #create root pending transaction key
    key = createPendingTransactionKey(domainName, idPendingTransaction)

    ctx = GetContext()

    receiverHash = Get(ctx, key)

    # tx: Transaction = GetScriptContainer()
    # refs = tx.References
    # if len(refs) < 1:
    #     return False
    #
    # ref = refs[0]
    # sentAsset = GetAssetId(ref)
    # if sentAsset is not GAS_ASSET_ID:
    #     return False
    #
    # buyer = GetScriptHash(ref)
    # for output in tx.Outputs:
    #     scriptHashReceiver = GetScriptHash(output)
    #     if scriptHashReceiver == receiverHash:
    #         totalReceived = totalReceived + output.Value
    #
    # #get saved price
    originalPrice = Get(ctx, createPriceKey(key)) + 0x30
    #
    # if totalReceived < originalPrice:
    #     return False

    #mark transaction executed
    Put(ctx, createExecutedKey(key), 0x01)

    #create score key
    scoreKey = createScoreKey(domainName)

    score = Get(ctx, scoreKey)
    #increment score and save
    score = score + 0x01
    Put(ctx, scoreKey, score)

    transactionAttr = Get(ctx, createAttributesKey(key))

    #recreate unique pending transaction
    tr = createTransactionHash(idPendingTransaction, transactionAttr, originalPrice)

    #remove from domains/pendingTransactions
    keyAllPending = createPendingTransactionsKey(domainName)
    removeHashFromHashes(keyAllPending, tr, "|")

    #save to domains/completedTransactions
    keyAllCompleted = createCompletedTransactionsKey(domainName)
    addHashToHashes(keyAllCompleted, tr)

    return True

#
# RETURN string
#
#   concat id:0;attr;price:0
#
#   Storage count
#   GET 0
#   DELETE 0
#   PUT 0
#
def createTransactionHash(idPendingTransaction, transactionAttr, price):
    tr = concat("id:", idPendingTransaction)
    tr = concat(tr, ";")
    tr = concat(tr, transactionAttr)
    tr = concat(tr, ";")
    tr = concat(tr, concat("price:", price))
    return tr

#
# RETURN void
#
#   domain;domain;domain
#
#   Storage count
#   GET 1
#   DELETE 0
#   PUT 1
#
def addDomainToStorage(hashKey, domain):
    keyDomains = createHashDomainsKey(hashKey)
    addHashToHashes(keyDomains, domain, ";")

#
# RETURN void
#
#   domain;domain;domain
#
#   Storage count
#   GET 1
#   DELETE 0
#   PUT 1
#
def removeDomainFromStorage(hashKey, domain):
	keyDomains = createHashDomainsKey(hashKey)
	removeHashFromHashes(keyDomains, domain, ";")

#
# RETURN void
#
#   toAdd1 delim toAdd2 delim toAdd3
#
#   Storage count
#   GET 1
#   DELETE 0
#   PUT 1
#
def addHashToHashes(key, toAdd, delim):
	allhashes = Get(GetContext(), key)
	if allhashes is None:
		Put(GetContext(), key, toAdd)
	else:
		allhashes = concat(allhashes, delim)
		allhashes = concat(allhashes, toAdd)
		Put(GetContext(), key, allhashes)

#
# RETURN void
#
#   toAdd1 delim toAdd3
#
#   Storage count
#   GET 1
#   DELETE 0
#   PUT 1
#
def removeHashFromHashes(key, toRemove, delim):
    ctx = GetContext()
    results = Get(ctx, key)
    results = customRemove(results, toRemove, delim)
    Put(ctx, key, results)

#
# RETURN string
#
#   use split to find and remove
#
#   Storage count
#   GET 0
#   DELETE 0
#   PUT 0
#
def customRemove(hashStr, toRemove, delim):
    str = concat(hashStr, delim)
    index = 0
    string = ""
    array = ""
    while index < len(str):
        c = str[index:index + 1]
        if c != delim:
            string = concat(string, c)
        else:
            if string is not toRemove:
                array = concat(array, string)
            string = ""
        index = index + 1
    if string: array = concat(array, string)

    return array

# ALL STORAGE KEY :: VALUE
#
# "simpli":scripthash
#
# "simpli/score":0                                      AKA createScoreKey
# "simpli/meta":value                                   AKA createMetaKey
# "simpli/lastPendingTransaction":0                     AKA createLastTransactionKey
# "simpli/pendingTransactions":attr|attr2               AKA createPendingTransactionsKey
# "simpli/completedTransactions":attr|attr2             AKA createCompletedTransactionsKey
# "simpli/subs":sub1:hash1;sub2:hash2;                  AKA createSubsKey
#
# "simpli/sub/scripthash": scripthash                   AKA createSubMainKey
# "simpli/sub/scripthash/name/": subdomain              AKA createSubRootNameKey
# "simpli/sub/scripthash/subdomainname": scripthash     AKA createSubNameKey
# "simpli/sub/scripthash/subApproved":0                 AKA createSubApprovedKey
# "simpli/sub/scripthash/masterApproved":0              AKA createMasterApprovedKey
#
# "scripthash/domains":m:simpli;s:simpli2;              AKA createHashDomainsKey
#
# "simpli/pendingTransaction/0":scripthash              AKA createPendingTransactionKey
# "simpli/pendingTransaction/0/executed":0              AKA createExecutedKey
# "simpli/pendingTransaction/0/attributes":att1;attr2   AKA createAttributesKey
# "simpli/pendingTransaction/0/price":0                 AKA createPriceKey
#
#

def createScoreKey(domainName):
	return concat(domainName, "/dscore")

def createMetaKey(domainName):
	return concat(domainName, "/dmeta")

def createLastTransactionKey(domainName):
	return concat(domainName, "/dlastIdPendingTransaction")

def createPendingTransactionsKey(domainName):
	return concat(domainName, "/dpendingTransactions")

def createCompletedTransactionsKey(domainName):
	return concat(domainName, "/dcompletedTransactions")

def createSubsKey(key):
	return concat(key , "/dsubs")

def createSubMainKey(key, subKey):
	return concat(concat(key, "/dsub/"), subKey)

def createSubRootNameKey(key):
	return concat(key, "/dname")

def createSubNameKey(key, subDomainName):
	return concat(concat(key, "/d"), subDomainName)

def createSubApprovedKey(key):
	return concat(key, "/dsubApproved")

def createMasterApprovedKey(key):
	return concat(key, "/dmasterApproved")

def createHashDomainsKey(owner):
    return concat(owner, "/ddomains")

def createPendingTransactionKey(key, idPendingTransaction):
	return concat(concat(key, "/dpendingTransaction/"), idPendingTransaction)

def createExecutedKey(key):
	return concat(key, "/dexecuted")

def createAttributesKey(key):
	return concat(key, "/dattributes")

def createPriceKey(key):
	return concat(key, "/dprice")
