package canon

import "aitl.example/domains/policy/data"

// Shared canonical types, owned by no single domain. Definitions are closed, so a consumer
// that refines one can only add constraints to fields the canonical type declares.

#Money: {
	// amount is in pounds
	amount:   int
	currency: "GBP" | "EUR" | "USD"
}

#CustomerRef: {
	customerId: string
	email:      data.#PIIField
}

#Carrier: "royal-mail" | "ups" | "DHL"

#OrderShipped: {
	orderId:        string
	carrier:        #Carrier
	trackingNumber: string
}
