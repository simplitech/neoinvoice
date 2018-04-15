# neoinvoice

neoinvoice is simple invoicing tool using NEO.
This tool allows you to register names you own, and than, create payments on behalf of this name.
After a name has been created, it possible to add meta tags to it and create invoices.
You need an encrypted WIF to log-in.

<b>IMPORTANT:</b> The payments are made to the smart contract, and the Validation Trigger <b>has not been implemented propertly</b>.
Another important upgrade would be implementing DNS checks using Oracles and TXT DNS entries.

The code is divided into 2 parts: the smart-contract made in with neo-python and a web frontend made using Vue and Neon.js.

How to run the web interface:
1 - Update the AppResource.js to point to the correct RPC and NEOScan ip address (currently our private network address)
2 - Deploy the smart contract and update the AppResource.js to point to the correct SmartContract Script Hash.

Having npm installed:
cd neoinvoice
npm install
npm run dev

<b>Usage Example</b>

The system is supposed to be used by two kinds of users: the seller and the buyer.
<b>The seller case</b>
For the Seller, 

To pay for an invoice, the user must first find the transaction he is willing to pay. He does that by using the domain name in combination with the id of the invoice.

If the invoice is correct, the user will be able to see each individual product or service that he is being charged for, and easiliy pay it using the 'Pay' button.

The payment, instead of going to the SmartContract and have it's funds managed by a Validation function, is transfered directly to the other party. This transaction also has an attribute, indicating if that payment is related to any pending transaction.

Instead of using a second transaction to 'conclude' the pending invoice, we use a modified node that reads every transaction, and if a transaction with invoice id is found, we check the transaction value, and if the value is the accorded one, the invoice will be marked as 'paid'.

![](https://imgur.com/afHQz1X.png)
![](https://imgur.com/9hWvkJI.png)
![](https://imgur.com/1S7XJoV.png)
![](https://imgur.com/H5wCq4a.png)
![](https://imgur.com/28HXc0X.png)
![](https://imgur.com/wM2lbNl.png)
![](https://imgur.com/xulnwVN.png)
![](https://imgur.com/0betgAc.png)
