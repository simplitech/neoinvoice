
public  static class teste{
    private static boolean existDomainAndOwnerOrSlaveWithHash(byte[] publicKey, String domainName) {
        if (!existDomain(domainName)) {
            return false;
        }
        if (!owner(publicKey, domainName)) {
            String slaveKey = Helper.asString(publicKey);
            return existSlave(slaveKey, domainName);
        }

        return true;
    }

    private static boolean existSlave(String slaveKey, String domainName) {
        String key = createDomainSlaveKey(domainName, slaveKey);
        byte[] domain = Storage.get(Storage.currentContext(), key);
        return domain != null;
    }

    private static byte[] existPendingTransaction(String domainName, long idPendingTransaction) {
        String key = createDomainPendingTransactionKey(domainName, idPendingTransaction);
        byte[] pendingTransaction = Storage.get(Storage.currentContext(), key);
        if (pendingTransaction == null) {
            return null;
        }

        return pendingTransaction;
    }

}